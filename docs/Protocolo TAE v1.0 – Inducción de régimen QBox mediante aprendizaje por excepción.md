# Protocolo TAE v1.0 – Inducción de régimen QBox mediante aprendizaje por excepción

**Duración total por sesión:** 45 minutos  
**Número de ensayos:** 240  
**Sujetos:** 100 (previstos en el experimento principal)  
**Sincronización:** Reloj atómico + triggers TTL en todos los sensores (MEG, NV, rubidio)

---

## 📋 Resumen del protocolo

El sujeto realiza una tarea de **predicción de secuencias sensoriales** (visuales y auditivas) mientras se registra su actividad cerebral y el campo toroidal terrestre. Periódicamente se introducen **excepciones** (estímulos que violan el patrón aprendido). La hipótesis es que durante las ventanas posteriores a la excepción, el sistema entra en un régimen de hiperdecoherencia (QBox) que se manifiesta como violaciones de la desigualdad de Leggett-Garg.

---

## 🧠 Estructura de un ensayo individual

Cada ensayo dura **5200 ms** y consta de 5 fases:

| Fase | Duración | Evento | Señal |
|------|----------|--------|-------|
| **1. Línea base** | 1000 ms | Pantalla negra, silencio. Se registra actividad espontánea. | Ninguna |
| **2. Secuencia causal (entrenamiento)** | 3000 ms | Presentación de 3 estímulos (A → B → C) con intervalos fijos. | Visual + auditivo |
| **3. Intervalo de predicción** | 500 ms | El sujeto debe predecir el siguiente estímulo presionando un botón (izquierda/derecha). | Respuesta motora |
| **4. Excepción (solo en ensayos críticos)** | 200 ms | Estímulo que viola la regla causal esperada. | Visual o auditivo |
| **5. Post-excepción / relajación** | 500 ms | Pantalla negra, silencio. Se registra la ventana QBox candidata. | Ninguna |

### Diagrama temporal del ensayo (escala en ms)

```
0        1000     1500     2000     2500     3000     3500     4000     4500     5000     5200
|--------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
BASE     A        B        C        PRED     (EXCEP)  POST     (RELAX)
         (vis)    (aud)    (vis)             opcional
```

**Leyenda:**
- A, B, C: estímulos de entrenamiento (secuencia causal fija)
- PRED: ventana de predicción (sujeto responde)
- EXCEP: estímulo excepcional (solo en 50% de los ensayos)
- POST: ventana crítica donde se espera el régimen QBox
- RELAX: tiempo muerto para retornar a línea base

---

## 🎯 Tipos de ensayos (4 condiciones)

| Tipo | Secuencia causal | ¿Excepción? | Probabilidad | Objetivo |
|------|----------------|-------------|--------------|----------|
| **Estándar** | A→B→C | No | 40% | Mantener el modelo predictivo |
| **Excepción visual** | A→B→C | Sí (estímulo D visual, incongruente) | 25% | Inducir QBox vía sistema visual |
| **Excepción auditiva** | A→B→C | Sí (sonido E, incongruente) | 25% | Inducir QBox vía sistema auditivo |
| **Excepción doble** | A→B→C | Sí (D visual + E auditivo, simultáneos) | 10% | Máxima violación predictiva |

**Contrabalanceo:** Los tipos de ensayo se presentan en orden aleatorio, con la restricción de que no haya más de 3 ensayos estándar seguidos.

---

## ⏱️ Tiempos exactos de estímulos (modo causal estándar)

### Estímulo A (visual)
- **Tipo:** Círculo rojo en pantalla (diámetro 5° de ángulo visual)
- **Duración:** 100 ms
- **Inicio:** 1000 ms desde el inicio del ensayo
- **Offset:** 1100 ms

### Estímulo B (auditivo)
- **Tipo:** Tono puro de 1000 Hz, 70 dB SPL
- **Duración:** 100 ms
- **Inicio:** 1500 ms
- **Offset:** 1600 ms

### Estímulo C (visual)
- **Tipo:** Cuadrado azul (5° lado)
- **Duración:** 100 ms
- **Inicio:** 2000 ms
- **Offset:** 2100 ms

### Intervalo de predicción
- **Inicio:** 2500 ms
- **Fin:** 3000 ms (el sujeto puede responder en cualquier momento dentro de esta ventana)
- **Respuesta esperada:** Botón izquierdo si cree que el siguiente estímulo será igual a A; botón derecho si será igual a B.

---

## ⚡ Excepciones (estímulos que violan la regla)

### Excepción visual D
- **Tipo:** Triángulo verde (5° base, 5° altura)
- **Duración:** 100 ms
- **Inicio:** 2600 ms (justo antes de la predicción, para maximizar la sorpresa)
- **Offset:** 2700 ms
- **Regla violada:** El sujeto esperaba A o B, pero aparece un triángulo verde (nunca visto en entrenamiento).

### Excepción auditiva E
- **Tipo:** Ruido blanco filtrado (banda 2000-4000 Hz), 70 dB SPL
- **Duración:** 100 ms
- **Inicio:** 2600 ms
- **Offset:** 2700 ms

### Excepción doble (D + E simultáneos)
- **Inicio:** 2600 ms
- **Duración:** 100 ms
- **Observación:** Ambos estímulos comienzan y terminan al mismo tiempo.

---

## 🧪 Ventana de registro QBox (post-excepción)

**Inicio:** 3000 ms (justo después del intervalo de predicción)  
**Fin:** 3500 ms (500 ms de duración)  
**Lo que se registra con alta resolución:**
- Tensor `Q_{ijkl}(t)` con 1000 muestras (cada 0.5 ms)
- Fase toroidal cerebral (derivada de MEG)
- Fase toroidal terrestre (derivada de magnetómetro de rubidio)
- Respuesta galvánica de la piel (GSR) como medida de arousal

**Por qué 500 ms:** Es la ventana típica en la que aparece la "onda de sorpresa" (P300) y los fenómenos de reorientación atencional. Según nuestra hipótesis, es también donde la hiperdecoherencia alcanza su máximo.

---

## 📊 Entrenamiento y familiarización (sesión previa de 20 min)

Antes del experimento principal, el sujeto realiza 3 bloques de entrenamiento con **retroalimentación**:

| Bloque | Nº ensayos | Tipo | Retroalimentación |
|--------|------------|------|-------------------|
| 1 | 20 | Estándar (sin excepciones) | Visual: "Correcto"/"Incorrecto" |
| 2 | 20 | Mixto (50% excepciones) | Visual + tono de error |
| 3 | 20 | Igual que bloque 2 | Sin retroalimentación (para habituar al sujeto al silencio post-error) |

**Criterio de éxito:** Precisión >80% en ensayos estándar del bloque 3. Si no lo alcanza, se repite el bloque 2.

---

## 🧠 Variables dependientes (medidas durante el ensayo)

| Variable | Sensor | Unidad | Ventana de interés |
|----------|--------|--------|--------------------|
| Coherencia predictiva | EEG-AGI | % de aciertos en predicción | 2500-3000 ms |
| Fase toroidal cerebral | MEG (SQUID) | radianes | 3000-3500 ms (post-excepción) |
| δ_QBox (violación LG) | Cálculo en tiempo real | adimensional | 3000-3500 ms |
| Pérdida de simetría toroidal (METFI) | Magnetómetro rubidio | índice 0-1 | 3000-3500 ms |
| Respuesta galvánica | Electrodo GSR | microsiemens | 2500-3500 ms |
| Pupilometría (opcional) | Eye tracker | diámetro pupilar | 1000-3500 ms |

---

## 🎲 Algoritmo de selección de excepciones en tiempo real (basado en TAE)

El sistema decide en cada ensayo si presentar excepción o no, basándose en el **estado de coherencia predictiva del sujeto**:

```python
umbral_aciertos_recientes = 0.7  # 70% de aciertos en últimos 10 ensayos
ventana_deslizante = 10

if coherencia_predictiva(ultimos_10_ensayos) > umbral_aciertos_recientes:
    # El sujeto está aprendiendo → aplicar excepción
    probabilidad_excepcion = 0.8
else:
    # El sujeto está confundido → darle ensayos estándar para reestabilizar
    probabilidad_excepcion = 0.2

# Luego elegir tipo de excepción según la fase toroidal cerebral actual
fase = get_fase_toroidal_cerebral()  # valor entre -π y π
if abs(fase) < 0.5:
    tipo = 'visual'
elif abs(fase) < 1.0:
    tipo = 'auditiva'
else:
    tipo = 'doble'
```

Este bucle de retroalimentación implementa el **aprendizaje por excepción** (TAE) puro: el sistema fuerza la entrada en régimen QBox exactamente cuando el sujeto está más preparado para violar sus predicciones.

---

## 📈 Análisis propuesto para detectar régimen QBox

Para cada sujeto y cada ensayo con excepción:

1. Extraer la ventana post-excepción (3000-3500 ms).
2. Calcular el tensor `Q_{ijkl}(t)` para los 306 canales MEG, 4 centros NV, 3 ejes rubidio y 2 polarizaciones → reducimos por promediado a canales "macro" (por ejemplo, promediando sobre regiones cerebrales).
3. Aplicar la red neuronal DPCC preentrenada para obtener `p_qbox` y `delta_LG`.
4. Si `p_qbox > 0.95` y `delta_LG > 0.5` durante al menos 10 ms consecutivos, marcar esa ventana como **régimen QBox confirmado**.

**Hipótesis nula:** La proporción de ventanas QBox confirmadas en ensayos con excepción no es diferente de la proporción en ensayos estándar (control).  
**Hipótesis alternativa:** Hay una proporción significativamente mayor de ventanas QBox tras excepciones (prueba χ², p < 0.001).

---

## 🧪 Ejemplo de ejecución de un ensayo excepcional

```
Tiempo (ms) | Evento                                    | Registro
0           | Pantalla negra, silencio                  | Baseline EEG
1000        | Círculo rojo (100 ms)                     | Trigger TTL #1
1500        | Tono 1000 Hz (100 ms)                     | Trigger TTL #2
2000        | Cuadrado azul (100 ms)                    | Trigger TTL #3
2500        | Ventana de predicción abierta              | Sujeto responde (bt)
2600        | **Excepción visual: triángulo verde**      | Trigger TTL #4
2700        | Fin excepción                              | 
3000        | Inicio ventana QBox                        | Inicio registro alta res
3500        | Fin ventana QBox                           | Fin registro alta res
5200        | Fin del ensayo                             | 
```

---

## 📋 Check-list para implementación en laboratorio

- [ ] Programación en Psychopy o Presentation de los estímulos con tiempos exactos.
- [ ] Sincronización de triggers TTL con MEG, NV, rubidio y GSR.
- [ ] Implementación del algoritmo adaptativo de selección de excepciones.
- [ ] Entrenamiento de la red DPCC con datos sintéticos (simulador QBox).
- [ ] Prueba piloto con 10 sujetos para ajustar umbrales de coherencia predictiva.
- [ ] Aprobación del comité de ética (riesgo mínimo, consentimiento informado detallando las excepciones sensoriales).

---

## 🔗 Conexión con el simulador QBox

Los datos generados por este protocolo (con sujetos reales) se pueden usar para **reentrenar** o **fine-tunear** la red neuronal DPCC. En concreto, las ventanas post-excepción que resulten en `p_qbox > 0.95` se pueden añadir al dataset como ejemplos reales de régimen QBox. Esto cerraría el ciclo:  
**Simulador → entrenamiento DPCC → experimento TAE → detección QBox real → mejora del simulador.**

---
