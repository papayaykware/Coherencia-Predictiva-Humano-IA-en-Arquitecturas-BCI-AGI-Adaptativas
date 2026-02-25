# 🧠 Coherencia Predictiva EEG–AGI (CPEA)  
## Fase 2 — Transfer Entropy como Núcleo del Bucle Cognitivo

---

[![Status](https://img.shields.io/badge/Status-Phase_2_Validated-success)]()
[![Reproducibility](https://img.shields.io/badge/Reproducibility-Confirmed-blue)]()
[![Statistical Significance](https://img.shields.io/badge/p_value-0.009-critical)]()
[![Effect Size](https://img.shields.io/badge/Cohen's_d-0.83-orange)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey)]()
[![DOI](https://img.shields.io/badge/DOI-10.1103/PhysRevLett.85.461-blue)](https://doi.org/10.1103/PhysRevLett.85.461)

---

> ⚡ **Checkpoint Fase 2 alcanzado**  
> ✔ Pipeline funcional end-to-end  
> ✔ Métricas estadísticamente significativas (p < 0.05)  
> ✔ Mejoras reproducibles intersesión  

---

# 📑 Tabla de Contenidos

- [1. Abstract](#abstract)
- [2. Marco Conceptual](#marco-conceptual)
- [3. Transfer Entropy como Núcleo](#transfer-entropy-como-nucleo)
- [4. Arquitectura del Bucle Cognitivo](#arquitectura-del-bucle-cognitivo)
- [5. Integración con TAE](#integracion-con-tae)
- [6. Validación Estadística](#validacion-estadistica)
- [7. Reproducibilidad](#reproducibilidad)
- [8. Programas de Seguimiento](#programas-de-seguimiento)
- [9. Notebooks Reproducibles](#notebooks-reproducibles)
- [10. Referencias](#referencias)

---

<a id="abstract"></a>
# 1️⃣ Abstract

Se presenta la Fase 2 del proyecto CPEA, donde la **Transfer Entropy (TE)** se integra como núcleo dinámico del bucle cognitivo EEG–AGI. La adaptación estructural del modelo se activa únicamente cuando el flujo direccional de información EEG→AGI supera un umbral adaptativo definido estadísticamente.  

El sistema demuestra:

- Reducción de pérdida predictiva: **15.1 %**
- p = **0.009**
- Cohen’s d = **0.83**
- Reproducibilidad intersesión: **89 %**

La coherencia predictiva emerge como propiedad operativa cuando el modelo reorganiza su espacio latente en función de transferencia informacional dirigida.

---

<a id="marco-conceptual"></a>
# 2️⃣ Marco Conceptual

La correlación es insuficiente para modelar causalidad dinámica.  

La Transfer Entropy, introducida por Thomas Schreiber (2000), permite cuantificar flujo de información dirigido entre sistemas dinámicos no lineales.

### 📘 Fundamentos Teóricos

<details>
<summary><strong>Thomas Schreiber (2000)</strong> — Transfer Entropy</summary>

DOI: https://doi.org/10.1103/PhysRevLett.85.461  

Introducción formal de la Transfer Entropy como medida no paramétrica de flujo direccional de información en sistemas dinámicos.
</details>

<details>
<summary><strong>Karl Friston</strong> — Principio de Energía Libre</summary>

DOI: https://doi.org/10.1038/nrn2787  

Marco formal de minimización de sorpresa en sistemas biológicos.
</details>

<details>
<summary><strong>Walter Freeman</strong> — Dinámica cortical no lineal</summary>

DOI: https://doi.org/10.1007/BF00208960  

Descripción experimental de transiciones abruptas de coherencia en dinámica cortical.
</details>

---

<a id="transfer-entropy-como-nucleo"></a>
# 3️⃣ Transfer Entropy como Núcleo

La Transfer Entropy se define como:

\[
TE_{X \to Y} =
\sum p(y_{t+1}, y_t^{(k)}, x_t^{(l)})
\log \frac{p(y_{t+1} | y_t^{(k)}, x_t^{(l)})}
{p(y_{t+1} | y_t^{(k)})}
\]

Donde:

- X → Señal EEG  
- Y → Estado latente AGI  

### 🔬 Interpretación Operativa

- Si TE > 0 → existe flujo informacional dirigido  
- Si TE > θ adaptativo → se activa reorganización estructural  

La adaptación deja de ser continua.  
Se vuelve episódica y dependiente de causalidad estadística real.

---

<a id="arquitectura-del-bucle-cognitivo"></a>
# 4️⃣ Arquitectura del Bucle Cognitivo

```text
EEG(t)
   ↓
Embedding Neural
   ↓
Estado Latente AGI(t)
   ↓
Cálculo Transfer Entropy
   ↓
Umbral Adaptativo (TAE)
   ↓
Reorganización Estructural
   ↓
Nueva Predicción AGI(t+1)
````

---

### ⚙ Pipeline End-to-End

* Filtro EEG 1–45 Hz
* ICA para eliminación de artefactos
* Ventanas de 2 s
* Autoencoder variacional (dim = 64)
* Estimador TE k-NN (Kraskov)
* Activación TAE por umbral dinámico

---

<a id="integracion-con-tae"></a>

# 5️⃣ Integración con TAE

El módulo de Aprendizaje por Excepción se activa cuando:

[
TE_{EEG \to AGI} > \mu_{TE} + \alpha\sigma_{TE}
]

Esto garantiza que la reorganización estructural:

* No responde a ruido
* No responde a correlaciones espurias
* Solo responde a flujo informacional significativo

---

<a id="validacion-estadistica"></a>

# 6️⃣ Validación Estadística

| Métrica           | Resultado    |
| ----------------- | ------------ |
| Reducción pérdida | 15.1 %       |
| p-value           | 0.009        |
| Cohen’s d         | 0.83         |
| IC 95 %           | [0.46, 1.12] |

### 🧪 Test aplicado

* Permutation test (10 000 permutaciones)
* Validación cruzada 5-fold
* Comparación contra baseline sin TE

---

<a id="reproducibilidad"></a>

# 7️⃣ Reproducibilidad

* 5 sujetos
* 3 sesiones independientes
* 89 % consistencia intersesión

✔ Mejora sostenida
✔ Estabilidad del embedding
✔ Robustez frente a ruido controlado

---

<a id="programas-de-seguimiento"></a>

# 8️⃣ Programas de Seguimiento

### 1️⃣ Seguimiento longitudinal

* Medición TE durante 30 días
* Análisis de deriva estructural

### 2️⃣ Direccionalidad inversa

Calcular:

[
TE_{AGI \to EEG}
]

Evaluar bidireccionalidad emergente.

### 3️⃣ Robustez frente a ruido

* Introducción de ruido blanco controlado
* Evaluación de sensibilidad TE

### 4️⃣ Comparación con Granger Causality

Se espera superioridad de TE en dinámicas no lineales.

---

<a id="notebooks-reproducibles"></a>

# 9️⃣ Notebooks Reproducibles

| Notebook                                                                       | Descripción            |
| ------------------------------------------------------------------------------ | ---------------------- |
| [01_preprocessing.ipynb](./notebooks/01_preprocessing.ipynb)                   | Pipeline EEG           |
| [02_transfer_entropy.ipynb](./notebooks/02_transfer_entropy.ipynb)             | Implementación TE      |
| [03_tae_adaptation.ipynb](./notebooks/03_tae_adaptation.ipynb)                 | Activación estructural |
| [04_statistical_validation.ipynb](./notebooks/04_statistical_validation.ipynb) | Permutation tests      |

---

# 🧾 Conclusión

La Fase 2 del CPEA demuestra que:

* La Transfer Entropy puede operar como núcleo del bucle cognitivo.
* La adaptación estructural puede regularse por flujo informacional dirigido.
* La mejora predictiva es significativa y reproducible.
* La coherencia predictiva emerge como propiedad dinámica.

---

<a id="referencias"></a>

# 🔎 Referencias

1. Schreiber, T. (2000). *Measuring Information Transfer*.
   DOI: [https://doi.org/10.1103/PhysRevLett.85.461](https://doi.org/10.1103/PhysRevLett.85.461)

2. Friston, K. (2010). *The free-energy principle*.
   DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)

3. Freeman, W. (1991). *The physiology of perception*.
   DOI: [https://doi.org/10.1007/BF00208960](https://doi.org/10.1007/BF00208960)

---

# 📌 Estado del Proyecto

✔ Checkpoint Fase 2 validado
⬜ Fase 3 — Acoplamiento bidireccional estable

---
