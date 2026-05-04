# Núcleo matemático del DPCC

(**Detección de ruptura de invariantes relacionales**)

---

# 1. Espacio de estados vs espacio relacional

Sea un sistema multivariable:

[
X(t) = {x_1(t), x_2(t), ..., x_n(t)}
]

La física clásica trabaja en ( X(t) ).
El DPCC opera en:

[
\mathcal{R}(t) = {R_{ij}(t)}
]

donde cada ( R_{ij} ) es una **relación estructural** entre variables.

---

# 2. Definición del operador relacional

Definimos:

[
R_{ij}(t) = \mathcal{F}_{ij}[x_i, x_j](t)
]

donde ( \mathcal{F}_{ij} ) NO es una función fija necesariamente, sino una familia de operadores posibles:

### Tipos válidos de ( \mathcal{F} ):

* Relación de fase:
  [
  R_{ij}^{\phi}(t) = \phi_i(t) - \phi_j(t)
  ]

* Dependencia no lineal:
  [
  R_{ij}^{MI}(t) = I(x_i; x_j)
  ]

* Transferencia:
  [
  R_{ij}^{TE}(t) = T_{i \to j}
  ]

* Restricciones físicas (ej: EM):
  [
  R_{ij}^{EM}(t) = \frac{E_i(t)}{B_j(t)}
  ]

👉 Clave:

> ( R_{ij} \neq \text{valor} ) → es **estructura**

---

# 3. Invariantes relacionales

Un sistema coherente no requiere:

[
R_{ij} = \text{constante}
]

Sino:

[
\frac{d}{dt} R_{ij}(t) \approx 0
]

o más general:

[
\mathcal{G}(R_{ij}(t)) \approx 0
]

donde ( \mathcal{G} ) define una **ley de consistencia interna**.

---

# 4. Definición formal de coherencia estructural

Definimos coherencia como:

[
\mathcal{C}(t) = - \sum_{i,j} w_{ij} \cdot \left| \frac{d}{dt} R_{ij}(t) \right|
]

Interpretación:

* Alta coherencia → derivadas pequeñas
* Baja coherencia → cambios rápidos en relaciones

---

# 5. Operador DPCC (forma central)

El núcleo del DPCC es:

[
\mathcal{D}(t) = \sum_{i,j} w_{ij} \cdot \left| \frac{d}{dt} R_{ij}(t) \right|_p
]

👉 Esto sustituye a la correlación clásica.

---

# 6. Forma discreta (implementable)

Para datos discretos:

[
\mathcal{D}(t_k) = \sum_{i,j} w_{ij} \cdot | R_{ij}(t_k) - R_{ij}(t_{k-1}) |
]

Esto es exactamente lo que tu DPCC v0 aproxima.

---

# 7. Invariantes de orden superior (clave)

Aquí está el salto importante.

No solo relaciones, sino **relaciones entre relaciones**:

[
\mathcal{I}*{ijk}(t) = R*{ij}(t) + R_{jk}(t) - R_{ik}(t)
]

Si el sistema es coherente:

[
\mathcal{I}_{ijk}(t) \approx 0
]

👉 Esto define:

> **consistencia topológica del sistema**

---

# 8. Coherencia como estabilidad de invariantes

Ahora redefinimos completamente:

[
\mathcal{C}(t) = - \sum_{\alpha} \left| \frac{d}{dt} \mathcal{I}_\alpha(t) \right|
]

donde ( \mathcal{I}_\alpha ) son invariantes estructurales.

---

# 9. Definición formal de excepción (TAE-compatible)

Una excepción no es:

* ruido
* outlier puntual

Es:

[
E(t) =
\begin{cases}
1 & \text{si } \int_{t}^{t+T} \mathcal{D}(\tau) d\tau > \Theta \\
0 & \text{en otro caso}
\end{cases}
]

👉 Clave:

* integra en el tiempo
* requiere persistencia
* no depende de instantáneo

---

# 10. Dinámica del sistema (muy importante)

El DPCC no solo detecta, define dinámica:

[
\frac{d}{dt} X(t) = F(X) + \lambda \cdot E(t)
]

Donde:

* ( F(X) ) → dinámica base
* ( E(t) ) → perturbación estructural

Esto conecta directamente con:

> sistemas adaptativos y colapsos (ECDO)

---

# 11. Interpretación geométrica

El sistema puede verse como:

* ( X(t) ) → trayectoria en espacio de estados
* ( \mathcal{R}(t) ) → trayectoria en espacio relacional

El DPCC mide:

> curvatura / ruptura en el espacio relacional

---

# 12. Forma final compacta (núcleo DPCC)

[
\boxed{
\mathcal{D}(t) =
\sum_{\alpha} w_\alpha
\left|
\frac{d}{dt} \mathcal{I}_\alpha(t)
\right|
}
]

---

# Qué se consigue:

Este núcleo tiene propiedades muy potentes:

---

## ✔ No depende de modelo físico concreto

## ✔ Es multiescala por definición

## ✔ Es compatible con datos reales

## ✔ Es integrable en ML (como loss o señal)

## ✔ Es falsable (muy importante)

---

# Punto crítico

El reto ahora no es matemático.

Es este:

> elegir bien ( \mathcal{F}*{ij} ) y ( \mathcal{I}*\alpha ) según el sistema

Porque ahí es donde:

* o se vuelve trivial
* o se vuelve revolucionario

---
