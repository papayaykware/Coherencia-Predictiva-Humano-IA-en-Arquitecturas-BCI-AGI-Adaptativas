# 🧠 Coherencia Predictiva Multiescala EEG–Cardíaco–Neuroentérica (CPEA-MS)

---

![Status](https://img.shields.io/badge/status-preregistered-blue)
![Stage](https://img.shields.io/badge/stage-phase%201%20infrastructure-orange)
![Validation](https://img.shields.io/badge/validation-permutation%20testing-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Reproducibility](https://img.shields.io/badge/reproducibility-notebooks%20included-success)

---

> ⚡ **Objetivo:** Formalizar y preregistrar un modelo matemático multiescala que cuantifique la coherencia predictiva como variable inferencial estructural en sistemas neurofisiológicos humanos.

---

# 📑 Tabla de Contenidos

* [1. Introducción](#1-introducción)
* [2. Marco Teórico](#2-marco-teórico)
* [3. Hipótesis](#3-hipótesis)
* [4. Diseño Experimental](#4-diseño-experimental)
* [5. Adquisición de Datos](#5-adquisición-de-datos)
* [6. Formalización Matemática](#6-formalización-matemática)
* [7. Modelo Predictivo AGI](#7-modelo-predictivo-agi)
* [8. Plan Estadístico](#8-plan-estadístico)
* [9. Programas de Seguimiento](#9-programas-de-seguimiento)
* [10. Criterios de Confirmación](#10-criterios-de-confirmación)
* [11. Arquitectura Reproducible](#11-arquitectura-reproducible)
* [12. Referencias](#12-referencias)

---

# 1. Introducción

<a name="1-introducción"></a>

El protocolo CPEA-MS formaliza la **Coherencia Predictiva Multiescala** como una variable cuantificable que integra:

* Actividad cortical (EEG)
* Variabilidad cardíaca (HRV)
* Oscilación neuroentérica (EGG)

La hipótesis central sostiene que la coherencia distribuida entre subsistemas fisiológicos no es epifenómeno, sino arquitectura inferencial activa.

---

# 2. Marco Teórico

<a name="2-marco-teórico"></a>

### 🔬 Fundamentos Neurodinámicos

* Sincronización transitoria (Varela)
* Arquitectura rítmica funcional (Buzsáki)
* Principio de energía libre (Friston)
* Complejidad cardíaca fractal (Goldberger)
* Integración vagal cerebro–corazón (Thayer)

> 💡 La coherencia se interpreta como reducción estructural de incertidumbre.

---

# 3. Hipótesis

<a name="3-hipótesis"></a>

### H1 — Incremento anticipatorio

El ICP_MS aumenta significativamente antes de eventos conductuales.

### H2 — Superioridad multiescala

[
ICP_{MS} > ICP_{EEG}
]

### H3 — Dinámica anticipatoria

[
\dot{ICP}(t) > 0
]

≥200 ms antes del evento.

---

# 4. Diseño Experimental

<a name="4-diseño-experimental"></a>

| Parámetro            | Especificación                                 |
| -------------------- | ---------------------------------------------- |
| Participantes        | n = 10–20                                      |
| Sesiones             | 30–50                                          |
| Trials por condición | ≥200                                           |
| Condiciones          | Reposo / Imaginación motora / Tarea predictiva |

---

# 5. Adquisición de Datos

<a name="5-adquisición-de-datos"></a>

## EEG

* 8–16 canales
* 256–512 Hz
* Análisis principal: 8–30 Hz

## Cardíaco

* ECG o PPG
* HRV espectral y no lineal

## Neuroentérico

* Electrogastrografía cutánea
* Banda 0.03–0.07 Hz

---

# 6. Formalización Matemática

<a name="6-formalización-matemática"></a>

## Matriz Multiescala

[
\mathbf{C}^{MS}(t)
]

Incluye coherencias:

* EEG–EEG
* EEG–Cardíaco
* EEG–Entérico
* Cardíaco–Entérico

---

## Índice de Coherencia Predictiva

[
ICP_{MS}(t) = \sum w_{ab}(t) C^{MS}_{ab}(t)
]

donde:

[
w_{ab}(t) = -\frac{\partial \mathcal{L}}{\partial C^{MS}_{ab}(t)}
]

---

> 🧠 **Interpretación:**
> El ICP_MS es un funcional dinámico ponderado por sensibilidad predictiva.

---

# 7. Modelo Predictivo AGI

<a name="7-modelo-predictivo-agi"></a>

* Transformer temporal multicanal
* Entrada: matriz ( C^{MS}(t) )
* Salida: estado futuro ( Y(t+\Delta) )

Loss:

[
\mathcal{L}(t) = |Y - \hat{Y}|^2
]

---

# 8. Plan Estadístico

<a name="8-plan-estadístico"></a>

* Permutation testing (10 000 iteraciones)
* FDR (Benjamini–Hochberg)
* AUC clasificadora
* Bootstrap para efecto anticipatorio

---

# 9. Programas de Seguimiento

<a name="9-programas-de-seguimiento"></a>

## 📈 Seguimiento Longitudinal

* 30 días consecutivos
* Modelo lineal mixto

## 🔄 Seguimiento Causal

* Transfer Entropy
* Granger Causality

## 🧬 Seguimiento Plasticidad

* Entrenamiento cognitivo 14 días
* Variación ICP_MS

---

# 10. Criterios de Confirmación

<a name="10-criterios-de-confirmación"></a>

✔ p < 0.05 (permutación)
✔ Generalización inter-sujeto
✔ Efecto anticipatorio reproducible
✔ Reducción significativa del error predictivo

---

# 11. Arquitectura Reproducible

<a name="11-arquitectura-reproducible"></a>

## 📂 Estructura del Repositorio

```
/data
/notebooks
    preprocessing.ipynb
    coherence_matrix.ipynb
    icp_computation.ipynb
    transformer_training.ipynb
/src
/docs
```

---

## 📓 Notebooks Reproducibles

* [Preprocessing Pipeline](./notebooks/preprocessing.ipynb)
* [Coherence Matrix Construction](./notebooks/coherence_matrix.ipynb)
* [ICP Computation](./notebooks/icp_computation.ipynb)
* [Transformer Training](./notebooks/transformer_training.ipynb)

---

> ⚙️ Compatible con Python 3.11
> Dependencias: MNE, NumPy, SciPy, PyTorch

---

# 12. Referencias

<a name="12-referencias"></a>

<details>
<summary>Friston (2010) – The Free-Energy Principle</summary>

DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)
Define el cerebro como sistema inferencial que minimiza sorpresa.

</details>

<details>
<summary>Buzsáki (2006) – Rhythms of the Brain</summary>

Oxford University Press
Fundamento estructural de oscilaciones neuronales.

</details>

<details>
<summary>Varela et al. (2001) – The Brainweb</summary>

DOI: [https://doi.org/10.1038/35067550](https://doi.org/10.1038/35067550)
Sincronización transitoria y coherencia funcional.

</details>

<details>
<summary>Thayer & Lane (2009) – Heart–Brain Connection</summary>

DOI: [https://doi.org/10.1016/j.neubiorev.2009.02.002](https://doi.org/10.1016/j.neubiorev.2009.02.002)
Modelo neurovisceral de integración vagal.

</details>

<details>
<summary>Goldberger (2002) – Fractal Physiology</summary>

DOI: [https://doi.org/10.1073/pnas.242407499](https://doi.org/10.1073/pnas.242407499)
Dinámica no lineal en fisiología cardíaca.

</details>

---

# 🧭 Index Lateral (Estilo GitBook)

* Overview
* Mathematical Formalization
* Experimental Design
* Statistical Plan
* Reproducibility
* References

---

# 📌 Estado del Proyecto

> 🟢 Fase 1 — Infraestructura y Marco Experimental
> 🟡 En preparación: implementación completa del ICP_MS
> 🔵 Próximo: validación cruzada multiescala

---

# 🧾 Licencia

MIT License

---

# 📎 DOI del Protocolo (Reservado)

Pendiente de registro OSF.

---
