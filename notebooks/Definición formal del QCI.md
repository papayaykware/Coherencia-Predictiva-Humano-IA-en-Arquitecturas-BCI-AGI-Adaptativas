# 🧠 1. Definición formal del QCI

Partimos de tu módulo:

* grafo de correlación ( A )
* valores propios ( \lambda_i )

Entonces definimos:

### 🔹 Densidad estructural

[
\rho = \frac{\sum A_{ij}}{N^2}
]

### 🔹 Entropía espectral

[
H = - \sum_i |\lambda_i| \log(|\lambda_i| + \epsilon)
]

### 🔹 Índice de Cuasi-Coherencia

[
QCI = \frac{\rho}{H + \epsilon}
]

QCI = \frac{\rho}{H + \epsilon}

---

# 2. Ejemplo numérico (interpretación realista)

Supongamos que tras procesar EEG obtienes:

* Matriz de adyacencia de 100 nodos
* Total de conexiones: 4200

### 🔹 Paso 1: densidad

[
\rho = \frac{4200}{100^2} = 0.42
]

---

### 🔹 Paso 2: espectro

Valores propios (simplificado):

[
\lambda = [3.2,\ 2.1,\ 1.5,\ 0.9,\ 0.3,\ ...]
]

Calculamos:

[
H \approx 4.8
]

---

### 🔹 Paso 3: QCI

[
QCI = \frac{0.42}{4.8} \approx 0.0875
]

---

# 3. Interpretación (esto es lo importante)

El valor en sí no significa nada aislado. Importa el régimen:

| QCI             | Interpretación                                    |
| --------------- | ------------------------------------------------- |
| **< 0.05**      | Ruido / incoherencia                              |
| **0.05 – 0.15** | Estructura débil (estado basal típico)            |
| **0.15 – 0.35** | Coherencia significativa                          |
| **> 0.35**      | Alta organización (estado crítico o foco extremo) |

👉 En el ejemplo:

**QCI ≈ 0.087 → coherencia baja-media, estado no estructurado**

---

# 4. Lectura profunda (clave para CPEA)

El QCI está capturando:

* **ρ alto** → mucha conectividad (orden local)
* **H bajo** → espectro concentrado (orden global)

👉 QCI alto =
**orden aperiódico estable (tipo cuasicristal)**

👉 QCI bajo =
**ruido o periodicidad trivial**

---

# 5. Relación directa con ICP (muy importante)

Puedes redefinir tu sistema así:

[
ICP_{extendido} = w_1 \cdot predicción + w_2 \cdot coherencia + w_3 \cdot QCI
]

ICP_{ext} = w_1 P + w_2 C + w_3 QCI

👉 Esto introduce:

* dimensión estructural (QCI)
* no solo temporal o predictiva

---

# 6. Código directo para calcularlo

```python
def compute_qci(adjacency):
    import numpy as np

    # densidad
    rho = adjacency.sum() / adjacency.size

    # espectro
    eigenvalues = np.linalg.eigvals(adjacency)
    H = -np.sum(np.abs(eigenvalues) * np.log(np.abs(eigenvalues) + 1e-8))

    QCI = rho / (H + 1e-8)

    return QCI
```

---
