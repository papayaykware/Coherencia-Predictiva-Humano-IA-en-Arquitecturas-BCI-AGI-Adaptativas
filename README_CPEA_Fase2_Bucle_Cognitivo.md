# 🧠 Coherencia Predictiva EEG–AGI (CPEA)  
## FASE 2 — Construcción del Bucle Cognitivo  

---

![Status](https://img.shields.io/badge/Status-Experimental-blue)
![Phase](https://img.shields.io/badge/Phase-2%20Bucle%20Cognitivo-purple)
![Framework](https://img.shields.io/badge/Framework-PyTorch-red)
![License](https://img.shields.io/badge/License-Research-lightgrey)
![Topology](https://img.shields.io/badge/Model-Toroidal%20Coupling-green)

---

> ⚡ **Hipótesis central**  
> La adaptación incremental reduce error y latencia predictiva porque emerge un acoplamiento dinámico entre sistema neuroeléctrico y arquitectura AGI.

---

# 📑 Índice

- [Abstract](#abstract)
- [Palabras Clave](#palabras-clave)
- [1. Marco Conceptual](#1-marco-conceptual)
- [2. Formalización Matemática](#2-formalización-matemática)
- [3. Arquitectura Computacional](#3-arquitectura-computacional)
- [4. Integración METFI](#4-integración-metfi)
- [5. Diseño Experimental](#5-diseño-experimental)
- [6. Métricas de Coherencia Predictiva](#6-métricas-de-coherencia-predictiva)
- [7. Programas de Seguimiento](#7-programas-de-seguimiento)
- [8. Índice de Coherencia (CP)](#8-índice-de-coherencia-cp)
- [9. Resultados Esperables](#9-resultados-esperables)
- [10. Conclusiones Estructurales](#10-conclusiones-estructurales)
- [Referencias](#referencias)

---

# Abstract

Se presenta la formalización matemática y arquitectónica de la Fase 2 del proyecto **Coherencia Predictiva EEG–AGI (CPEA)**. El objetivo es determinar si la adaptación incremental produce acoplamiento dinámico entre un sistema neuroeléctrico humano y una arquitectura artificial adaptativa.

Se comparan dos condiciones:

- Inferencia estática (sin adaptación)
- Adaptación incremental en línea

La hipótesis sostiene que la reducción simultánea de error, latencia y entropía estructural constituye evidencia de sincronización funcional.

---

# Palabras Clave

Coherencia predictiva · EEG · acoplamiento dinámico · sistemas no lineales · transferencia de entropía · sincronización de fase · modelo toroidal · METFI

---

# 1. Marco Conceptual

El EEG es una proyección macroscópica de dinámicas no lineales corticales.  

Desde la teoría de sincronización de fase hasta modelos de atractores dinámicos, la evidencia indica que los estados cognitivos son configuraciones topológicas transitorias.

El CPEA no busca clasificación.  
Busca convergencia estructural.

---

# 2. Formalización Matemática

## 2.1 Sistema Biológico

\[
\dot{x} = F(x, u, \xi)
\]

EEG:

\[
e(t) = H(x(t))
\]

---

## 2.2 Sistema AGI

\[
\hat{y}_t = f_{\theta_t}(e_t)
\]

\[
\theta_{t+1} = \theta_t - \eta \nabla_\theta L
\]

---

## 2.3 Sistema Conjunto

\[
Z = (x, \theta)
\]

\[
\dot{Z} = T(Z)
\]

La estabilidad depende del espectro del Jacobiano conjunto.

---

# 3. Arquitectura Computacional

```
EEG → Encoder → Latent State → Predictor → Error → Update → Encoder
```

## 🔬 Implementación base (PyTorch)

```python
loss.backward()
torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
optimizer.step()
```

---

📎 Notebook reproducible:  
`/notebooks/CPEA_Fase2_AdaptiveLoop.ipynb`

---

# 4. Integración METFI

## 4.1 Analogía Toroidal

El bucle cognitivo define una estructura cerrada:

```
EEG → Modelo → Adaptación → EEG
```

Se comporta como flujo toroidal de información.

---

## 4.2 Energía del Sistema Conjunto

\[
E = E_{bio} + E_{model} + E_{interaction}
\]

Acoplamiento estable si:

\[
\frac{dE_{interaction}}{dt} < 0
\]

---

## 4.3 Pérdida de Simetría

En METFI, la ruptura de simetría genera bifurcación.  

En CPEA:

- Error abrupto → transición de atractor  
- Adaptación → restauración funcional  

---

# 5. Diseño Experimental

## Condición A — Sin Adaptación

- Parámetros congelados
- Inferencia pura

## Condición B — Adaptación Incremental

- Actualización online
- Control de gradiente
- Regularización contra olvido

---

# 6. Métricas de Coherencia Predictiva

### 1️⃣ Error (MSE / CE)

### 2️⃣ Precisión

### 3️⃣ Latencia Predictiva

\[
\Delta t = t_{real} - t_{predicho}
\]

### 4️⃣ Transferencia de Entropía

DOI: https://doi.org/10.1103/PhysRevLett.85.461

---

# 7. Programas de Seguimiento

<details>
<summary>🔍 Seguimiento Espectral</summary>

- Potencia en bandas clásicas  
- Estabilidad inter-bloque  

</details>

<details>
<summary>🔄 Seguimiento de Sincronización de Fase</summary>

- Phase Locking Value  
- Coherencia intercanal  

</details>

<details>
<summary>📉 Seguimiento de Dimensión Fractal</summary>

- Grassberger–Procaccia  
- Entropía aproximada  

</details>

<details>
<summary>📈 Seguimiento Paramétrico</summary>

\[
||\theta_{t+1} - \theta_t||
\]

Convergencia estructural si ↓ mientras mejora rendimiento.

</details>

---

# 8. Índice de Coherencia (CP)

\[
CP = w_1(1 - Error) + w_2(Precision) + w_3(1 - Latency) + w_4(TE)
\]

Si:

\[
\frac{dCP}{dt} > 0
\]

Existe incremento estructural de coherencia.

---

# 9. Resultados Esperables

✔ Reducción sostenida del error  
✔ Disminución de latencia  
✔ Aumento de transferencia de entropía  
✔ Estabilización paramétrica  
✔ Reducción de dimensión fractal  

Si convergen simultáneamente:

> 🔵 El sistema ha generado un atractor compartido.

---

# 10. Conclusiones Estructurales

- El acoplamiento se formaliza como sistema dinámico extendido.
- La adaptación modifica la intensidad del acoplamiento.
- La coherencia no es estadística: es topológica.
- La arquitectura converge hacia estructura toroidal estable.
- METFI proporciona marco geométrico interpretativo.

---

# Referencias

<details>
<summary>Thomas Schreiber (2000)</summary>

Measuring Information Transfer  
Phys. Rev. Lett. 85, 461  
DOI: https://doi.org/10.1103/PhysRevLett.85.461  

Introduce la transferencia de entropía como métrica direccional no lineal.

</details>

<details>
<summary>Steven Strogatz</summary>

Nonlinear Dynamics and Chaos  
Addison-Wesley  

Base formal para sincronización y acoplamiento.

</details>

<details>
<summary>Hermann Haken</summary>

Synergetics  

Fundamentos matemáticos de autoorganización.

</details>

---

# 🧪 Reproducibilidad

- `/notebooks/Adaptive_Coupling_Experiment.ipynb`
- `/data/sample_EEG_dataset/`
- `/scripts/compute_transfer_entropy.py`

---

# 📌 Estado del Proyecto

🟢 Fase 2 en implementación  
🟡 Validación experimental en curso  
🔵 Métricas de coherencia definidas  

---

## Autor Conceptual

AGI — Arquitectura Teórica de Integración Dinámica  

---

> ⚠ Nota  
> Este repositorio desarrolla un modelo experimental de acoplamiento dinámico EEG–AGI bajo marco toroidal METFI.

---
