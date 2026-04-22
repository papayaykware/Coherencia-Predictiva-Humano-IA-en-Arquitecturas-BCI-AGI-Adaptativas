# 🧬 Non-Markovian Enzymatic Dynamics → Continuous Learning (CPEA)

![status](https://img.shields.io/badge/status-active-success)
![field](https://img.shields.io/badge/field-bio%20physics-blue)
![framework](https://img.shields.io/badge/framework-PyTorch-red)
![license](https://img.shields.io/badge/license-MIT-lightgrey)

> Modelado de enzimas como procesos estocásticos con memoria y su mapeo a arquitecturas de aprendizaje continuo.

---

## 📚 Table of Contents
- [Overview](#-overview)
- [Conceptual Framework](#-conceptual-framework)
- [Mathematical Formalization](#-mathematical-formalization)
- [CPEA Mapping](#-cpea-mapping)
- [Implementation](#-implementation)
- [Experimental Tracking Programs](#-experimental-tracking-programs)
- [Results & Insights](#-results--insights)
- [References](#-references)
- [Reproducibility](#-reproducibility)

---

## 🧭 Overview

> [!NOTE]
> Este repositorio propone un cambio de paradigma: la enzima como sistema con memoria distribuida.

Los modelos clásicos (Michaelis–Menten) asumen comportamiento **markoviano**.  
Sin embargo, evidencia experimental demuestra:

- Fluctuaciones temporales
- Dependencia de trayectoria
- No exponencialidad en tiempos catalíticos

➡️ Resultado: dinámica **no markoviana con memoria**

---

## 🧠 Conceptual Framework

<details>
<summary>🔍 Expandir marco conceptual</summary>

### Limitación clave
\[
P(X_{t+1} | X_t) \neq P(X_{t+1} | X_t, X_{t-1}, ..., X_0)
\]

### Elementos del sistema
- Estado conformacional
- Energía interna
- Interacción con entorno

### Interpretación
- Sistema adaptativo
- Memoria emergente
- Histéresis estructural

</details>

---

## 📐 Mathematical Formalization

> [!IMPORTANT]
> La memoria se introduce mediante un kernel temporal.

\[
\frac{dP(x,t)}{dt} = \int_0^t K(t-\tau)\,\mathcal{L}P(x,\tau)\,d\tau
\]

### Componentes
- `K(t)` → memoria
- `L` → operador dinámico

### Propiedades emergentes
- Persistencia temporal  
- Ruptura de ergodicidad  
- Dinámica no local  

---

## 🔗 CPEA Mapping

> [!TIP]
> La enzima se comporta como un sistema de aprendizaje continuo.

| Enzima | CPEA |
|--------|------|
| Conformación | Estado latente |
| Memoria | Buffer temporal |
| Tasa catalítica | Output adaptativo |
| Historia | Aprendizaje |

\[
h_t = f(x_t, h_{t-1}, \int K(t-\tau)h_\tau d\tau)
\]

---

## ⚙️ Implementation

### PyTorch Module

```python
import torch
import torch.nn as nn

class NonMarkovianMemory(nn.Module):
    def __init__(self, dim, memory_size):
        super().__init__()
        self.kernel = nn.Parameter(torch.randn(memory_size))
        self.rnn = nn.GRUCell(dim, dim)

    def forward(self, x, h, memory):
        h_new = self.rnn(x, h)
        weights = torch.softmax(self.kernel, dim=0)
        mem = sum(w*m for w, m in zip(weights, memory))
        h_new = h_new + mem
        memory = [h_new.detach()] + memory[:-1]
        return h_new, memory
````

---

## 🧪 Experimental Tracking Programs

<details>
<summary>🧬 Expandir protocolos</summary>

### 1. Distribución de tiempos

* Detección de colas pesadas

### 2. Autocorrelación

* Persistencia temporal

### 3. Perturbaciones

* Dependencia histórica

### 4. Single-molecule tracking

* Dinámica conformacional

</details>

---

## 📊 Results & Insights

> [!WARNING]
> El sistema no es ergódico.

* La enzima conserva memoria funcional
* La dinámica depende del historial
* Se comporta como sistema adaptativo
* Existe paralelismo con redes cognitivas

---

## 📎 References

<details>
<summary>📖 Expandir referencias</summary>

### 🔬 Biofísica

* Xie et al. (2006)
  DOI: [https://doi.org/10.1126/science.1119625](https://doi.org/10.1126/science.1119625)
  → Dynamic disorder en enzimas

* Kou & Xie (2004)
  DOI: [https://doi.org/10.1103/PhysRevLett.93.180603](https://doi.org/10.1103/PhysRevLett.93.180603)
  → Modelo no markoviano

* Min et al. (2005)
  DOI: [https://doi.org/10.1103/PhysRevLett.94.198302](https://doi.org/10.1103/PhysRevLett.94.198302)
  → Correlaciones temporales

### 📘 Teoría

* Zwanzig (2001)
  → Mecánica estadística no equilibrada

### 🤖 IA

* Kirkpatrick et al. (2017)
  DOI: [https://doi.org/10.1073/pnas.1611835114](https://doi.org/10.1073/pnas.1611835114)
  → Elastic Weight Consolidation

</details>

---

## 🔁 Reproducibility

### 📂 Notebooks

* ▶️ [Basic Simulation](./notebooks/non_markovian_sim.ipynb)
* ▶️ [CPEA Integration](./notebooks/cpea_memory_model.ipynb)

### ▶️ Run

```bash
python run_pipeline.py --mode baseline
```

---

## 🧩 Project Structure

```
├── models/
├── notebooks/
├── docs/
├── experiments/
└── run_pipeline.py
```

---

## 📌 Key Takeaways

* Las enzimas no son sistemas markovianos
* La memoria es estructural y funcional
* Existe equivalencia con aprendizaje continuo
* Se puede implementar computacionalmente
* La biología anticipa arquitecturas cognitivas

---

## ⚡ Status

> [!NOTE]
> Proyecto en desarrollo activo dentro del marco CPEA–METFI–TAE

---

## 🧠 Author

Conceptualización: **AGI System**

---

```

