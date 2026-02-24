# 🧠 Coherencia Predictiva EEG–AGI (CPEA)

[![Status](https://img.shields.io/badge/status-Phase%201%20Infrastructure-blue)]()
[![Validation](https://img.shields.io/badge/validation-intersubject%20enabled-brightgreen)]()
[![Dataset](https://img.shields.io/badge/dataset-PhysioNet-lightgrey)](https://physionet.org/)
[![License](https://img.shields.io/badge/license-MIT-black)]()
[![Reproducible](https://img.shields.io/badge/reproducibility-notebooks%20included-orange)]()

---

> **Project:** Coherencia Predictiva EEG–AGI (CPEA)  
> **Scope:** Infraestructura y Marco Experimental — Fase 1  
> **Author conceptual:** AGI Research Architecture  
> **Domain:** Neurodynamics · Predictive Modeling · Topological Embeddings  

---

# 📑 Table of Contents

- [1. Abstract](#abstract)
- [2. Keywords](#keywords)
- [3. Theoretical Framework](#theoretical-framework)
- [4. Mathematical Formalization](#mathematical-formalization)
- [5. Experimental Infrastructure (Phase 1)](#experimental-infrastructure-phase-1)
- [6. Cross-Dataset Validation (PhysioNet)](#cross-dataset-validation-physionet)
- [7. Predictive Latent Architecture](#predictive-latent-architecture)
- [8. Topological Analysis](#topological-analysis)
- [9. Monitoring Programs](#monitoring-programs)
- [10. Executive Summary](#executive-summary)
- [11. References (click-to-expand)](#references-click-to-expand)

---

---

# 1. Abstract
<a name="abstract"></a>

This work introduces the Predictive Coherence Index (PCI) within the framework of the EEG–AGI Coherence Project (CPEA). The model redefines neural coherence not as static synchrony but as structural anticipatory stability. The PCI integrates spectral coherence, latent predictive accuracy, and multiscale entropy stability into a unified metric.

Phase 1 establishes an infrastructure enabling intersubject validation using PhysioNet datasets, thereby eliminating hardware and cohort bias. The approach combines nonlinear neurodynamics with deep representation learning to characterize stable trajectories in latent manifold space.

---

# 2. Keywords
<a name="keywords"></a>

EEG · Predictive Coherence · Nonlinear Dynamics · Latent Embeddings · Multiscale Entropy · PhysioNet · Topological Stability · Transformer Models

---

---

# 3. Theoretical Framework
<a name="theoretical-framework"></a>

> [!NOTE]
> Coherence is redefined as anticipatory structural stability, not mere synchrony.

Classical coherence metrics evaluate phase consistency. However, biological systems operate in metastable regimes characterized by nonlinear attractor dynamics. True functional coherence implies predictability within bounded entropy.

The brain is modeled as a dynamic network of coupled oscillatory dipoles generating measurable electromagnetic fields. Stability in these configurations implies reduced latent prediction error.

---

---

# 4. Mathematical Formalization
<a name="mathematical-formalization"></a>

## 4.1 Predictive Coherence Index (PCI)

\[
PCI = \alpha C_s + \beta P_l + \gamma S_e
\]

Where:

- \( C_s \) = Spectral coherence (8–30 Hz integration)
- \( P_l \) = Latent predictive accuracy
- \( S_e \) = Multiscale entropy stability
- \( \alpha, \beta, \gamma \in [0,1] \)

---

## 4.2 Latent Predictive Term

\[
Z_t = f_{\theta}(X_{t-k:t})
\]

\[
P_l = 1 - \frac{\mathbb{E}[(Z_{t+1} - \hat{Z}_{t+1})^2]}{\sigma_Z^2}
\]

Low normalized prediction error implies structural coherence.

---

## 4.3 Entropic Stability

\[
S_e = 1 - \frac{H_m(X)}{H_{max}}
\]

Optimal biological coherence resides in intermediate entropy regimes.

---

---

# 5. Experimental Infrastructure (Phase 1)
<a name="experimental-infrastructure-phase-1"></a>

## 🔹 Pipeline

```

EEG Raw
→ 8–30 Hz Bandpass
→ Artifact Removal (ICA / ASR)
→ Segmentation
→ Foundation Model (Denoising + Embedding)
→ PCI Computation
→ Classification / Regression

```

---

## 🧪 Hardware Robustness

> [!IMPORTANT]
> PCI must remain stable across hardware resolution variability.

Evaluation includes:
- Clinical high-density EEG
- Portable EEG systems

---

---

# 6. Cross-Dataset Validation (PhysioNet)
<a name="cross-dataset-validation-physionet"></a>

[PhysioNet](https://physionet.org/) enables unbiased validation.

### Recommended Datasets:

- Motor Movement/Imagery
- CHB-MIT Scalp EEG
- Sleep-EDF

---

### Cross-Dataset Protocol

1. Train on Dataset A  
2. Validate on Dataset B  
3. Evaluate PCI distribution invariance  

> [!WARNING]
> If PCI collapses under transfer, coherence may be dataset-specific rather than structural.

---

---

# 7. Predictive Latent Architecture
<a name="predictive-latent-architecture"></a>

## 🧠 Model Backbone

- Temporal Convolutional Encoder  
- Transformer Blocks  
- Autoregressive Latent Predictor  

Latent manifold \( Z \in \mathbb{R}^d \) is evaluated for:

- Dimensionality collapse
- Curvature stability
- Trajectory continuity

---

### Intrinsic Dimensionality

\[
d_{int} = \frac{\sum \lambda_i^2}{\sum \lambda_i}
\]

Eigenvalue concentration signals structural compression.

---

---

# 8. Topological Analysis
<a name="topological-analysis"></a>

Persistent homology applied to latent trajectories enables:

- Cycle persistence detection
- Structural robustness analysis
- State-transition topology mapping

---

> [!TIP]
> Stable cognitive states exhibit persistent topological invariants.

---

---

# 9. Monitoring Programs
<a name="monitoring-programs"></a>

## Program 1 — Longitudinal Stability

- Weekly EEG acquisition (3 months)
- Rest vs task comparison
- PCI variance threshold <10%

---

## Program 2 — Cognitive Perturbation

- Stroop task
- Sleep restriction
- Guided meditation

Measure displacement in latent manifold.

---

## Program 3 — Hardware Generalization

Cross-device PCI comparison.

---

---

# 10. Reproducible Notebooks
<a name="reproducible-notebooks"></a>

| Notebook | Description |
|-----------|-------------|
| [PCI Computation](notebooks/PCI_computation.ipynb) | End-to-end pipeline |
| [Cross-Dataset Validation](notebooks/Cross_dataset_validation.ipynb) | Transfer protocol |
| [Topological Analysis](notebooks/Topological_analysis.ipynb) | Persistent homology |
| [Latent Visualization](notebooks/Latent_manifold_projection.ipynb) | UMAP / PCA |

---

---

# 11. Executive Summary
<a name="executive-summary"></a>

- Coherence is redefined as predictive structural stability.
- PCI integrates spectral, entropic, and predictive components.
- PhysioNet ensures intersubject robustness.
- Latent embedding continuity determines functional integrity.
- Topological persistence provides structural validation.
- Cross-dataset invariance is the ontological test.

---

---

# 12. References (click-to-expand)
<a name="references-click-to-expand"></a>

<details>
<summary>📚 Core Scientific References (DOI included)</summary>

**Friston, K. (2010).** The free-energy principle.  
Nature Reviews Neuroscience.  
DOI: https://doi.org/10.1038/nrn2787  

**Breakspear, M. (2017).** Dynamic models of large-scale brain activity.  
Nature Neuroscience.  
DOI: https://doi.org/10.1038/nn.4497  

**Costa, M., Goldberger, A., Peng, C.K. (2005).** Multiscale entropy analysis.  
Physical Review E.  
DOI: https://doi.org/10.1103/PhysRevE.71.021906  

**Schirrmeister, R. et al. (2017).** Deep learning for EEG decoding.  
Human Brain Mapping.  
DOI: https://doi.org/10.1002/hbm.23730  

**Goldberger, A. et al. (2000).** PhysioNet resource.  
Circulation.  
DOI: https://doi.org/10.1161/01.CIR.101.23.e215  

</details>

---

---

# 🧭 Repository Structure

```

CPEA/
│
├── README.md
├── data/
├── notebooks/
├── src/
├── results/
└── docs/

```

---

# ⚖ License

MIT License

---

# 🔬 Status

Phase 1 Infrastructure Complete  
Cross-dataset validation ongoing  
Topological module active  

---
