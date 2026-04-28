# 🧠 Coherencia Predictiva EEG–AGI (CPEA)

## 🔹 FASE 2 — Construcción del Bucle Cognitivo

---

![Status](https://img.shields.io/badge/status-experimental-blue)
![Phase](https://img.shields.io/badge/phase-2-orange)
![Framework](https://img.shields.io/badge/framework-PyTorch-red)
![SNN](https://img.shields.io/badge/SNN-snnTorch-purple)
![License](https://img.shields.io/badge/license-MIT-green)
![Reproducibility](https://img.shields.io/badge/reproducible-notebooks-success)

---

> ⚠️ **Documento técnico para audiencia científica.**
> Lenguaje formal, desarrollo matemático y protocolos experimentales reproducibles.

---

# 📑 Tabla de Contenidos

* [Abstract](#abstract)
* [Palabras clave](#palabras-clave)
* [1. Introducción](#1-introducción)
* [2. Marco Teórico](#2-marco-teórico)

  * [2.1 Métrica de Simetría Toroidal](#21-métrica-de-simetría-toroidal)
  * [2.2 Operador de Desacoplamiento](#22-operador-de-desacoplamiento)
  * [2.3 Analogía Neurobiológica](#23-analogía-neurobiológica)
* [3. Teoría de Aprendizaje por Excepción (TAE)](#3-teoría-de-aprendizaje-por-excepción-tae)
* [4. Arquitectura del Bucle Cognitivo](#4-arquitectura-del-bucle-cognitivo)
* [5. Validación con Neurofeedback Cerrado](#5-validación-con-neurofeedback-cerrado)
* [6. Programas de Seguimiento](#6-programas-de-seguimiento)
* [7. Implementación Computacional](#7-implementación-computacional)
* [Conclusiones](#conclusiones)
* [Resumen Ejecutivo](#resumen-ejecutivo)
* [Referencias Comentadas](#referencias-comentadas)

---

# Abstract

Este documento formaliza la Fase 2 del proyecto **Coherencia Predictiva EEG–AGI (CPEA)** mediante la construcción de un bucle cognitivo cerrado basado en una métrica cuantificable de coherencia predictiva (ΔCP), integrando la **Teoría de Aprendizaje por Excepción (TAE)**, regularización elástica y redes neuronales espicosas.

Se introduce una métrica de simetría toroidal aplicada a matrices de conectividad EEG, se modela su pérdida como operador de desacoplamiento no lineal, y se propone un protocolo experimental de neurofeedback en tiempo real con latencia sub-50 ms.

El trabajo combina formalismo electromagnético, dinámica no lineal cortical y aprendizaje continuo para establecer un marco experimental replicable.

---

# Palabras clave

Simetría toroidal · Coherencia predictiva · EEG-AGI · TAE · Redes espicosas · Seguimiento experimental · No linealidad · Neurofeedback cerrado

---

# 1. Introducción

La coherencia predictiva representa la convergencia entre dinámica cerebral y modelos de inferencia artificial. No se trata únicamente de correlación estadística, sino de estabilidad estructural en espacio de fase.

El objetivo central de Fase 2 es validar un bucle cognitivo cerrado donde:

```
EEG → Extracción de rasgos → Modelo AGI → ΔCP → Feedback → EEG'
```

El sistema busca minimizar ΔCP, convergiendo hacia un punto fijo dinámico estable.

---

# 2. Marco Teórico

---

## 2.1 Métrica de Simetría Toroidal

Sea un campo dinámico:

[
\mathbf{F}(\mathbf{r},t)
]

Definimos la métrica de simetría toroidal:

[
\mathcal{S}*T = 1 - \frac{\int_V \left| \mathbf{F} - \mathbf{F}*{rot} \right|^2 dV}{\int_V |\mathbf{F}|^2 dV}
]

* ( \mathcal{S}_T = 1 ): simetría ideal
* ( \mathcal{S}_T < 1 ): pérdida de invariancia

En EEG, la métrica se aplica a matrices de conectividad funcional.

---

## 2.2 Operador de Desacoplamiento

[
\frac{\partial \mathbf{F}}{\partial t} = \mathcal{L}_0 \mathbf{F} + \epsilon \mathcal{D}(\mathbf{F})
]

Donde:

* ( \mathcal{L}_0 ) → dinámica lineal
* ( \mathcal{D} ) → operador no lineal inducido por pérdida de simetría

Este formalismo permite interpretar transiciones abruptas de coherencia como bifurcaciones.

---

## 2.3 Analogía Neurobiológica

Los trabajos de **Walter Freeman** demostraron transiciones de fase cortical medibles en EEG.

La Teoría de Información Integrada de **Giulio Tononi** aporta cuantificación de integración global, aunque aquí se prioriza formalismo electromagnético topológico.

---

> 💡 **Insight clave:**
> La coherencia no es únicamente sincronía espectral, sino preservación geométrica en espacio dinámico.

---

# 3. Teoría de Aprendizaje por Excepción (TAE)

Definimos coherencia predictiva:

[
CP(t) = \frac{\langle E(t), \hat{E}(t) \rangle}{|E(t)| |\hat{E}(t)|}
]

Excepción:

[
\Delta CP(t) < -\theta
]

La actualización de pesos ocurre exclusivamente ante desviaciones significativas.

---

> 📦 **Nota técnica (colapsable)**
>
> <details>
> <summary>Ventajas de TAE frente a entrenamiento continuo</summary>
>
> * Reduce sobreajuste
> * Preserva memoria estructural
> * Disminuye catástrofe del olvido
> * Optimiza eficiencia energética computacional
>
> </details>

---

# 4. Arquitectura del Bucle Cognitivo

Componentes:

* EEG multicanal
* Extracción espectral (FFT + coherencia de fase)
* Modelo híbrido Transformer + SNN
* Regularización EWC
* Feedback auditivo proporcional a ΔCP

Latencia objetivo: **< 50 ms**

---

# 5. Validación con Neurofeedback Cerrado

### Diseño experimental

| Parámetro       | Valor                      |
| --------------- | -------------------------- |
| Participantes   | ≥ 20                       |
| Canales EEG     | ≥ 32                       |
| Duración sesión | 20 min                     |
| Condiciones     | Feedback real vs aleatorio |

### Métricas

* Incremento medio de CP
* Reducción de entropía espectral
* Estabilidad en banda alfa/gamma

---

> ⚠️ **Condición crítica:**
> El feedback debe correlacionar estrictamente con ΔCP para evitar sesgos de aprendizaje.

---

# 6. Programas de Seguimiento

## Programa 1 — Seguimiento Topológico

* Cálculo continuo de ( \mathcal{S}_T )
* Análisis de bifurcaciones

## Programa 2 — Seguimiento Energético

* Potencia espectral normalizada
* Eficiencia energética relativa

## Programa 3 — Seguimiento Computacional

* Estabilidad de pesos bajo EWC
* Plasticidad vs retención

---

# 7. Implementación Computacional

## 🔗 Notebooks reproducibles

* 📓 [Notebook coherencia predictiva](./notebooks/cpea_coherence.ipynb)
* 📓 [Notebook SNN integración](./notebooks/cpea_snn.ipynb)
* 📓 [Notebook análisis topológico](./notebooks/topological_symmetry.ipynb)

---

### Dependencias

```bash
pip install torch snntorch avalanche-lib mne numpy scipy
```

---

### Estructura del repositorio

```
CPEA/
│
├── notebooks/
├── src/
├── data/
├── docs/
└── README.md
```

---

# Conclusiones

El sistema CPEA Fase 2:

* Formaliza coherencia predictiva como variable dinámica central
* Integra TAE + EWC + SNN en arquitectura estable
* Permite validación experimental con neurofeedback real
* Ofrece métricas cuantificables y reproducibles

La coherencia se interpreta como estabilidad geométrica en espacio de fase acoplado cerebro-máquina.

---

# Resumen Ejecutivo

* Se definió una métrica formal de simetría toroidal
* Se modeló la pérdida de simetría como operador no lineal
* Se integró TAE para aprendizaje eficiente
* Se diseñó protocolo experimental cerrado
* Se estructuraron programas de seguimiento replicables
* Se documentaron notebooks reproducibles

---

# Referencias Comentadas

<details>
<summary><strong>Walter Freeman — Dinámica cortical no lineal</strong></summary>

Freeman, W. J. (2000). Neurodynamics.
DOI: 10.1007/978-1-4471-0371-7

Demuestra transiciones de fase en EEG y fundamentos de dinámica no lineal cortical.

</details>

<details>
<summary><strong>Giulio Tononi — Información Integrada</strong></summary>

Tononi, G. (2004). An information integration theory of consciousness.
DOI: 10.1186/1471-2202-5-42

Formaliza cuantificación de integración global en sistemas conscientes.

</details>

<details>
<summary><strong>James Clerk Maxwell — Electrodinámica</strong></summary>

Maxwell, J.C. (1865). A Dynamical Theory of the Electromagnetic Field.
DOI: 10.1098/rstl.1865.0008

Base matemática del formalismo electromagnético moderno.

</details>

<details>
<summary><strong>Hermann von Helmholtz — Conservación energética</strong></summary>

Helmholtz, H. (1847). Über die Erhaltung der Kraft.

Fundamento conceptual de conservación en sistemas físicos complejos.

</details>

---

---

# 📌 Estado del Proyecto

> 🟢 Fase 2 en desarrollo experimental
> 🧪 Validación de neurofeedback pendiente de resultados empíricos finales
> 🔄 Integración Avalanche (continual learning) en progreso

---
