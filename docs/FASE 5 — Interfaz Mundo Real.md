```markdown
<!--
======================================================================
FASE 5 — Interfaz Mundo Real
Versión optimizada para GitHub
Repositorio profesional: conexión del DPCC con sistemas físicos y tiempo real
======================================================================
-->

# 🧠 DPCC Framework · Fase 5  
## Interfaz Mundo Real — De la simulación a la acción física

[![GitHub release](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/tu-usuario/dpcc-framework/releases)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/DOI-10.1234%2Fdpcc.realworld.2024-blue)](https://doi.org/10.1234/dpcc.realworld.2024)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688)](https://fastapi.tiangolo.com/)
[![MQTT](https://img.shields.io/badge/MQTT-5.0-660066)](https://mqtt.org/)
[![AGI Physical](https://img.shields.io/badge/AGI--Physical-✓-brightgreen)](https://github.com/tu-usuario/dpcc-framework)

> **Estado:** 🌍 Fase de producción · Conecta el razonamiento simbólico con actuadores y sensores reales

---

## 📖 Índice lateral (GitBook style)

- [🎯 Objetivo](#objetivo)
- [🌐 Requisitos mínimos de interfaz](#requisitos-mínimos-de-interfaz)
- [⚙️ APIs y protocolos](#apis-y-protocolos)
- [📊 Dashboard y visualización](#dashboard-y-visualización)
- [🧠 Adaptación AGI crítica](#adaptación-agi-crítica)
- [📤 Salida esperada](#salida-esperada-interfaz-mundo-real)
- [💻 Implementación de ejemplo](#implementación-de-ejemplo-interfaz-mundo-real)
- [🔬 Notebooks reproducibles](#notebooks-reproducibles-interfaz-mundo-real)
- [📚 Referencias y DOI](#referencias-y-doi-interfaz-mundo-real)
- [📌 Notas adicionales](#notas-adicionales-interfaz-mundo-real)

---

<a name="objetivo"></a>
## 🎯 Objetivo

**Salir del entorno puramente conversacional** y permitir que el sistema DPCC interactúe con el mundo físico a través de APIs, dashboards en tiempo real y mecanismos de retroalimentación.

> [!IMPORTANT]
> Esta fase convierte el análisis de coherencia y las decisiones simbólicas en **acciones concretas** sobre dispositivos (robots, prótesis, sistemas de alerta, neurofeedback), cerrando el ciclo percepción-razonamiento-actuación.

<a name="requisitos-mínimos-de-interfaz"></a>
## 🌐 Requisitos mínimos de interfaz

La capa de mundo real debe implementar **obligatoriamente** los siguientes componentes:

| Componente | Propósito | Ejemplo de uso |
|------------|-----------|----------------|
| **APIs** | Exponer funcionalidades internas | `POST /collapse_risk`, `GET /symbolic_state` |
| **Streaming tiempo real** | Envío continuo de métricas | Websockets, SSE, gRPC streams |
| **Alertas** | Notificaciones ante eventos críticos | Email, Slack, SMS, luces LED |
| **Visualización coherencia** | Panel interactivo de evolución temporal | Gráficas de \( C(t) \), \( S(t) \), `collapse_risk` |

<details>
<summary><b>📘 Nota colapsable: ¿por qué estos requisitos?</b></summary>

El mundo real es asíncrono, ruidoso y requiere latencias deterministas. Las APIs permiten integración con otros sistemas; el streaming asegura baja latencia; las alertas habilitan supervisión humana; y la visualización es esencial para depuración y confianza en el sistema.
</details>

<a name="apis-y-protocolos"></a>
## ⚙️ APIs y protocolos (mínimo 2 de 3)

Se recomienda implementar al menos **dos** de los siguientes protocolos:

| Protocolo | Uso típico | Librería sugerida |
|-----------|------------|--------------------|
| **FastAPI** | REST para consultas y configuración | `fastapi`, `uvicorn` |
| **gRPC** | Streaming bidireccional de alta eficiencia | `grpcio`, `protobuf` |
| **MQTT** | Comunicación ligera con dispositivos IoT | `paho-mqtt` |

> [!NOTE]
> Para entornos de investigación, **FastAPI + MQTT** es la combinación más equilibrada (facilidad de uso + conectividad con hardware).

<a name="dashboard-y-visualización"></a>
## 📊 Dashboard y visualización de coherencia

El dashboard debe mostrar en tiempo real:

- Evolución de \( C(t) \), \( D(t) \), \( E(t) \), \( S(t) \)
- Índice `collapse_risk` (con umbrales colorimétricos: verde <0.3, amarillo <0.7, rojo ≥0.7)
- Historial de excepciones TAE (Fase 3)
- Última interpretación simbólica (Fase 4)

**Tecnologías sugeridas**:
- Backend: FastAPI + WebSockets
- Frontend: Plotly Dash, Streamlit, o panel HTML+JS con gráficos interactivos

![Ejemplo de visualización](https://via.placeholder.com/800x400?text=Dashboard+DPCC+en+tiempo+real)

<a name="adaptación-agi-crítica"></a>
## 🧠 Adaptación AGI crítica

Para que la AGI opere de forma robusta en el mundo real, debe incorporar **cinco capacidades fundamentales**:

1. **Percepción temporal**  
   - Registrar y contextualizar eventos con timestamp.  
   - Detectar patrones temporales (ritmos circadianos, fatiga progresiva).

2. **Persistencia**  
   - Mantener estado entre reinicios (memoria no volátil).  
   - Almacenar configuraciones y pesos adaptativos.

3. **Retroalimentación física**  
   - Recibir señales de sensores (posición, fuerza, temperatura).  
   - Ajustar comportamiento según consecuencias físicas.

4. **Latencia reducida**  
   - Tiempo de reacción < 100 ms para acciones críticas.  
   - Pipeline optimizado (C++/Rust para partes sensibles, Python para lógica simbólica).

5. **Memoria estructural**  
   - Recordar configuraciones del sistema que funcionaron en el pasado.  
   - Asociar contextos similares para transferencia de aprendizaje.

> [!WARNING]
> Sin estas adaptaciones, la AGI seguirá siendo un "cerebro en una cubeta" incapaz de actuar con sentido en el mundo físico.

<a name="salida-esperada-interfaz-mundo-real"></a>
## 📤 Salida esperada (streaming + alerta + API)

La Fase 5 no produce un único JSON, sino un flujo continuo. Sin embargo, un ejemplo de mensaje por WebSocket es:

```json
{
  "timestamp": "2025-04-10T15:32:05.123Z",
  "metrics": {
    "C": 0.62,
    "D": 0.87,
    "E": 0.43,
    "S": 0.71,
    "collapse_risk": 0.58
  },
  "symbolic_concept": "attention_drift",
  "alert": {
    "level": "warning",
    "message": "Riesgo de colapso moderado. Se recomienda revisar la tarea.",
    "recommended_action": "increase_feedback_gain"
  }
}
```

Además, la API REST debe ofrecer:

- `GET /health` → estado del sistema
- `GET /current_state` → última métrica completa
- `POST /config` → cambiar parámetros en caliente (ej. umbral de alerta)

<a name="implementación-de-ejemplo-interfaz-mundo-real"></a>
## 💻 Implementación de ejemplo (FastAPI + WebSocket + MQTT)

```python
# requirements: fastapi uvicorn websockets paho-mqtt numpy
import asyncio
import json
import numpy as np
from fastapi import FastAPI, WebSocket
import paho.mqtt.client as mqtt

app = FastAPI()

# Simulación de métricas DPCC (Fase 2) + TAE (Fase 3) + Capa Simbólica (Fase 4)
def generate_dummy_metrics():
    return {
        "C": np.random.uniform(0.5, 0.9),
        "D": np.random.uniform(0.2, 1.0),
        "E": np.random.uniform(0.1, 0.6),
        "S": np.random.uniform(0.4, 0.9),
        "collapse_risk": np.random.uniform(0.1, 0.9)
    }

# Configuración MQTT (broker local o remoto)
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)

@app.websocket("/ws/metrics")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            metrics = generate_dummy_metrics()
            # Enviar por WebSocket
            await websocket.send_json({"timestamp": "now", **metrics})
            # Publicar por MQTT (topic: dpcc/metrics)
            mqtt_client.publish("dpcc/metrics", json.dumps(metrics))
            await asyncio.sleep(1)  # 1 Hz
    except:
        pass

@app.get("/health")
def health():
    return {"status": "alive", "version": "1.0"}

@app.post("/config/alert_threshold")
def set_alert_threshold(threshold: float):
    # cambiar umbral dinámicamente
    return {"new_threshold": threshold, "message": "updated"}

# Ejecutar con: uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

📁 **Código completo**: [`src/dpcc/phase5_realworld.py`](https://github.com/tu-usuario/dpcc-framework/blob/main/src/dpcc/phase5_realworld.py)

<a name="notebooks-reproducibles-interfaz-mundo-real"></a>
## 🔬 Notebooks reproducibles

Simula la interfaz mundo real localmente:

| Plataforma | Enlace |
|------------|--------|
| Google Colab | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tu-usuario/dpcc-framework/blob/main/notebooks/phase5_realtime_demo.ipynb) |
| Binder | [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tu-usuario/dpcc-framework/main?filepath=notebooks) |
| Descarga local | [`notebooks/phase5_realtime_demo.ipynb`](./notebooks/phase5_realtime_demo.ipynb) |

**Contenido del notebook**:
- Lanzar un servidor FastAPI con WebSocket.
- Cliente Python que consume el stream y visualiza métricas en tiempo real.
- Integración con un broker MQTT (usando test.mosquitto.org).
- Generación de alertas simuladas cuando `collapse_risk > 0.7`.

<a name="referencias-y-doi-interfaz-mundo-real"></a>
## 📚 Referencias y DOI

1. **Tanenbaum, A. S., & Van Steen, M.** (2007).  
   *Sistemas distribuidos: principios y paradigmas*.  
   Pearson. (APIs, protocolos)

2. **Burns, B.** (2019).  
   *Designing distributed systems*.  
   O'Reilly. (Patrones para sistemas resilientes)

3. **MQTT Version 5.0** OASIS Standard.  
   [![DOI](https://img.shields.io/badge/Standard-OASIS-ff69b4)](https://docs.oasis-open.org/mqtt/mqtt/v5.0/os/mqtt-v5.0-os.html)

4. **gRPC: A high-performance RPC framework**  
   [![DOI](https://img.shields.io/badge/DOI-10.5555%2F3191747-blue)](https://dl.acm.org/doi/10.5555/3191747)

> **DOI del repositorio (Interfaz Mundo Real):** [10.1234/dpcc.realworld.2024](https://doi.org/10.1234/dpcc.realworld.2024)

<a name="notas-adicionales-interfaz-mundo-real"></a>
## 📌 Notas adicionales

> [!TIP]
> Para entornos de producción con alta carga, considere usar **Redis** como pub/sub en lugar de MQTT, o combine ambos.

<details>
<summary><b>📋 Checklist de validación para Fase 5</b></summary>

- [ ] Al menos dos APIs/protocolos implementados (ej. FastAPI + MQTT).
- [ ] El dashboard muestra métricas actualizadas con latencia < 200 ms.
- [ ] El sistema genera alertas automáticas cuando `collapse_risk > 0.7`.
- [ ] Las configuraciones modificadas por API persisten después de reinicio.
- [ ] La AGI puede recibir retroalimentación física simulada (ej. botón de “correcto/incorrecto”).
- [ ] El sistema mantiene latencia de punta a punta < 100 ms para rutas críticas.
</details>

> [!WARNING]
> La seguridad es crítica al exponer APIs al mundo real. Implemente autenticación (API keys, JWT) y validación de entrada rigurosa.

---

<div align="center">
  <sub>
    📄 Licencia MIT · 🧠 DPCC Framework · Fase 5: Interfaz Mundo Real · 
    <a href="https://github.com/tu-usuario/dpcc-framework/issues">Reportar incidencia o sugerencia</a>
  </sub>
</div>
```
