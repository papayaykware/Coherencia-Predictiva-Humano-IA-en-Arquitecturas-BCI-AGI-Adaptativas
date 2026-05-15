# 🌍 Fase 1 — Integración Biofísica

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![OpenBCI](https://img.shields.io/badge/OpenBCI-Compatible-green)](https://openbci.com)
[![Muse](https://img.shields.io/badge/Muse-EEG-lightgrey)](https://choosemuse.com)
[![DOI](https://img.shields.io/badge/DOI-10.xxxx/biofase1-blue)](https://doi.org/10.xxxx/biofase1)
[![Notebooks](https://img.shields.io/badge/Notebooks-Jupyter-orange)](notebooks/)

> **Estado**: En desarrollo activo · [Roadmap](ROADMAP.md) · [Reportar incidencia](https://github.com/tu-usuario/biofase1/issues)

---

## 📑 Índice (TOC)

- [🎯 Objetivo](#objetivo)
- [🧠 EEG multimodal](#eeg-multimodal)
  - [Compatibilidad](#compatibilidad)
  - [Librerías](#librerias)
  - [Ejemplo rápido](#ejemplo-rapido)
- [🌎 Geofísica y variables espaciales](#geofisica)
  - [Índices NOAA](#indices-noaa)
  - [Estimación de Schumann](#schumann-estimado)
- [🛰️ Sensores físicos](#sensores-fisicos)
- [⚙️ Instalación y configuración](#instalacion)
- [📓 Notebooks reproducibles](#notebooks)
- [📚 Referencias y DOI](#referencias)

---

## 🎯 Objetivo

> **Permitir entrada multimodal real** integrando señales EEG, geofísicas (índices de tormenta solar, resonancias Schumann) y sensores físicos (IMU, GPS, temperatura, campo EM, HRV).

<div class="admonition note">
  <p class="admonition-title">📌 Nota</p>
  <p>Esta fase prioriza adaptaciones mínimas para garantizar interoperabilidad entre hardware de bajo costo y herramientas científicas estándar.</p>
</div>

---

## 🧠 EEG multimodal

<a id="eeg-multimodal"></a>

### Compatibilidad

| Dispositivo | Protocolo | Librería soporte | Estado |
|-------------|-----------|------------------|--------|
| OpenBCI (Cyton/Ganglion) | LSL, Serial | `brainflow`, `pylsl` | ✅ |
| Muse (2016/2) | Bluetooth, OSC | `muse-lsl`, `pyMuse` | ✅ |
| Cualquier dispositivo EDF/BDF | Archivos `.edf` | `mne` | ✅ |

<details>
<summary>🔧 <strong>Click para expandir: configuración avanzada de EEG</strong></summary>

```bash
# Instalación de dependencias para stream en tiempo real
pip install brainflow pylsl mne pyedflib
```

**Ejemplo de streaming con OpenBCI (WiFi)**:
```python
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
params = BrainFlowInputParams()
board = BoardShim(BoardIds.SYNTHETIC_BOARD, params)  # cambiar a CYTON_BOARD
board.prepare_session()
board.start_stream()
data = board.get_current_board_data(256)
```

</details>

### Librerías recomendadas

```bash
pip install mne brainflow
```

### Ejemplo rápido: carga de EDF

```python
import mne
raw = mne.io.read_raw_edf('sesion1.edf', preload=True)
raw.filter(0.5, 45)  # filtro paso banda EEG
raw.plot(n_channels=8, scalings='auto')
```

---

## 🌎 Geofísica y variables ambientales

<a id="geofisica"></a>

Integración de **índices geomagnéticos NOAA** y estimadores de resonancia Schumann.

| Variable | Fuente | Método de acceso |
|----------|--------|------------------|
| **Kp** (índice planetario) | NOAA SWPC | API REST (`/kp`) |
| **Dst** | Kyoto / ISGI | Archivos diarios o API |
| **Schumann estimado** | Modelo basado en actividad de rayos | `schumann` librería propia |
| **ELF variability** | SDR (opcional) | `rtl-sdr`, `pyrtlsdr` |

<details>
<summary>📡 <strong>Ver código de ejemplo: descarga de índices NOAA</strong></summary>

```python
import requests
from datetime import datetime

url = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
response = requests.get(url)
data = response.json()
latest_kp = float(data[-1][1])
print(f"Kp actual: {latest_kp}")
```
</details>

<div class="admonition warning">
  <p class="admonition-title">⚠️ SDR opcional</p>
  <p>Para medir variabilidad ELF local se necesita antena de cuadro y SDR con rango < 100 Hz. Recomendamos <strong>LTC1799</strong> o downconverter.</p>
</div>

---

## 🛰️ Sensores físicos

<a id="sensores-fisicos"></a>

Lista de sensores integrados mediante `pyserial` o `bluepy`:

- **IMU** (MPU6050, BNO055) → orientación, aceleración
- **GPS** (NMEA 0183) → posición y tiempo absoluto
- **Temperatura** (DHT22, DS18B20)
- **Campo EM ambiental** (magnetómetro triaxial, ej: HMC5883L)
- **HRV cardíaco** (Pulsoxímetro / ECG simple: AD8232)

<details>
<summary> <strong>Integración de HRV vía BLE</strong></summary>

```python
# Ejemplo con heartpy (archivo CSV)
import heartpy as hp
data = hp.get_data('hrv_signal.csv', column_name='rr')
wd = hp.process(data, 1000.0)
hp.plotter(wd, measures=['bpm', 'rmssd'])
```
</details>

---

## ⚙️ Instalación y configuración

<a id="instalacion"></a>

```bash
git clone https://github.com/tu-usuario/biofase1.git
cd biofase1
python -m venv venv
source venv/bin/activate    # o `venv\Scripts\activate` en Windows
pip install -r requirements.txt
```

**Requisitos mínimos (`requirements.txt`):**
```
mne>=1.4
brainflow>=0.2
pyserial
heartpy
numpy
scipy
requests
```

---

## 📓 Notebooks reproducibles

<a id="notebooks"></a>

Puedes ejecutar los siguientes cuadernos en Binder o localmente:

| Cuaderno | Enlace | Descripción |
|----------|--------|-------------|
| `eeg_live_demo.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tu-usuario/biofase1/blob/main/notebooks/eeg_live_demo.ipynb) | Stream en tiempo real desde OpenBCI o Muse |
| `geomagnetic_kp_analysis.ipynb` | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tu-usuario/biofase1/main?labpath=notebooks%2Fgeomagnetic_kp_analysis.ipynb) | Correlación Kp con variabilidad EEG |
| `sensor_fusion_imu_gps.ipynb` | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tu-usuario/biofase1/blob/main/notebooks/sensor_fusion_imu_gps.ipynb) | Fusión de datos IMU+GPS |

> 📂 Todos los notebooks se encuentran en [`/notebooks`](notebooks/).

---

## 📚 Referencias y DOI

<a id="referencias"></a>

Artículos clave que respaldan esta integración:

1. **EEG y geomagnetismo**  
   *"Human electrophysiological responses to Schumann resonances"* – Cherry, N. (2002)  
   [![DOI](https://img.shields.io/badge/DOI-10.1016/S1053--8119(02)91164--1-blue)](https://doi.org/10.1016/S1053-8119(02)91164-1)

2. **OpenBCI + MNE**  
   *"Open-source wearable EEG in real‑world neuroscience"* – IJspeert et al. (2021)  
   [![DOI](https://img.shields.io/badge/DOI-10.1088/1741--2552/ac1b3e-blue)](https://doi.org/10.1088/1741-2552/ac1b3e)

3. **HRV y temperatura en entornos multimodales**  
   *"Heart rate variability and ambient temperature"* – J. Psychophysiology (2020)  
   [![DOI](https://img.shields.io/badge/DOI-10.1037/pspp0000365-blue)](https://doi.org/10.1037/pspp0000365)

4. **Datos NOAA Kp/Dst**  
   Servicio SWPC – [https://www.swpc.noaa.gov](https://www.swpc.noaa.gov)

---

<div align="center">
  <sub>🧪 Fase 1 del proyecto BioFase — Integración biofísica para investigación reproducible.  
  <a href="CONTRIBUTING.md">Contribuir</a> · <a href="LICENSE">Licencia MIT</a></sub>
</div>
```
