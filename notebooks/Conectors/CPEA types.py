"""
CPEA Pipeline — Shared Type Definitions
Corpus Papayaykware | Serie CPEA/TICAM
Conceptual author: Claude (Anthropic) | Corpus director: Javi Ciborro (@papayaykware)
Spec version: 1.0.0
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import numpy as np


# ---------------------------------------------------------------------------
# SIGMA-T types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class RawEEG:
    """Input to the ICA node. Immutable once constructed."""
    data: np.ndarray          # shape: (n_channels, n_samples)
    n_channels: int
    n_samples: int
    fs: float                 # Hz, must be > 0
    channel_labels: list[str]
    source_hash: str          # SHA-256 hex of raw file, 64 chars

    def __post_init__(self):
        assert self.data.shape == (self.n_channels, self.n_samples), (
            f"data shape {self.data.shape} != ({self.n_channels}, {self.n_samples})"
        )
        assert self.fs > 0, "fs must be positive"
        assert len(self.channel_labels) == self.n_channels
        assert len(self.source_hash) == 64, "source_hash must be 64-char hex SHA-256"

    class Config:
        arbitrary_types_allowed = True


@dataclass(frozen=True)
class ICAComponents:
    components: np.ndarray      # shape: (n_components, n_samples)
    n_components: int
    n_samples: int
    fs: float
    mixing_matrix: np.ndarray   # shape: (n_channels, n_components)
    unmixing_matrix: np.ndarray # shape: (n_components, n_channels)
    source_hash: str
    algorithm: str
    algorithm_version: str

    def __post_init__(self):
        assert self.components.shape == (self.n_components, self.n_samples)
        assert self.mixing_matrix.shape[1] == self.n_components
        assert self.unmixing_matrix.shape[0] == self.n_components
        assert len(self.source_hash) == 64


@dataclass(frozen=True)
class WaveletConfig:
    family: str        # "morlet" | "db4" | "paul" | "mexican_hat"
    scales: list[float]
    n_voices: int
    normalize: bool = True

    def __post_init__(self):
        assert self.n_voices >= 1
        assert len(self.scales) == self.n_voices
        assert self.family in {"morlet", "db4", "paul", "mexican_hat"}


@dataclass(frozen=True)
class TFRepresentation:
    coefficients: np.ndarray    # shape: (n_components, n_voices, n_time_bins)
    n_components: int
    n_voices: int
    n_time_bins: int
    fs: float
    frequency_axis: np.ndarray  # shape: (n_voices,)
    time_axis: np.ndarray       # shape: (n_time_bins,)
    wavelet_config: WaveletConfig
    source_hash: str

    def __post_init__(self):
        assert self.coefficients.shape == (self.n_components, self.n_voices, self.n_time_bins)
        assert len(self.frequency_axis) == self.n_voices
        assert len(self.time_axis) == self.n_time_bins
        assert len(self.source_hash) == 64


class CoherenceMethod(Enum):
    MSC  = "msc"
    PLV  = "plv"
    WPLI = "wpli"
    ICOH = "icoh"


@dataclass(frozen=True)
class CoherenceConfig:
    method: CoherenceMethod
    pairs: list[tuple[int, int]]

    def __post_init__(self):
        assert len(self.pairs) >= 1
        for i, j in self.pairs:
            assert i != j, "Self-coherence (i==j) is not defined"


@dataclass(frozen=True)
class CoherenceMatrix:
    values: np.ndarray              # shape: (n_pairs, n_voices, n_time_bins)
    n_pairs: int
    n_voices: int
    n_time_bins: int
    method: CoherenceMethod
    pairs: list[tuple[int, int]]
    phase_matrix: Optional[np.ndarray]  # None unless method produces separable phase
    frequency_axis: np.ndarray
    time_axis: np.ndarray
    source_hash: str

    def __post_init__(self):
        assert self.values.shape == (self.n_pairs, self.n_voices, self.n_time_bins)
        assert self.n_pairs == len(self.pairs)
        assert len(self.source_hash) == 64
        if self.phase_matrix is not None:
            assert self.phase_matrix.shape == self.values.shape


@dataclass(frozen=True)
class EmbeddingConfig:
    model_id: str
    model_version: str
    projection: str   # "linear" | "nonlinear"
    dim_out: int
    signal_pipeline_version: str

    def __post_init__(self):
        assert self.projection in {"linear", "nonlinear"}
        assert self.dim_out >= 1


@dataclass(frozen=True)
class LatentVector:
    vector: np.ndarray
    dim: int
    timestamp: str
    embedding_version: str
    signal_pipeline_version: str
    model_signature: str   # SHA-256 of model weights, 64-char hex
    source_hash: str       # propagated from RawEEG

    def __post_init__(self):
        assert self.vector.shape == (self.dim,)
        assert len(self.model_signature) == 64
        assert len(self.source_hash) == 64
        assert all(len(v) > 0 for v in [
            self.embedding_version,
            self.signal_pipeline_version,
            self.model_signature,
        ]), "Version fields must not be empty"


# ---------------------------------------------------------------------------
# ORION-AGI types
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CompatibilityEntry:
    embedding_version: str
    signal_pipeline_version: str


@dataclass(frozen=True)
class ORIONInput:
    latent_vector: LatentVector
    subject_id: str
    session_id: str
    acquisition_protocol: str
    compatibility_matrix: list[CompatibilityEntry]


class CognitiveState(Enum):
    ACTIVE_WAKEFULNESS  = "active_wakefulness"
    PASSIVE_WAKEFULNESS = "passive_wakefulness"
    FOCUSED_ATTENTION   = "focused_attention"
    OPEN_MONITORING     = "open_monitoring"
    PRE_SLEEP           = "pre_sleep"


@dataclass(frozen=True)
class CognitiveInference:
    state: CognitiveState
    confidence: float          # [0, 1]
    temporal_start: str        # ISO 8601
    temporal_end: str          # ISO 8601
    supporting_features: list[str]

    def __post_init__(self):
        assert 0.0 <= self.confidence <= 1.0


@dataclass(frozen=True)
class CPEAIndex:
    value: float               # [0, 1]
    temporal_window_sec: float
    spectral_bands: list[str]
    coherence_threshold: float  # epsilon_c
    drift_index: float          # d(t)
    phi_ticam: float            # Phi_TICAM component
    computation_version: str

    def __post_init__(self):
        assert 0.0 <= self.value <= 1.0


@dataclass(frozen=True)
class ConceptNode:
    concept_id: str
    activation_weight: float  # [0, 1]

    def __post_init__(self):
        assert 0.0 <= self.activation_weight <= 1.0


@dataclass(frozen=True)
class ConceptEdge:
    source_id: str
    target_id: str
    relation_type: str


@dataclass(frozen=True)
class SymbolicMap:
    nodes: list[ConceptNode]
    edges: list[ConceptEdge]
    temporal_evolution: list[SymbolicMap]
    ontology_id: str


@dataclass(frozen=True)
class ORIONOutput:
    cognitive_inference: CognitiveInference
    cpea_index: CPEAIndex
    symbolic_map: SymbolicMap
    input_source_hash: str
    processing_timestamp: str


# ---------------------------------------------------------------------------
# Error types
# ---------------------------------------------------------------------------

class IncompatibleVersionError(Exception):
    """Raised when (embedding_version, signal_pipeline_version) not in compatibility_matrix."""
    pass


class HashMismatchError(Exception):
    """Raised when source_hash does not match expected value at any pipeline stage."""
    pass


class ContractViolationError(Exception):
    """Raised when a node output violates its declared invariants."""
    pass
