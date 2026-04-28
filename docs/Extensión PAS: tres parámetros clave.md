# 1. Definición: nodo PAS dentro de CPEA

En CPEA, cada nodo i es un sistema predictivo que minimiza error:

* Estado interno: ( h_i(t) )
* Entrada: ( x_i(t) )
* Predicción: ( \hat{x}_i(t) = f(h_i(t)) )
* Error: ( \epsilon_i(t) = x_i(t) - \hat{x}_i(t) )

---

## Extensión PAS: tres parámetros clave

Introducimos un vector de rasgos PAS por nodo:

[
\Theta_i^{PAS} = { \alpha_i, \beta_i, \tau_i }
]

Donde:

### 1. Sensibilidad al error ((\alpha_i))

Amplifica la señal de error:

[
\tilde{\epsilon}_i(t) = \alpha_i \cdot \epsilon_i(t)
]

* PAS: ( \alpha_i \gg 1 )
* No-PAS: ( \alpha_i \approx 1 )

---

### 2. Peso de actualización ((\beta_i))

Controla cuánto impacta el error en el estado:

[
h_i(t+1) = h_i(t) + \beta_i \cdot \tilde{\epsilon}_i(t)
]

* PAS: mayor ajuste por unidad de error
* Riesgo: inestabilidad

---

### 3. Constante de integración temporal ((\tau_i))

Introduce memoria extendida:

[
h_i(t+1) = (1 - \frac{1}{\tau_i}) h_i(t) + \frac{1}{\tau_i} \cdot \beta_i \tilde{\epsilon}_i(t)
]

* PAS: ( \tau_i \uparrow ) (integra más historia)
* No-PAS: menor memoria efectiva

---

# 2. Dinámica de red CPEA con nodos PAS

Ahora incorporamos interacción entre nodos.

## Acoplamiento:

[
x_i(t) = s_i(t) + \sum_{j} W_{ij} \cdot h_j(t) + \eta_i(t)
]

Donde:

* ( s_i(t) ): input externo
* ( W_{ij} ): conectividad
* ( \eta_i(t) ): ruido

---

## Error modulado por red

[
\epsilon_i(t) = x_i(t) - f(h_i(t))
]

pero ahora:

[
x_i(t) \text{ contiene información de otros nodos}
]

---

# 3. Función global (energía libre CPEA extendida)

Definimos:

[
\mathcal{F} = \sum_i \alpha_i \cdot \epsilon_i(t)^2 + \lambda \sum_{i,j} W_{ij} \cdot (h_i - h_j)^2
]

Interpretación:

* Primer término: precisión local (amplificada en PAS)
* Segundo término: coherencia global

---

# 4. Emergencia del “demonio colectivo”

Introducimos un operador global no local:

## Sorpresa local:

[
S_i(t) = -\log P(\epsilon_i(t))
]

## Redundancia:

[
R_i(t) = \sum_j I(h_i, h_j)
]

---

## Peso dinámico del nodo:

[
\omega_i(t) = \frac{S_i(t)}{R_i(t) + \delta}
]

---

## Modulación de conectividad:

[
W_{ij}(t+1) = W_{ij}(t) + \gamma \cdot \omega_i(t) \cdot h_i(t) \cdot h_j(t)
]

---

### Interpretación

* Nodos con alta sorpresa y baja redundancia → ganan influencia
* Nodos redundantes → pierden peso
* La red se reorganiza dinámicamente

Esto es tu “demonio” en forma matemática.

---

# 5. Papel específico del nodo PAS en esta dinámica

Sustituyendo:

[
S_i(t) \propto \alpha_i \cdot \epsilon_i(t)^2
]

Entonces:

* PAS → mayor ( S_i )
* → mayor ( \omega_i )
* → mayor influencia en la red

---

## Resultado emergente

Un nodo PAS:

* Detecta antes desviaciones
* Influye más en la reconfiguración global
* Puede acelerar la convergencia… o desestabilizarla

---

# 6. Condiciones de estabilidad

Aquí está el punto fino del modelo:

Para evitar explosión dinámica:

[
\alpha_i \cdot \beta_i < C
]

y

[
\frac{\alpha_i}{\tau_i} < K
]

Donde C y K dependen de:

* conectividad media
* nivel de ruido
* tamaño de red

---

## Régimenes del sistema

### 1. Subcrítico

* Baja sensibilidad
* Baja adaptación
* Red rígida

### 2. Crítico (óptimo)

* PAS moderados
* Alta coherencia
* Máxima transferencia de información

### 3. Supercrítico

* PAS altos sin regulación
* Caos dinámico
* Falsas correlaciones

---

# 7. Predicciones testables

Este modelo permite predicciones claras:

### A nivel individual (EEG)

* PAS → mayor varianza en error predictivo
* Mayor coherencia en condiciones estructuradas
* Mayor colapso bajo ruido

---

### A nivel red

* Inclusión de nodos PAS:

  * ↓ tiempo de sincronización
  * ↑ sensibilidad global
  * ↑ riesgo de inestabilidad

---

### A nivel “demonio colectivo”

* PAS facilitan su emergencia
* Pero no lo constituyen
* Actúan como sensores de gradiente informacional

---

# 8. Forma compacta del modelo

Sistema completo:

[
\tilde{\epsilon}_i = \alpha_i (x_i - f(h_i))
]

[
h_i(t+1) = (1 - \frac{1}{\tau_i}) h_i(t) + \frac{\beta_i}{\tau_i} \tilde{\epsilon}_i
]

[
\omega_i = \frac{-\log P(\epsilon_i)}{\sum_j I(h_i,h_j)}
]

[
W_{ij}(t+1) = W_{ij}(t) + \gamma \cdot \omega_i h_i h_j
]

---

# 9. Lectura conceptual final

Has convertido PAS en:

> Un parámetro de precisión adaptativa dentro de un sistema de inferencia distribuida.

Y eso encaja perfectamente con:

* CPEA → coherencia global
* TAE → aprendizaje por excepción
* Demonio colectivo → redistribución emergente

---
