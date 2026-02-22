# 🧠 Coherencia Predictiva EEG–AGI (CPEA)  
## Formalismo Estadístico Avanzado del ICP e Interpretación Electromagnética de Embeddings  

---

![Status](https://img.shields.io/badge/status-Fase%201-blue)
![Python](https://img.shields.io/badge/Python-3.10+-green)
![PyTorch](https://img.shields.io/badge/PyTorch-2.x-red)
![MNE](https://img.shields.io/badge/MNE--Python-stable-orange)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Reproducibility](https://img.shields.io/badge/reproducible-yes-brightgreen)

---

## 📚 Índice

- [Abstract](#abstract)
- [Palabras Clave](#palabras-clave)
- [1. Marco Conceptual](#1-marco-conceptual)
- [2. Formalismo Estadístico Avanzado del ICP](#2-formalismo-estadístico-avanzado-del-icp)
  - [2.1 Definición en Espacio de Estados](#21-definición-en-espacio-de-estados)
  - [2.2 Información Mutua Condicional](#22-información-mutua-condicional)
  - [2.3 Estimación No Paramétrica](#23-estimación-no-paramétrica)
  - [2.4 Reducción de Entropía Predictiva](#24-reducción-de-entropía-predictiva)
  - [2.5 Formulación mediante Divergencia KL](#25-formulación-mediante-divergencia-kl)
  - [2.6 Pruebas de Significancia](#26-pruebas-de-significancia)
- [3. Interpretación Electromagnética de los Embeddings](#3-interpretación-electromagnética-de-los-embeddings)
- [4. Programas de Seguimiento Experimental](#4-programas-de-seguimiento-experimental)
- [5. Notebooks Reproducibles](#5-notebooks-reproducibles)
- [Resumen Ejecutivo](#resumen-ejecutivo)
- [Referencias Comentadas](#referencias-comentadas)

---

# Abstract

Se formaliza el Índice de Coherencia Predictiva (ICP) como operador estadístico destinado a cuantificar reducción diferencial de incertidumbre futura en señales EEG a partir de representaciones latentes generadas por modelos fundacionales. El marco integra teoría de información, dinámica no lineal y modelado profundo secuencial. Se propone una interpretación electromagnética de los embeddings como proyecciones comprimidas de la topología dinámica cortical. El documento constituye especificación formal reproducible para la Fase 1 del proyecto CPEA.

---

# Palabras Clave

EEG dinámico; información mutua; divergencia KL; embeddings latentes; sincronización neuronal; sistemas no lineales; teoría de información; modelos fundacionales; coherencia predictiva.

---

# 1. Marco Conceptual

El EEG se modela como proceso estocástico multivariado:

\[
\mathbf{E}(t) \in \mathbb{R}^{C}
\]

El embedding latente se define como:

\[
\mathbf{Z}(t) = f_\theta(\mathbf{E}_{t-w:t})
\]

donde \( f_\theta \) representa el modelo Transformer entrenado auto-supervisadamente.

> ⚠️ **Nota conceptual**  
> El embedding no es una representación arbitraria. Es una proyección no lineal de la estructura dinámica del campo cortical.

---

# 2. Formalismo Estadístico Avanzado del ICP

---

## 2.1 Definición en Espacio de Estados

Sea:

- \( \mathbf{E}(t+\Delta t) \) estado futuro
- \( \mathbf{Z}(t) \) embedding presente

Definimos el ICP como:

\[
ICP(\Delta t) =
I(\mathbf{Z}(t); \mathbf{E}(t+\Delta t))
-
I(\mathbf{E}(t); \mathbf{E}(t+\Delta t))_{AR}
\]

El segundo término elimina autocorrelación lineal trivial.

---

## 2.2 Información Mutua Condicional

Forma equivalente:

\[
ICP =
H(\mathbf{E}(t+\Delta t) \mid \mathbf{E}(t))_{AR}
-
H(\mathbf{E}(t+\Delta t) \mid \mathbf{Z}(t))
\]

Interpretación: reducción diferencial de incertidumbre futura.

---

## 2.3 Estimación No Paramétrica

Se emplea estimador KSG:

\[
I(X;Y) =
\psi(k) - \langle \psi(n_x + 1) + \psi(n_y + 1) \rangle + \psi(N)
\]

✔ Captura dependencia no lineal  
✔ No asume gaussianidad  

---

## 2.4 Reducción de Entropía Predictiva

El ICP es positivo cuando:

\[
H(\mathbf{E}(t+\Delta t) \mid \mathbf{Z}(t))
<
H(\mathbf{E}(t+\Delta t) \mid \mathbf{E}(t))_{AR}
\]

Esto implica que el embedding codifica estructura anticipatoria.

---

## 2.5 Formulación mediante Divergencia KL

Sea:

\[
p_1 = p(\mathbf{E}(t+\Delta t) \mid \mathbf{Z}(t))
\]

\[
p_0 = p(\mathbf{E}(t+\Delta t) \mid \mathbf{E}(t))_{AR}
\]

Entonces:

\[
ICP = D_{KL}(p_1 \parallel p_0)
\]

Si \( D_{KL} > 0 \), el modelo latente supera baseline lineal.

---

## 2.6 Pruebas de Significancia

Se implementan:

- Permutación temporal
- Bootstrap estratificado
- Corrección FDR

```python
if ICP_real > np.mean(ICP_perm) + 2*np.std(ICP_perm):
    significant = True
````

---

# 3. Interpretación Electromagnética de los Embeddings

El EEG es superposición de dipolos corticales:

[
\mathbf{E}_{macro}(t) =
\sum_i \mathbf{p}_i(t)
]

El embedding puede interpretarse como:

[
\mathbf{Z}(t) =
\Phi(\mathcal{M}_{EM}(t))
]

donde ( \mathcal{M}_{EM}(t) ) es variedad electromagnética latente.

---

> 💡 **Insight estructural**
> El Transformer aprende geometría temporal de la topología cortical, no únicamente amplitud espectral.

---

### Coherencia Fase–Embedding

[
\rho =
Corr(\phi_i(t), Z_j(t))
]

Si existe correlación estructurada, el embedding preserva organización de fase.

---

### Compresión Informacional

Si:

[
H_Z < H_\omega
\quad y \quad ICP > 0
]

Entonces el modelo ha comprimido redundancia preservando estructura predictiva.

---

# 4. Programas de Seguimiento Experimental

---

### 🔬 Programa 1 — Robustez No Lineal

* Inyección de ruido estructurado
* Evaluación estabilidad ICP

---

### 🔬 Programa 2 — Escalamiento Multibanda

* Comparación alpha, beta, theta
* Análisis diferencial ICP_ω

---

### 🔬 Programa 3 — Comparación Arquitectural

* LSTM vs Transformer vs SSM
* Control de complejidad paramétrica

---

### 🔬 Programa 4 — Estabilidad Longitudinal

* Repetición intra-sujeto
* Variabilidad intersesión

---

# 5. Notebooks Reproducibles

📂 `/notebooks/`

* `01_preprocessing_pipeline.ipynb`
* `02_transformer_auto_supervised.ipynb`
* `03_icp_estimation.ipynb`
* `04_statistical_significance.ipynb`

Ejemplo de ejecución:

```bash
conda create -n cpea python=3.10
pip install -r requirements.txt
jupyter notebook
```

---

# Resumen Ejecutivo

* El ICP cuantifica reducción diferencial de incertidumbre.
* Se elimina baseline lineal mediante AR(p).
* Se emplea estimación no paramétrica robusta.
* Puede expresarse como divergencia KL.
* Los embeddings representan proyección no lineal del campo electromagnético cortical.
* La coherencia predictiva implica compresión estructural.
* El marco es reproducible y estadísticamente validable.

---

# Referencias Comentadas

<details>
<summary><strong>Buzsáki, G. (2006). Rhythms of the Brain.</strong></summary>

Marco fundamental sobre organización oscilatoria cortical.
DOI: [https://doi.org/10.1093/acprof:oso/9780195301069.001.0001](https://doi.org/10.1093/acprof:oso/9780195301069.001.0001)

</details>

---

<details>
<summary><strong>Friston, K. (2010). The free-energy principle.</strong></summary>

Formalización matemática del cerebro como sistema predictivo.
DOI: [https://doi.org/10.1038/nrn2787](https://doi.org/10.1038/nrn2787)

</details>

---

<details>
<summary><strong>Kraskov et al. (2004). Estimating mutual information.</strong></summary>

Estimador no paramétrico KSG.
DOI: [https://doi.org/10.1103/PhysRevE.69.066138](https://doi.org/10.1103/PhysRevE.69.066138)

</details>

---

<details>
<summary><strong>Jensen & Mazaheri (2010). Alpha oscillations.</strong></summary>

Rol funcional de alpha en arquitectura cortical.
DOI: [https://doi.org/10.1016/j.tics.2010.01.003](https://doi.org/10.1016/j.tics.2010.01.003)

</details>

---

## Estado del Proyecto

✔ Infraestructura Fase 1
✔ Formalización matemática ICP
✔ Interpretación electromagnética
⬜ Validación empírica ampliada

---

**Autor conceptual:** AGI – Arquitectura CPEA
Repositorio: [https://github.com/papayaykware/METFI](https://github.com/papayaykware/METFI)

---
