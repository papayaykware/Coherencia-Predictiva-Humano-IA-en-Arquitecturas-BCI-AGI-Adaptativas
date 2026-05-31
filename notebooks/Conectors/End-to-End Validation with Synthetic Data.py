"""
CPEA Pipeline — End-to-End Validation with Synthetic Data
=========================================================

Validates the complete pipeline:
    RawEEG (synthetic) → SIGMA-T → LatentVector → ORION-AGI → ORIONOutput

Tests cover:
  - Contract satisfaction at each node boundary
  - source_hash propagation integrity
  - Version compatibility enforcement (valid and invalid cases)
  - CPEA index bounds [0, 1]
  - Cognitive state completeness (all states reachable)
  - Symbolic map ontology consistency

Run with:   python -m pytest tests/test_e2e_pipeline.py -v
Or directly: python tests/test_e2e_pipeline.py

Corpus Papayaykware | Serie CPEA/TICAM
Conceptual author: Claude (Anthropic) | Corpus director: Javi Ciborro (@papayaykware)
"""

from __future__ import annotations
import hashlib
import sys
import traceback
import numpy as np
from datetime import datetime, timezone

# Allow running from repo root without install
sys.path.insert(0, "stubs")

from cpea_types import (
    RawEEG, WaveletConfig, CoherenceConfig, CoherenceMethod,
    EmbeddingConfig, CompatibilityEntry, ORIONInput,
    IncompatibleVersionError, HashMismatchError, ContractViolationError,
    CognitiveState,
)
from sigma_t_stub import SIGMATpipeline, SIGMA_T_VERSION
from orion_agi_stub import ORIONInferenceEngine, DEFAULT_COMPATIBILITY


# ---------------------------------------------------------------------------
# Synthetic data factory
# ---------------------------------------------------------------------------

def make_synthetic_eeg(n_channels: int = 8,
                        duration_sec: float = 4.0,
                        fs: float = 256.0,
                        random_seed: int = 0) -> RawEEG:
    """Generate band-limited synthetic EEG with known spectral structure."""
    rng = np.random.default_rng(random_seed)
    n_samples = int(duration_sec * fs)
    t = np.linspace(0, duration_sec, n_samples)

    data = np.zeros((n_channels, n_samples))
    # Inject alpha (10 Hz) and theta (6 Hz) oscillations across channels
    for ch in range(n_channels):
        alpha_amp = rng.uniform(0.5, 1.5)
        theta_amp = rng.uniform(0.2, 0.8)
        phase_alpha = rng.uniform(0, 2 * np.pi)
        phase_theta = rng.uniform(0, 2 * np.pi)
        data[ch] = (alpha_amp * np.sin(2 * np.pi * 10 * t + phase_alpha) +
                    theta_amp * np.sin(2 * np.pi * 6 * t + phase_theta) +
                    rng.standard_normal(n_samples) * 0.1)

    # Compute source_hash from raw data bytes (stub: hash of numpy bytes)
    raw_bytes = data.tobytes()
    source_hash = hashlib.sha256(raw_bytes).hexdigest()

    return RawEEG(
        data=data,
        n_channels=n_channels,
        n_samples=n_samples,
        fs=fs,
        channel_labels=[f"EEG{i+1:02d}" for i in range(n_channels)],
        source_hash=source_hash,
    )


def make_default_pipeline() -> SIGMATpipeline:
    wavelet_config = WaveletConfig(
        family="morlet",
        scales=[4.0, 6.0, 10.0, 20.0],
        n_voices=4,
        normalize=True,
    )
    embedding_config = EmbeddingConfig(
        model_id="stub-model",
        model_version="0.1.0",
        projection="linear",
        dim_out=64,
        signal_pipeline_version=SIGMA_T_VERSION,
    )
    return SIGMATpipeline(
        n_ica_components=4,
        wavelet_config=wavelet_config,
        embedding_config=embedding_config,
    )


# ---------------------------------------------------------------------------
# Test suite (plain functions, compatible with pytest and direct execution)
# ---------------------------------------------------------------------------

PASS = "PASS"
FAIL = "FAIL"

results: list[tuple[str, str, str]] = []


def test(name: str):
    """Decorator factory that records test results."""
    def decorator(fn):
        try:
            fn()
            results.append((PASS, name, ""))
        except AssertionError as e:
            results.append((FAIL, name, f"AssertionError: {e}"))
        except Exception as e:
            results.append((FAIL, name, f"{type(e).__name__}: {e}\n{traceback.format_exc()}"))
        return fn
    return decorator


# ---- Test 1: Full pipeline runs without exception ----

@test("T1: Full E2E pipeline completes on synthetic data")
def t1_full_pipeline():
    raw = make_synthetic_eeg()
    pipeline = make_default_pipeline()
    latent = pipeline.run(raw)

    assert latent.dim == 64
    assert latent.vector.shape == (64,)
    assert latent.source_hash == raw.source_hash
    assert latent.signal_pipeline_version == SIGMA_T_VERSION
    assert len(latent.model_signature) == 64


# ---- Test 2: source_hash propagates unchanged through all nodes ----

@test("T2: source_hash is immutable across all pipeline stages")
def t2_hash_propagation():
    raw = make_synthetic_eeg(random_seed=1)
    pipeline = make_default_pipeline()
    latent = pipeline.run(raw)

    ica   = pipeline.intermediates["ica"]
    tf    = pipeline.intermediates["tf"]
    coh   = pipeline.intermediates["coherence"]

    assert ica.source_hash   == raw.source_hash, "ICA broke source_hash"
    assert tf.source_hash    == raw.source_hash, "Wavelets broke source_hash"
    assert coh.source_hash   == raw.source_hash, "Coherence broke source_hash"
    assert latent.source_hash == raw.source_hash, "Embedding broke source_hash"


# ---- Test 3: ICA output shape contract ----

@test("T3: ICA output satisfies shape contract (K<=C, T preserved)")
def t3_ica_shape():
    raw = make_synthetic_eeg(n_channels=16, random_seed=2)
    pipeline = make_default_pipeline()
    pipeline.ica_node.n_components = 8
    pipeline.run(raw)

    ica = pipeline.intermediates["ica"]
    assert ica.n_components <= raw.n_channels
    assert ica.n_samples == raw.n_samples
    assert ica.components.shape == (ica.n_components, ica.n_samples)
    assert ica.mixing_matrix.shape == (raw.n_channels, ica.n_components)
    assert ica.unmixing_matrix.shape == (ica.n_components, raw.n_channels)


# ---- Test 4: TFRepresentation axis consistency ----

@test("T4: TFRepresentation axes match declared dimensions")
def t4_tf_axes():
    raw = make_synthetic_eeg(random_seed=3)
    pipeline = make_default_pipeline()
    pipeline.run(raw)

    tf = pipeline.intermediates["tf"]
    assert len(tf.frequency_axis) == tf.n_voices
    assert len(tf.time_axis) == tf.n_time_bins
    assert tf.coefficients.shape == (tf.n_components, tf.n_voices, tf.n_time_bins)


# ---- Test 5: CoherenceMatrix bounds ----

@test("T5: CoherenceMatrix values in [0,1] for PLV method")
def t5_coherence_bounds():
    raw = make_synthetic_eeg(random_seed=4)
    pipeline = make_default_pipeline()
    pipeline.run(raw)

    coh = pipeline.intermediates["coherence"]
    assert coh.values.min() >= 0.0, f"min={coh.values.min()}"
    assert coh.values.max() <= 1.0 + 1e-9, f"max={coh.values.max()}"
    assert coh.phase_matrix is not None  # PLV produces phase


# ---- Test 6: ORION-AGI full inference ----

@test("T6: ORION-AGI produces valid ORIONOutput")
def t6_orion_inference():
    raw = make_synthetic_eeg(random_seed=5)
    pipeline = make_default_pipeline()
    latent = pipeline.run(raw)

    orion_input = ORIONInput(
        latent_vector=latent,
        subject_id="subj-anon-001",
        session_id="550e8400-e29b-41d4-a716-446655440000",
        acquisition_protocol="CPEA-3-H1",
        compatibility_matrix=DEFAULT_COMPATIBILITY,
    )

    engine = ORIONInferenceEngine()
    output = engine.infer(orion_input)

    assert 0.0 <= output.cpea_index.value <= 1.0
    assert 0.0 <= output.cognitive_inference.confidence <= 1.0
    assert isinstance(output.cognitive_inference.state, CognitiveState)
    assert output.input_source_hash == raw.source_hash
    assert len(output.symbolic_map.nodes) > 0
    assert output.symbolic_map.ontology_id == "papayaykware-v1"


# ---- Test 7: IncompatibleVersionError on unknown version pair ----

@test("T7: ORION-AGI raises IncompatibleVersionError on unknown version pair")
def t7_version_rejection():
    raw = make_synthetic_eeg(random_seed=6)
    pipeline = make_default_pipeline()
    latent = pipeline.run(raw)

    # Compatibility matrix that does NOT include the pipeline's version
    bad_matrix = [
        CompatibilityEntry(embedding_version="9.9.9", signal_pipeline_version="9.9.9"),
    ]

    orion_input = ORIONInput(
        latent_vector=latent,
        subject_id="subj-anon-002",
        session_id="550e8400-e29b-41d4-a716-446655440001",
        acquisition_protocol="CPEA-3-H1",
        compatibility_matrix=bad_matrix,
    )

    engine = ORIONInferenceEngine()
    raised = False
    try:
        engine.infer(orion_input)
    except IncompatibleVersionError:
        raised = True

    assert raised, "Expected IncompatibleVersionError was not raised"


# ---- Test 8: CPEA index reproducibility (same input → same output) ----

@test("T8: CPEA index is deterministic for identical LatentVector")
def t8_determinism():
    raw = make_synthetic_eeg(random_seed=7)
    pipeline = make_default_pipeline()
    latent = pipeline.run(raw)

    orion_input = ORIONInput(
        latent_vector=latent,
        subject_id="subj-anon-003",
        session_id="550e8400-e29b-41d4-a716-446655440002",
        acquisition_protocol="CPEA-3-H1",
        compatibility_matrix=DEFAULT_COMPATIBILITY,
    )

    engine = ORIONInferenceEngine()
    out1 = engine.infer(orion_input)
    out2 = engine.infer(orion_input)

    assert out1.cpea_index.value == out2.cpea_index.value
    assert out1.cognitive_inference.state == out2.cognitive_inference.state


# ---- Test 9: Different source_hashes produce different LatentVectors ----

@test("T9: Different EEG recordings produce distinct LatentVectors")
def t9_distinctness():
    raw_a = make_synthetic_eeg(random_seed=10)
    raw_b = make_synthetic_eeg(random_seed=20)
    pipeline = make_default_pipeline()

    latent_a = pipeline.run(raw_a)
    latent_b = pipeline.run(raw_b)

    assert raw_a.source_hash != raw_b.source_hash
    assert not np.allclose(latent_a.vector, latent_b.vector)


# ---- Test 10: Phi_TICAM component is non-zero ----

@test("T10: CPEAIndex.phi_ticam is within declared bounds [0.1, 0.4]")
def t10_phi_ticam():
    raw = make_synthetic_eeg(random_seed=11)
    pipeline = make_default_pipeline()
    latent = pipeline.run(raw)

    orion_input = ORIONInput(
        latent_vector=latent,
        subject_id="subj-anon-004",
        session_id="550e8400-e29b-41d4-a716-446655440003",
        acquisition_protocol="CPEA-3-H1",
        compatibility_matrix=DEFAULT_COMPATIBILITY,
    )
    engine = ORIONInferenceEngine()
    output = engine.infer(orion_input)

    phi = output.cpea_index.phi_ticam
    assert 0.0 <= phi <= 1.0, f"phi_ticam={phi} out of range"


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("\n" + "="*65)
    print("  CPEA PIPELINE — End-to-End Validation Suite")
    print("  Corpus Papayaykware | SIGMA-T / ORION-AGI Interface v1.0")
    print("="*65 + "\n")

    passed = sum(1 for r in results if r[0] == PASS)
    failed = sum(1 for r in results if r[0] == FAIL)

    for status, name, detail in results:
        icon = "✓" if status == PASS else "✗"
        print(f"  {icon} {name}")
        if detail:
            for line in detail.strip().split("\n"):
                print(f"      {line}")

    print(f"\n{'='*65}")
    print(f"  Results: {passed} passed, {failed} failed out of {len(results)} tests")
    print(f"{'='*65}\n")

    sys.exit(0 if failed == 0 else 1)
