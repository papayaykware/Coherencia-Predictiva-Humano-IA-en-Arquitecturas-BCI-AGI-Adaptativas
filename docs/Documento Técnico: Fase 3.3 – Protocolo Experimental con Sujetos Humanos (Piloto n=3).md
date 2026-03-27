## Documento Técnico: **Fase 3.3 – Protocolo Experimental con Sujetos Humanos (Piloto n=3)**

**Autor:** Proyecto CPEA
**Versión:** 1.0
**Fecha:** 2026-03-27
**Estado:** Listo para implementación

---

### 1. Objetivo
Ejecutar un estudio piloto con **tres (3) sujetos humanos** para validar la viabilidad del pipeline CPEA en un entorno con hardware real (EEG), demostrar la funcionalidad del **Índice de Coherencia Predictiva (ICP)** en tiempo real, y recopilar datos anonimizados para análisis post-sesión que guíen la Fase 4.

### 2. Criterios de Inclusión y Ética
- **Sujetos:** 3 voluntarios sanos (incluyendo al menos 1 investigador principal para pruebas de concepto).
- **Consentimiento Informado:** Cada sujeto firmará un formulario de consentimiento informado específico para este estudio piloto, explicando los procedimientos, la anonimización de datos y el propósito no médico de la investigación.
- **Anonimización:** Todos los datos se almacenarán con un ID de sujeto (S01, S02, S03). No se guardarán nombres, fechas de nacimiento ni ningún otro identificador personal directo. Los archivos de datos se guardarán en la carpeta `data/raw/pilot_study/` sin metadatos identificables.

### 3. Hardware y Configuración
- **Dispositivo EEG:** Se utilizará un dispositivo de grado de investigación o consumidor de alta calidad (ej., **Muse 2** o **Emotiv EPOC X**). Se documentará la configuración de impedancia y la tasa de muestreo (ej., 256 Hz).
- **Entorno:** Sala silenciosa y con iluminación controlada. El sujeto estará sentado cómodamente frente a una pantalla.
- **Software:** El pipeline se ejecutará desde el script `src/pipeline/run_pipeline.py` con el modo `--mode online`. La visualización en tiempo real del ICP se implementará en una interfaz simple (se recomienda usar `run_pipeline_with_ui.py` si está disponible, o crear un script ad-hoc).

### 4. Paradigma Experimental: Motor Imagery Binaria (Extendido)
Se utilizará un paradigma de **Imaginación Motora (MI)** binaria (Izquierda vs. Derecha) con 4 bloques, pero integrando la respuesta de la AGI para calcular el ICP.

**Estructura de una Sesión (por sujeto):**
1.  **Preparación:** Colocación del casco EEG, prueba de impedancia y calibración inicial del sistema (5-10 min).
2.  **Bloques de Entrenamiento (1 bloque):** El sujeto realiza 20 ensayos de MI con feedback visual (flecha en pantalla) pero **sin** la AGI. Estos datos se usan para ajustar el clasificador de intents.
3.  **Bloques Experimentales (3 bloques):**
    - Cada bloque: **40 ensayos**.
    - **Estructura de un ensayo:**
        - **Descanso (2-3 seg):** Pantalla negra.
        - **Cue (1 seg):** Una flecha apuntando a la izquierda o derecha.
        - **Período de MI (4-6 seg):** El sujeto imagina el movimiento de la mano correspondiente.
        - **Procesamiento y Decodificación ( < 0.5 seg):** El pipeline clasifica el intent.
        - **Respuesta de la AGI (1-2 seg):** Un prompt estructurado (`intent_decodificado`) se envía a la AGI (modelo local vía Ollama, ej., `llama3`). La respuesta de la AGI se muestra en pantalla.
        - **Feedback Post-AGI (1 seg):** Se muestra un mensaje simple.
    - **Entre bloques:** Descanso de 2 minutos.

### 5. Variables a Registrar (en Tiempo Real)
Para cada ensayo, el script `run_pipeline.py` (o su versión con interfaz) debe registrar en un archivo CSV estructurado (`data/raw/pilot_study/SXX_sesion.csv`):

| Campo | Descripción |
| :--- | :--- |
| `trial_id` | Número de ensayo secuencial |
| `timestamp_start` | Timestamp Unix de inicio del cue |
| `intent_correcto` | Intento real (L / R) |
| `intent_predicho` | Intento clasificado por el pipeline |
| `accuracy_trial` | 1 si `intent_predicho` == `intent_correcto`, else 0 |
| `eeg_features` | Vector de características EEG (ej., band power alpha/beta) serializado |
| `agi_response` | Respuesta textual completa de la AGI |
| `agi_embedding` | Embedding vector de la respuesta de la AGI (si se calcula) |
| `icp_trial` | **ICP calculado en vivo para ese ensayo** |
| `latencia_procesamiento` | Tiempo (ms) desde fin MI hasta obtención respuesta AGI |

### 6. Cálculo del Índice de Coherencia Predictiva (ICP) en Vivo
Se implementará una versión simplificada y en tiempo real del ICP definido en `CPEA_ICP_Formalism.md`.

$$ICP_{trial} = w_1 \cdot Acc_{trial} + w_2 \cdot MI_{rolling} + w_3 \cdot (1 / \tau_{trial})$$

- **$Acc_{trial}$**: Accuracy del clasificador en el ensayo actual (0 o 1).
- **$MI_{rolling}$**: Información Mutua (MI) calculada sobre una ventana deslizante de los últimos N ensayos (ej., N=10) entre `intent_correcto` y `intent_predicho`. Valores altos indican una decodificación fiable a corto plazo.
- **$\tau_{trial}$**: Latencia de procesamiento (ms) desde el final del período de MI hasta que la respuesta de la AGI es recibida. Se usa $1/\tau$ para penalizar latencias altas.
- **$w_1, w_2, w_3$**: Pesos (ej., 0.4, 0.4, 0.2). Estos se pueden ajustar en la configuración.

**Implementación:**
El script `src/pipeline/run_pipeline.py` debe ser modificado para, al final de cada ciclo, calcular estos tres componentes y escribir el ICP resultante en el CSV y mostrarlo en la interfaz de usuario (UI).

### 7. Datos Anonimizados y Análisis Post-Sesión
Una vez finalizadas todas las sesiones (3 sujetos x 3 bloques experimentales = 360 ensayos totales):

1.  **Consolidación:** Se consolidarán los archivos CSV de todos los sujetos en un único dataframe para análisis.
2.  **Análisis Estadístico Descriptivo:**
    - **Accuracy media por sujeto y global:** Se calculará la media y desviación estándar de la columna `accuracy_trial`. Se realizará un test binomial para ver si supera el azar (50%).
    - **Evolución del ICP:** Se graficará el ICP medio por bloque para cada sujeto. Se buscará una tendencia ascendente (aprendizaje) que indique una mejora en la coherencia predictiva.
    - **Análisis de Latencia:** Se calculará la latencia media de procesamiento ($\tau$) para cada sujeto, identificando posibles cuellos de botella (ej., respuesta AGI lenta).
3.  **Análisis Cualitativo de Respuestas AGI:** Se revisarán las respuestas textuales de la AGI (`agi_response`). El objetivo es verificar que la AGI está utilizando correctamente los features EEG en el prompt y no está generando respuestas no deseadas o incoherentes.

### 8. Entregables al Finalizar la Fase
- [ ] **Código modificado:** Scripts actualizados para ejecución online con cálculo de ICP en tiempo real (`run_pipeline.py` o `run_pipeline_with_ui.py`).
- [ ] **Dataset piloto:** Carpeta `data/raw/pilot_study/` con los CSV anonimizados de S01, S02, S03.
- [ ] **Notebook de análisis:** `notebooks/04_pilot_analysis.ipynb` que cargue los datos, reproduzca las gráficas de evolución de ICP y accuracy, y genere un resumen estadístico.
- [ ] **Documentación:** Se actualizará el `README.md` con instrucciones para ejecutar el estudio piloto y se añadirá este documento a la carpeta `docs/` como `Fase3.3_Protocolo_Piloto_Humano.md`.

### 9. Consideraciones Críticas para la Implementación
- **Estabilidad del Pipeline:** Antes de involucrar a otros sujetos, el investigador principal debe ejecutar al menos una sesión completa para asegurar la estabilidad de la conexión con el EEG, la AGI y el registro de datos.
- **Safe-Switch:** Se debe implementar el "Safe-Switch" (documentado en `Preprint CPEA...md`) en la UI, permitiendo al sujeto o al investigador detener el flujo de datos del EEG hacia la AGI en cualquier momento por razones de confort o seguridad.
- **Revisión Ética:** Aunque es un piloto con n=3, se recomienda tener una breve nota de aprobación ética (o justificación de exención) para documentar la buena práctica científica.

---
