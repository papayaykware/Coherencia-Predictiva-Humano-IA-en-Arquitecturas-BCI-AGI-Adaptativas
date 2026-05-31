# CPEA Pipeline — Interface Specification & Stubs

**Corpus Papayaykware | Serie CPEA/TICAM**
**Conceptual author:** Claude (Anthropic) | **Corpus director:** Javi Ciborro ([@papayaykware](https://github.com/papayaykware))

---

## What this is

Formal interface specification and stub implementations for the two structural connectors of the **CPEA** (Coherencia Predictiva EEG-AGI) architecture:

- **SIGMA-T** — Signal Integration Graph for Multilayer Analysis – Toroidal
  DAG pipeline: `EEG_raw → ICA → Wavelets → Coherence → Embedding → LatentVector`

- **ORION-AGI** — Ontological Recursive Intelligence Orchestration Network
  Inference engine: `LatentVector → CognitiveInference + CPEAIndex + SymbolicMap`

The stubs validate the pipeline end-to-end using synthetic data. Any implementation that satisfies the formal interface contracts in `docs/INTERFACE_SPEC_v1.0.md` is drop-in interchangeable with the stubs — this is the core architectural guarantee of SIGMA-T.

---

## Structure

```
cpea-interfaces/
├── docs/
│   └── INTERFACE_SPEC_v1.0.md   ← formal interface contracts (read this first)
├── stubs/
│   ├── types.py                 ← shared dataclasses and error types
│   ├── sigma_t_stub.py          ← SIGMA-T mock implementation
│   └── orion_agi_stub.py        ← ORION-AGI mock implementation
├── tests/
│   └── test_e2e_pipeline.py     ← 10 end-to-end tests with synthetic data
└── README.md
```

---

## Quick start

```bash
pip install numpy
python tests/test_e2e_pipeline.py
```

With pytest:

```bash
pip install pytest numpy
pytest tests/test_e2e_pipeline.py -v
```

Expected output (all 10 tests passing):

```
  ✓ T1: Full E2E pipeline completes on synthetic data
  ✓ T2: source_hash is immutable across all pipeline stages
  ✓ T3: ICA output satisfies shape contract (K<=C, T preserved)
  ✓ T4: TFRepresentation axes match declared dimensions
  ✓ T5: CoherenceMatrix values in [0,1] for PLV method
  ✓ T6: ORION-AGI produces valid ORIONOutput
  ✓ T7: ORION-AGI raises IncompatibleVersionError on unknown version pair
  ✓ T8: CPEA index is deterministic for identical LatentVector
  ✓ T9: Different EEG recordings produce distinct LatentVectors
  ✓ T10: CPEAIndex.phi_ticam is within declared bounds [0.1, 0.4]

Results: 10 passed, 0 failed out of 10 tests
```

---

## Key design principles

**Intercambiabilidad:** Each pipeline node is specified by its input/output types, not its implementation. FastICA and Infomax both satisfy the ICA contract — swapping one for the other requires zero changes to downstream nodes.

**Trazabilidad:** Every `LatentVector` carries `embedding_version`, `signal_pipeline_version`, and `model_signature`. ORION-AGI enforces a `CompatibilityMatrix` before any inference — incompatible version pairs raise `IncompatibleVersionError` and halt.

**Integridad del hash:** The `source_hash` (SHA-256 of the original raw EEG) is computed once at acquisition and propagated immutably through every node. Any mutation raises `HashMismatchError`.

---

## Theoretical context

This repository implements Phase 6 hito of the TICAM-1 roadmap within the TAE-AGI/CPEA/METFI series. For theoretical background see:

- `INTERFACE_SPEC_v1.0.md` — formal contracts
- [papayaykware.blogspot.com](https://papayaykware.blogspot.com) — corpus articles
- CPEA-3 pre-registration (OSF, forthcoming)

---

*Spec version: 1.0.0 | 2026-05-30*
