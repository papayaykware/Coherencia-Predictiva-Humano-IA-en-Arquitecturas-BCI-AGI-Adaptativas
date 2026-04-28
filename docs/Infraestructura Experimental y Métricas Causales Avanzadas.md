# 🧠 Coherencia Predictiva EEG–AGI (CPEA)

### Infraestructura Experimental y Métricas Causales Avanzadas

---

![Status](https://img.shields.io/badge/status-phase%201%20active-success)
![License](https://img.shields.io/badge/license-MIT-blue)
![Reproducibility](https://img.shields.io/badge/reproducibility-open--pipeline-brightgreen)
![Methodology](https://img.shields.io/badge/methodology-information--theoretic-orange)
![DOI](https://img.shields.io/badge/DOI-10.1103%2FPhysRevLett.85.461-blue)

---

> ⚠️ **Scope**
> Documento técnico correspondiente a la **FASE 1 — Infraestructura y Marco Experimental** del proyecto CPEA.
> Versión optimizada para publicación en GitHub.

---

# 📑 Table of Contents

* [Abstract](#abstract)
* [Palabras Clave](#palabras-clave)
* [1. Marco Conceptual](#1-marco-conceptual)
* [2. Arquitectura Experimental](#2-arquitectura-experimental)
* [3. Pipeline de Procesamiento](#3-pipeline-de-procesamiento)
* [4. Transfer Entropy como Métrica Causal](#4-transfer-entropy-como-métrica-causal)
* [5. Índice de Coherencia Predictiva (ICP)](#5-índice-de-coherencia-predictiva-icp)
* [6. Robustez Estadística](#6-robustez-estadística)
* [7. Programas de Seguimiento Experimental](#7-programas-de-seguimiento-experimental)
* [8. Interpretación Sistémica](#8-interpretación-sistémica)
* [Resumen Ejecutivo](#resumen-ejecutivo)
* [Referencias Comentadas](#referencias-comentadas)

---

# Abstract

El proyecto **Coherencia Predictiva EEG–AGI (CPEA)** propone un marco metodológico destinado a cuantificar la convergencia estructural entre dinámicas electroencefalográficas humanas y representaciones latentes generadas por arquitecturas de inteligencia artificial generalizada. La coherencia entre ambos sistemas se conceptualiza como reducción dirigida de incertidumbre, formalizada mediante métricas de teoría de la información, particularmente *Transfer Entropy*.

Se desarrolla la infraestructura experimental de la Fase 1, el pipeline de procesamiento, la formalización matemática del Índice de Coherencia Predictiva (ICP) y un conjunto de programas de seguimiento orientados a validar estabilidad, robustez y direccionalidad causal del acoplamiento informacional.

---

# Palabras Clave

EEG · Transfer Entropy · Causalidad dirigida · Dinámica no lineal · Representaciones latentes · Neuroinformática · Complejidad · AGI · Información efectiva

---

# 1. Marco Conceptual

La hipótesis central del CPEA establece que, si un modelo fundacional internaliza regularidades profundas de la dinámica cognitiva, sus estados latentes deben contener información predictiva cuantificable respecto a la evolución temporal del EEG.

No se evalúa similitud superficial.
Se evalúa **homología informacional dirigida**.

El cerebro humano opera como sistema dinámico no lineal caracterizado por:

* Multiescala temporal
* Dependencia de estado
* No estacionariedad
* Transiciones críticas

Por tanto, las métricas lineales resultan insuficientes.

---

# 2. Arquitectura Experimental

## 2.1 Infraestructura EEG

* ≥ 64 canales
* ≥ 500 Hz
* Sincronización sub-milisegundo
* Registro simultáneo de estados latentes del modelo

> 💡 **Rationale**
> La precisión temporal es crítica para evitar falsos positivos en métricas causales.

---

# 3. Pipeline de Procesamiento

```text
EEG Raw
   ↓
Filtrado 8–30 Hz
   ↓
Rechazo de artefactos (ICA + kurtosis)
   ↓
Segmentación temporal
   ↓
Embeddings latentes
   ↓
Cálculo ICP + Transfer Entropy
```

## 3.1 Filtrado 8–30 Hz

Incluye bandas alfa y beta asociadas a estados atencionales y reduce contaminación electromiográfica.

---

# 4. Transfer Entropy como Métrica Causal

## 4.1 Definición Formal

[
TE_{Y \to X} =
\sum p(x_{t+1}, x_t^{(k)}, y_t^{(l)})
\log \frac{p(x_{t+1} | x_t^{(k)}, y_t^{(l)})}
{p(x_{t+1} | x_t^{(k)})}
]

Donde:

* (X_t): señal EEG
* (Y_t): estado latente AGI
* (k,l): dimensiones de embedding

Interpretación: reducción de incertidumbre futura de (X) al incorporar historia de (Y).

---

## 4.2 Extensión Multivariada

[
TE_{Y \to X | Z}
]

Permite eliminar efectos espurios debidos a variables comunes.

---

> 📌 **Ventaja Clave**
> No asume linealidad ni gaussianidad.

---

# 5. Índice de Coherencia Predictiva (ICP)

[
ICP =
\alpha C_s

* \beta \frac{TE_{Y \to X}}{H(X)}
* \gamma \Delta P
  ]

Donde:

* (C_s): coherencia espectral
* (H(X)): entropía
* (\Delta P): mejora predictiva
* (\alpha, \beta, \gamma): pesos ajustables

---

> 🔬 **Interpretación**
> El ICP mide convergencia estructural informacional, no equivalencia ontológica.

---

# 6. Robustez Estadística

* Permutaciones temporales
* Surrogate data
* Bootstrap
* Corrección FDR

Robustez:

[
R = 1 - \frac{\sigma_{ICP}}{\mu_{ICP}}
]

---

# 7. Programas de Seguimiento Experimental

## 7.1 Seguimiento Longitudinal

* Repeticiones intra-sujeto
* Evaluación estabilidad TE
* Análisis deriva estructural

## 7.2 Seguimiento Bajo Perturbación

* Carga cognitiva
* Ruido auditivo
* Fatiga controlada

## 7.3 Seguimiento Inter-sujeto

* Comparación grafos causales
* Identificación invariantes topológicos

---

> 📊 **Reproducibilidad**
> Notebooks sugeridos:
>
> * `/notebooks/TE_estimation.ipynb`
> * `/notebooks/ICP_pipeline.ipynb`
> * `/notebooks/Multivariate_network_analysis.ipynb`

---

# 8. Interpretación Sistémica

Si:

[
TE_{AGI \to EEG} > TE_{EEG \to AGI}
]

Se interpreta predominio informacional direccional.

No implica causalidad física.
Implica estructura predictiva asimétrica.

---

# Resumen Ejecutivo

* La coherencia debe medirse como reducción dirigida de incertidumbre.
* Transfer Entropy permite capturar causalidad no lineal.
* El ICP integra coherencia espectral y métricas informacionales.
* La robustez requiere validación por permutación y bootstrap.
* La convergencia evaluada es estructural, no ontológica.
* El diseño experimental contempla estabilidad longitudinal y resiliencia bajo perturbación.

---

# Referencias Comentadas

<details>
<summary><strong>Schreiber (2000)</strong> – Transfer Entropy</summary>

DOI: [https://doi.org/10.1103/PhysRevLett.85.461](https://doi.org/10.1103/PhysRevLett.85.461)
Introduce formalmente la Transfer Entropy como métrica no lineal de causalidad.

</details>

<details>
<summary><strong>Kraskov et al. (2004)</strong> – Mutual Information Estimation</summary>

DOI: [https://doi.org/10.1103/PhysRevE.69.066138](https://doi.org/10.1103/PhysRevE.69.066138)
Estimador KSG basado en vecinos más cercanos, base para TE robusta.

</details>

<details>
<summary><strong>Vicente et al. (2011)</strong> – TE en Neurociencia</summary>

DOI: [https://doi.org/10.1007/s10827-010-0262-3](https://doi.org/10.1007/s10827-010-0262-3)
Aplicación de Transfer Entropy en conectividad efectiva cerebral.

</details>

<details>
<summary><strong>Breakspear (2017)</strong> – Dinámica cerebral no lineal</summary>

DOI: [https://doi.org/10.1038/nn.4497](https://doi.org/10.1038/nn.4497)
Marco teórico sobre cerebro como sistema dinámico multiescala.

</details>

<details>
<summary><strong>Friston (2010)</strong> – Free Energy Principle</summary>

DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)
Principio de reducción de incertidumbre en sistemas biológicos.

</details>

---

# 🔎 Reproducibilidad y Transparencia

* Código abierto recomendado bajo licencia MIT
* Datos anonimizados
* Scripts de validación cruzada incluidos
* Registro preregistrado sugerido tipo OSF

---

# 📌 Estado del Proyecto

FASE 1 — Infraestructura y Marco Experimental
Transfer Entropy integrada como métrica de robustez causal

---
