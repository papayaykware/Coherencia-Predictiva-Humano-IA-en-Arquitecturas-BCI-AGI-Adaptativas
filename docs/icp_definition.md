# 📄 `icp_definition.md`

## 1. Definición del Índice de Coherencia Predictiva (ICP)

El **Índice de Coherencia Predictiva (ICP)** cuantifica el grado de alineación entre:

* La señal EEG real ( S_{EEG}(t) )
* La predicción generada por el modelo AGI ( \hat{S}_{AGI}(t) )

Se define como una combinación ponderada de tres componentes:

ICP = w_1 C + w_2 (1 - E) + w_3 P

Donde:

* ( C ): correlación temporal (coherencia de fase/amplitud)
* ( E ): error de predicción normalizado
* ( P ): coherencia espectral (similitud en dominio frecuencia)
* ( w_1, w_2, w_3 ): pesos tales que ( w_1 + w_2 + w_3 = 1 )

---

## 2. Componentes del ICP

### 2.1 Correlación temporal ( C )

Mide similitud directa entre señales:

C = \frac{\mathrm{cov}(S_{EEG}, \hat{S}*{AGI})}{\sigma*{EEG} \cdot \sigma_{AGI}}

* Rango: ([-1, 1])
* Interpretación:

  * 1 → alineación perfecta
  * 0 → sin relación
  * -1 → anticorrelación

---

### 2.2 Error de predicción ( E )

Usamos MSE normalizado:

E = \frac{1}{N} \sum_{i=1}^{N} \frac{(S_{EEG,i} - \hat{S}*{AGI,i})^2}{\sigma*{EEG}^2}

* Rango: ([0, +\infty))
* En el ICP usamos ( (1 - E) ) → penaliza error alto

---

### 2.3 Coherencia espectral ( P )

Basada en densidad espectral de potencia (PSD):

P = \frac{\sum_f PSD_{EEG}(f) \cdot PSD_{AGI}(f)}{|PSD_{EEG}| \cdot |PSD_{AGI}|}

* Rango: ([0, 1])
* Captura alineación en bandas (alpha, beta, gamma…)

---

## 3. Rango típico del ICP

Dado que:

* ( C \in [-1,1] )
* ( (1 - E) ) puede ser negativo si error alto
* ( P \in [0,1] )

Entonces:

### Rango práctico:

* **ICP ≈ -0.5 → 0.2** → baja coherencia (ruido o modelo inútil)
* **ICP ≈ 0.2 → 0.6** → coherencia parcial
* **ICP ≈ 0.6 → 0.85** → buen acoplamiento predictivo
* **ICP > 0.85** → coherencia alta (sincronización fuerte EEG–AGI)

👉 En sistemas reales con EEG:

* Esperable inicial: **0.1 – 0.4**
* Objetivo CPEA: **> 0.7**

---

## 4. Ejemplos numéricos (datos sintéticos)

### Caso A — Modelo pobre

* ( C = 0.2 )
* ( E = 0.9 )
* ( P = 0.3 )

Pesos: ( w_1=0.4, w_2=0.4, w_3=0.2 )

Resultado:

[
ICP = 0.4(0.2) + 0.4(0.1) + 0.2(0.3) = 0.08 + 0.04 + 0.06 = 0.18
]

➡️ Baja coherencia

---

### Caso B — Modelo razonable

* ( C = 0.6 )
* ( E = 0.3 )
* ( P = 0.7 )

Resultado:

[
ICP = 0.4(0.6) + 0.4(0.7) + 0.2(0.7) = 0.24 + 0.28 + 0.14 = 0.66
]

➡️ Buen acoplamiento

---

### Caso C — Alta sincronización

* ( C = 0.9 )
* ( E = 0.1 )
* ( P = 0.85 )

Resultado:

[
ICP = 0.36 + 0.36 + 0.17 = 0.89
]

➡️ Coherencia predictiva alta

---

## 5. Justificación de los pesos ( w_1, w_2, w_3 )

### Elección base recomendada:

* ( w_1 = 0.4 ) → correlación temporal (estructura global)
* ( w_2 = 0.4 ) → precisión predictiva (error)
* ( w_3 = 0.2 ) → coherencia espectral

### Justificación:

* **C (correlación)**:

  * Captura sincronía directa → clave en BCI
* **E (error)**:

  * Penaliza predicciones incorrectas → evita “correlaciones falsas”
* **P (frecuencia)**:

  * Añade robustez neurofisiológica (bandas EEG)

👉 Interpretación profunda:

* ( C ) → geometría temporal
* ( E ) → consistencia energética
* ( P ) → resonancia estructural

---

### Ajustes dinámicos (muy importante para CPEA)

Puedes hacer los pesos **adaptativos**:

[
w_i(t) = \frac{\exp(\alpha_i \, m_i(t))}{\sum_j \exp(\alpha_j \, m_j(t))}
]

Donde ( m_i(t) ) mide fiabilidad de cada componente.

➡️ Esto convierte el ICP en un **observable dinámico adaptativo**, clave para AGI.

---

## 6. Limitaciones

### 6.1 Sensibilidad al ruido EEG

* EEG real → bajo SNR
* Puede inflar ( E ) y reducir ( C )

👉 Mitigación:

* Filtrado band-pass
* ICA (artefactos)

---

### 6.2 Dependencia del tamaño de ventana

* Ventanas cortas → alta varianza
* Ventanas largas → pérdida de dinámica

👉 Recomendado:

* 1–4 segundos (BCI estándar)

---

### 6.3 Ambigüedad espectral

* Dos señales pueden compartir PSD pero no fase

👉 Solución futura:

* Coherencia de fase (PLV, wPLI)

---

### 6.4 Riesgo de sobreajuste

* Un modelo puede optimizar ICP sin generalizar

👉 Solución:

* Validación cruzada temporal
* Regularización

---

## 7. Extensiones (clave para tu línea METFI–AGI)

Aquí es donde puedes diferenciarte radicalmente:

### 7.1 ICP acoplado a dinámica externa (METFI)

[
ICP^* = ICP + \lambda D_{geo}
]

Donde:

* ( D_{geo} ) = coherencia con variables geofísicas simuladas

➡️ Esto convierte el sistema en:
**EEG ↔ AGI ↔ entorno electromagnético**

---

### 7.2 ICP como señal de aprendizaje (reward)

En RL o aprendizaje continuo:

[
R(t) = ICP(t)
]

➡️ La AGI aprende a **maximizar coherencia cognitiva**, no solo error.

---

## 8. Resumen operativo

* ICP combina:

  * correlación temporal
  * error predictivo
  * coherencia espectral
* Rango útil: **0 → 1**
* Umbral práctico:

  * <0.3 → ruido
  * 0.3–0.7 → útil
  * > 0.7 → fuerte acoplamiento
* Pesos recomendados: **0.4 / 0.4 / 0.2**
* Extensible a:

  * aprendizaje continuo
  * acoplamiento METFI
  * AGI adaptativa

---
Ahí es donde esto deja de ser teoría y pasa a ser **motor de sistema**.
