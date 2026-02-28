# 🧠 Coherencia Predictiva EEG–AGI (CPEA)

[![Status](https://img.shields.io/badge/status-active_research-blue)](#)
[![Stage](https://img.shields.io/badge/stage-Phase_4_Publication-purple)](#)
[![License](https://img.shields.io/badge/license-MIT-green)](#)
[![Python](https://img.shields.io/badge/python-3.10+-yellow)](#)
[![PyTorch](https://img.shields.io/badge/framework-PyTorch-red)](#)
[![BCI](https://img.shields.io/badge/domain-BCI-critical)](#)

---

> **Dynamic Structural Alignment Between Neural Oscillations and Adaptive Artificial Systems**

---

# 📑 Table of Contents

* [Overview](#-overview)
* [Conceptual Framework](#-conceptual-framework)
* [Mathematical Formulation](#-mathematical-formulation)
* [System Architecture](#-system-architecture)
* [Experimental Modes](#-experimental-modes)
* [Reproducibility](#-reproducibility)
* [Notebooks](#-notebooks)
* [Technical Boundaries](#-technical-boundaries)
* [Scientific References](#-scientific-references)
* [Citation](#-citation)
* [License](#-license)

---

# 📌 Overview

CPEA introduces a structural paradigm shift in Brain–Computer Interfaces.

Traditional BCI systems perform static classification over EEG feature vectors.
CPEA models the interaction between neural activity and artificial systems as a **dynamical coupling problem**.

The central hypothesis:

> A stable Brain–AI interaction emerges when the latent representation of the model evolves coherently with the oscillatory structure of the EEG signal.

This repository contains:

* Adaptive EEG processing pipeline
* Deep representation model
* Phase coherence module
* Continual learning integration
* Interactive Hugging Face demo

---

# 🧩 Conceptual Framework

## From Classification to Dynamic Alignment

Instead of asking:

```
What class does this EEG segment represent?
```

CPEA evaluates:

```
Is the internal state of the model dynamically aligned with neural oscillatory structure?
```

This reframes BCI as a **nonlinear dynamical alignment problem**.

---

> [!NOTE]
> Coherence is treated as an intrinsic structural metric, not merely a statistical correlation.

---

# 📐 Mathematical Formulation

Let:

* ( X(t) ): multichannel EEG signal
* ( Z(t) ): latent embedding
* ( \mathcal{H} ): Hilbert transform

### Coherence Index

[
C(t) = \frac{|\langle \mathcal{H}(X(t)), \mathcal{H}(Z(t)) \rangle|}{|\mathcal{H}(X(t))||\mathcal{H}(Z(t))|}
]

### Training Objective

[
\mathcal{L} = \mathcal{L}*{task} - \lambda C(t) + \gamma \mathcal{L}*{EWC}
]

Where:

* ( \mathcal{L}_{task} ): classification loss
* ( \mathcal{L}_{EWC} ): Elastic Weight Consolidation penalty

---

# 🏗 System Architecture

## 1️⃣ Signal Processing Layer

* Band-pass filtering (1–40 Hz)
* ICA artifact attenuation
* Continuous Wavelet Transform

## 2️⃣ Deep Representation Layer

* Temporal convolutions
* Lightweight Transformer encoder
* Latent embedding space

## 3️⃣ Coherence Module

* Instantaneous phase extraction
* Cosine phase similarity
* Continuous structural scoring

## 4️⃣ Continual Learning Core

* Elastic Weight Consolidation
* Selective replay buffer
* Incremental embedding adaptation

---

> [!TIP]
> Coherence drop triggers adaptive update before classification collapse occurs.

---

# 🧪 Experimental Modes

| Mode            | Description            | Purpose              |
| --------------- | ---------------------- | -------------------- |
| Baseline        | No adaptation          | Static comparison    |
| Adaptive        | Online updates enabled | Stability evaluation |
| Noise Injection | EMG contamination      | Robustness test      |
| Cross-Subject   | Transfer learning      | Generalization       |

---

<details>
<summary><strong>📊 Metrics Reported</strong></summary>

* Classification Accuracy
* Coherence Index ( C(t) )
* Adaptation Latency
* Parameter Drift Magnitude
* Spectral Stability

</details>

---

# 🔬 Reproducibility

Public EEG datasets supported:

* Motor Imagery datasets
* SSVEP benchmarks

Full training pipeline documented in:

```
/training_pipeline.md
```

Hyperparameters available in:

```
/configs/default.yaml
```

---

# 📓 Notebooks

| Notebook                                                               | Description             |
| ---------------------------------------------------------------------- | ----------------------- |
| [01_preprocessing.ipynb](./notebooks/01_preprocessing.ipynb)           | EEG preprocessing       |
| [02_model_training.ipynb](./notebooks/02_model_training.ipynb)         | Model training          |
| [03_coherence_analysis.ipynb](./notebooks/03_coherence_analysis.ipynb) | Coherence visualization |
| [04_continual_learning.ipynb](./notebooks/04_continual_learning.ipynb) | Online adaptation       |

---

# ⚠ Technical Boundaries

> [!WARNING]
> This demo is research-grade and not a clinical system.

Limitations:

* Simulated near-real-time inference
* Limited electrode montage
* No hardware-level BCI integration
* Reduced artifact modeling

---

# 📚 Scientific References

<details>
<summary><strong>Buzsáki, G. (2006). Rhythms of the Brain</strong></summary>

Oxford University Press.
Comprehensive analysis of neural oscillations and synchronization.

</details>

<details>
<summary><strong>Freeman, W. J. (2000). Neurodynamics</strong></summary>

Springer.
Nonlinear dynamical models of cortical activity.

</details>

<details>
<summary><strong>Kirkpatrick et al. (2017). Overcoming catastrophic forgetting</strong></summary>

PNAS. DOI: [https://doi.org/10.1073/pnas.1611835114](https://doi.org/10.1073/pnas.1611835114)
Introduces Elastic Weight Consolidation.

</details>

<details>
<summary><strong>Delorme & Makeig (2004). EEGLAB</strong></summary>

J. Neurosci. Methods. DOI: [https://doi.org/10.1016/j.jneumeth.2003.10.009](https://doi.org/10.1016/j.jneumeth.2003.10.009)
Standard open-source EEG processing framework.

</details>

<details>
<summary><strong>Roy et al. (2019). Deep learning-based EEG analysis</strong></summary>

J. Neural Engineering. DOI: [https://doi.org/10.1088/1741-2552/ab260c](https://doi.org/10.1088/1741-2552/ab260c)
Systematic review of deep EEG architectures.

</details>

---

# 📎 Citation

If using this framework:

```bibtex
@article{CPEA2026,
  title={Coherence Predictive EEG–AGI: Dynamic Structural Alignment},
  author={Conceptual Author: AGI},
  year={2026},
  note={Phase 4 Technical Publication}
}
```

---

# 📜 License

MIT License.

---

# 🌐 Hugging Face Demo

🔗 [https://huggingface.co/spaces/your_space_link](https://huggingface.co/spaces/your_space_link)

---

# 📌 Project Status

```
Phase 4 — Technical Publication
Hugging Face Demo Active
Preprint Preparation Ongoing
Community Feedback Collection Active
```
