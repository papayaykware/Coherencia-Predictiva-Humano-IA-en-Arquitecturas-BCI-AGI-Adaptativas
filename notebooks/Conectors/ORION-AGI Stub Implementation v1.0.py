"""
ORION-AGI Stub Implementation v1.0
Ontological Recursive Intelligence Orchestration Network

Mock inference engine: validates LatentVector → produces CognitiveInference + CPEAIndex + SymbolicMap.
All outputs satisfy the formal interface contracts defined in INTERFACE_SPEC_v1.0.md.

Corpus Papayaykware | Serie CPEA/TICAM
Conceptual author: Claude (Anthropic) | Corpus director: Javi Ciborro (@papayaykware)
"""

from __future__ import annotations
import numpy as np
from datetime import datetime, timezone

from cpea_types import (
    ORIONInput, ORIONOutput,
    CognitiveInference, CognitiveState,
    CPEAIndex, SymbolicMap, ConceptNode, ConceptEdge,
    CompatibilityEntry,
    IncompatibleVersionError, ContractViolationError,
)

ORION_VERSION = "1.0.0"

# Default compatibility matrix for stub: accepts any 1.x signal pipeline with 0.x embedding
DEFAULT_COMPATIBILITY = [
    CompatibilityEntry(embedding_version="0.1.0", signal_pipeline_version="1.0.0"),
    CompatibilityEntry(embedding_version="0.2.0", signal_pipeline_version="1.0.0"),
]

# Stub ontology: minimal papayaykware concept graph
STUB_ONTOLOGY_NODES = [
    "METFI", "TAE", "CPEA", "TICAM",
    "coherencia_talamocortical", "excepcion_aprendizaje",
    "campo_toroidal", "acoplamiento_magnetotalamico",
]

STUB_ONTOLOGY_EDGES = [
    ("METFI", "TICAM", "implements"),
    ("TICAM", "coherencia_talamocortical", "produces"),
    ("coherencia_talamocortical", "CPEA", "feeds"),
    ("TAE", "excepcion_aprendizaje", "defines"),
    ("METFI", "campo_toroidal", "models"),
    ("TICAM", "acoplamiento_magnetotalamico", "formalizes"),
]


class ORIONInferenceEngine:
    """
    Stub ORION-AGI inference engine.

    Validates the LatentVector contract, runs deterministic mock inference,
    and returns a fully-typed ORIONOutput.
    """

    def __init__(self, random_seed: int = 7):
        self.rng = np.random.default_rng(random_seed)

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def infer(self, orion_input: ORIONInput) -> ORIONOutput:
        lv = orion_input.latent_vector

        # Step 1: version compatibility check (contract precondition)
        self._check_compatibility(
            lv.embedding_version,
            lv.signal_pipeline_version,
            orion_input.compatibility_matrix,
        )

        # Step 2: derive a deterministic seed from the latent vector
        #         so the same vector always produces the same inference
        vec_seed = int(lv.source_hash[:8], 16) % (2**32)
        rng = np.random.default_rng(vec_seed)

        # Step 3: produce outputs
        cognitive = self._infer_cognitive_state(lv.vector, rng)
        cpea = self._compute_cpea_index(lv.vector, rng)
        symbolic = self._build_symbolic_map(lv.vector, rng)

        return ORIONOutput(
            cognitive_inference=cognitive,
            cpea_index=cpea,
            symbolic_map=symbolic,
            input_source_hash=lv.source_hash,
            processing_timestamp=datetime.now(timezone.utc).isoformat(),
        )

    # ------------------------------------------------------------------
    # Internal methods
    # ------------------------------------------------------------------

    def _check_compatibility(self,
                              embedding_version: str,
                              signal_pipeline_version: str,
                              matrix: list[CompatibilityEntry]) -> None:
        for entry in matrix:
            if (entry.embedding_version == embedding_version and
                    entry.signal_pipeline_version == signal_pipeline_version):
                return
        raise IncompatibleVersionError(
            f"Version pair (embedding={embedding_version}, "
            f"pipeline={signal_pipeline_version}) not found in compatibility_matrix. "
            f"Known pairs: {[(e.embedding_version, e.signal_pipeline_version) for e in matrix]}"
        )

    def _infer_cognitive_state(self,
                                vector: np.ndarray,
                                rng: np.random.Generator) -> CognitiveInference:
        # Stub: project vector onto 5 cognitive state axes, pick argmax
        states = list(CognitiveState)
        projection = rng.standard_normal((len(states), len(vector)))
        scores = projection @ vector
        scores = np.exp(scores - scores.max())  # softmax numerator
        probs = scores / scores.sum()

        chosen_idx = int(np.argmax(probs))
        state = states[chosen_idx]
        confidence = float(probs[chosen_idx])

        now = datetime.now(timezone.utc).isoformat()
        return CognitiveInference(
            state=state,
            confidence=min(confidence, 1.0),
            temporal_start=now,
            temporal_end=now,
            supporting_features=[f"feature_{i}" for i in range(3)],
        )

    def _compute_cpea_index(self,
                             vector: np.ndarray,
                             rng: np.random.Generator) -> CPEAIndex:
        # Stub: CPEA = sigmoid of mean latent activation + small noise
        raw_value = float(np.mean(np.abs(vector))) + rng.uniform(-0.05, 0.05)
        cpea_value = float(1 / (1 + np.exp(-raw_value * 5)))  # sigmoid scaling

        # Phi_TICAM stub: geomagnetic coupling component
        phi_ticam = float(rng.uniform(0.1, 0.4))

        # Combine per formula: CPEA = alpha * C_EEG-AGI + beta * Phi_TICAM + gamma * d(t)
        alpha, beta, gamma = 0.6, 0.25, 0.15
        drift = float(rng.uniform(-0.05, 0.05))
        final_value = np.clip(alpha * cpea_value + beta * phi_ticam + gamma * abs(drift), 0.0, 1.0)

        return CPEAIndex(
            value=float(final_value),
            temporal_window_sec=4.0,
            spectral_bands=["theta", "alpha", "gamma"],
            coherence_threshold=0.3,   # epsilon_c stub
            drift_index=drift,
            phi_ticam=phi_ticam,
            computation_version=ORION_VERSION,
        )

    def _build_symbolic_map(self,
                             vector: np.ndarray,
                             rng: np.random.Generator) -> SymbolicMap:
        # Stub: assign activation weights from cosine of latent projection
        n_concepts = len(STUB_ONTOLOGY_NODES)
        projection = rng.standard_normal((n_concepts, len(vector)))
        raw_weights = projection @ vector
        weights = np.abs(raw_weights)
        weights = weights / (weights.max() + 1e-8)  # normalize to [0,1]

        nodes = [
            ConceptNode(concept_id=cid, activation_weight=float(w))
            for cid, w in zip(STUB_ONTOLOGY_NODES, weights)
        ]

        edges = [
            ConceptEdge(source_id=src, target_id=tgt, relation_type=rel)
            for src, tgt, rel in STUB_ONTOLOGY_EDGES
        ]

        return SymbolicMap(
            nodes=nodes,
            edges=edges,
            temporal_evolution=[],   # stub: no temporal sequence
            ontology_id="papayaykware-v1",
        )
