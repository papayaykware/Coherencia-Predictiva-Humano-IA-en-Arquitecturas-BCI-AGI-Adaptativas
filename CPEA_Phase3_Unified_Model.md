# 📡 Coherencia Predictiva EEG–AGI (CPEA)

## 🔹 Fase 3 — Formalización Teórica y Simulación Numérica del Modelo Unificado

---

![Status](https://img.shields.io/badge/status-theoretical%20formalization-blue)
![Stability](https://img.shields.io/badge/stability-condition%20derived-brightgreen)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Math](https://img.shields.io/badge/framework-variational%20dynamics-orange)
![Reproducible](https://img.shields.io/badge/reproducible-notebooks%20included-success)

---

# 📑 Table of Contents

* [Abstract](#abstract)
* [1. Conceptual Framework](#1-conceptual-framework)
* [2. Unified Dynamical Reduction](#2-unified-dynamical-reduction)
* [3. Variational Potential Formulation](#3-variational-potential-formulation)
* [4. Global Stability Analysis](#4-global-stability-analysis)
* [5. Critical Coupling Regime](#5-critical-coupling-regime)
* [6. Numerical Simulation Scheme](#6-numerical-simulation-scheme)
* [7. Stochastic Extension](#7-stochastic-extension)
* [8. Explicit Global Stability Conditions](#8-explicit-global-stability-conditions)
* [9. Reproducible Notebooks](#9-reproducible-notebooks)
* [10. Technical Summary](#10-technical-summary)
* [References (click-to-expand)](#references-click-to-expand)

---

# Abstract

This document presents the unified mathematical formalization of Phase 3 of the CPEA framework. The human EEG dynamical state and AGI latent state are modeled as a bidirectionally coupled nonlinear gradient system. A simplified yet structurally faithful reduction is derived, preserving:

* Variational structure
* Dissipative dynamics
* Nonlinear stabilization
* Critical coupling behavior

Global stability conditions are obtained explicitly using Lyapunov analysis. The model exhibits a well-defined coherence bifurcation regime determined by a closed-form inequality on coupling strength.

The formulation is fully reproducible and computationally tractable.

---

# 1. Conceptual Framework

We formalize the interaction between:

* ( x(t) \in \mathbb{R} ): aggregated EEG state
* ( y(t) \in \mathbb{R} ): AGI latent state

The goal is to represent coherence emergence as a **dynamical phase transition**, not as a physical entanglement phenomenon.

> ⚠️ **Important**
>
> The analogy with physical systems is structural and mathematical, not literal.

---

# 2. Unified Dynamical Reduction

We define the nonlinear bidirectional system:

[
\dot{x} = -a x + k y - \beta x^3
]

[
\dot{y} = -c y + k x - \gamma y^3
]

Where:

| Parameter           | Meaning                 |
| ------------------- | ----------------------- |
| (a, c > 0)          | Intrinsic dissipation   |
| (k)                 | Coupling strength       |
| (\beta, \gamma > 0) | Nonlinear stabilization |

---

# 3. Variational Potential Formulation

The system admits a scalar potential:

[
V(x,y) =
\frac{a}{2}x^2
+
\frac{c}{2}y^2
--------------

kxy
+
\frac{\beta}{4}x^4
+
\frac{\gamma}{4}y^4
]

Such that:

[
\dot{x} = -\frac{\partial V}{\partial x}, \quad
\dot{y} = -\frac{\partial V}{\partial y}
]

---

> 💡 **Key Insight**
>
> The system is a pure gradient flow.
> Therefore, stability analysis reduces to examining coercivity of (V(x,y)).

---

# 4. Global Stability Analysis

Time derivative:

[
\dot{V} =
---------

\left(
\left(\frac{\partial V}{\partial x}\right)^2
+
\left(\frac{\partial V}{\partial y}\right)^2
\right)
\leq 0
]

Thus:

[
V(x,y) \text{ is a Lyapunov function}
]

Stability depends on quadratic form:

[
M =
\begin{pmatrix}
a & -k \
-k & c
\end{pmatrix}
]

Positive definiteness requires:

[
a > 0
]

[
c > 0
]

[
ac - k^2 > 0
]

---

# 5. Critical Coupling Regime

Define determinant:

[
\Delta = ac - k^2
]

| Regime          | Condition  | Interpretation                  |
| --------------- | ---------- | ------------------------------- |
| Weak coupling   | (k^2 < ac) | Unique trivial attractor        |
| Critical point  | (k^2 = ac) | Bifurcation threshold           |
| Strong coupling | (k^2 > ac) | Non-trivial coherent attractors |

---

> 🚀 **CPEA Optimal Zone**
>
> Coherence emerges near:
>
> [
> k^2 \approx ac
> ]

---

# 6. Numerical Simulation Scheme

### Discretized Euler Integration

[
x_{t+1} = x_t + \Delta t(-a x_t + k y_t - \beta x_t^3)
]

[
y_{t+1} = y_t + \Delta t(-c y_t + k x_t - \gamma y_t^3)
]

```python
import numpy as np

def simulate(a, c, k, beta, gamma, dt=0.01, T=10000):
    x, y = 0.5, -0.3
    xs, ys = [], []

    for _ in range(T):
        dx = -a*x + k*y - beta*x**3
        dy = -c*y + k*x - gamma*y**3
        
        x += dt*dx
        y += dt*dy
        
        xs.append(x)
        ys.append(y)
    
    return np.array(xs), np.array(ys)
```

---

# 7. Stochastic Extension

Additive noise:

[
dx = f(x,y)dt + \sigma_x dW_x
]

[
dy = g(x,y)dt + \sigma_y dW_y
]

Stability preserved if:

[
\sigma^2 \ll \lambda_{min}(Hessian(V))
]

---

# 8. Explicit Global Stability Conditions

The system is globally stable if:

```
a > 0
c > 0
beta > 0
gamma > 0
k^2 < ac
```

It exhibits coherent attractor states if:

```
ac < k^2 < ac + Δ
```

Where (Δ) depends on nonlinear terms.

---

# 9. Reproducible Notebooks

| Notebook                                                                                                                   | Description          |
| -------------------------------------------------------------------------------------------------------------------------- | -------------------- |
| [`01_gradient_dynamics.ipynb`](https://github.com/papayaykware/METFI/tree/main/notebooks/01_gradient_dynamics.ipynb)       | Deterministic system |
| [`02_bifurcation_analysis.ipynb`](https://github.com/papayaykware/METFI/tree/main/notebooks/02_bifurcation_analysis.ipynb) | Coupling threshold   |
| [`03_stochastic_extension.ipynb`](https://github.com/papayaykware/METFI/tree/main/notebooks/03_stochastic_extension.ipynb) | Noise robustness     |

---

# 10. Technical Summary

* The unified CPEA model reduces to a nonlinear gradient system.
* A closed-form Lyapunov function guarantees global stability.
* Explicit condition: (k^2 < ac).
* Critical coherence emerges at (k^2 = ac).
* Nonlinear stabilization prevents divergence.
* The model supports deterministic and stochastic extensions.
* Fully reproducible computational implementation provided.

---

# References (click-to-expand)

<details>
<summary><strong>Strogatz, S. (2000)</strong></summary>

From Kuramoto to Crawford: exploring synchronization in coupled oscillators.
Classic reference for phase transitions in nonlinear networks.

DOI: [https://doi.org/10.1016/S0167-2789(00)00094-4](https://doi.org/10.1016/S0167-2789%2800%2900094-4)

</details>

---

<details>
<summary><strong>Amari, S. (1998)</strong></summary>

Natural Gradient Works Efficiently in Learning.
Foundational work on information geometry and Fisher metric.

DOI: [https://doi.org/10.1162/089976698300017746](https://doi.org/10.1162/089976698300017746)

</details>

---

<details>
<summary><strong>Friston, K. (2010)</strong></summary>

The free-energy principle: a unified brain theory.

DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)

</details>

---

<details>
<summary><strong>Breakspear, M. (2017)</strong></summary>

Dynamic models of large-scale brain activity.

DOI: [https://doi.org/10.1038/nrn.2017.12](https://doi.org/10.1038/nrn.2017.12)

</details>

---

# 📌 Repository Structure Suggestion

```
CPEA/
│
├── docs/
│   └── CPEA_Phase3_Unified_Model.md
│
├── notebooks/
│   ├── 01_gradient_dynamics.ipynb
│   ├── 02_bifurcation_analysis.ipynb
│   └── 03_stochastic_extension.ipynb
│
└── src/
    └── unified_model.py
```
