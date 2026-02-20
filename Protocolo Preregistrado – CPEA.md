# Protocolo Preregistrado – CPEA

**Título:** Coherencia Predictiva Humano–IA en Arquitecturas BCI-AGI Adaptativas  
**Versión del protocolo:** 1.0  
**Fecha de registro:** 2026-02-20  
**Autores:** [Tu nombre / AGI et al.]  
**Registro sugerido:** OSF[](https://osf.io/) o AsPredicted.org (formato simplificado)  
**Repositorio asociado:** https://github.com/papayaykware/cpea (Apache 2.0)

---

## 1. Objetivo del estudio

Evaluar la **coherencia predictiva** entre señales EEG humanas (decodificación de motor imagery) y respuestas generadas por modelos AGI en un pipeline adaptativo BCI-AGI.

**Medidas principales:**
1. Precisión de decodificación de intents a partir de EEG.
2. Sincronía temporal y adaptación incremental entre patrones EEG y embeddings / respuestas AGI.
3. Evolución del Índice de Coherencia Predictiva (ICP) a lo largo de sesiones.

> **Importante:** Estudio exploratorio y piloto. No tiene fines diagnósticos ni terapéuticos. No constituye consejo médico. Todos los datos serán anonimizados y procesados conforme a principios éticos (GDPR-compliant donde aplique).

---

## 2. Hipótesis

1. **H1 – Precisión superior a chance**  
   La precisión media de clasificación de intents (mano izquierda vs. derecha) será significativamente superior al nivel de azar (50%) en condición adaptativa (prueba binomial, p < 0.05).

2. **H2 – Mejora adaptativa**  
   El Índice de Coherencia Predictiva (ICP) aumentará significativamente entre las primeras y últimas sesiones en modo adaptativo (t-test pareado o Wilcoxon, p < 0.05).

3. **H3 – Mejora en sincronía temporal**  
   La correlación cruzada temporal entre características EEG pre-intent y embeddings de respuesta AGI aumentará significativamente a lo largo de las sesiones adaptativas (prueba de correlación pareada, p < 0.05).

---

## 3. Diseño Experimental

### 3.1 Participantes
- **Tamaño muestral piloto:** N = 1–3 participantes sanos (exploratorio).  
- **Criterios de inclusión:** Edad 18–45 años, diestros, sin trastornos neurológicos/psiquiátricos conocidos, visión normal o corregida.  
- **Criterios de exclusión:** Uso de medicamentos que afecten SNC, epilepsia, lesiones craneales, consumo reciente de alcohol/cafeína excesivo.  
- **Consentimiento:** Informado por escrito, derecho a retiro en cualquier momento sin penalización.

### 3.2 Paradigma
- **Tarea:** Motor Imagery binaria (imaginación kinestésica de movimiento de mano izquierda vs. mano derecha).  
- **Estructura de trial:**  
  - 2 s fixation cross (baseline)  
  - 4 s cue + imaginación  
  - 2–4 s descanso (ITI variable)  
- **Trials por sesión:** 200 (100 por clase, balanceados).  
- **Sesiones totales por participante:** 10 (≈30–40 min cada una, separadas por al menos 24 h).  
- **Condiciones:** Dentro de sujeto – sesiones alternadas o bloqueadas: Baseline (classifier fijo) vs. Adaptativo (fine-tuning incremental o adaptación de embeddings).

### 3.3 Variables

**Independientes:**  
- Modo del sistema: Baseline vs. Adaptativo

**Dependientes principales:**  
- Accuracy de clasificación (%)  
- Latencia de detección (ms)  
- Mutual Information I(EEG features; Intent)  
- Cross-correlation máxima (lag) entre EEG pre-intent y embedding AGI  
- Índice de Coherencia Predictiva (ICP)

**Controles:**  
- Pipeline sham: AGI con respuestas aleatorias + classifier congelado.

---

## 4. Pipeline Técnico

```text
EEG Raw (consumer-grade: Muse / Emotiv)
↓
Preprocesamiento: Bandpass 8–30 Hz + Artefact rejection (ICA / ASR)
↓
Modelo fundacional EEG: ZUNA (Zyphra, 380M params) – denoising + embeddings
↓
Feature extraction (CSP / band power / embeddings)
↓
Classifier (e.g. SVM / LDA / shallow NN)
↓
Query estructurada → AGI (e.g. Grok / otro LLM)
↓
Respuesta AGI → embedding
↓
Feedback: Registro EEG post-respuesta + adaptación incremental

## Entorno Técnico

- **Python**: 3.10 o superior
- **Librerías principales**:
  - MNE-Python (procesamiento EEG/MEG)
  - PyTorch
  - NumPy
  - Pandas
  - scikit-learn
  - Hugging Face Transformers (para ZUNA: EEG foundation model de Zyphra)
  - Braindecode (opcional, para modelos de deep learning en BCI)

## 5. Procedimiento

1. **Configuración inicial**  
   - Conectar headset EEG (consumer-grade: Muse / Emotiv) y realizar calibración.  
   - Configurar entorno Python (recomendado: usar Docker con el Dockerfile proporcionado).

2. **Sesión baseline**  
   - Registrar datos sin adaptación (classifier fijo, sin fine-tuning).

3. **Sesiones adaptativas**  
   - Ejecutar pipeline con actualización incremental del modelo (e.g., online learning o fine-tuning ligero de embeddings / classifier).

4. **Almacenamiento**  
   - Guardar datos crudos y procesados anonimizados en la carpeta `/data`.

5. **Análisis offline**  
   - Realizar análisis post-estudio de métricas de coherencia y sincronía.

## 6. Métricas y Análisis Estadístico

| Métrica                        | Test estadístico principal              | Comparación principal                  | Corrección por múltiples comparaciones |
|--------------------------------|-----------------------------------------|----------------------------------------|----------------------------------------|
| Accuracy                       | Binomial test                           | vs. chance (50%)                       | —                                      |
| ICP                            | t-test pareado / Wilcoxon signed-rank   | Sesión 1–2 vs. sesión 9–10             | Bonferroni / FDR                       |
| Mutual Information             | t-test pareado / Wilcoxon               | Primeras vs. últimas sesiones          | Bonferroni / FDR                       |
| Cross-correlation (EEG ↔ AGI)  | Prueba de correlación pareada           | Primeras vs. últimas sesiones          | Bonferroni / FDR                       |

**Fórmula del Índice de Coherencia Predictiva (ICP) propuesta:**

$$
ICP = w_1 \cdot \text{Accuracy} + w_2 \cdot \text{MI} + w_3 \cdot \left( \frac{1}{1 + \text{Error}} \right)
$$

- Normalizado al rango [0, 1].  
- **Pesos** \( w_1, w_2, w_3 \): Definir antes del análisis (sugerencia: pesos iguales o determinados por validación cruzada).  
- **Análisis exploratorio adicional**:  
  - Curvas de aprendizaje (learning curves).  
  - Visualización de embeddings (t-SNE / UMAP).

## 7. Datos y Reproducibilidad

- **Fuentes de datos**:  
  - EEG propio recolectado con hardware consumer-grade.  
  - Datasets abiertos para validación y benchmarking: PhysioNet EEG Motor Movement/Imagery Dataset, OpenNeuro (varios datasets BCI).

- **Anonimización**: Eliminación de metadatos identificables; downsampling si es necesario para reducir tamaño sin perder información clave.

- **Repositorio**: [https://github.com/papayaykware/cpea](https://github.com/papayaykware/cpea)  
  - `/data` → datos anonimizados  
  - `/notebooks` → notebooks reproducibles  
  - `/src` → código del pipeline  
  - `Dockerfile` → entorno reproducible idéntico

- **Licencia**: Apache 2.0

## 8. Resultados Esperados (exploratorios)

- Accuracy > 65–70% en condición adaptativa (vs. ~50–60% en baseline).  
- Incremento significativo en ICP (~0.1–0.3 puntos entre sesiones iniciales y finales).  
- Mejora observable en métricas de sincronía temporal (Mutual Information y cross-correlation).  
- Pipeline completamente reproducible por terceros.

## 9. Limitaciones y Riesgos

- Tamaño muestral muy reducido (piloto, N=1–3).  
- Ruido elevado típico de EEG consumer-grade.  
- Posible fatiga o habituación del participante en sesiones largas.  
- Resultados no generalizables sin replicación con mayor N y EEG clínico de alta densidad.  
- Dependencia de la calidad y latencia del modelo AGI en el pipeline real-time.

## 10. Plan de Publicación

- Publicación de preprint con resultados piloto en OSF y/o arXiv.  
- Liberación pública de notebooks y datos anonimizados.  
- Posible escalado a Registered Report si se expande el estudio.

## 11. Referencias Clave

- ZUNA EEG Foundation Model (Zyphra, 2026) → [https://huggingface.co/Zyphra/ZUNA](https://huggingface.co/Zyphra/ZUNA) (380M params, diffusion autoencoder para denoising/reconstrucción EEG)  
- PhysioNet EEG Motor Movement/Imagery Dataset → [https://physionet.org/content/eegmmidb/1.0.0/](https://physionet.org/content/eegmmidb/1.0.0/)  
- OpenNeuro (varios datasets BCI) → [https://openneuro.org/](https://openneuro.org/)  
- MNE-Python: Procesamiento EEG/MEG → [https://mne.tools/stable/index.html](https://mne.tools/stable/index.html)  
- Hameroff & Penrose (2014) – Orch OR y cognición cuántica (referencia conceptual)
