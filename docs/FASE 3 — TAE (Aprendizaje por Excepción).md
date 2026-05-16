```markdown
<!--
======================================================================
FASE 3 — TAE (Aprendizaje por Excepción)
Versión optimizada para GitHub
Repositorio profesional con TAE: aprendizaje adaptativo no supervisado
basado en rupturas, anomalías y bifurcaciones.
======================================================================
-->

# 🧠 DPCC Framework · Fase 3  
## TAE — Aprendizaje por Excepción (Exception-Driven Learning)

[![GitHub release](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/tu-usuario/dpcc-framework/releases)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.1234%2Fdpcc.tae.2024-blue)](https://doi.org/10.1234/dpcc.tae.2024)
[![AGI Ready](https://img.shields.io/badge/AGI--Ready-✓-brightgreen)](https://github.com/tu-usuario/dpcc-framework)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **Estado:** 🧪 Fase experimental · Validación sobre entornos caóticos y tareas motoras no estacionarias

---

## 📖 Índice lateral (GitBook style)

- [🎯 Objetivo](#objetivo)
- [💡 Núcleo conceptual](#núcleo-conceptual)
- [🤖 Algoritmos mínimos recomendados](#algoritmos-mínimos-recomendados)
- [🧠 Adaptación AGI requerida](#adaptación-agi-requerida)
- [📤 Salida esperada](#salida-esperada-tae)
- [💻 Implementación de ejemplo](#implementación-de-ejemplo-tae)
- [🔬 Notebooks reproducibles](#notebooks-reproducibles-tae)
- [📚 Referencias y DOI](#referencias-y-doi-tae)
- [📌 Notas adicionales](#notas-adicionales-tae)

---

<a name="objetivo"></a>
## 🎯 Objetivo

**Permitir aprendizaje adaptativo no supervisado** donde el sistema **no aprende de la norma**, sino exclusivamente de:

- Rupturas estructurales
- Anomalías dinámicas
- Incoherencias entre canales
- Rarezas estadísticas
- Bifurcaciones en el espacio de fases

> [!IMPORTANT]
> A diferencia del aprendizaje tradicional basado en ejemplos frecuentes, TAE se activa solo ante desviaciones significativas, reduciendo el overfitting a la normalidad y mejorando la detección de transiciones críticas.

<a name="núcleo-conceptual"></a>
## 💡 Núcleo conceptual

El sistema mantiene un modelo interno de la "línea base" de coherencia dinámica. Cuando la discrepancia entre lo esperado y lo observado supera un umbral adaptativo, se activa una **excepción** y el motor TAE:

1. **Almacena** la excepción en un buffer de replay priorizado.
2. **Reajusta** localmente los pesos de las capas de atención.
3. **Modifica** los embeddings contextuales para incorporar la nueva dinámica.

<details>
<summary><b>📘 Nota colapsable: diferencia con aprendizaje por refuerzo o supervisado</b></summary>

TAE es **no supervisado y asíncrono**. No requiere etiquetas ni recompensas externas. La señal de aprendizaje es la propia sorpresa computacional (entropía predicha vs real). Es análogo a los mecanismos de atención adaptativa en sistemas biológicos (ej. habituación/deshabituación).
</details>

<a name="algoritmos-mínimos-recomendados"></a>
## 🤖 Algoritmos mínimos recomendados

Para una implementación funcional de TAE se recomienda incluir al menos **4 de los siguientes 6** enfoques:

| Algoritmo | Rol en TAE | Implementación sugerida |
|-----------|------------|--------------------------|
| **Autoencoders** | Detección de anomalías por error de reconstrucción | `keras.Autoencoder` con umbral dinámico |
| **Contrastive Learning** | Diferenciación entre lo normal y lo excepcional | SimCLR adaptado a series temporales |
| **Replay Buffers** | Almacenamiento priorizado de excepciones | `deque` con puntaje de rareza |
| **EWC híbrido** | Consolidación de pesos sin olvidar excepciones | Elastic Weight Consolidation + regularización por rareza |
| **Isolation Forest** | Detección rápida de rarezas en embeddings | `sklearn.ensemble.IsolationForest` |
| **Spiking Neural Networks (SNN)** | Codificación temporal de eventos excepcionales | `snnTorch` con umbral de spike adaptativo |

> [!NOTE]
> La combinación `Autoencoder + Isolation Forest + Replay Buffer` es suficiente para la mayoría de los casos de uso. SNN es opcional para sistemas neuromórficos de baja latencia.

<a name="adaptación-agi-requerida"></a>
## 🧠 Adaptación AGI requerida

Para que TAE sea compatible con una arquitectura AGI (Inteligencia General Artificial) deben implementarse los siguientes cuatro mecanismos:

1. **Reevaluación dinámica de pesos**  
   Los pesos sinápticos no son estáticos. Una excepción activa una poda local y un reentrenamiento de las conexiones afectadas.

2. **Modificación de embeddings**  
   El espacio latente se ajusta incrementalmente mediante un `embedding shift` regularizado por la frecuencia de aparición de la excepción.

3. **Priorización de excepciones estructurales**  
   No todas las anomalías tienen igual importancia. Se calcula un **índice de impacto estructural** (IES) basado en la propagación del error a otras métricas (C, D, E, S).

4. **Detección de cambios ontológicos**  
   Si una excepción persiste y modifica la distribución subyacente, el sistema debe **crear una nueva clase conceptual** (ej. "régimen motor fatigado" vs "régimen motor sano").

> [!TIP]
> El cambio ontológico se detecta mediante la divergencia de Jensen-Shannon entre las ventanas de embeddings pre y post-excepción. Si > 0.4, se instancia una nueva categoría.

<a name="salida-esperada-tae"></a>
## 📤 Salida esperada (formato JSON)

El pipeline TAE retorna un resumen de la excepción procesada y las acciones realizadas:

```json
{
  "exception_detected": true,
  "exception_type": "structural_rupture",
  "novelty_score": 0.87,
  "embedding_update": true,
  "weight_revision": {
    "layers_affected": ["attention_3", "dense_5"],
    "magnitude": 0.23
  },
  "ontological_shift": false,
  "replay_buffer_size": 147
}
```

- `exception_detected`: booleano, activado por superación de umbral adaptativo.
- `exception_type`: `"statistical_outlier"`, `"phase_discontinuity"`, `"fractal_break"`, `"structural_rupture"`.
- `novelty_score`: \( \in [0,1] \) combinando error de autoencoder, raridad en Isolation Forest y divergencia de embedding.
- `embedding_update`: si se reentrenó el espacio latente.
- `weight_revision`: capas modificadas y magnitud media del cambio.
- `ontological_shift`: si se creó una nueva categoría.
- `replay_buffer_size`: número total de excepciones almacenadas.

<a name="implementación-de-ejemplo-tae"></a>
## 💻 Implementación de ejemplo (TAE mínimo con Autoencoder + Isolation Forest)

```python
import numpy as np
from sklearn.ensemble import IsolationForest
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model

# ========== 1. Autoencoder ==========
input_dim = 64  # ventana de embeddings
input_layer = Input(shape=(input_dim,))
encoded = Dense(32, activation='relu')(input_layer)
decoded = Dense(input_dim, activation='linear')(encoded)
ae = Model(input_layer, decoded)
ae.compile(optimizer='adam', loss='mse')

# Datos de línea base (1000 muestras normales)
baseline = np.random.randn(1000, input_dim)
ae.fit(baseline, baseline, epochs=5, verbose=0)

# ========== 2. Isolation Forest ==========
iso_forest = IsolationForest(contamination=0.05, random_state=42)
iso_forest.fit(baseline)

# ========== 3. Función de excepción ==========
def detect_exception(embedding, ae, iso_forest, threshold_mse=0.15):
    recon_error = np.mean((ae.predict(embedding.reshape(1, -1)) - embedding)**2)
    iso_score = iso_forest.decision_function(embedding.reshape(1, -1))[0]
    novelty = (recon_error / threshold_mse) * (1 - (iso_score + 1)/2)
    if recon_error > threshold_mse and iso_score < -0.1:
        return {"exception_detected": True, "novelty_score": min(1.0, novelty)}
    return {"exception_detected": False, "novelty_score": novelty}

# Simulación de una excepción
test_embedding = np.random.randn(input_dim) * 2.0  # anomalía
result = detect_exception(test_embedding, ae, iso_forest)
print(result)
```

📁 **Código completo**: [`src/dpcc/phase3_tae.py`](https://github.com/tu-usuario/dpcc-framework/blob/main/src/dpcc/phase3_tae.py)

<a name="notebooks-reproducibles-tae"></a>
## 🔬 Notebooks reproducibles

Explora TAE de forma interactiva:

| Plataforma | Enlace |
|------------|--------|
| Google Colab | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tu-usuario/dpcc-framework/blob/main/notebooks/phase3_tae_demo.ipynb) |
| Binder | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tu-usuario/dpcc-framework/main?filepath=notebooks) |
| Descarga local | [`notebooks/phase3_tae_demo.ipynb`](./notebooks/phase3_tae_demo.ipynb) |

**Contenido del notebook**:
- Generación de series normales y con rupturas sintéticas.
- Entrenamiento del Autoencoder + Isolation Forest.
- Visualización de la evolución del `novelty_score` ante excepciones.
- Ejemplo de `embedding_update` y cambio ontológico simulado.

<a name="referencias-y-doi-tae"></a>
## 📚 Referencias y DOI

Artículos clave que respaldan los principios de TAE:

1. **Rumelhart, D. E., Hinton, G. E., & Williams, R. J.** (1986).  
   *Learning representations by back-propagating errors*.  
   Nature, 323(6088), 533-536.  
   [![DOI](https://img.shields.io/badge/DOI-10.1038%2F323533a0-blue)](https://doi.org/10.1038/323533a0)

2. **Kirchdoerfer, T., & Ortiz, M.** (2016).  
   *Data-driven computational mechanics*.  
   Computer Methods in Applied Mechanics and Engineering, 304, 81-101.  
   [![DOI](https://img.shields.io/badge/DOI-10.1016%2Fj.cma.2016.02.002-blue)](https://doi.org/10.1016/j.cma.2016.02.002)

3. **Kirkpatrick, J., et al.** (2017).  
   *Overcoming catastrophic forgetting in neural networks*.  
   PNAS, 114(13), 3521-3526. (EWC original)  
   [![DOI](https://img.shields.io/badge/DOI-10.1073%2Fpnas.1611835114-blue)](https://doi.org/10.1073/pnas.1611835114)

4. **Chen, T., et al.** (2020).  
   *A simple framework for contrastive learning of visual representations*.  
   ICML. (SimCLR)  
   [![DOI](https://img.shields.io/badge/DOI-10.48550%2FarXiv.2002.05709-blue)](https://arxiv.org/abs/2002.05709)

> **DOI del repositorio TAE (Zenodo):** [10.1234/dpcc.tae.2024](https://doi.org/10.1234/dpcc.tae.2024)

<a name="notas-adicionales-tae"></a>
## 📌 Notas adicionales

> [!WARNING]
> TAE puede generar una explosión de excepciones si el umbral es demasiado sensible. Se recomienda comenzar con `percentil 95` del error de reconstrucción sobre datos de calibración.

<details>
<summary><b>📋 Checklist de validación para TAE</b></summary>

- [ ] El `novelty_score` aumenta significativamente ante rupturas sintéticas (p < 0.01).
- [ ] El buffer de replay almacena > 100 excepciones sin desbordamiento.
- [ ] La actualización de embeddings no destruye conocimiento previo (menos del 5% de caída en métricas de línea base).
- [ ] El sistema detecta cambios ontológicos cuando la distribución cambia durante más de 50 pasos consecutivos.
- [ ] La latencia de procesamiento por excepción es < 50 ms (para tiempo real).
</details>

> [!TIP]
> Para integrar TAE con el **Motor DPCC (Fase 2)**, utilice el `collapse_risk` como entrada de rareza al Isolation Forest. Las excepciones detectadas realimentan los pesos del motor para mejorar la predicción de colapsos futuros.

---

<div align="center">
  <sub>
    📄 Licencia MIT · 🧠 DPCC Framework · Fase 3: TAE (Aprendizaje por Excepción) · 
    <a href="https://github.com/tu-usuario/dpcc-framework/issues">Reportar incidencia o sugerir mejora</a>
  </sub>
</div>
```
