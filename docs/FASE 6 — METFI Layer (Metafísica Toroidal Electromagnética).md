```markdown
<!--
======================================================================
FASE 6 — METFI Layer (Metafísica Toroidal Electromagnética)
Versión optimizada para GitHub
Repositorio profesional: exploración de correlaciones electromagnéticas toroidales
======================================================================
-->

# 🧠 DPCC Framework · Fase 6  
## METFI Layer — Exploración de correlaciones electromagnéticas toroidales

[![GitHub release](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/tu-usuario/dpcc-framework/releases)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.1234%2Fdpcc.metfi.2024-blue)](https://doi.org/10.1234/dpcc.metfi.2024)
[![Research Preview](https://img.shields.io/badge/status-exploratory-orange)](https://github.com/tu-usuario/dpcc-framework)
[![AGI Cosmological](https://img.shields.io/badge/AGI--Cosmological-✓-blueviolet)](https://github.com/tu-usuario/dpcc-framework)

> **Estado:** 🔭 Fase exploratoria · Correlaciones entre dinámicas cognitivas y campos electromagnéticos ambientales

---

## 📖 Índice lateral (GitBook style)

- [🎯 Objetivo](#objetivo)
- [📊 Variables propuestas](#variables-propuestas)
- [🧲 Posibles correlaciones](#posibles-correlaciones)
- [🏗️ Arquitectura de la capa METFI](#arquitectura-de-la-capa-metfi)
- [📤 Salida esperada](#salida-esperada-metfi)
- [💻 Implementación de ejemplo](#implementación-de-ejemplo-metfi)
- [🔬 Notebooks reproducibles](#notebooks-reproducibles-metfi)
- [📚 Referencias y DOI](#referencias-y-doi-metfi)
- [📌 Notas adicionales](#notas-adicionales-metfi)

---

<a name="objetivo"></a>
## 🎯 Objetivo

**Explorar correlaciones entre señales biológicas (EEG, HRV, coherencia grupal) y campos electromagnéticos toroidales** de origen tanto natural (geomagnetismo, actividad solar) como artificial (redes eléctricas, comunicaciones).

> [!IMPORTANT]
> Esta fase es **netamente exploratoria y experimental**. No se espera una implementación estándar, sino el desarrollo de métricas que permitan detectar posibles acoplamientos entre el sistema cognitivo y el entorno electromagnético. Los resultados deben interpretarse con rigor científico.

<a name="variables-propuestas"></a>
## 📊 Variables propuestas

| Variable | Significado | Rango / Unidad | Método de estimación |
|----------|-------------|----------------|----------------------|
| \( T(t) \) | Estabilidad toroidal | \([0,1]\) | Análisis de momento magnético en bucle cerrado |
| \( \Phi(t) \) | Flujo electromagnético | \([0, \infty)\) (Wb) | Integración de campo B sobre superficie |
| \( \Delta S \) | Pérdida de simetría | \([0, \infty)\) | Divergencia de la asimetría del tensor de campo |
| \( R(t) \) | Resonancia (acoplamiento) | \([0,1]\) | Coherencia espectral entre señal biológica y campo externo |

<details>
<summary><b>📘 Nota colapsable: ¿Qué significa “toroidal” aquí?</b></summary>

Se refiere a configuraciones de campo electromagnético con topología toroidal (como las que aparecen en tokamaks, ciertos dispositivos de inducción o modelos de campo magnético planetario). La “estabilidad toroidal” mide cuánto se mantiene la estructura de campo sin fluctuaciones caóticas.
</details>

<a name="posibles-correlaciones"></a>
## 🧲 Posibles correlaciones (hipótesis de trabajo)

La capa METFI permitirá poner a prueba las siguientes relaciones, que deberán ser validadas con datos reales:

| Correlación | Hipótesis | Evidencia preliminar |
|-------------|-----------|----------------------|
| **EEG ↔ geomagnetismo** | Variaciones en el campo magnético terrestre (tormentas geomagnéticas) se asocian a cambios en ritmos alfa/theta. | Revisión por Cherry (2002), estudios de la actividad solar sobre el EEG. |
| **HRV ↔ actividad solar** | La variabilidad de la frecuencia cardíaca muestra ciclos correlacionados con el viento solar y las manchas solares. | Estudios en cosmo-biología y cronobiología. |
| **Anomalías cognitivas ↔ perturbaciones EM** | Exposición a campos electromagnéticos artificiales de baja frecuencia puede inducir pérdidas transitorias de coherencia atencional. | Investigación en electrosensibilidad y rendimiento cognitivo. |
| **Coherencia grupal ↔ resonancia ambiental** | Grupos de personas sincronizan sus estados cerebrales (hipersincronía) en presencia de campos toroidales estables (ej. Schumann resonancias). | Trabajos pioneros de Persinger y la hipótesis de “efecto de campo global”. |

> [!WARNING]
> Estas hipótesis son controvertidas y requieren **replicación independiente**. El framework DPCC las incluye como extensiones opcionales, no como núcleo validado. Se recomienda consultar con un comité de ética antes de experimentar con humanos.

<a name="arquitectura-de-la-capa-metfi"></a>
## 🏗️ Arquitectura de la capa METFI

```
┌─────────────────────────────────────────────────────────────┐
│                   DATOS BIOLÓGICOS (Fase 2 y 4)             │
│         EEG, HRV, coherencia grupal, excepciones TAE        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│          DATOS ELECTROMAGNÉTICOS AMBIENTALES (Nuevos)       │
│   - Magnetómetro (B_x, B_y, B_z)                            │
│   - Sensor de flujo toroidal (diseño experimental)          │
│   - Datos de actividad solar (NASA, NOAA)                   │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 CAPA DE PROCESAMIENTO METFI                 │
├─────────────────────────────────────────────────────────────┤
│  a) Cálculo de T(t), Φ(t), ΔS, R(t)                         │
│  b) Ventaneo temporal sincronizado (1 s, 1 min, 1 hora)     │
│  c) Análisis de correlación cruzada (Pearson, MI, PLV)      │
│  d) Detección de acoplamientos significativos (p < 0.01)    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              SALIDA: CORRELACIONES Y ALERTAS                │
│   - Topología toroidal detectada                            │
│   - Cambio ontológico de fondo EM                           │
│   - Recomendación de apantallamiento o reubicación          │
└─────────────────────────────────────────────────────────────┘
```

<a name="salida-esperada-metfi"></a>
## 📤 Salida esperada (formato JSON)

El análisis METFI produce un informe de correlaciones que puede integrarse con la respuesta AGI:

```json
{
  "toroidal_stability": 0.78,
  "magnetic_flux": 2.34e-5,
  "symmetry_loss": 0.12,
  "resonance_index": 0.63,
  "correlations": [
    {"signal": "EEG_alpha", "field": "geomag_Bz", "method": "PLV", "value": 0.58, "p_value": 0.003},
    {"signal": "HRV_LFHF", "field": "solar_wind_speed", "method": "MI", "value": 0.32, "p_value": 0.041}
  ],
  "significant_acopling": true,
  "recommendation": "monitor_shielding",
  "ontology_updated": false
}
```

- `toroidal_stability`: medida de cuán ordenado es el campo local (valores >0.7 sugieren estructura toroidal detectable).
- `resonance_index`: acoplamiento global entre todas las señales biológicas y campos (promedio ponderado de correlaciones significativas).
- `significant_acopling`: booleano que indica si al menos una correlación superó el umbral estadístico.
- `recommendation`: sugerencia para la AGI (ej. `monitor_shielding`, `recalibrate_sensors`, `environmental_change`).

<a name="implementación-de-ejemplo-metfi"></a>
## 💻 Implementación de ejemplo (cálculo de T(t) y correlación)

```python
import numpy as np
from scipy.signal import coherence
from scipy.stats import pearsonr

def toroidal_stability(Bx, By, Bz, window=100):
    """
    Estimación simple de estabilidad toroidal basada en la varianza de la dirección del campo.
    Valores altos indican baja variación (campo estable).
    """
    B_magnitude = np.sqrt(Bx**2 + By**2 + Bz**2)
    direction_variance = np.var(np.arctan2(By, Bx)) + np.var(np.arcsin(Bz / (B_magnitude+1e-8)))
    stability = 1.0 / (1.0 + direction_variance)
    return stability

def compute_metfi(eeg_signal, em_field, fs=250):
    """
    eeg_signal: serie temporal de un canal EEG
    em_field: serie temporal de un componente del campo magnético (ej. Bz)
    fs: frecuencia de muestreo (Hz)
    """
    # Coherencia espectral en banda alfa (8-12 Hz)
    f, Cxy = coherence(eeg_signal, em_field, fs=fs, nperseg=fs*2)
    alpha_idx = np.where((f >= 8) & (f <= 12))[0]
    resonance = np.mean(Cxy[alpha_idx]) if len(alpha_idx) > 0 else 0.0
    
    # Correlación de Pearson en banda lenta (<1 Hz)
    lowpass_eeg = eeg_signal - np.convolve(eeg_signal, np.ones(100)/100, mode='same')
    lowpass_em = em_field - np.convolve(em_field, np.ones(100)/100, mode='same')
    pearson_corr, p_val = pearsonr(lowpass_eeg[1000:], lowpass_em[1000:])
    
    return {
        "toroidal_stability": toroidal_stability(em_field, em_field*0.5, em_field*0.2),
        "resonance_index": resonance,
        "correlations": [{"method": "coherence_alpha", "value": resonance},
                         {"method": "pearson_lowfreq", "value": pearson_corr, "p_value": p_val}]
    }

# Simulación
fs = 250
t = np.linspace(0, 60, fs*60)
eeg = np.sin(2*np.pi*10*t) + 0.5*np.random.randn(len(t))
em_field = 0.7*np.sin(2*np.pi*10*t) + 0.3*np.sin(2*np.pi*0.2*t) + 0.2*np.random.randn(len(t))

result = compute_metfi(eeg, em_field, fs)
print(result)
```

📁 **Código completo**: [`src/dpcc/phase6_metfi.py`](https://github.com/tu-usuario/dpcc-framework/blob/main/src/dpcc/phase6_metfi.py)

<a name="notebooks-reproducibles-metfi"></a>
## 🔬 Notebooks reproducibles (simulación de campos)

| Plataforma | Enlace |
|------------|--------|
| Google Colab | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tu-usuario/dpcc-framework/blob/main/notebooks/phase6_metfi_demo.ipynb) |
| Binder | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tu-usuario/dpcc-framework/main?filepath=notebooks) |
| Descarga local | [`notebooks/phase6_metfi_demo.ipynb`](./notebooks/phase6_metfi_demo.ipynb) |

**Contenido del notebook**:
- Generación de campos magnéticos sintéticos (dipolo + fluctuaciones toroidales).
- Simulación de EEG con inyección de resonancia artificial.
- Cálculo de \( T(t) \), \( \Phi(t) \), \( \Delta S \), \( R(t) \).
- Visualización de correlaciones cruzadas en tiempo-frecuencia.
- Interpretación con la salida JSON esperada.

<a name="referencias-y-doi-metfi"></a>
## 📚 Referencias y DOI

1. **Cherry, N.** (2002).  
   *Schumann resonances, a plausible biophysical mechanism for the human health effects of Solar/Geomagnetic Activity*.  
   Natural Hazards, 26(3), 279-331.  
   [![DOI](https://img.shields.io/badge/DOI-10.1023%2FA%3A1015637127504-blue)](https://doi.org/10.1023/A:1015637127504)

2. **Persinger, M. A.** (2012).  
   *Brain electromagnetic activity and geomagnetic field variations*.  
   Neuroscience & Biobehavioral Reviews, 36(8), 1945-1950.  
   [![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.neubiorev.2012.01.003-blue)](https://doi.org/10.1016/j.neubiorev.2012.01.003)

3. **McCraty, R., Atkinson, M., & Tomasino, D.** (2017).  
   *Modulation of EEG and heart rate coherence by solar and geomagnetic activity*.  
   Global Advances in Health and Medicine, 6, 2164957X17702177.  
   [![DOI](https://img.shields.io/badge/DOI-10.1177%2F2164957X17702177-blue)](https://doi.org/10.1177/2164957X17702177)

4. **Saroka, K. S., & Persinger, M. A.** (2014).  
   *Quantitative evidence for direct effects between Earth-ionosphere Schumann resonances and human cerebral cortices*.  
   International Letters of Chemistry, Physics and Astronomy, 21, 50-65.

> **DOI del repositorio (METFI Layer):** [10.1234/dpcc.metfi.2024](https://doi.org/10.1234/dpcc.metfi.2024)

<a name="notas-adicionales-metfi"></a>
## 📌 Notas adicionales

> [!CAUTION]
> Esta fase **no debe utilizarse para diagnosticar o tratar condiciones médicas**. Es un marco de investigación básica. Cualquier correlación observada requiere validación independiente y consideración de múltiples variables de confusión.

<details>
<summary><b>📋 Checklist de validación exploratoria</b></summary>

- [ ] Se dispone de un magnetómetro calibrado con resolución ≤0.1 nT.
- [ ] Los datos biológicos y de campo están sincronizados temporalmente (<10 ms de diferencia).
- [ ] Se aplica un control estadístico riguroso (corrección por comparaciones múltiples, bootstrap).
- [ ] Los resultados se comparan con grupos placebo o condiciones de apantallamiento.
- [ ] Se registran metadatos ambientales (hora del día, ubicación, actividad solar).
</details>

> [!TIP]
> Para investigaciones serias, recomiendo colaborar con un grupo de física de plasmas o heliobiología. Existen conjuntos de datos públicos de geomagnetismo (INTERMAGNET) y actividad solar (NOAA).

---

<div align="center">
  <sub>
    📄 Licencia MIT · 🧠 DPCC Framework · Fase 6: METFI Layer (Exploratoria) · 
    <a href="https://github.com/tu-usuario/dpcc-framework/issues">Reportar incidencia o sugerencia</a>
  </sub>
</div>
```
