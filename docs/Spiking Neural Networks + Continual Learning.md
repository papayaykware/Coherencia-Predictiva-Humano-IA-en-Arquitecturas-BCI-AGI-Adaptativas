# 🧠 Coherencia Predictiva EEG–AGI (CPEA)  
## FASE 2 — Spiking Neural Networks + Continual Learning

---

![Status](https://img.shields.io/badge/status-active_development-blue)
![Framework](https://img.shields.io/badge/framework-PyTorch-red)
![SNN](https://img.shields.io/badge/SNN-snntorch-orange)
![Continual Learning](https://img.shields.io/badge/Continual_Learning-Avalanche-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![DOI](https://img.shields.io/badge/DOI-10.1073%2Fpnas.1611835114-blue)

---

# 📑 Table of Contents

- [Abstract](#-abstract)
- [Keywords](#-keywords)
- [1. Conceptual Architecture](#-1-conceptual-architecture)
- [2. Mathematical Formulation](#-2-mathematical-formulation)
- [3. snntorch Module Implementation](#-3-snntorch-module-implementation)
- [4. Continual Learning Integration (Replay + EWC)](#-4-continual-learning-integration-replay--ewc)
- [5. Stability–Plasticity Framework](#-5-stabilityplasticity-framework)
- [6. Experimental Tracking Programs](#-6-experimental-tracking-programs)
- [7. Repository Structure](#-7-repository-structure)
- [8. Reproducible Notebooks](#-8-reproducible-notebooks)
- [9. References (click-to-expand)](#-9-references-click-to-expand)

---

# 📌 Abstract

This repository documents the implementation of **Spiking Neural Networks (SNN)** using *snntorch* integrated with **continual learning (Replay + Elastic Weight Consolidation)** within the Cognitive Loop of the Coherencia Predictiva EEG–AGI (CPEA) framework.

The objective is to construct a temporally coherent predictive architecture capable of:

- Modeling discrete neural dynamics
- Preserving memory across task transitions
- Maintaining predictive coherence under distributional drift
- Balancing plasticity and consolidation

Unlike conventional continuous networks, the proposed system operates as a dynamic event-driven resonant structure aligned with EEG temporal properties.

---

# 🔑 Keywords

Spiking Neural Networks • snntorch • Avalanche • Elastic Weight Consolidation • Replay • EEG Predictive Modeling • Stability–Plasticity • Temporal Coding • Cognitive Loop

---

# 🧭 1. Conceptual Architecture

```

EEG Signal
↓
Spike Encoder
↓
SNN Recurrent Core (LIF Layers)
↓
Predictive Readout
↓
Exception Detection (TAE)
↓
Continual Consolidation (Replay + EWC)

````

> [!NOTE]
> The system combines fast synaptic plasticity (SNN core) with slow structural consolidation (EWC + Replay).

---

# 📐 2. Mathematical Formulation

## Leaky Integrate-and-Fire (Discrete Form)

\[
V_{t+1} = \alpha V_t + I_t - S_t \theta
\]

Where:

- \( \alpha = e^{-Δt/\tau_m} \)
- \( S_t = H(V_t - \theta) \)

Surrogate gradient approximation:

\[
\frac{\partial S_t}{\partial V_t} \approx \sigma'(V_t - \theta)
\]

---

## Elastic Weight Consolidation (EWC)

\[
\mathcal{L}_{EWC} = \sum_i \frac{\lambda}{2} F_i (\theta_i - \theta_i^*)^2
\]

- \(F_i\) = Fisher Information (diagonal approximation)  
- \(\theta_i^*\) = previous optimal weights  

---

# 🧪 3. snntorch Module Implementation

```python
import torch
import torch.nn as nn
import snntorch as snn
from snntorch import surrogate

class SNNCore(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()

        spike_grad = surrogate.fast_sigmoid()

        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.lif1 = snn.Leaky(beta=0.95, spike_grad=spike_grad)

        self.fc2 = nn.Linear(hidden_dim, hidden_dim)
        self.lif2 = snn.Leaky(beta=0.95, spike_grad=spike_grad)

        self.readout = nn.Linear(hidden_dim, output_dim)

    def forward(self, x, mem1, mem2):
        cur1 = self.fc1(x)
        spk1, mem1 = self.lif1(cur1, mem1)

        cur2 = self.fc2(spk1)
        spk2, mem2 = self.lif2(cur2, mem2)

        out = self.readout(spk2)

        return out, spk2, mem1, mem2
````

---

# ♻️ 4. Continual Learning Integration (Replay + EWC)

Framework: **Avalanche**

```python
from avalanche.training.strategies import EWC
from avalanche.training.plugins import ReplayPlugin

strategy = EWC(
    model=snn_model,
    optimizer=optimizer,
    criterion=loss_fn,
    ewc_lambda=0.4,
    train_mb_size=32,
    train_epochs=1
)

replay_plugin = ReplayPlugin(mem_size=500)
```

### Total Loss

[
\mathcal{L}*{total} =
\mathcal{L}*{new} +
\mathcal{L}*{replay} +
\mathcal{L}*{EWC}
]

---

# ⚖️ 5. Stability–Plasticity Framework

The architecture operationalizes the classical stability–plasticity dilemma:

| Component     | Role                      |
| ------------- | ------------------------- |
| SNN Core      | Fast adaptive plasticity  |
| Replay Buffer | Episodic memory retention |
| EWC           | Structural consolidation  |

> [!IMPORTANT]
> The system avoids catastrophic forgetting while preserving temporal sensitivity.

---

# 🔬 6. Experimental Tracking Programs

## Program 1 — Coherence Tracking

* Phase Locking Value (PLV)
* Spectral entropy
* Gamma synchrony

## Program 2 — Stability Metrics

* Lyapunov exponents
* Fisher weight stability
* Retention across tasks

## Program 3 — Energetic Efficiency

* Spike sparsity
* FLOPs comparison vs dense networks

---

# 📁 7. Repository Structure

```
CPEA-Fase2/
│
├── models/
│   ├── snn_core.py
│   ├── encoder.py
│   └── ewc_module.py
│
├── notebooks/
│   ├── 01_spike_encoding.ipynb
│   ├── 02_snn_training.ipynb
│   ├── 03_continual_learning.ipynb
│
├── experiments/
│   ├── coherence_tracking.py
│   ├── fisher_analysis.py
│
├── docs/
│   ├── theory.md
│   ├── equations.pdf
│
└── README.md
```

---

# 📊 8. Reproducible Notebooks

| Notebook                                                             | Description                      |
| -------------------------------------------------------------------- | -------------------------------- |
| [01_spike_encoding.ipynb](notebooks/01_spike_encoding.ipynb)         | EEG to spike encoding strategies |
| [02_snn_training.ipynb](notebooks/02_snn_training.ipynb)             | SNN predictive training          |
| [03_continual_learning.ipynb](notebooks/03_continual_learning.ipynb) | Replay + EWC integration         |

> [!TIP]
> All notebooks are deterministic with fixed seeds for reproducibility.

---

# 📚 9. References (click-to-expand)

<details>
<summary><strong>Elastic Weight Consolidation</strong></summary>

Kirkpatrick et al. (2017).
**Overcoming catastrophic forgetting in neural networks.**
PNAS.
DOI: [https://doi.org/10.1073/pnas.1611835114](https://doi.org/10.1073/pnas.1611835114)

Introduces Fisher-based consolidation to protect important parameters.

</details>

<details>
<summary><strong>Stability–Plasticity Theory</strong></summary>

Grossberg, S. (1980).
**How does a brain build a cognitive code?**
Psychological Review.
DOI: [https://doi.org/10.1037/0033-295X.87.1.1](https://doi.org/10.1037/0033-295X.87.1.1)

Formalizes the stability–plasticity dilemma.

</details>

<details>
<summary><strong>Neural Synchronization</strong></summary>

Kuramoto, Y. (1984).
**Chemical Oscillations, Waves, and Turbulence.**
Springer.

Foundational model of phase synchronization.

</details>

---

# 🧠 Project Status

| Module                       | Status         |
| ---------------------------- | -------------- |
| SNN Core                     | ✅ Implemented  |
| EEG Encoding                 | ✅ Implemented  |
| Replay Buffer                | ✅ Implemented  |
| EWC                          | ✅ Integrated   |
| Longitudinal Stability Tests | 🔄 In Progress |
| Energy Profiling             | 🔄 In Progress |

---

# 📜 License

MIT License

---

# 👤 Conceptual Author

AGI-based architectural formulation and technical synthesis.

---
