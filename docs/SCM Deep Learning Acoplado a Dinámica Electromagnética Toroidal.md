<!-- ========================================================= -->
<!-- ===============  CPEA – FASE 2 README  ================== -->
<!-- ========================================================= -->

# 🧠⚡ CPEA — Fase 2  
## Construcción del Bucle Cognitivo Causal EEG–AGI  
### SCM Deep Learning Acoplado a Dinámica Electromagnética Toroidal

---

![Status](https://img.shields.io/badge/status-active%20development-0a9396)
![Framework](https://img.shields.io/badge/framework-DoWhy%20%2B%20PyTorch-005f73)
![Causality](https://img.shields.io/badge/causality-structural%20model-critical)
![Topology](https://img.shields.io/badge/topology-toroidal%20field-informational)
![License](https://img.shields.io/badge/license-research-blue)
![Reproducible](https://img.shields.io/badge/reproducibility-notebooks%20included-success)

---

> ⚠️ **Repositorio en evolución estructural**  
> Esta fase introduce formalización matemática avanzada y validación causal robusta del sistema EEG–AGI.

---

# 📑 Índice Navegable

- [1. Visión General](#1-visión-general)
- [2. Arquitectura Conceptual](#2-arquitectura-conceptual)
- [3. Modelo Estructural Causal (SCM)](#3-modelo-estructural-causal-scm)
- [4. Acoplamiento con Redes Profundas](#4-acoplamiento-con-redes-profundas)
- [5. Integración Electromagnética Toroidal](#5-integración-electromagnética-toroidal)
- [6. Gradiente Causal Profundo](#6-gradiente-causal-profundo)
- [7. Función de Pérdida Causal–Electromagnética](#7-función-de-pérdida-causal–electromagnética)
- [8. Programas de Seguimiento Experimental](#8-programas-de-seguimiento-experimental)
- [9. Notebooks Reproducibles](#9-notebooks-reproducibles)
- [10. Referencias Científicas](#10-referencias-científicas)

---

# 1️⃣ Visión General

La **Fase 2 del proyecto CPEA** redefine el bucle cognitivo EEG–AGI como un sistema:

- Predictivo  
- Intervencional  
- Estructuralmente causal  
- Físicamente coherente  

El núcleo de esta fase consiste en integrar:

✔ Modelos Estructurales Causales (SCM)  
✔ Framework DoWhy  
✔ Redes profundas  
✔ Dinámica electromagnética toroidal  

---

> 💡 **Principio Rector**
>
> Un sistema cognitivo artificial acoplado a EEG no puede limitarse a correlaciones estadísticas.  
> Debe modelar explícitamente relaciones causales bajo intervención.

---

# 2️⃣ Arquitectura Conceptual

## 🔷 Componentes principales

\[
\mathcal{S} = (\mathcal{V}, \mathcal{E}, \mathcal{F}, P(U))
\]

Donde:

- \(E_t\) → Estado EEG  
- \(Z_t\) → Embedding profundo causal  
- \(\Theta_t\) → Parámetros del modelo  
- \(I_t\) → Intervención  
- \(T_t\) → Estado topológico toroidal  
- \(U_t\) → Variables exógenas  

---

### 🔁 Flujo estructural

```

T_t → E_t → Z_t → Θ_t
↑         ↓
└──────── E_{t+1}

````

Cada “slice” temporal es un DAG acíclico.

---

# 3️⃣ Modelo Estructural Causal (SCM)

## 📐 Ecuaciones estructurales

\[
T_t = f_T(U_T)
\]

\[
E_t = f_E(T_t, \Theta_{t-1}, U_E)
\]

\[
Z_t = f_Z(E_t; \phi)
\]

\[
\Theta_t = f_\Theta(Z_t, I_t; \psi)
\]

---

> 🔎 **Distinción fundamental**
>
> \[
> P(Y|X) \neq P(Y|do(X))
> \]
>
> La segunda representa intervención causal.

---

## 🎯 Identificación por ajuste backdoor

\[
P(E_{t+1} \mid do(I_t)) = \sum_z P(E_{t+1} \mid I_t, Z_t=z) P(Z_t=z)
\]

---

# 4️⃣ Acoplamiento con Redes Profundas

## 🧬 Embedding como nodo causal

El espacio latente:

\[
Z_t \in \mathbb{R}^d
\]

no es meramente funcional.  
Es un nodo causal explícito dentro del DAG.

---

## 🔐 Regularización por independencia

\[
\mathcal{L}_{indep} =
\sum_{i \neq j}
\left|
I(Z_i ; Z_j \mid PA(Z_i))
\right|
\]

Se reduce redundancia causal espuria.

---

# 5️⃣ Integración Electromagnética Toroidal

## ⚡ Fundamento físico

El EEG deriva de dinámicas electromagnéticas gobernadas por Maxwell:

\[
\nabla \times \mathbf{B} =
\mu_0 \mathbf{J} +
\mu_0 \epsilon_0 \frac{\partial \mathbf{E}}{\partial t}
\]

---

## 🌀 Representación Toroidal

El campo reducido:

\[
\mathbf{F}(\theta,\phi,t) =
\sum_{m,n} a_{mn}(t) e^{i(m\theta+n\phi)}
\]

Donde:

- \(a_{mn}\) → coeficientes armónicos
- \((\theta,\phi)\) → coordenadas del toro

---

## 📌 Variable estructural

\[
T_t = \{a_{mn}(t)\}
\]

Nodo causal explícito:

\[
T_t → E_t
\]

---

### 📊 Efecto causal topológico

\[
\Delta_{topo} =
\mathbb{E}[E_t \mid do(a_{mn}=a^*)]
-
\mathbb{E}[E_t \mid do(a_{mn}=0)]
\]

---

> 🧠 Si el efecto persiste tras refutación,  
> el modo toroidal es causalmente activo.

---

# 6️⃣ Gradiente Causal Profundo

No equivale a backpropagation clásico.

\[
\nabla_{causal} =
\frac{\partial}{\partial I_t}
\mathbb{E}[E_{t+1} \mid do(I_t)]
\]

Expansión:

\[
\nabla_{causal}
=
\sum_z
\frac{\partial P(E_{t+1} \mid I_t, Z_t=z)}
{\partial I_t}
P(Z_t=z)
\]

---

> ⚠️ Diferencia crítica:  
> El gradiente causal depende de identificación estructural,  
> no solo de diferenciabilidad computacional.

---

# 7️⃣ Función de Pérdida Causal–Electromagnética

\[
\mathcal{L} =
\mathcal{L}_{pred}
+
\lambda \mathcal{L}_{ATE}
+
\gamma \mathcal{L}_{topo}
+
\eta \mathcal{L}_{stability}
\]

---

## 🔬 Pérdida topológica

\[
\mathcal{L}_{topo}
=
\sum_{m,n}
\left|
\Delta_{topo}^{emp}
-
\Delta_{topo}^{model}
\right|
\]

---

# 8️⃣ Programas de Seguimiento Experimental

## 🧪 1. Intervención Paramétrica

- Manipulación controlada de \(I_t\)
- Estimación de ATE
- Refutación con placebo

---

## 🧪 2. Seguimiento Topológico

- Descomposición armónica toroidal
- Análisis espectral dinámico
- Comparación pre/post intervención

---

## 🧪 3. Robustez

- Submuestreo temporal
- Inclusión de confusores sintéticos
- Permutación estructural

---

> 📌 Objetivo: Validación estructural, no correlacional.

---

# 9️⃣ Notebooks Reproducibles

📁 `/notebooks/`

- [`01_scm_construction.ipynb`](./notebooks/01_scm_construction.ipynb)
- [`02_dowhy_integration.ipynb`](./notebooks/02_dowhy_integration.ipynb)
- [`03_toroidal_decomposition.ipynb`](./notebooks/03_toroidal_decomposition.ipynb)
- [`04_causal_gradient_analysis.ipynb`](./notebooks/04_causal_gradient_analysis.ipynb)

---

> 💻 Requisitos:
>
> ```bash
> pip install dowhy torch numpy scipy networkx
> ```

---

# 🔟 Referencias Científicas

<details>
<summary><strong>Pearl, J. (2009). Causality.</strong></summary>

Modelo formal de SCM y operador do.  
Base matemática de inferencia causal estructural.  
</details>

---

<details>
<summary><strong>Schreiber, T. (2000). Measuring Information Transfer.</strong></summary>

Phys. Rev. Lett. 85, 461–464.  
DOI: https://doi.org/10.1103/PhysRevLett.85.461  
Define Transferencia de Entropía.  
</details>

---

<details>
<summary><strong>Spirtes, Glymour & Scheines (2000). Causation, Prediction, and Search.</strong></summary>

Fundamentos algorítmicos de descubrimiento causal.  
</details>

---

<details>
<summary><strong>Sharma & Kiciman (2020). DoWhy.</strong></summary>

Proceedings of KDD 2020.  
DOI: https://doi.org/10.1145/3447548.3467308  
Framework de inferencia causal reproducible.  
</details>

---

<details>
<summary><strong>Friston, K. (2010). The Free-Energy Principle.</strong></summary>

Nature Reviews Neuroscience.  
DOI: https://doi.org/10.1038/nrn2787  
Marco dinámico para sistemas auto-organizados.  
</details>

---

<details>
<summary><strong>Buzsáki, G. (2006). Rhythms of the Brain.</strong></summary>

Relación entre oscilaciones neuronales y organización funcional.  
</details>

---

# 📌 Síntesis Final

- El embedding profundo se redefine como nodo causal.
- Se formaliza acoplamiento SCM–Deep Learning.
- Se integra topología toroidal como variable estructural.
- Se define gradiente causal diferenciado.
- La pérdida incorpora coherencia electromagnética.
- Se establecen programas de seguimiento experimental.
- El sistema pasa de predictivo a intervencional.

---

# 🧠⚡ CPEA — Fase 2

> Arquitectura causal profunda con coherencia electromagnética estructural.

---

**Repositorio diseñado para investigación avanzada en causalidad, neurodinámica y AGI estructural.**
````
