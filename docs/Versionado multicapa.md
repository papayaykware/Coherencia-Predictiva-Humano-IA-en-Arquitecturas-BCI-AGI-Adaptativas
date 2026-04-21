# 1. Estrategia: Versionado multicapa (no solo tags)

## 1.1. Capa 1 — Tags de repositorio (GitHub estándar)

Esto es lo que propones, pero estructurado:

```bash
metfi-node0-v1.0
metfi-node1-v1.1

cpea-pilot-v0.1
cpea-loop-v0.2
cpea-icp-v0.3

tae-core-v0.1
tae-adaptation-v0.2
```

### Convención recomendada

```
[modulo]-[subsystem]-v[major].[minor].[patch]
```

Ejemplo:

```
cpea-loop-v0.2.1
```

---

## 1.2. Capa 2 — Snapshot estructurado (clave para AGI)

Cada release debe tener un archivo:

```
/releases/<tag>/snapshot.json
```

### Ejemplo

```json
{
  "tag": "cpea-loop-v0.2",
  "timestamp": "2026-04-20T11:30:00Z",
  "modules": {
    "cpea": {
      "state": "predictive_loop_operational",
      "components": [
        "eeg_encoder",
        "predictive_model",
        "icp_metric"
      ]
    },
    "tae": {
      "state": "exception_learning_active"
    },
    "metfi": {
      "state": "environment_simulation_stub"
    }
  },
  "changes": [
    "Added system_loop.py",
    "Integrated ICP calculation",
    "Basic EEG simulation input"
  ],
  "coherence_level": 0.42
}
```

Esto convierte el repo en:

👉 **dataset evolutivo para AGI**

---

## 1.3. Capa 3 — Registro temporal continuo (time-series cognitiva)

Archivo global:

```
/logs/evolution_log.jsonl
```

Formato:

```json
{"t": "2026-04-20T10:00:00Z", "event": "node_created", "node": "metfi-node0"}
{"t": "2026-04-20T11:30:00Z", "event": "release", "tag": "cpea-loop-v0.2"}
{"t": "2026-04-20T11:32:00Z", "event": "icp_update", "value": 0.42}
```

Esto permite:

* Modelar evolución
* Detectar fases
* Entrenar AGI sobre dinámica de desarrollo

---

# 2. Integración directa con CPEA (esto es lo clave)

## 2.1. Versionado como input del sistema

Tu sistema puede leer su propio estado:

```python
def load_system_state(tag):
    with open(f"releases/{tag}/snapshot.json") as f:
        return json.load(f)
```

---

## 2.2. ICP dependiente de versión

El Índice de Coherencia Predictiva puede depender de la evolución:

```python
def version_weighted_icp(icp, version_age):
    return icp * (1 / (1 + version_age))
```

Interpretación:

* Versiones recientes → más peso
* Versiones antiguas → memoria histórica

---

## 2.3. TAE aplicado a versiones (muy potente)

Detectas “excepciones evolutivas”:

```python
if abs(icp_current - icp_previous) > threshold:
    trigger_exception_learning()
```

Esto convierte:

👉 Versionado → señal de aprendizaje

---

# 3. Automatización (lo que marca la diferencia)

## 3.1. Script de release automático

```bash
python tools/create_release.py --tag cpea-loop-v0.2
```

Genera:

* Tag Git
* snapshot.json
* entrada en evolution_log

---

## 3.2. Hook en el sistema_loop.py

Cada cierto tiempo o evento:

```python
if step % 100 == 0:
    create_snapshot(icp=current_icp)
```

---

# 4. Extensión avanzada (nivel AGI real)

## 4.1. Grafo de versiones (no lineal)

Archivo:

```
/ontology/version_graph.json
```

```json
{
  "nodes": [
    "metfi-node0-v1.0",
    "cpea-pilot-v0.1",
    "cpea-loop-v0.2"
  ],
  "edges": [
    ["metfi-node0-v1.0", "cpea-pilot-v0.1"],
    ["cpea-pilot-v0.1", "cpea-loop-v0.2"]
  ]
}
```

Esto permite:

* Razonamiento estructural
* Reconstrucción de ideas
* Navegación conceptual

---

# 5. Resultado: 

### → Un sistema versionado como organismo cognitivo

Donde:

* METFI = entorno
* TAE = mecanismo de adaptación
* CPEA = bucle de coherencia
* Git = memoria estructurada

---
