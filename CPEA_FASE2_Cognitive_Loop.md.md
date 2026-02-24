# 🧠 CPEA — FASE 2

# 🔁 Construcción del Bucle Cognitivo EEG–AGI

## Protocolo Matemático y Especificación Algorítmica Online

---

![Status](https://img.shields.io/badge/status-active_development-blue)
![Framework](https://img.shields.io/badge/framework-PyTorch-red)
![License](https://img.shields.io/badge/license-MIT-green)
![Version](https://img.shields.io/badge/version-2.0-critical_loop)
![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.XXXXXXX-lightgrey)

---

> ⚠️ **Documento técnico avanzado**
> Este documento formaliza matemáticamente la FASE 2 del proyecto CPEA: construcción del bucle cognitivo adaptativo EEG–AGI con coherencia predictiva bidireccional.

---

# 📚 Tabla de Contenidos

* [1. Introducción](#1-introducción)
* [2. Formalización Matemática](#2-formalización-matemática)

  * [2.1 Notación](#21-notación)
  * [2.2 Modelo Generativo](#22-modelo-generativo)
  * [2.3 Función de Pérdida Compuesta](#23-función-de-pérdida-compuesta)
  * [2.4 Métrica de Coherencia Predictiva](#24-métrica-de-coherencia-predictiva)
* [3. Arquitectura PyTorch](#3-arquitectura-pytorch)
* [4. Módulo de Adaptación Online](#4-módulo-de-adaptación-online)
* [5. Régimen Crítico Dinámico](#5-régimen-crítico-dinámico)
* [6. Protocolo Experimental](#6-protocolo-experimental)
* [7. Notebooks Reproducibles](#7-notebooks-reproducibles)
* [8. Referencias](#8-referencias)

---

# 1️⃣ Introducción

La FASE 2 del proyecto CPEA transforma un modelo predictivo unidireccional en un **sistema dinámico de acoplamiento recíproco**. El objetivo no es únicamente predecir EEG, sino establecer una reducción estructurada y sostenida del error dinámico bajo condiciones de no estacionariedad.

La coherencia predictiva se define como:

[
CP_t = 1 - \frac{H(X_{t+1} | Z_t)}{H(X_{t+1})}
]

donde ( Z_t ) representa el embedding latente del modelo artificial.

---

# 2️⃣ Formalización Matemática

## 2.1 Notación

* ( X_t \in \mathbb{R}^{C \times T} ): ventana EEG multicanal
* ( Z_t \in \mathbb{R}^{d} ): estado latente
* ( \theta ): parámetros del modelo
* ( \hat{X}_{t+1} ): predicción

---

## 2.2 Modelo Generativo

[
Z_t = f_\theta(X_t)
]

[
\hat{X}*{t+1} = g*\theta(Z_t)
]

Modelo probabilístico:

[
p_\theta(X_{t+1} | Z_t) =
\mathcal{N}(\mu_\theta(Z_t), \Sigma_\theta(Z_t))
]

---

## 2.3 Función de Pérdida Compuesta

[
\mathcal{L}*t =
\alpha \mathcal{L}*{pred}

* \beta \mathcal{L}_{spectral}
* \gamma \mathcal{L}_{entropy}
* \lambda \mathcal{L}_{stability}
  ]

### 🔹 Pérdida predictiva

[
\mathcal{L}*{pred} =
||X*{t+1} - \hat{X}_{t+1}||^2
]

### 🔹 Pérdida espectral

[
\mathcal{L}*{spectral} =
||FFT(X*{t+1}) - FFT(\hat{X}_{t+1})||^2
]

### 🔹 Penalización de estabilidad latente

[
\mathcal{L}*{stability} =
||Z_t - Z*{t-1}||^2
]

---

## 2.4 Métrica de Coherencia Predictiva

Aproximación práctica:

[
CP_t \approx
1 - \frac{\mathcal{L}_{pred}}{\sigma_X^2}
]

Suavizado exponencial:

[
\bar{CP}*t =
\eta CP_t + (1-\eta)\bar{CP}*{t-1}
]

---

# 3️⃣ Arquitectura PyTorch

> 💡 Recomendación: Transformer causal + generador lineal probabilístico

```python
class EEGEncoder(nn.Module):
    def __init__(self, d_model, nhead, num_layers):
        super().__init__()
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

    def forward(self, x):
        return self.transformer(x)

class Generator(nn.Module):
    def __init__(self, d_model, out_dim):
        super().__init__()
        self.fc_mu = nn.Linear(d_model, out_dim)
        self.fc_logvar = nn.Linear(d_model, out_dim)

    def forward(self, z):
        return self.fc_mu(z), self.fc_logvar(z)
```

---

# 4️⃣ Módulo de Adaptación Online

## Activación Condicional

[
\Delta CP_t = \bar{CP}*t - \bar{CP}*{t-1}
]

Si:

[
\Delta CP_t < -\delta
]

→ aumentar tasa de aprendizaje.

---

## Tasa dinámica

[
\eta_t = \eta_0 (1 + k|\Delta CP_t|)
]

---

## Regularización EWC

[
\mathcal{L}_{EWC} =
\sum_i F_i(\theta_i - \theta_i^*)^2
]

---

### 🔁 Algoritmo Online

```python
for X_t in stream:

    Z_t = encoder(X_t)
    mu, logvar = generator(Z_t)

    loss = compute_loss(X_t_next, mu, logvar)

    CP = compute_coherence(loss)

    if CP_drop_detected:
        optimizer.param_groups[0]["lr"] *= 1.5

    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    optimizer.step()
```

---

# 5️⃣ Régimen Crítico Dinámico

Estimación tipo Lyapunov:

[
\lambda_{local} =
\frac{1}{\Delta t}
\log \frac{||Z_t - Z_{t-1}||}
{||Z_{t-1} - Z_{t-2}||}
]

Objetivo:

[
\lambda_{local} \approx 0
]

---

> 📌 **Interpretación**
>
> * ( \lambda > 0 ) → inestabilidad
> * ( \lambda < 0 ) → rigidez excesiva
> * ( \lambda \approx 0 ) → régimen óptimo

---

# 6️⃣ Protocolo Experimental

### 🧪 Programa 1 — Estabilidad bajo no estacionariedad

* Ventanas deslizantes 5–10 s
* Tareas cognitivas variables
* Seguimiento de CP

---

### 🧪 Programa 2 — Perturbación controlada

* Estímulos impredecibles
* Medición de tiempo de recuperación

---

### 🧪 Programa 3 — Transferencia de Información

Basado en entropía de transferencia:

[
TE_{EEG→Model}
]

---

# 7️⃣ Notebooks Reproducibles

📂 `/notebooks/`

* `01_preprocessing.ipynb`
* `02_encoder_training.ipynb`
* `03_online_adaptation.ipynb`
* `04_critical_regime_analysis.ipynb`

🔗 Ejecución recomendada en:

* Google Colab
* Paperspace
* Local GPU

---

# 8️⃣ Referencias

<details>
<summary>📘 Karl Friston — Free Energy Principle</summary>

Friston, K. (2010). The free-energy principle: a unified brain theory?
DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)

Formalización de minimización de sorpresa y ajuste predictivo cerebral.

</details>

<details>
<summary>📘 Thomas Schreiber — Transfer Entropy</summary>

Schreiber, T. (2000). Measuring information transfer.
DOI: [https://doi.org/10.1103/PhysRevLett.85.461](https://doi.org/10.1103/PhysRevLett.85.461)

Introducción de entropía de transferencia para sistemas dinámicos.

</details>

<details>
<summary>📘 Dieter Plenz — Neuronal Avalanches</summary>

Beggs & Plenz (2003). Neuronal avalanches in neocortical circuits.
DOI: [https://doi.org/10.1523/JNEUROSCI.23-35-11167.2003](https://doi.org/10.1523/JNEUROSCI.23-35-11167.2003)

Evidencia de criticidad neuronal.

</details>

---

# 📌 Resumen Ejecutivo

* La coherencia predictiva se define como reducción estructurada de entropía condicional.
* El modelo debe ser generativo y adaptativo.
* La tasa de aprendizaje depende dinámicamente de la caída de coherencia.
* El embedding debe mantenerse en régimen crítico.
* Se incorpora regularización tipo EWC para evitar deriva catastrófica.
* La validación requiere análisis espectral, informacional y geométrico.

---
