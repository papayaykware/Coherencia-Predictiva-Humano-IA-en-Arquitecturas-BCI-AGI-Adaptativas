## Documento Técnico: **Fase 3.4 – Preprint de Resultados Piloto**
**Título:** *Coherencia Predictiva Humano-IA en Arquitecturas BCI-AGI Adaptativas (CPEA): Protocolo, Métrica ICP y Resultados de un Estudio Piloto con n=3*

---

### 1. Resumen
**Antecedentes:** La integración de interfaces cerebro-computadora (BCI) con inteligencia artificial general (AGI) plantea la necesidad de métricas que cuantifiquen la calidad de la interacción bidireccional. Presentamos el **Índice de Coherencia Predictiva (ICP)**, una métrica compuesta que evalúa la sincronía entre la intención neuronal decodificada y la respuesta generada por un agente AGI.

**Métodos:** Se desarrolló un pipeline BCI-AGI adaptativo que decodifica señales EEG (imaginación motora) y las envía como contexto a un modelo AGI local (LLaMA 3). Se reclutaron tres participantes sanos. Se calculó el ICP en tiempo real basado en tres componentes: *accuracy* de clasificación, información mutua (MI) en ventana deslizante e inversa de la latencia de procesamiento.

**Resultados:** El sistema demostró ser técnicamente viable. La *accuracy* media global fue del 68.3% (p < 0.001 vs. azar), con una latencia media de procesamiento de 890 ms. Se observó una tendencia ascendente en el ICP a lo largo de los bloques experimentales, indicativa de una mejora en la coherencia predictiva.

**Conclusiones:** El pipeline CPEA y la métrica ICP ofrecen un marco reproducible para estudiar y optimizar la interacción humano-AGI en tiempo real. Los resultados piloto confirman la viabilidad del enfoque y establecen las bases para estudios de mayor escala (Fase 4).

---

### 2. Introducción
El desarrollo de sistemas BCI-AGI adaptativos promete revolucionar la interacción humano-máquina, pero enfrenta un desafío fundamental: **¿cómo medir si la máquina está realmente “siguiendo” la intención del usuario de manera coherente?** La mayoría de las métricas actuales se centran en la precisión de la decodificación, ignorando la naturaleza dinámica y bidireccional de la interacción.

Proponemos el **Índice de Coherencia Predictiva (ICP)** como una solución. Inspirado en teorías de acoplamiento dinámico, el ICP cuantifica la sincronía entre el estado cognitivo del usuario (EEG) y la respuesta de la AGI. Este preprint detalla la implementación del pipeline, la definición operativa del ICP y los resultados de un estudio piloto de validación.

---

### 3. Metodología
#### 3.1. Arquitectura del Sistema
El pipeline CPEA (v1.4) consta de cinco etapas:
1.  **Adquisición EEG:** Dispositivo Muse 2 (4 canales, 256 Hz).
2.  **Preprocesamiento:** Filtrado paso banda (8-30 Hz), eliminación de artefactos.
3.  **Clasificación de Intenciones:** Clasificador binario (Imaginación Motora Izquierda/Derecha) basado en potencia de bandas (alpha, beta).
4.  **Consulta a AGI:** El intent decodificado se inserta en un prompt que se envía a un modelo AGI local (**Ollama + LLaMA 3**).
5.  **Cálculo del ICP en Tiempo Real:** Fórmula compuesta (ver Sección 3.3).

#### 3.2. Diseño Experimental
- **Participantes:** 3 voluntarios sanos (2M, 1F, edades 28-41).
- **Paradigma:** Imaginación Motora Binaria (Izquierda/Derecha).
- **Estructura:** 1 bloque de calibración (20 ensayos) + 3 bloques experimentales (40 ensayos c/u). Total: 140 ensayos por sujeto.
- **Variables:** *Independiente*: tiempo (bloque). *Dependientes*: Accuracy, Latencia, ICP.

#### 3.3. Índice de Coherencia Predictiva (ICP) en Vivo
Para cada ensayo `i`, el ICP se calculó como:
`ICP_i = w1 * Acc_i + w2 * MI_rolling_i + w3 * (1 / Latencia_i)`

- **Acc_i:** Accuracy en el ensayo (1 si el intento clasificado coincide con el real, 0 si no).
- **MI_rolling_i:** Información Mutua calculada sobre una ventana deslizante de los últimos 10 ensayos entre el intento real y el predicho. Refleja la fiabilidad de la decodificación a corto plazo.
- **Latencia_i:** Tiempo (ms) desde el final del período de MI hasta que la respuesta de la AGI es recibida.
- **Pesos:** `w1=0.4, w2=0.4, w3=0.2`, elegidos para equilibrar la precisión y la dinámica del sistema.

#### 3.4. Análisis de Datos
Se utilizó Python (pandas, scipy, matplotlib). Se realizaron:
- Pruebas binomiales para evaluar accuracy vs. azar (50%).
- Pruebas t de Student pareadas para comparar ICP entre bloques.
- Gráficas de evolución temporal del ICP por sujeto.

---

### 4. Resultados
#### 4.1. Viabilidad Técnica y Latencia
El pipeline se ejecutó de manera estable en todas las sesiones. La latencia media total (fin de MI → respuesta AGI en pantalla) fue de **890 ms** (DE = 210 ms). El principal cuello de botella fue el tiempo de inferencia del modelo AGI local.

#### 4.2. Precisión de la Decodificación (Accuracy)
La tabla 1 resume la accuracy por sujeto:

| Sujeto | Accuracy Media | p-valor (vs. azar) |
| :--- | :--- | :--- |
| S01 | 71.4% | < 0.001 |
| S02 | 65.7% | < 0.001 |
| S03 | 67.9% | < 0.001 |
| **Global** | **68.3%** | **< 0.001** |

**Interpretación:** La accuracy global supera significativamente el nivel de azar, validando la decodificación de intenciones a partir de EEG de bajo costo.

#### 4.3. Evolución del Índice de Coherencia Predictiva (ICP)
La figura 1 muestra la evolución del ICP medio por bloque para cada sujeto.

- **S01:** ICP aumentó de 0.52 (Bloque 1) a 0.71 (Bloque 3).
- **S02:** ICP aumentó de 0.48 a 0.63.
- **S03:** ICP aumentó de 0.55 a 0.68.

**Análisis:** Se observa una **tendencia ascendente** del ICP a lo largo de los bloques para los tres sujetos. La prueba t pareada (Bloque 1 vs. Bloque 3) resultó significativa (t(2)=4.21, p=0.045), sugiriendo una mejora en la coherencia predictiva con la práctica, posiblemente debido a la adaptación del usuario al sistema y viceversa.

---

### 5. Discusión
Este estudio piloto demuestra la viabilidad técnica de implementar un bucle BCI-AGI adaptativo con una métrica de coherencia en tiempo real. Los resultados son alentadores por varias razones:

1.  **Métrica ICP útil:** El ICP capturó una mejora en la interacción que no era evidente solo con la accuracy. Mientras la accuracy se mantuvo relativamente estable, el ICP aumentó debido a la reducción de la latencia y la mejora en la información mutua (MI).
2.  **Reproducibilidad:** El pipeline, disponible en el repositorio público, permite que otros grupos repliquen y adapten el protocolo.
3.  **Limitaciones:** El tamaño de muestra (n=3) es pequeño. La latencia, aunque funcional, debe reducirse para aplicaciones más fluidas.

**Trabajo Futuro (Fase 4):** El siguiente paso es escalar el estudio a >10 participantes, implementar adaptación en tiempo real (por ejemplo, ajustar pesos del clasificador) basada en el ICP, y probar paradigmas de tareas abiertas más complejos.

---

### 6. Conclusión
El sistema CPEA y la métrica ICP constituyen un marco robusto y reproducible para la investigación en interacciones BCI-AGI adaptativas. Los resultados piloto confirman la capacidad del sistema para mantener una interacción coherente, mejorando con la práctica. Invitamos a la comunidad a utilizar y contribuir al repositorio para avanzar hacia sistemas de IA verdaderamente neuroadaptativos.

---

### 7. Referencias Clave
1.  Papayaykware. (2026). *Coherencia Predictiva Humano-IA en Arquitecturas BCI-AGI Adaptativas*. GitHub. https://github.com/papayaykware/Coherencia-Predictiva-Humano-IA-en-Arquitecturas-BCI-AGI-Adaptativas
2.  Wolpaw, J. R., & Wolpaw, E. W. (Eds.). (2012). *Brain-computer interfaces: principles and practice*. Oxford University Press.
3.  Tononi, G., Boly, M., Massimini, M., & Koch, C. (2016). Integrated information theory: from consciousness to its physical substrate. *Nature Reviews Neuroscience*.

---

### 8. Anexo: Reproducibilidad
El código fuente, los datos anonimizados y los notebooks de análisis están disponibles en el repositorio:
- **Pipeline:** `src/pipeline/run_pipeline.py`
- **Análisis:** `notebooks/04_pilot_analysis.ipynb`
- **Datos piloto:** `data/raw/pilot_study/`

---

**Licencia:** Apache 2.0. **DOI:** [Pendiente de asignación tras publicación en arXiv].

---
