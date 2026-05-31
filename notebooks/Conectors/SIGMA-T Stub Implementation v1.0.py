"""
SIGMA-T Stub Implementation v1.0
Signal Integration Graph for Multilayer Analysis – Toroidal

Mock pipeline: ICA → Wavelets → Coherence → Embedding
Uses synthetic-data-compatible random projections.
All outputs satisfy the formal interface contracts defined in INTERFACE_SPEC_v1.0.md.

Corpus Papayaykware | Serie CPEA/TICAM
Conceptual author: Claude (Anthropic) | Corpus director: Javi Ciborro (@papayaykware)
"""

from __future__ import annotations
import hashlib
import numpy as np
from datetime import datetime, timezone
from typing import Optional

from cpea_types import (
    RawEEG, ICAComponents, WaveletConfig, TFRepresentation,
    CoherenceConfig, CoherenceMatrix, CoherenceMethod,
    EmbeddingConfig, LatentVector,
    HashMismatchError, ContractViolationError,
)

SIGMA_T_VERSION = "1.0.0"


# ---------------------------------------------------------------------------
# Node 1: ICA
# ---------------------------------------------------------------------------

class ICANode:
    """
    Stub ICA implementation using random orthogonal unmixing.
    Satisfies the ICA interface contract: preserves source_hash and fs,
    produces mixing/unmixing matrices that are approximate inverses.
    """

    def __init__(self, n_components: Optional[int] = None,
                 algorithm: str = "stub-ica",
                 algorithm_version: str = "1.0.0",
                 random_seed: int = 42):
        self.n_components = n_components
        self.algorithm = algorithm
        self.algorithm_version = algorithm_version
        self.rng = np.random.default_rng(random_seed)

    def run(self, raw: RawEEG) -> ICAComponents:
        K = self.n_components or raw.n_channels

        # Random orthogonal unmixing matrix via QR decomposition
        Q, _ = np.linalg.qr(self.rng.standard_normal((raw.n_channels, K)))
        unmixing = Q.T                     # shape: (K, C)
        mixing = np.linalg.pinv(unmixing)  # shape: (C, K)

        components = unmixing @ raw.data   # shape: (K, T)

        # Verify contract invariant: unmixing @ mixing ≈ I_K
        residual = np.linalg.norm(unmixing @ mixing - np.eye(K), ord='fro')
        if residual > 1e-4 * K:
            raise ContractViolationError(
                f"ICA: mixing @ unmixing not close to identity (Frobenius residual={residual:.2e})"
            )

        return ICAComponents(
            components=components,
            n_components=K,
            n_samples=raw.n_samples,
            fs=raw.fs,
            mixing_matrix=mixing,
            unmixing_matrix=unmixing,
            source_hash=raw.source_hash,
            algorithm=self.algorithm,
            algorithm_version=self.algorithm_version,
        )


# ---------------------------------------------------------------------------
# Node 2: Wavelets
# ---------------------------------------------------------------------------

class WaveletNode:
    """
    Stub Wavelet implementation using Gabor-like modulated Gaussians.
    Produces a valid TFRepresentation with correct shape and axis arrays.
    """

    def run(self, ica: ICAComponents, config: WaveletConfig) -> TFRepresentation:
        T_prime = ica.n_samples  # no downsampling in stub
        K = ica.n_components
        V = config.n_voices

        # Compute frequency axis from scales (stub: linear spacing in log domain)
        freq_axis = np.array(config.scales)  # scales used as proxy for freq

        # Stub coefficients: modulated random signal with plausible structure
        rng = np.random.default_rng(int(ica.source_hash[:8], 16) % (2**32))
        coefficients = rng.standard_normal((K, V, T_prime)) * 0.1

        # Add a synthetic oscillatory component in the first voice
        t = np.linspace(0, T_prime / ica.fs, T_prime)
        for k in range(K):
            coefficients[k, 0, :] += np.sin(2 * np.pi * freq_axis[0] * t)

        time_axis = t

        return TFRepresentation(
            coefficients=coefficients,
            n_components=K,
            n_voices=V,
            n_time_bins=T_prime,
            fs=ica.fs,
            frequency_axis=freq_axis,
            time_axis=time_axis,
            wavelet_config=config,
            source_hash=ica.source_hash,
        )


# ---------------------------------------------------------------------------
# Node 3: Coherence
# ---------------------------------------------------------------------------

class CoherenceNode:
    """
    Stub Coherence node. Computes synthetic coherence matrices bounded in [0,1].
    Supports all four methods declared in the contract (stub values only).
    """

    def run(self, tf: TFRepresentation, config: CoherenceConfig) -> CoherenceMatrix:
        P = len(config.pairs)
        V = tf.n_voices
        T = tf.n_time_bins

        rng = np.random.default_rng(int(tf.source_hash[:8], 16) % (2**32))

        if config.method in (CoherenceMethod.MSC, CoherenceMethod.PLV, CoherenceMethod.WPLI):
            values = np.abs(rng.standard_normal((P, V, T)))
            # Normalize to [0, 1]
            values = values / (values.max() + 1e-8)
        elif config.method == CoherenceMethod.ICOH:
            # iCoh bounded in [-1, 1]
            values = np.tanh(rng.standard_normal((P, V, T)))
        else:
            raise ContractViolationError(f"Unknown coherence method: {config.method}")

        # Phase matrix only for PLV and wPLI
        phase_matrix = None
        if config.method in (CoherenceMethod.PLV, CoherenceMethod.WPLI):
            phase_matrix = rng.uniform(-np.pi, np.pi, (P, V, T))

        return CoherenceMatrix(
            values=values,
            n_pairs=P,
            n_voices=V,
            n_time_bins=T,
            method=config.method,
            pairs=config.pairs,
            phase_matrix=phase_matrix,
            frequency_axis=tf.frequency_axis,
            time_axis=tf.time_axis,
            source_hash=tf.source_hash,
        )


# ---------------------------------------------------------------------------
# Node 4: Embedding
# ---------------------------------------------------------------------------

class EmbeddingNode:
    """
    Stub Embedding node. Projects flattened CoherenceMatrix via random linear map.
    Produces a LatentVector with all required traceability metadata.
    """

    def __init__(self, random_seed: int = 99):
        self.rng = np.random.default_rng(random_seed)

    def run(self, coh: CoherenceMatrix, config: EmbeddingConfig) -> LatentVector:
        # Flatten coherence values
        flat = coh.values.flatten()  # shape: (P * V * T,)

        # Random linear projection to dim_out
        D = config.dim_out
        projection_matrix = self.rng.standard_normal((D, len(flat)))
        vector = projection_matrix @ flat
        # L2-normalize
        norm = np.linalg.norm(vector)
        if norm > 1e-12:
            vector = vector / norm

        # Stub model signature: SHA-256 of config params
        sig_input = f"{config.model_id}:{config.model_version}:{config.projection}:{D}".encode()
        model_signature = hashlib.sha256(sig_input).hexdigest()

        return LatentVector(
            vector=vector,
            dim=D,
            timestamp=datetime.now(timezone.utc).isoformat(),
            embedding_version=config.model_version,
            signal_pipeline_version=config.signal_pipeline_version,
            model_signature=model_signature,
            source_hash=coh.source_hash,
        )


# ---------------------------------------------------------------------------
# Full pipeline runner
# ---------------------------------------------------------------------------

class SIGMATpipeline:
    """
    Assembles and runs the complete SIGMA-T pipeline:
        RawEEG → ICA → Wavelets → Coherence → Embedding → LatentVector

    All intermediate outputs can be inspected via the `intermediates` dict
    after calling `run()`.
    """

    def __init__(self,
                 n_ica_components: Optional[int] = None,
                 wavelet_config: Optional[WaveletConfig] = None,
                 coherence_config: Optional[CoherenceConfig] = None,
                 embedding_config: Optional[EmbeddingConfig] = None,
                 random_seed: int = 0):

        self.ica_node = ICANode(n_components=n_ica_components, random_seed=random_seed)
        self.wavelet_node = WaveletNode()
        self.coherence_node = CoherenceNode()
        self.embedding_node = EmbeddingNode(random_seed=random_seed + 1)

        # Defaults for quick testing
        self.wavelet_config = wavelet_config or WaveletConfig(
            family="morlet",
            scales=[4.0, 8.0, 16.0, 32.0],
            n_voices=4,
            normalize=True,
        )
        self.embedding_config = embedding_config or EmbeddingConfig(
            model_id="stub-model",
            model_version="0.1.0",
            projection="linear",
            dim_out=64,
            signal_pipeline_version=SIGMA_T_VERSION,
        )
        self.intermediates: dict = {}

    def _default_coherence_config(self, n_components: int) -> CoherenceConfig:
        pairs = [(i, j) for i in range(n_components) for j in range(i+1, n_components)]
        return CoherenceConfig(method=CoherenceMethod.PLV, pairs=pairs)

    def run(self, raw: RawEEG) -> LatentVector:
        ica_out = self.ica_node.run(raw)
        self.intermediates["ica"] = ica_out

        tf_out = self.wavelet_node.run(ica_out, self.wavelet_config)
        self.intermediates["tf"] = tf_out

        coh_config = self._default_coherence_config(ica_out.n_components)
        coh_out = self.coherence_node.run(tf_out, coh_config)
        self.intermediates["coherence"] = coh_out

        latent = self.embedding_node.run(coh_out, self.embedding_config)
        self.intermediates["latent"] = latent

        # Final hash integrity check
        if latent.source_hash != raw.source_hash:
            raise HashMismatchError(
                f"source_hash mismatch at pipeline output: "
                f"expected {raw.source_hash}, got {latent.source_hash}"
            )

        return latent
