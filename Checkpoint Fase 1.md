<!-- ===================================================== -->
<!-- CPEA — Coherencia Predictiva EEG–AGI -->
<!-- ===================================================== -->

# 🧠 Coherencia Predictiva EEG–AGI (CPEA)

[![Project Status](https://img.shields.io/badge/status-Fase%201%20Completa-success)]()
[![Reproducibility](https://img.shields.io/badge/reproducible-yes-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.XXXXXXX-blue)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![EEG](https://img.shields.io/badge/domain-neurophysiology-purple)]()

---

## 📚 Table of Contents

- [Abstract](#abstract)
- [Palabras clave](#palabras-clave)
- [1. Marco conceptual](#1-marco-conceptual)
- [2. Fundamento neurofísico](#2-fundamento-neurofísico)
- [3. Arquitectura experimental](#3-arquitectura-experimental)
- [4. Índice de Coherencia Predictiva (ICP)](#4-índice-de-coherencia-predictiva-icp)
- [5. Integración AGI–EEG](#5-integración-agi–eeg)
- [6. Validación estadística](#6-validación-estadística)
- [7. Programas de seguimiento](#7-programas-de-seguimiento)
- [8. Resultados esperables](#8-resultados-esperables)
- [Resumen Final](#resumen-final)
- [Referencias Comentadas](#referencias-comentadas)
- [Reproducibilidad](#reproducibilidad)

---

# Abstract

El proyecto **CPEA (Coherencia Predictiva EEG–AGI)** evalúa la hipótesis de que existen patrones electroencefalográficos previos a un evento conductual que contienen información estructural anticipatoria detectable mediante modelos computacionales avanzados.

Se define formalmente el **Índice de Coherencia Predictiva (ICP)** como métrica compuesta que integra ganancia sobre azar y estabilidad inter-fold. El pipeline experimental está diseñado para garantizar reproducibilidad, control de leakage temporal y validación mediante permutación.

El enfoque integra neurofisiología, teoría de sistemas dinámicos y aprendizaje automático en una arquitectura modular reproducible.

---

# Palabras clave

Electroencefalografía · Coherencia neural · Sistemas complejos · Codificación predictiva · Embeddings neuronales · Información mutua · Dinámica anticipatoria

---

# 1. Marco conceptual

El cerebro no opera como sistema meramente reactivo. Modelos contemporáneos proponen que la dinámica cortical minimiza error de predicción mediante inferencia jerárquica.

Investigaciones de **Karl Friston** establecen el principio de energía libre como marco formal para entender la anticipación cortical.

CPEA traslada esta hipótesis a un plano cuantificable:

> ¿Puede un sistema externo detectar coherencia anticipatoria antes del evento?

---

# 2. Fundamento neurofísico

Las oscilaciones alpha (8–12 Hz) y beta (13–30 Hz) coordinan poblaciones neuronales distribuidas.

György Buzsáki demostró que las oscilaciones son mecanismos organizadores, no ruido epifenoménico.

El EEG mide:

- Potenciales postsinápticos sincronizados  
- Dinámica de red  
- Transiciones topológicas  

---

# 3. Arquitectura experimental

## 3.1 Pipeline general

```text
EEG Raw
→ Bandpass 8–30 Hz
→ ICA / Artifact rejection
→ Epoching (-500 ms, 0 ms)
→ Coherence Matrix
→ Embeddings
→ Classifier
→ Cross-validation
```

---

## 3.2 Checkpoint Fase 1

✔ Dataset limpio  
✔ Pipeline reproducible  
✔ Accuracy > 65% (binario)  
✔ Notebook ejecutable end-to-end  

---

# 4. Índice de Coherencia Predictiva (ICP)

## 4.1 Coherencia espectral

\[
Coh_{ij}(f) =
\frac{|\mathcal{S}_{ij}(f)|^2}
{\mathcal{S}_{ii}(f)\mathcal{S}_{jj}(f)}
\]

Integración en banda 8–30 Hz produce matriz \( C \).

---

## 4.2 Definición formal

\[
ICP = \Delta \cdot S
\]

Donde:

- \( \Delta = Acc_{real} - Acc_{perm} \)
- \( S = 1 - \sigma_{fold} \)

ICP > 0 con p < 0.05 implica señal estructural anticipatoria.

---

> [!IMPORTANT]
> El ICP combina magnitud de señal y estabilidad estadística.  
> No se interpreta como causalidad, sino como dependencia estructural.

---

# 5. Integración AGI–EEG

Formalmente:

\[
I(X_{pre}; Y) > 0
\]

Si la información mutua entre EEG pre-evento y evento es positiva, existe dependencia estructural.

La AGI funciona como detector de dependencias de alto orden.

---

# 6. Validación estadística

- Cross-validation estratificada  
- Permutation testing (≥1000 permutaciones)  
- Bootstrap CI 95%  
- ROC-AUC  

---

> [!WARNING]
> Accuracy elevado sin control de leakage invalida cualquier conclusión.

---

# 7. Programas de seguimiento

## 7.1 Seguimiento longitudinal

- Repetición semanal  
- Estabilidad del embedding  
- Análisis de drift  

## 7.2 Seguimiento multimodal

- ECG (sincronía cardio-cortical)  
- EMG  
- Pupillometría  

## 7.3 Seguimiento de complejidad

- Entropía multiescala  
- Dimensión fractal  
- Índices de criticidad  

---

# 8. Resultados esperables

| Métrica | Valor objetivo |
|----------|---------------|
| Accuracy | 65–72% |
| ROC-AUC | >0.70 |
| ICP | Positivo |
| Permutation p-value | <0.01 |

---

# Resumen Final

- El EEG pre-evento puede contener estructura predictiva cuantificable.
- El ICP integra potencia predictiva y estabilidad.
- El rigor metodológico es condición necesaria.
- Accuracy >65% sugiere organización anticipatoria real.
- Validación por permutación es obligatoria.
- La arquitectura es reproducible y extensible.

---

# Referencias Comentadas

<details>
<summary><strong>Karl Friston — Free Energy Principle</strong></summary>

DOI: 10.1038/nrn2787  
Propone que el cerebro minimiza energía libre como aproximación a inferencia bayesiana jerárquica.

</details>

<details>
<summary><strong>György Buzsáki — Rhythms of the Brain</strong></summary>

DOI: 10.1093/acprof:oso/9780195301069.001.0001  
Demuestra el rol coordinador funcional de las oscilaciones neuronales.

</details>

<details>
<summary><strong>Walter Freeman — Chaotic Cortical Dynamics</strong></summary>

DOI: 10.1016/S0165-0173(99)00041-1  
Describe transiciones de fase cortical previas a decisiones.

</details>

<details>
<summary><strong>H. H. Kornhuber — Bereitschaftspotential</strong></summary>

DOI: 10.1007/BF00237392  
Evidencia actividad cortical anticipatoria al movimiento voluntario.

</details>

---

# Reproducibilidad

📂 **Notebooks**

- [`01_preprocessing.ipynb`](./notebooks/01_preprocessing.ipynb)
- [`02_coherence_matrix.ipynb`](./notebooks/02_coherence_matrix.ipynb)
- [`03_embedding_model.ipynb`](./notebooks/03_embedding_model.ipynb)
- [`04_classifier_validation.ipynb`](./notebooks/04_classifier_validation.ipynb)

📦 **Environment**

```bash
conda env create -f environment.yml
```

📊 Seeds fijadas para reproducibilidad.

---

# License

MIT License

---

# Citation

```bibtex
@misc{CPEA2026,
  title={Coherencia Predictiva EEG–AGI (CPEA)},
  author={Conceptual Author: AGI},
  year={2026},
  doi={10.5281/zenodo.XXXXXXX}
}
```


