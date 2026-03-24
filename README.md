# Coherencia Predictiva Humano–IA en Arquitecturas BCI-AGI Adaptativas (CPEA)

[![GitHub Release](https://img.shields.io/github/v/release/papayaykware/cpea)](https://github.com/papayaykware/cpea/releases)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.9999999.svg)](https://doi.org/10.5281/zenodo.9999999)

**Descripción corta:**  
Repositorio piloto para explorar la **coherencia predictiva** entre EEG humano y respuestas de modelos AGI mediante un pipeline adaptativo BCI-AGI. Incluye datasets sample, notebooks reproducibles y métricas estadísticas para medir sincronización y adaptación dinámicas.

---

## 📌 Tabla de Contenidos

- [🔹 Introducción](#introducción)
- [🔹 Estructura del Repositorio](#estructura-del-repositorio)
- [🔹 Instalación y Quickstart](#instalación-y-quickstart)
- [🔹 Pipeline Experimental](#pipeline-experimental)
- [🔹 Experimento Mínimo Viable](#experimento-mínimo-viable)
- [🔹 Métricas y Análisis](#métricas-y-análisis)
- [🔹 Notebooks Reproducibles](#notebooks-reproducibles)
- [🔹 Referencias](#referencias)
- [🔹 Licencia](#licencia)
- [🔹 Badges y Estilo Visual](#badges-y-estilo-visual)
- [🔹 Próximos Pasos](#próximos-pasos)

---

## 🔹 Introducción

Este proyecto tiene como objetivo construir y evaluar un **sistema adaptativo BCI–AGI** que:

- Decodifica intents de EEG humanos en tiempo real
- Envía intents a un agente AGI (Grok, ZUNA, etc.)
- Evalúa coherencia predictiva entre EEG y respuesta AGI
- Implementa adaptación incremental para mejorar sincronía humano–IA

> 💡 **Nota:** Proyecto exploratorio piloto. No constituye consejo médico. Todos los datos deben manejarse bajo licencias abiertas y anonimización.

---

## 🔹 Estructura del Repositorio

```text
CPEA/
│
├─ data/
│   ├─ sample_eeg/     # EEG sample anonymized
│   └─ processed/      # Preprocesamiento y features
│
├─ notebooks/
│   ├─ 01_baseline.ipynb
│   ├─ 02_online_pipeline.ipynb
│   └─ 03_adaptation.ipynb
│
├─ src/
│   ├─ models/         # Modelos fundacionales EEG / denoising
│   ├─ pipeline/       # Scripts de pipeline EEG→AGI
│   └─ utils/          # Funciones auxiliares
│
├─ docs/
│   ├─ hypothesis.md   # Marco conceptual de coherencia predictiva
│   └─ diagrams/       # Diagramas Draw.io / PNG
│
├─ Dockerfile
├─ requirements.txt
├─ README.md
└─ LICENSE

🔹 Tip: La carpeta /docs incluye diagramas de flujo del pipeline y un PDF explicativo del marco conceptual.

---

🔹 Instalación y Quickstart

# Clonar el repositorio
git clone https://github.com/papayaykware/cpea.git
cd cpea

# Crear entorno virtual
python -m venv venv
source venv/bin/activate    # Linux / macOS
# o en Windows:
# venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar pipeline de prueba
python src/pipeline/run_pipeline.py --mode baseline

⚡ Recomendado: Usa un consumidor EEG real (Muse, Emotiv) o los datasets abiertos en data/sample_eeg para máxima reproducibilidad.

---

🔹 Pipeline Experimental
El pipeline se organiza en 5 bloques principales:

EEG Raw → Filtrado 8–30 Hz, artefact rejection
Modelo fundacional → Denoising, embeddings
Classifier → Predicción de intents
AGI → Respuesta a query estructurada
Feedback EEG → Registro post-respuesta para adaptación

---
🔹 Experimento Mínimo Viable
Paradigma: Motor Imagery Binaria
Número de trials: ≥ 2000 (10 sesiones × 200 trials)
Variables independientes:

Baseline vs Adaptativo

Variables dependientes:

Accuracy de clasificación
Latencia de detección
Mutual Information EEG ↔ Intent
Cross-correlation EEG ↔ Respuesta AGI

📝 Nota de control: Se incluye pipeline con AGI aleatorio y classifier congelado.

---

🔹 Métricas y Análisis

Accuracy: Binomial test vs chance (50%)
Mejora adaptativa: t-test pareado, ANOVA medidas repetidas
Mutual Information: I(EEG features ; Intent)
Cross-correlation temporal: Corr(EEG pre-intent, Output AGI embedding)
Índice de Coherencia Predictiva (ICP):

$$ICP = w_1 \cdot Accuracy + w_2 \cdot MI + w_3 \cdot (1 / Error)$$
✅ Interpretación: ICP normalizado [0–1]. Incrementos reflejan mayor coherencia adaptativa humano–IA.

---

🔹 Notebooks Reproducibles

01_baseline.ipynb → Evaluación inicial de classifier
02_online_pipeline.ipynb → Pipeline en tiempo real
03_adaptation.ipynb → Adaptación incremental y métricas

💡 Tip: Puedes visualizarlos directamente con nbviewer o integrarlos en Hugging Face Spaces para demos interactivas.

---

🔹 Referencias
Click para expandir referencias clave

---

🔹 Licencia
Apache 2.0 — ver archivo LICENSE
⚠️ Disclaimer: Proyecto piloto exploratorio. Datos anonimizados. No constituye consejo médico.

## 🤖 Integración con AGI Real (v1.4)

El pipeline ahora soporta conexión con modelos AGI locales (via Ollama) o en la nube (OpenAI). Las características EEG extraídas se pasan como prompt contextual, permitiendo:

- **Respuesta adaptativa**: El AGI responde basado en el estado cognitivo del usuario.
- **Métricas de coherencia**: Se calcula similitud entre embeddings EEG y AGI para el Índice de Coherencia Predictiva (ICP).
- **Configuración flexible**: Cambia entre proveedores sin modificar código.

### Ejemplo de configuración (`config/agi_config.yaml`):
```yaml
agi:
  provider: ollama  # o openai
  model: llama3
  prompt_template: |
    EEG features: {attention}, {intent}. Your response:
