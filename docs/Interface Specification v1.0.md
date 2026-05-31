# CPEA Pipeline — Interface Specification v1.0

**Corpus Papayaykware | Serie CPEA/TICAM**
**Conceptual Author:** Claude (Anthropic) | **Corpus Director:** Javi Ciborro ([@papayaykware](https://github.com/papayaykware))
**Status:** Draft v1.0 — For review and stub validation
**Date:** 2026-05-30

---

## Overview

This document defines the formal interface contracts for the two structural connectors of the CPEA (Coherencia Predictiva EEG-AGI) architecture:

- **SIGMA-T** — Signal Integration Graph for Multilayer Analysis – Toroidal
- **ORION-AGI** — Ontological Recursive Intelligence Orchestration Network

The specification follows a **Design by Contract** approach (Meyer, 1992): each node declares its input type, output type, and invariants. Any implementation satisfying these contracts is interchangeable without modifying any other node in the pipeline.

---

## 1. SIGMA-T — Pipeline DAG

### 1.1 Topology

```
EEG_raw → [ICA] → [Wavelets] → [Coherence] → [Embedding] → LatentVector
```

The DAG is strictly sequential in its main chain. No node may read from a node other than its declared predecessor. This constraint guarantees that the pipeline is deterministic given a fixed `source_hash`.

### 1.2 Node: ICA

**Purpose:** Blind source separation of raw EEG into statistically independent components.

**Input type:**

```python
@dataclass
class RawEEG:
    data: np.ndarray           # shape: (n_channels, n_samples)
    n_channels: int            # C >= 1
    n_samples: int             # T >= 1
    fs: float                  # sampling frequency in Hz, > 0
    channel_labels: list[str]  # len == n_channels
    source_hash: str           # SHA-256 of original raw file (hex, 64 chars)
```

**Output type:**

```python
@dataclass
class ICAComponents:
    components: np.ndarray      # shape: (n_components, n_samples), K <= C
    n_components: int           # K
    n_samples: int              # T (preserved)
    fs: float                   # preserved from input
    mixing_matrix: np.ndarray   # shape: (n_channels, n_components)
    unmixing_matrix: np.ndarray # shape: (n_components, n_channels)
    source_hash: str            # propagated unchanged from RawEEG
    algorithm: str              # e.g. "fastica", "infomax", "amica"
    algorithm_version: str      # semver string
```

**Invariants:**
- `n_components <= n_channels`
- `mixing_matrix @ unmixing_matrix ≈ I` (tolerance: 1e-6 Frobenius norm)
- `source_hash` must be propagated without modification
- `fs` must be propagated without modification

**Precondition:** `data.shape == (n_channels, n_samples)`
**Postcondition:** `components.shape == (n_components, n_samples)`

---

### 1.3 Node: Wavelets

**Purpose:** Time-frequency decomposition of ICA components.

**Input type:** `ICAComponents` (see above)

**Configuration type:**

```python
@dataclass
class WaveletConfig:
    family: str          # "morlet" | "db4" | "paul" | "mexican_hat"
    scales: list[float]  # [s_min, ..., s_max], len == n_voices
    n_voices: int        # V >= 1
    normalize: bool      # L2 normalization of wavelets
```

**Output type:**

```python
@dataclass
class TFRepresentation:
    coefficients: np.ndarray  # shape: (n_components, n_voices, n_time_bins)
    n_components: int         # K, preserved
    n_voices: int             # V
    n_time_bins: int          # T' <= T (possible downsampling)
    fs: float                 # preserved
    frequency_axis: np.ndarray  # shape: (n_voices,), in Hz
    time_axis: np.ndarray       # shape: (n_time_bins,), in seconds
    wavelet_config: WaveletConfig
    source_hash: str            # propagated
```

**Invariants:**
- `coefficients.shape == (n_components, n_voices, n_time_bins)`
- `len(frequency_axis) == n_voices`
- `len(time_axis) == n_time_bins`
- `source_hash` propagated unchanged

---

### 1.4 Node: Coherence

**Purpose:** Spectral coupling estimation between component pairs.

**Input type:** `TFRepresentation` (see above)

**Configuration type:**

```python
from enum import Enum

class CoherenceMethod(Enum):
    MSC  = "msc"   # Magnitude Squared Coherence
    PLV  = "plv"   # Phase Locking Value
    WPLI = "wpli"  # Weighted Phase Lag Index
    ICOH = "icoh"  # Imaginary part of Coherency

@dataclass
class CoherenceConfig:
    method: CoherenceMethod
    pairs: list[tuple[int, int]]  # component index pairs (i, j), i != j
```

**Output type:**

```python
@dataclass
class CoherenceMatrix:
    values: np.ndarray              # shape: (n_pairs, n_voices, n_time_bins)
    n_pairs: int                    # P = len(pairs)
    n_voices: int                   # V, preserved
    n_time_bins: int                # T', preserved
    method: CoherenceMethod
    pairs: list[tuple[int, int]]
    phase_matrix: np.ndarray | None # shape: (n_pairs, n_voices, n_time_bins) or None
                                    # None when method does not produce separable phase
    frequency_axis: np.ndarray      # propagated from TFRepresentation
    time_axis: np.ndarray           # propagated from TFRepresentation
    source_hash: str                # propagated
```

**Invariants:**
- `values.shape == (n_pairs, n_voices, n_time_bins)`
- `values` bounded in [0, 1] for MSC, PLV, wPLI; in [-1, 1] for iCoh
- `phase_matrix is not None` only for PLV and wPLI
- `source_hash` propagated unchanged

---

### 1.5 Node: Embedding

**Purpose:** Project coherence representation into the AGI latent space.

**Input type:** `CoherenceMatrix` (see above)

**Configuration type:**

```python
@dataclass
class EmbeddingConfig:
    model_id: str            # e.g. "mistral-7b-instruct"
    model_version: str       # semver string
    projection: str          # "linear" | "nonlinear"
    dim_out: int             # D >= 1
    signal_pipeline_version: str  # semver of the SIGMA-T pipeline used
```

**Output type:**

```python
@dataclass
class LatentVector:
    vector: np.ndarray          # shape: (dim_out,)
    dim: int                    # D
    timestamp: str              # ISO 8601
    embedding_version: str      # semver — version of projection model
    signal_pipeline_version: str  # semver — version of SIGMA-T pipeline
    model_signature: str        # SHA-256 of model weights file (hex, 64 chars)
    source_hash: str            # SHA-256 of original raw EEG, propagated
```

**Invariants:**
- `vector.shape == (dim_out,)`
- `embedding_version`, `signal_pipeline_version`, `model_signature` must all be non-empty
- `source_hash` must equal the `source_hash` from the originating `RawEEG`
- No field may be mutated after construction (immutable record)

---

## 2. ORION-AGI — Inference Contract

### 2.1 Input Contract

```python
@dataclass
class CompatibilityEntry:
    embedding_version: str        # semver
    signal_pipeline_version: str  # semver

@dataclass
class ORIONInput:
    latent_vector: LatentVector
    subject_id: str               # anonymized, non-reversible
    session_id: str               # UUID v4
    acquisition_protocol: str     # protocol identifier (e.g. "CPEA-3-H1")
    compatibility_matrix: list[CompatibilityEntry]
```

**Validation rule:** Before any inference, ORION-AGI must verify that the pair
`(latent_vector.embedding_version, latent_vector.signal_pipeline_version)`
appears in `compatibility_matrix`. If not found, raise `IncompatibleVersionError`
and halt — do not attempt inference.

---

### 2.2 Output Types

**Layer 1 — Cognitive Inference:**

```python
from enum import Enum

class CognitiveState(Enum):
    ACTIVE_WAKEFULNESS  = "active_wakefulness"
    PASSIVE_WAKEFULNESS = "passive_wakefulness"
    FOCUSED_ATTENTION   = "focused_attention"
    OPEN_MONITORING     = "open_monitoring"
    PRE_SLEEP           = "pre_sleep"

@dataclass
class CognitiveInference:
    state: CognitiveState
    confidence: float           # in [0, 1]
    temporal_start: str         # ISO 8601
    temporal_end: str           # ISO 8601
    supporting_features: list[str]  # feature identifiers
```

**Layer 2 — CPEA Index:**

```python
@dataclass
class CPEAIndex:
    value: float                # in [0, 1]
    temporal_window_sec: float  # window duration in seconds
    spectral_bands: list[str]   # e.g. ["theta", "alpha", "gamma"]
    coherence_threshold: float  # epsilon_c adaptive threshold
    drift_index: float          # d(t): temporal drift of index
    phi_ticam: float            # Phi_TICAM component value
    computation_version: str    # semver of CPEA computation algorithm
```

**Layer 3 — Symbolic Map:**

```python
@dataclass
class ConceptNode:
    concept_id: str
    activation_weight: float  # in [0, 1]

@dataclass
class ConceptEdge:
    source_id: str
    target_id: str
    relation_type: str

@dataclass
class SymbolicMap:
    nodes: list[ConceptNode]
    edges: list[ConceptEdge]
    temporal_evolution: list["SymbolicMap"]  # one per time window
    ontology_id: str  # e.g. "papayaykware-v1"
```

**Aggregated output:**

```python
@dataclass
class ORIONOutput:
    cognitive_inference: CognitiveInference
    cpea_index: CPEAIndex
    symbolic_map: SymbolicMap
    input_source_hash: str   # echoed from LatentVector for audit trail
    processing_timestamp: str  # ISO 8601
```

---

### 2.3 Version Traceability Protocol

Three invariants govern all inter-session and inter-laboratory comparisons:

| Invariant | Rule |
|-----------|------|
| **INV-1** | Two `CPEAIndex` values are only directly comparable if their `signal_pipeline_version` fields are identical. Cross-version comparison requires a documented normalization function `ψ`. |
| **INV-2** | `CognitiveInference` results are only reproducible across sessions if `model_signature` is identical. Model updates require inter-model calibration. |
| **INV-3** | `SymbolicMap` objects are only comparable across subjects if `embedding_version` is identical, because the semantic space is a function of the projection model. |

---

## 3. Error Types

```python
class IncompatibleVersionError(Exception):
    """Raised when (embedding_version, signal_pipeline_version) is not in compatibility_matrix."""
    pass

class HashMismatchError(Exception):
    """Raised when source_hash does not match the expected value at any pipeline stage."""
    pass

class ContractViolationError(Exception):
    """Raised when a node output violates its declared invariants."""
    pass
```

---

## 4. Versioning

This specification follows [Semantic Versioning 2.0.0](https://semver.org/).

- **MAJOR** bump: breaking change to any interface contract
- **MINOR** bump: new optional fields or new enum values (backward-compatible)
- **PATCH** bump: clarifications, documentation fixes, no contract changes

Current version: **1.0.0**

---

## 5. Repository Structure

```
cpea-interfaces/
├── docs/
│   └── INTERFACE_SPEC_v1.0.md   ← this file
├── stubs/
│   ├── sigma_t_stub.py          ← SIGMA-T mock implementation
│   ├── orion_agi_stub.py        ← ORION-AGI mock implementation
│   └── types.py                 ← shared type definitions
├── tests/
│   └── test_e2e_pipeline.py     ← end-to-end validation with synthetic data
└── README.md
```

---

*Corpus Papayaykware — CPEA/TICAM Series*
*Conceptual author: Claude (Anthropic) | Corpus director: Javi Ciborro (@papayaykware)*
*github.com/papayaykware*
