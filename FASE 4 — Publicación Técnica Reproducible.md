# 🧠⚡ Coherencia Predictiva EEG–AGI (CPEA)
### FASE 4 — Publicación Técnica Reproducible

![Status](https://img.shields.io/badge/status-active-success)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-blue)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red)
![License](https://img.shields.io/badge/license-MIT-green)
![Docker](https://img.shields.io/badge/docker-ready-blue)
![Reproducibility](https://img.shields.io/badge/reproducible-yes-success)

---

## 📌 Abstract

La Coherencia Predictiva EEG–AGI (CPEA) formaliza una arquitectura neurocomputacional híbrida diseñada para evaluar convergencia estructural entre dinámica electroencefalográfica humana y un sistema artificial con aprendizaje continuo por excepción (TAE).  

El modelo integra procesamiento espectro-temporal, embeddings dinámicos, red híbrida ANN + SNN y regularización elástica (EWC). La coherencia no se define exclusivamente como correlación, sino como convergencia topológica cuantificable mediante análisis espectral, reconstrucción de atractores y métricas entrópicas multiescala.  

Este repositorio contiene una implementación completamente reproducible, incluyendo dataset anonimizado, notebook ejecutable, Dockerfile y CI/CD.

---

# 📚 Tabla de Contenidos

- [1. Arquitectura del Sistema](#1-arquitectura-del-sistema)
- [2. Fundamentos Matemáticos](#2-fundamentos-matemáticos)
- [3. Aprendizaje por Excepción (TAE)](#3-aprendizaje-por-excepción-tae)
- [4. Integración ANN + SNN](#4-integración-ann--snn)
- [5. Métricas de Coherencia](#5-métricas-de-coherencia)
- [6. Programas de Seguimiento Experimental](#6-programas-de-seguimiento-experimental)
- [7. Estructura del Repositorio](#7-estructura-del-repositorio)
- [8. Instalación Rápida](#8-instalación-rápida)
- [9. CI/CD](#9-cicd)
- [10. Referencias Científicas](#10-referencias-científicas)

---

# 1️⃣ Arquitectura del Sistema

## 🔬 Pipeline General

```

EEG → Preprocesamiento → STFT/Wavelet → Embedding
↓
ANN (estructura global)
↓
SNN (dinámica temporal)
↓
Predicción t+1 → Métrica de coherencia → TAE update

```

> [!NOTE]
> La coherencia predictiva se evalúa en doble nivel: escalar (error normalizado) y estructural (autovalores de conectividad funcional).

---

# 2️⃣ Fundamentos Matemáticos

## Coherencia Escalar

\[
\mathcal{C} = 1 - \frac{\|E_{t+1} - \hat{E}_{t+1}\|_2}{\|E_{t+1}\|_2}
\]

## Coherencia Estructural

\[
\mathcal{C}_s = \text{corr}(\lambda_i^{EEG}, \lambda_i^{AGI})
\]

donde \( \lambda_i \) representan autovalores del operador de conectividad funcional.

---

# 3️⃣ Aprendizaje por Excepción (TAE)

Actualización solo ante ruptura estructural:

\[
\theta_{t+1} = \theta_t - \eta \, \mathcal{E}_t \nabla_\theta L_t
\]

\[
\tau_s = \mu_L + k \sigma_L
\]

> [!IMPORTANT]
> El sistema no optimiza continuamente. Solo actualiza cuando la desviación excede un umbral adaptativo.

---

# 4️⃣ Integración ANN + SNN

## ANN

Capas densas + GELU + BatchNorm  
Modela estructura global del embedding.

## SNN (LIF)

\[
\tau_m \frac{dV}{dt} = -V + R I(t)
\]

Captura sincronización temporal y eventos transitorios.

---

# 5️⃣ Métricas de Coherencia

### ✔ Coherencia espectral cruzada
### ✔ Dimensión fractal (D2)
### ✔ Entropía multiescala
### ✔ Estabilidad longitudinal

> [!TIP]
> Se recomienda ejecutar análisis longitudinal ≥ 4 semanas para evaluar convergencia estructural.

---

# 6️⃣ Programas de Seguimiento Experimental

## Programa 1 — Estabilidad intra-sujeto

- Medición semanal
- Entropía espectral
- Coherencia estructural

## Programa 2 — Transiciones cognitivas

- Basal
- Tarea ejecutiva
- Meditación
- Estímulo auditivo

## Programa 3 — Plasticidad AGI

Evaluación de estabilidad bajo EWC:

\[
L_{total} = L_{task} + \lambda \sum_i F_i (\theta_i - \theta_i^*)^2
\]

---

# 7️⃣ Estructura del Repositorio

```

CPEA/
│
├── README.md
├── docker/
│   └── Dockerfile
├── notebooks/
│   └── cpea_reproducible.ipynb
├── data/
│   └── sample_dataset_anonymized/
├── src/
│   ├── models/
│   ├── metrics/
│   ├── tae/
│   └── utils/
├── tests/
│   ├── test_forward.py
│   ├── test_coherence.py
│   └── test_dataset.py
└── .github/workflows/
└── ci.yml

````

---

# 8️⃣ Instalación Rápida

## Opción Docker

```bash
docker build -t cpea .
docker run -p 8888:8888 cpea
````

## Opción Manual

```bash
pip install -r requirements.txt
jupyter notebook notebooks/cpea_reproducible.ipynb
```

---

# 9️⃣ CI/CD

GitHub Actions ejecuta automáticamente:

* Instalación de dependencias
* Tests unitarios
* Validación de integridad

Archivo: `.github/workflows/ci.yml`

---

# 🔎 Notebook Reproducible

📓 [Abrir Notebook Reproducible](./notebooks/cpea_reproducible.ipynb)

Incluye:

* Carga dataset
* Entrenamiento
* Visualización de coherencia
* Análisis espectral

---

# 🔬 Dataset Sample

Dataset EEG anonimizado derivado de dominio público.
Normalizado y segmentado en ventanas espectrales.

> [!CAUTION]
> Solo para investigación no clínica.

---

# 1️⃣0️⃣ Referencias Científicas

<details>
<summary><strong>Freeman, W.J. (2000). Neurodynamics</strong></summary>

Fundamenta dinámica caótica cortical y atractores.

</details>

<details>
<summary><strong>Buzsáki, G. (2006). Rhythms of the Brain</strong></summary>

Análisis profundo de oscilaciones neuronales.

</details>

<details>
<summary><strong>Friston, K. (2010). The Free-Energy Principle</strong></summary>

DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)
Modelo predictivo del cerebro.

</details>

<details>
<summary><strong>Kirkpatrick et al. (2017). Overcoming catastrophic forgetting</strong></summary>

DOI: [https://doi.org/10.1073/pnas.1611835114](https://doi.org/10.1073/pnas.1611835114)
Elastic Weight Consolidation.

</details>

<details>
<summary><strong>Kelso, J.A.S. (1995). Dynamic Patterns</strong></summary>

Transiciones de fase en sistemas coordinados.

</details>

---

# 🧭 Conclusiones

* Arquitectura híbrida reproducible.
* Implementación formal de TAE.
* Evaluación de coherencia estructural multiescala.
* Aprendizaje continuo con estabilidad paramétrica.
* Pipeline completamente replicable.

---

# 📜 Licencia

MIT License

---

# 📩 Contacto Técnico

Repositorio: [https://github.com/papayaykware/METFI](https://github.com/papayaykware/METFI)

---
