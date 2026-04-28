# 🧠 CPEA — Coherencia Predictiva EEG–AGI

### Predictive Coherence between Human Neural Dynamics and Adaptive Artificial Intelligence

![Status](https://img.shields.io/badge/status-preprint-blue)
![Research](https://img.shields.io/badge/type-research-green)
![BCI](https://img.shields.io/badge/domain-brain--computer--interface-purple)
![AI](https://img.shields.io/badge/AI-adaptive-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)

![Python](https://img.shields.io/badge/python-3.11-blue)
![PyTorch](https://img.shields.io/badge/framework-pytorch-red)
![SNN](https://img.shields.io/badge/neural%20model-spiking-yellow)

---

# 📄 Abstract

Las interfaces cerebro–computadora han evolucionado significativamente gracias al desarrollo de técnicas de aprendizaje profundo y neuroingeniería. Sin embargo, la mayoría de los sistemas actuales se fundamentan en paradigmas de decodificación neuronal orientados a clasificar estados cognitivos discretos.

Este trabajo introduce **CPEA (Coherencia Predictiva EEG–AGI)**, una arquitectura diseñada para investigar el acoplamiento dinámico entre actividad neuronal humana registrada mediante EEG y modelos de inteligencia artificial adaptativa.

El sistema se basa en tres principios fundamentales:

* representación latente de señales EEG
* modelado predictivo de dinámica neuronal
* adaptación continua guiada por la **Teoría del Aprendizaje por Excepción (TAE)**

Dentro de este marco, la interacción humano-máquina se interpreta como un sistema dinámico acoplado en el que el modelo artificial anticipa la evolución de estados neuronales mientras el sujeto responde a los estímulos generados por el sistema.

El objetivo del proyecto es explorar la viabilidad de **sistemas cognitivos híbridos humano-IA** caracterizados por sincronización dinámica y aprendizaje adaptativo.

---

# 🔑 Keywords

EEG
Brain-Computer Interface
Artificial General Intelligence
Predictive Coding
Continual Learning
Human-AI Coupling
Neural Synchronization
TAE — Teoría del Aprendizaje por Excepción

---

# 📚 Table of Contents

* [Overview](#overview)
* [Conceptual Framework](#conceptual-framework)
* [System Architecture](#system-architecture)
* [Predictive Coherence](#predictive-coherence)
* [Experimental Programs](#experimental-programs)
* [Repository Structure](#repository-structure)
* [Reproducible Notebooks](#reproducible-notebooks)
* [Summary](#summary)
* [References](#references)

---

# Overview

CPEA propone una arquitectura experimental que investiga el **acoplamiento dinámico entre actividad neuronal humana y modelos de inteligencia artificial adaptativa**.

A diferencia de las BCI tradicionales, el sistema no se limita a decodificar señales neuronales. En cambio, establece un **bucle cognitivo cerrado** donde:

```
EEG → Encoder → Latent Representation → Predictive Model → Feedback → EEG
```

Este enfoque permite estudiar la posibilidad de **coherencia dinámica sostenida entre cerebro humano y sistema artificial**.

> [!NOTE]
> En CPEA, el cerebro humano y el modelo artificial se interpretan como **dos sistemas dinámicos acoplados**.

---

# Conceptual Framework

## Neural Synchronization

Las oscilaciones cerebrales reflejan la coordinación entre poblaciones neuronales distribuidas. Esta sincronización puede cuantificarse mediante la **coherencia espectral**:

[
C(f) = \frac{|S_{xy}(f)|^2}{S_{xx}(f)S_{yy}(f)}
]

donde:

* (S_{xy}(f)) es la densidad espectral cruzada
* (S_{xx}(f)), (S_{yy}(f)) son espectros individuales

---

## Predictive Coding

La neurociencia contemporánea describe el cerebro como un sistema que **minimiza continuamente el error entre predicción y percepción**.

CPEA extiende este principio a la interacción humano-IA.

---

## TAE — Teoría del Aprendizaje por Excepción

<details>
<summary>Expandir explicación</summary>

La **TAE** plantea que los sistemas cognitivos aprenden principalmente cuando eventos inesperados fuerzan reorganizaciones estructurales.

En CPEA, estos eventos se detectan cuando el error predictivo supera un umbral crítico:

[
\epsilon_t > \epsilon_c
]

</details>

---

# System Architecture

La arquitectura CPEA está compuesta por cuatro módulos principales.

---

## 1️⃣ EEG Acquisition

Registro multicanal de actividad neuronal mediante sistemas EEG.

Ejemplos:

* OpenBCI
* Muse S
* g.tec

---

## 2️⃣ Neural Encoder

Transforma la señal EEG en representaciones latentes.

[
z_t = f_\theta(E_t)
]

Este proceso captura correlaciones espaciales y temporales entre canales.

---

## 3️⃣ Predictive Model

Modelo que anticipa la evolución de estados neuronales.

[
\hat{z}*{t+1} = g*\phi(z_t)
]

---

## 4️⃣ Feedback Loop

El sistema genera estímulos cognitivos que influyen en la actividad neuronal del sujeto.

Se establece así un **bucle de co-adaptación humano-IA**.

---

# Predictive Coherence

La hipótesis central del proyecto establece que un modelo artificial puede alcanzar **coherencia dinámica con el cerebro humano**.

Se consideran tres métricas principales:

| Métrica              | Descripción                             |
| -------------------- | --------------------------------------- |
| Error predictivo     | Diferencia entre estado real y predicho |
| Coherencia espectral | Sincronización entre señales            |
| Estabilidad temporal | Persistencia de la sincronización       |

---

# Experimental Programs

## Program 1 — Spectral Coherence

Objetivo:

evaluar sincronización entre EEG y representación latente.

Indicador:

```
Coherencia media > 0.7
```

---

## Program 2 — Neural Prediction

Evaluar capacidad predictiva del modelo.

Indicador:

```
R² > 0.6
```

para predicciones a corto plazo.

---

## Program 3 — Human-AI Co-adaptation

Sesiones de interacción prolongada.

Indicador:

disminución progresiva del error predictivo.

---

## Program 4 — Cross-Subject Analysis

Identificar invariantes cognitivos entre participantes.

Indicador:

clustering consistente en el espacio latente.

---

# Repository Structure

```
CPEA/
│
├── README.md
├── paper
│   └── CPEA_preprint.md
│
├── notebooks
│   ├── eeg_encoder.ipynb
│   ├── predictive_model.ipynb
│   └── coherence_analysis.ipynb
│
├── models
│   ├── encoder
│   └── predictive
│
├── datasets
│
└── experiments
```

---

# Reproducible Notebooks

| Notebook           | Descripción                       |
| ------------------ | --------------------------------- |
| EEG Encoder        | entrenamiento de encoder neuronal |
| Predictive Model   | predicción de dinámica EEG        |
| Coherence Analysis | cálculo de coherencia espectral   |

📎 Ejemplo:

```
notebooks/eeg_encoder.ipynb
```

---

# Summary

• CPEA propone una arquitectura para el acoplamiento dinámico entre EEG humano y sistemas de inteligencia artificial.

• El sistema utiliza representaciones latentes para modelar dinámicas neuronales complejas.

• La coherencia predictiva se define como la capacidad del modelo artificial para anticipar la evolución de la actividad neuronal.

• El aprendizaje se interpreta mediante la Teoría del Aprendizaje por Excepción.

• El sistema funciona como un bucle cognitivo cerrado donde humano e IA se adaptan mutuamente.

• Programas experimentales permiten evaluar coherencia neuronal sostenida.

---

# References

<details>
<summary>Friston 2010 — Free Energy Principle</summary>

DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)

Describe el cerebro como sistema predictivo que minimiza error de predicción.

</details>

---

<details>
<summary>Buzsáki 2006 — Rhythms of the Brain</summary>

DOI: [https://doi.org/10.1093/acprof:oso/9780195301069.001.0001](https://doi.org/10.1093/acprof:oso/9780195301069.001.0001)

Estudio sobre oscilaciones neuronales y coordinación de redes cerebrales.

</details>

---

<details>
<summary>Varela et al. 2001 — Brainweb</summary>

DOI: [https://doi.org/10.1038/35067550](https://doi.org/10.1038/35067550)

Investigación sobre sincronización neuronal en procesos cognitivos.

</details>

---

<details>
<summary>Singer 1999 — Neuronal Synchrony</summary>

DOI: [https://doi.org/10.1016/S0896-6273(00)80789-3](https://doi.org/10.1016/S0896-6273%2800%2980789-3)

La sincronización neuronal como mecanismo de integración cerebral.

</details>

---

# Citation

```
CPEA — Predictive Coherence EEG–AGI
Preprint repository
```

---

# License

MIT License

---

## ⚙️ Repositorio experimental

GitHub:

```
https://github.com/papayaykware/CPEA
```

