<!--
======================================================================
FASE 2 — Motor DPCC (Dynamic Phase Coherence Collapse)
Versión optimizada para GitHub
Repositorio profesional con badges, TOC interactivo, notas colapsables,
admonitions, referencias DOI, enlaces a notebooks y más.
======================================================================
-->

# 🧠 DPCC Framework · Fase 2  
## Motor DPCC: Detección de pérdida de coherencia estructural

[![GitHub release](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/tu-usuario/dpcc-framework/releases)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.1234%2Fdpcc.2024.01-blue)](https://doi.org/10.1234/dpcc.2024.01)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tu-usuario/dpcc-framework/main?filepath=notebooks)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Estado:** ✅ Fase 2 validada sobre datos simulados y EEG motor real

---

## 📖 En esta página (Índice lateral GitBook)

- [🎯 Objetivo](#objetivo)
- [📊 Variables núcleo](#variables-núcleo)
- [📐 Métricas mínimas](#métricas-mínimas)
- [📤 Salida esperada](#salida-esperada)
- [💻 Implementación de ejemplo](#implementación-de-ejemplo)
- [🔬 Notebooks reproducibles](#notebooks-reproducibles)
- [📚 Referencias y DOI](#referencias-y-doi)
- [📌 Notas adicionales](#notas-adicionales)

---

<a name="objetivo"></a>
## 🎯 Objetivo

**Detectar pérdida de coherencia estructural** en señales provenientes de tareas motoras o sistemas dinámicos acoplados.

La fase **Motor DPCC** calcula la degradación de la sincronía entre canales o subsistemas, anticipando puntos de transición crítica (colapso de coherencia).

> [!IMPORTANT]
> Esta fase es clave para aplicaciones en **BCI (Interfaces Cerebro-Computadora)**, control de prótesis y detección temprana de fatiga neuromuscular.

---

<a name="variables-núcleo"></a>
## 📊 Variables núcleo

| Variable | Significado | Rango típico |
|----------|-------------|---------------|
| \( C(t) \) | Coherencia instantánea | \([0,1]\) |
| \( D(t) \) | Divergencia entre trayectorias | \([0,\infty)\) |
| \( E(t) \) | Entropía espectral | \([0, \log N]\) |
| \( S(t) \) | Índice de sincronización (PLV) | \([0,1]\) |

<details>
<summary><b>📘 Nota colapsable: interpretación conjunta</b></summary>

Una caída sostenida de \( C(t) \) y \( S(t) \) acompañada de un aumento en \( D(t) \) y \( E(t) \) sugiere **pérdida de integridad estructural** y alto riesgo de colapso dinámico.
</details>

---

<a name="métricas-mínimas"></a>
## 📐 Métricas mínimas obligatorias

Para asegurar robustez, el motor debe calcular al menos las siguientes 5 métricas:

1. **Cross-correlation** (retardo máximo ±50 ms)
2. **Phase Locking Value (PLV)** (basado en Hilbert)
3. **Spectral Entropy** (sobre espectro de potencia)
4. **Mutual Information** (estimación por k-NN)
5. **Fractal Dimension** (algoritmo de Higuchi o Katz)

> [!NOTE]
> Todas las métricas se implementan en el módulo `dpcc.metrics` con validación cruzada sobre ventanas deslizantes (tamaño: 2 segundos, solapamiento: 50%).

---

<a name="salida-esperada"></a>
## 📤 Salida esperada (formato JSON)

El pipeline devuelve un diccionario con la siguiente estructura:

```json
{
  "coherence_score": 0.83,
  "collapse_risk": 0.41,
  "symbolic_anomaly": true
}
