# 🧠 NeuroPipeline · FASE 0 — Infraestructura Base

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![MNE](https://img.shields.io/badge/MNE-1.6+-purple.svg)](https://mne.tools/)
[![Docker](https://img.shields.io/badge/docker-✔-2496ED.svg)](https://docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-alpha-orange)](https://github.com/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yourusername/yourrepo/blob/main/notebooks/demo.ipynb)

> **Reproducible EEG/MEG pipeline infrastructure** – Ready for signal processing, deep learning, and real‑time APIs.

---

## 📑 Índice (TOC navegable)

<!-- TOC anchors (internal links) -->
- [🎯 Objetivo](#-objetivo)
- [📋 Requisitos mínimos](#-requisitos-mínimos)
- [📁 Estructura del repositorio](#-estructura-del-repositorio)
- [🐳 Instalación y entorno reproducible](#-instalación-y-entorno-reproducible)
  - [Usando Docker](#usando-docker)
  - [Entorno nativo con conda/pip](#entorno-nativo-con-condapip)
- [🚀 Inicio rápido](#-inicio-rápido)
- [🔌 API y WebSockets](#-api-y-websockets)
- [🧪 Experimentos y cuadernos](#-experimentos-y-cuadernos)
- [📚 Referencias y DOI](#-referencias-y-doi)
- [🤝 Contribución](#-contribución)
- [📜 Licencia](#-licencia)

---

## 🎯 Objetivo

Crear un **entorno completamente reproducible** para el desarrollo de pipelines de análisis de señales fisiológicas (EEG, MEG, etc.) con soporte para:

- Procesamiento con **MNE‑Python**
- Modelado profundo con **PyTorch**
- Servicios en tiempo real con **FastAPI + WebSockets**
- Contenerización con **Docker** (CUDA opcional)

---

## 📋 Requisitos mínimos

| Componente       | Versión / Especificación            | Nota                               |
|------------------|--------------------------------------|------------------------------------|
| Python           | 3.11 o superior                      | Obligatorio                        |
| PyTorch          | ≥2.0 (CUDA opcional)                 | CPU/GPU                            |
| MNE              | ≥1.6                                 | Análisis de señales                |
| NumPy / SciPy    | Últimas estables                     | Cálculo científico                 |
| Pandas           | ≥2.0                                 | Manipulación de datos              |
| FastAPI          | ≥0.100                               | API REST + WebSockets              |
| Docker           | 24+                                  | Para contenedores (recomendado)    |

> [!TIP]
> Si dispones de GPU NVIDIA, instala PyTorch con `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118` y verifica CUDA con `torch.cuda.is_available()`.

---

## 📁 Estructura del repositorio

```bash
repo/
├── data/               # Datos crudos y procesados (ignorados por git)
├── models/             # Pesos de modelos guardados (.pt, .pkl)
├── notebooks/          # Jupyter notebooks exploratorios y reproducibles
├── signals/            # Módulo de procesamiento de señales (filtros, ICA, etc.)
├── dpcc/               # Módulo de control de calidad y preprocesado
├── tae/                # Módulo de transformadores atencionales (PyTorch)
├── metfi/              # Extracción de características temporales y espectrales
├── api/                # Endpoints FastAPI, WebSockets, schemas
├── docs/               # Documentación adicional (Sphinx/ MkDocs)
├── tests/              # Pruebas unitarias e integrales (pytest)
└── experiments/        # Configuraciones y logs de experimentos (MLflow / TensorBoard)
```

<details>
<summary><strong>📌 <em>Click para ver descripción de cada carpeta</em></strong></summary>

- **`signals/`** – Wrappers para MNE, filtros personalizados, detección de artefactos.  
- **`dpcc/`** – Data Preprocessing, Cleaning & Control (ej. eliminación de canales ruidosos).  
- **`tae/`** – Implementación de Time‑Attention Encoders (transformers para series temporales).  
- **`metfi/`** – Feature extraction: bandas de potencia, entropía, conectividad funcional.  
- **`api/`** – FastAPI routers, gestión de sesiones WebSocket, modelos Pydantic.  
- **`experiments/`** – Scripts de entrenamiento, configuraciones Hydra/YAML, resultados.  

</details>

---

## 🐳 Instalación y entorno reproducible

### Usando Docker (recomendado)

```bash
# Clona el repositorio
git clone https://github.com/tu_usuario/tu_repo.git
cd tu_repo

# Construye la imagen (incluye CUDA si Dockerfile está configurado)
docker build -t neuropipeline:latest .

# Ejecuta el contenedor con montaje de datos
docker run --gpus all -p 8000:8000 -v $(pwd)/data:/app/data neuropipeline:latest
```

### Entorno nativo con conda/pip

```bash
# Crear entorno virtual (Python 3.11)
conda create -n neuroenv python=3.11
conda activate neuroenv

# Instalar dependencias
pip install torch mne numpy scipy pandas fastapi uvicorn websockets

# Verifica instalación
python -c "import mne; print(mne.__version__)"
```

> [!WARNING]
> Asegúrate de que `data/`, `models/` y `experiments/` no sean versionados. Añádelos a `.gitignore`.

---

## 🚀 Inicio rápido

1. **Preprocesa una señal de ejemplo**  
   ```python
   from signals import preprocess
   raw = preprocess.load_sample_data()
   filtered = preprocess.apply_bandpass(raw, l_freq=1, h_freq=40)
   ```

2. **Ejecuta la API localmente**  
   ```bash
   uvicorn api.main:app --reload --port 8000
   ```
   Accede a la documentación interactiva: [http://localhost:8000/docs](http://localhost:8000/docs)

3. **Prueba la conexión WebSocket**  
   ```bash
   # Usando wscat (npm install -g wscat)
   wscat -c ws://localhost:8000/ws
   > {"type": "ping"}
   ```

---

## 🔌 API y WebSockets

La API expone endpoints para:

| Método | Endpoint          | Descripción                           |
|--------|-------------------|---------------------------------------|
| `POST` | `/process/`       | Envía una señal y recibe características calculadas |
| `GET`  | `/health`         | Verifica el estado del servicio       |
| `WS`   | `/ws`             | Canal bidireccional para datos en tiempo real |

<details>
<summary>📘 Ver ejemplo de petición HTTP</summary>

```bash
curl -X POST "http://localhost:8000/process/" \
  -H "Content-Type: application/json" \
  -d '{"signal": [0.1, 0.2, 0.3], "fs": 128}'
```
</details>

> [!NOTE]
> La implementación completa se encuentra en `api/`. Para entornos de producción, usa `gunicorn` con workers Uvicorn.

---

## 🧪 Experimentos y cuadernos

Todos los notebooks reproducibles se almacenan en `notebooks/`. Puedes ejecutarlos localmente o en Google Colab.

- **`notebooks/01_preprocessing_demo.ipynb`** – Limpieza y visualización con MNE  
- **`notebooks/02_tae_training.ipynb`** – Entrenamiento del modelo Transformer Atencional  
- **`notebooks/03_realtime_websocket.ipynb`** – Cliente WebSocket para streaming

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tu_usuario/tu_repo/blob/main/notebooks/01_preprocessing_demo.ipynb)

> [!TIP]
> Utiliza `papermill` para parametrizar y ejecutar notebooks automáticamente desde scripts.

---

## 📚 Referencias y DOI

El pipeline se basa en los siguientes trabajos:

- **MNE software** – Gramfort *et al.* (2013) – DOI: [10.3389/fnins.2013.00267](https://doi.org/10.3389/fnins.2013.00267)  
- **Time-Aware Transformers** – Wu *et al.* (2020) – DOI: [10.48550/arXiv.2006.11491](https://doi.org/10.48550/arXiv.2006.11491)  
- **Reproducible EEG pipelines** – Holdgraf *et al.* (2019) – DOI: [10.25080/Majora-7ddc1dd1-010](https://doi.org/10.25080/Majora-7ddc1dd1-010)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)  
*Cita este repositorio como: Tu Nombre, "NeuroPipeline Base Infrastructure", Zenodo, 2025.*

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Abre un *issue* describiendo la mejora o bug.
2. Haz fork del proyecto y crea una rama (`feature/nueva-funcionalidad`).
3. Asegura que las pruebas pasen (`pytest tests/`).
4. Envía un *pull request*.

Consulta `CONTRIBUTING.md` (próximamente) para lineamientos completos.

---

## 📜 Licencia

Distribuido bajo licencia **MIT**. Consulta el archivo `LICENSE` para más detalles.

---

✨ *Hecho para investigación reproducible en neurociencia y señales biomédicas.*
```
