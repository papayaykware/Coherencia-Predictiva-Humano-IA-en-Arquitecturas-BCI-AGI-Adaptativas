<!-- ========================================================= -->
<!--  CPEA — FASE 1 | Infraestructura y Aprendizaje Continuo  -->
<!-- ========================================================= -->

<p align="center">
  <h1 align="center">🧠 Coherencia Predictiva EEG–AGI (CPEA)</h1>
  <h3 align="center">Fase 1 — Infraestructura Experimental y Aprendizaje Continuo</h3>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Experimental-blue" />
  <img src="https://img.shields.io/badge/Stage-Phase%201-informational" />
  <img src="https://img.shields.io/badge/Framework-PyTorch-red" />
  <img src="https://img.shields.io/badge/Domain-NeuroAI-purple" />
  <img src="https://img.shields.io/badge/License-Research-lightgrey" />
  <img src="https://img.shields.io/badge/Build-Passing-brightgreen" />
</p>

---

# 📑 Índice

- [Abstract](#abstract)
- [Palabras clave](#palabras-clave)
- [1. Marco Conceptual](#1-marco-conceptual)
- [2. Fundamentación Neurofísica](#2-fundamentación-neurofísica)
- [3. Problema Técnico](#3-problema-técnico)
- [4. Arquitectura Propuesta](#4-arquitectura-propuesta)
- [5. Formalización Matemática](#5-formalización-matemática)
- [6. Infraestructura Experimental](#6-infraestructura-experimental)
- [7. Geometría del Manifold Latente](#7-geometría-del-manifold-latente)
- [8. Métricas de Coherencia Predictiva](#8-métricas-de-coherencia-predictiva)
- [9. Programas de Seguimiento](#9-programas-de-seguimiento)
- [10. Implementación PyTorch](#10-implementación-pytorch)
- [Conclusiones](#conclusiones)
- [Resumen Ejecutivo](#resumen-ejecutivo)
- [Referencias Comentadas](#referencias-comentadas)

---

---

# Abstract

La Fase 1 del proyecto **Coherencia Predictiva EEG–AGI (CPEA)** establece la infraestructura experimental necesaria para sostener un acoplamiento dinámico entre la actividad electroencefalográfica humana y una arquitectura artificial con plasticidad adaptativa. Se introduce un módulo de aprendizaje continuo implementado en PyTorch que permite la adaptación online de embeddings latentes, preservando estabilidad estructural y evitando olvido catastrófico.

El modelo asume que la señal EEG es intrínsecamente no estacionaria y que la coherencia entre sistemas biológicos y artificiales solo puede mantenerse mediante plasticidad computacional regulada. Se formaliza la coherencia predictiva como convergencia dinámica entre espacios latentes bajo restricciones geométricas y métricas informacionales.

---

# Palabras clave

Coherencia predictiva · EEG · aprendizaje continuo · embeddings dinámicos · plasticidad artificial · Elastic Weight Consolidation · meta-learning · dinámica no lineal · Transfer Entropy · manifold latente

---

# 1. Marco Conceptual

> [!NOTE]
> La coherencia predictiva no se define como correlación lineal, sino como convergencia topológica dinámica entre sistemas.

El sistema nervioso opera en régimen no estacionario. Las redes corticales se reorganizan constantemente. Un modelo artificial estático introduce desacoplamiento progresivo.

La Fase 1 aborda este problema mediante:

- Adaptación incremental.
- Preservación estructural.
- Seguimiento geométrico del embedding.

---

# 2. Fundamentación Neurofísica

La literatura neurocientífica ha mostrado:

- Organización jerárquica oscilatoria.
- Dinámica cercana a criticidad.
- Sincronización multiescala.

La señal EEG refleja superposición de corrientes postsinápticas sincronizadas, lo que implica estructura dinámica en el dominio de campo electromagnético.

---

# 3. Problema Técnico

## 3.1 Deriva de distribución

Cambios debidos a:

- Estado cognitivo.
- Fatiga.
- Adaptación.
- Contexto emocional.

## 3.2 Olvido catastrófico

Actualización sin regularización destruye memoria estructural.

---

# 4. Arquitectura Propuesta

```text
EEG Stream
   ↓
Preprocessing
   ↓
Encoder (Self-Supervised)
   ↓
Latent Embedding
   ↓
Online Adaptation Module
   ↓
Coherence Evaluation
````

## Componentes

* Encoder Transformer/CNN 1D
* Elastic Weight Consolidation
* Replay Buffer
* Meta-adaptación ligera

---

# 5. Formalización Matemática

Sea:

* ( x_t ) señal EEG
* ( z_t = f_\theta(x_t) )

Coherencia:

[
C = \mathbb{E}[\cos(z_t, \hat{z}*{t+1})] + \lambda TE(z_t \rightarrow \hat{z}*{t+1})
]

Regularización EWC:

[
L = L_{pred} + \beta \sum_i F_i (\theta_i - \theta_i^*)^2
]

---

# 6. Infraestructura Experimental

| Componente | Especificación  |
| ---------- | --------------- |
| EEG        | ≥ 32 canales    |
| Muestreo   | ≥ 500 Hz        |
| Latencia   | < 10 ms         |
| GPU        | CUDA-compatible |

---

# 7. Geometría del Manifold Latente

Se evalúan:

* Curvatura local.
* Dimensión intrínseca.
* Persistencia homológica.

> [!TIP]
> El seguimiento topológico permite detectar colapsos latentes antes de degradación predictiva visible.

---

# 8. Métricas de Coherencia Predictiva

* Similaridad coseno dinámica
* Transfer Entropy
* Divergencia Jensen–Shannon
* Distancia Wasserstein

---

# 9. Programas de Seguimiento

## Programa 1 — Deriva Latente

* Ventanas de 5 min.
* Distancia Wasserstein.
* Variación dimensional.

## Programa 2 — Plasticidad Adaptativa

* Cambio cognitivo inducido.
* Medición de convergencia.

## Programa 3 — Robustez al Ruido

* Artefactos controlados.
* Evaluación topológica.

---

# 10. Implementación PyTorch

### Estructura del módulo continuo

```python
class OnlineAdapter:
    def __init__(self, model, fisher_matrix, old_params):
        self.model = model
        self.fisher = fisher_matrix
        self.old_params = old_params

    def ewc_loss(self):
        loss = 0
        for name, param in self.model.named_parameters():
            loss += (self.fisher[name] * (param - self.old_params[name])**2).sum()
        return loss

    def update(self, batch, optimizer, beta):
        optimizer.zero_grad()
        pred_loss = self.model.loss(batch)
        loss = pred_loss + beta * self.ewc_loss()
        loss.backward()
        optimizer.step()
```

---

## 📓 Notebooks Reproducibles

* [`notebooks/phase1_encoder_training.ipynb`](./notebooks/phase1_encoder_training.ipynb)
* [`notebooks/online_adaptation_demo.ipynb`](./notebooks/online_adaptation_demo.ipynb)
* [`notebooks/coherence_metrics_analysis.ipynb`](./notebooks/coherence_metrics_analysis.ipynb)

---

# Conclusiones

La adaptación online no constituye una optimización opcional. Es la condición necesaria para sostener coherencia estructural entre sistemas biológicos y arquitecturas artificiales dinámicas.

El espacio latente debe entenderse como variedad evolutiva, no representación estática.

---

# Resumen Ejecutivo

* El EEG es dinámico y no estacionario.
* La coherencia predictiva requiere plasticidad artificial.
* Elastic Weight Consolidation equilibra estabilidad y adaptación.
* El seguimiento geométrico del manifold es esencial.
* La adaptación online preserva alineamiento topológico.
* La Fase 1 establece infraestructura experimental escalable.

---

# Referencias Comentadas

<details>
<summary><strong>Friston, K. (2010) — The Free-Energy Principle</strong></summary>

DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)
Marco matemático para dinámica cerebral basada en minimización de energía libre.

</details>

<details>
<summary><strong>Buzsáki, G. (2006) — Rhythms of the Brain</strong></summary>

Oxford University Press
Organización jerárquica oscilatoria del cerebro.

</details>

<details>
<summary><strong>Kirkpatrick et al. (2017) — Overcoming catastrophic forgetting</strong></summary>

DOI: [https://doi.org/10.1073/pnas.1611835114](https://doi.org/10.1073/pnas.1611835114)
Introduce Elastic Weight Consolidation.

</details>

<details>
<summary><strong>Schreiber, T. (2000) — Measuring Information Transfer</strong></summary>

DOI: [https://doi.org/10.1103/PhysRevLett.85.461](https://doi.org/10.1103/PhysRevLett.85.461)
Formalización de Transfer Entropy.

</details>

---

<p align="center">
  <strong>CPEA — Phase 1 Infrastructure Complete</strong><br>
  NeuroAI · Continuous Learning · Structural Coherence
</p>
```
