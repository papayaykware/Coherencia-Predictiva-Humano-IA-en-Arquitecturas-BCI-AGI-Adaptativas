<!-- ========================================================= -->
<!--  CPEA — FASE 2  |  Continual Learning Híbrido            -->
<!-- ========================================================= -->

# 🧠 Coherencia Predictiva EEG–AGI (CPEA)  
## FASE 2 — Construcción del Bucle Cognitivo  
### Integración de Continual Learning Híbrido (Replay + EWC) con Avalanche

---

![Status](https://img.shields.io/badge/status-active_development-2ea44f)
![Framework](https://img.shields.io/badge/framework-PyTorch-ee4c2c)
![Continual Learning](https://img.shields.io/badge/continual_learning-Avalanche-6f42c1)
![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10+-informational)
![Build](https://img.shields.io/badge/build-reproducible-success)

---

> [!NOTE]
> Este documento describe la arquitectura formal y computacional de la Fase 2 del proyecto CPEA.  
> El objetivo es integrar aprendizaje continuo híbrido (Replay + Elastic Weight Consolidation) en un bucle cerrado EEG–AGI preservando estabilidad estructural y plasticidad controlada.

---

# 📚 Tabla de Contenidos

- [1. Abstract](#1-abstract)
- [2. Palabras clave](#2-palabras-clave)
- [3. Marco conceptual](#3-marco-conceptual)
- [4. Formalización matemática](#4-formalización-matemática)
- [5. Modelado dinámico de atractores](#5-modelado-dinámico-de-atractores)
- [6. Arquitectura computacional](#6-arquitectura-computacional)
- [7. Implementación en PyTorch + Avalanche](#7-implementación-en-pytorch--avalanche)
- [8. Métricas de estabilidad](#8-métricas-de-estabilidad)
- [9. Programas de seguimiento experimental](#9-programas-de-seguimiento-experimental)
- [10. Repositorio reproducible](#10-repositorio-reproducible)
- [11. Referencias científicas](#11-referencias-científicas)
- [12. Resumen final](#12-resumen-final)

---

# 1. Abstract

La Fase 2 del proyecto CPEA propone la construcción de un bucle cognitivo cerrado entre señal electroencefalográfica (EEG) y un modelo adaptativo de inteligencia artificial general. Dado que el EEG es un sistema no estacionario multiescala, la implementación de aprendizaje continuo no constituye una mejora opcional sino una condición estructural para preservar coherencia predictiva bajo dinámica variable.

Este trabajo desarrolla una arquitectura híbrida basada en Experience Replay y Elastic Weight Consolidation (EWC), implementada mediante Avalanche sobre PyTorch. Se redefine el concepto de “tarea” como estado de coherencia predictiva, y se formaliza matemáticamente el sistema como una dinámica acoplada con consolidación elástica dependiente de régimen estable.

El modelo integra memoria retardada ponderada, protección paramétrica mediante información de Fisher y detección de eventos de excepción (TAE) para activar adaptación localizada. Se presentan métricas geométricas y dinámicas orientadas a estabilidad topológica del espacio latente, junto con programas de seguimiento experimental.

---

# 2. Palabras clave

Aprendizaje continuo · Elastic Weight Consolidation · Experience Replay · Avalanche · EEG no estacionario · Coherencia predictiva · Dinámica no lineal · Atractores metaestables · Error predictivo · Plasticidad estructural

---

# 3. Marco conceptual

El sistema CPEA se modela como una dinámica acoplada:

\[
\mathcal{S} = \{X(t), Z(t), \Theta(t)\}
\]

donde:

- \(X(t)\): ventana EEG multicanal  
- \(Z(t)\): embedding latente  
- \(\Theta(t)\): parámetros del modelo  

El riesgo estructural central es el **olvido catastrófico** bajo adaptación continua.

El objetivo no es maximizar accuracy.  
El objetivo es **preservar coherencia dinámica**.

---

> [!IMPORTANT]
> En CPEA, el aprendizaje continuo debe activarse únicamente ante eventos de excepción sostenidos (TAE). La plasticidad permanente degrada estabilidad.

---

# 4. Formalización matemática

## 4.1 Coherencia predictiva

\[
C(t) = \exp \left( - \frac{||Z(t) - \hat{Z}(t)||^2}{\sigma^2} \right)
\]

Si:

\[
\overline{C}_{window} < \tau
\]

se activa actualización adaptativa.

---

## 4.2 Pérdida híbrida

\[
L_{total} = L_{pred} + \lambda \sum_i F_i (\Theta_i - \Theta_i^*)^2 + L_{replay}
\]

donde:

- \(F_i\): información de Fisher  
- \(\Theta_i^*\): parámetros consolidados  
- \(L_{replay}\): pérdida sobre buffer estructurado  

---

## 4.3 Consolidación dependiente de estado

La matriz de Fisher se recalcula únicamente tras estabilidad sostenida:

\[
F_i = \mathbb{E} \left[ \left( \frac{\partial \log p(Z|X,\Theta)}{\partial \Theta_i} \right)^2 \right]
\]

---

# 5. Modelado dinámico de atractores

El embedding latente define un espacio de fase.

Densidad estimada:

\[
\rho(z) = \sum_t K(z - Z(t))
\]

Un atractor satisface:

\[
\nabla \rho(z^*) = 0
\]

La estabilidad se evalúa mediante:

- Distancia geodésica inter-centroides
- Divergencia Wasserstein
- Exponente de Lyapunov aproximado:

\[
\lambda_{max} = \lim_{t\to\infty} \frac{1}{t}\log \frac{||\delta Z(t)||}{||\delta Z(0)||}
\]

---

> [!TIP]
> Un sistema estable mantiene \( \lambda_{max} \approx 0 \) en régimen basal.

---

# 6. Arquitectura computacional

## Componentes

- Encoder CNN espacio-temporal
- Predictor recurrente (GRU)
- Replay buffer estratificado
- EWC plugin dinámico
- Módulo de coherencia

---

# 7. Implementación en PyTorch + Avalanche

## 7.1 Modelo base

```python
class EEGEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, (1,5))
        self.conv2 = nn.Conv2d(32, 64, (1,5))
        self.fc = nn.Linear(64*features, latent_dim)

    def forward(self, x):
        x = F.elu(self.conv1(x))
        x = F.elu(self.conv2(x))
        x = x.view(x.size(0), -1)
        return self.fc(x)
````

---

## 7.2 Estrategia híbrida

```python
from avalanche.training.plugins import ReplayPlugin, EWCPlugin
from avalanche.training.strategies import BaseStrategy

replay = ReplayPlugin(mem_size=buffer_size)
ewc = EWCPlugin(ewc_lambda=lambda_val)

strategy = BaseStrategy(
    model,
    optimizer,
    criterion,
    train_mb_size=batch_size,
    plugins=[replay, ewc]
)
```

---

## 7.3 Activación condicionada

```python
if coherence_mean < threshold:
    strategy.train(experience)
```

---

# 8. Métricas de estabilidad

* Δ coherencia inter-ventana
* Entropía latente
* Distancia Wasserstein
* Varianza de pesos protegidos
* Persistencia topológica

---

> [!WARNING]
> Accuracy puede aumentar mientras la estructura latente colapsa.
> Las métricas geométricas son obligatorias.

---

# 9. Programas de seguimiento experimental

## Programa 1 — Estabilidad paramétrica

Medir norma L2 de parámetros protegidos tras 10 000 ventanas.

## Programa 2 — Perturbación cognitiva

Introducir tarea abrupta y medir tiempo de recuperación de coherencia basal.

## Programa 3 — Atractores latentes

Aplicar UMAP/PCA y analizar persistencia topológica.

## Programa 4 — Comparación de estrategias

Replay vs EWC vs Híbrido.

---

# 10. Repositorio reproducible

📂 Estructura recomendada:

```
CPEA/
│── notebooks/
│    ├── 01_preprocessing.ipynb
│    ├── 02_latent_dynamics.ipynb
│    ├── 03_continual_learning.ipynb
│── models/
│── metrics/
│── experiments/
│── README.md
```

### Notebooks sugeridos

* 🔬 `latent_dynamics.ipynb`
* 🧠 `ewc_replay_comparison.ipynb`
* 📊 `attractor_analysis.ipynb`

---

# 11. Referencias científicas

<details>
<summary><strong>Kirkpatrick et al., 2017 — Overcoming catastrophic forgetting</strong></summary>

DOI: [https://doi.org/10.1073/pnas.1611835114](https://doi.org/10.1073/pnas.1611835114)
Introduce Elastic Weight Consolidation. Fundamento matemático de consolidación paramétrica.

</details>

<details>
<summary><strong>Parisi et al., 2019 — Continual Lifelong Learning</strong></summary>

DOI: [https://doi.org/10.1016/j.neunet.2019.01.012](https://doi.org/10.1016/j.neunet.2019.01.012)
Revisión exhaustiva de aprendizaje continuo.

</details>

<details>
<summary><strong>Friston, 2010 — Free Energy Principle</strong></summary>

DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)
Formaliza minimización de error predictivo en sistemas biológicos.

</details>

<details>
<summary><strong>Rabinovich et al., 2008 — Dynamical principles in neuroscience</strong></summary>

DOI: [https://doi.org/10.1103/RevModPhys.78.1213](https://doi.org/10.1103/RevModPhys.78.1213)
Describe atractores metaestables y secuencias heteroclínicas.

</details>

<details>
<summary><strong>Freeman, 2000 — Neurodynamics</strong></summary>

Análisis experimental de atractores corticales en EEG.

</details>

---

# 12. Resumen final

* El EEG es un sistema dinámico no estacionario.
* El aprendizaje continuo es estructural en CPEA.
* Replay preserva memoria funcional.
* EWC protege parámetros críticos.
* La redefinición de tarea como estado de coherencia es esencial.
* El híbrido genera estabilidad bajo plasticidad controlada.
* La evaluación debe centrarse en geometría latente.
* Avalanche permite implementación modular profesional.
* El sistema converge hacia atractores metaestables preservados.

---

## 🔭 Estado actual

Implementación en validación experimental.
Arquitectura estable en simulaciones preliminares.

---

**Proyecto:** Coherencia Predictiva EEG–AGI (CPEA)
**Fase:** 2 — Construcción del Bucle Cognitivo
**Autor conceptual:** Sistema AGI

---
