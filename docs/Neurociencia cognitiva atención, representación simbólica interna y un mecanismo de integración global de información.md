# 1. Sistema de atención neuronal dinámico

## Principio neurocognitivo

La atención funciona como un mecanismo que **selecciona y amplifica información relevante** mientras suprime información irrelevante. Neurobiológicamente implica redes frontoparietales y modulaciones de actividad cortical.

En modelos computacionales modernos se relaciona con mecanismos de **Attention Mechanism**.

---

## Arquitectura en CPEA

El módulo de atención actúa sobre el estado cerebral simulando **ganancia neuronal variable**.

```text
estado cerebral
↓
módulo de atención
↓
ponderación dinámica de regiones
↓
actividad amplificada o suprimida
```

---

## Implementación

### neural_attention.py

```python
import torch
import torch.nn as nn

class NeuralAttention(nn.Module):

    def __init__(self, state_dim):

        super().__init__()

        self.attention = nn.Linear(state_dim, state_dim)

        self.softmax = nn.Softmax(dim=-1)

    def forward(self, brain_state):

        weights = self.softmax(self.attention(brain_state))

        attended_state = brain_state * weights

        return attended_state, weights
```

---

## Dinámica funcional

El sistema prioriza regiones cerebrales relevantes:

```
actividad regional
↓
cálculo de pesos de atención
↓
amplificación selectiva
```

Esto permite:

* selección de estímulos relevantes
* mejora de predicción
* reducción de ruido neuronal

---

# 2. Lenguaje interno simbólico-neuronal

La cognición humana combina dos niveles:

* representaciones neuronales distribuidas
* símbolos conceptuales abstractos

Este módulo permite convertir **estados neuronales en representaciones simbólicas internas**.

---

## Principio

Los patrones neuronales se proyectan a un espacio simbólico que representa conceptos o relaciones.

```
estado cerebral
↓
encoder simbólico
↓
tokens conceptuales
```

---

## Implementación

### neural_symbolic_language.py

```python
import torch
import torch.nn as nn

class NeuralSymbolicLanguage(nn.Module):

    def __init__(self, state_dim, vocab_size=100):

        super().__init__()

        self.encoder = nn.Linear(state_dim, vocab_size)

        self.softmax = nn.Softmax(dim=-1)

    def forward(self, brain_state):

        logits = self.encoder(brain_state)

        symbolic_distribution = self.softmax(logits)

        token = torch.argmax(symbolic_distribution)

        return token, symbolic_distribution
```

---

## Función cognitiva

Este módulo permite que el sistema genere **representaciones conceptuales internas**.

Ejemplo conceptual:

```
patrón neuronal → token simbólico → concepto
```

Esto facilita:

* razonamiento abstracto
* memoria conceptual
* comunicación con sistemas simbólicos

---

# 3. Modelo de conciencia computacional (integración global)

La conciencia puede modelarse como un proceso de **integración global de información** entre múltiples módulos cerebrales.

Una de las teorías influyentes es **Global Workspace Theory**.

---

## Principio del workspace global

Múltiples procesos especializados compiten por acceso a un **espacio global de difusión**.

```
módulos cognitivos
↓
competencia
↓
selección
↓
difusión global
```

El contenido seleccionado se vuelve **globalmente accesible**.

---

## Arquitectura en CPEA

El workspace recibe información de:

* percepción
* memoria episódica
* modelo generativo
* atención

---

## Implementación

### global_workspace.py

```python
import torch
import torch.nn as nn

class GlobalWorkspace(nn.Module):

    def __init__(self, input_dim, workspace_dim=256):

        super().__init__()

        self.project = nn.Linear(input_dim, workspace_dim)

        self.broadcast = nn.Linear(workspace_dim, input_dim)

    def forward(self, modules_outputs):

        combined = torch.cat(modules_outputs, dim=-1)

        workspace = torch.relu(self.project(combined))

        broadcast_signal = self.broadcast(workspace)

        return workspace, broadcast_signal
```

---

## Dinámica de conciencia simulada

El ciclo sería:

```
procesos cognitivos
↓
integración en workspace
↓
selección de contenido dominante
↓
difusión global
```

Esto crea una forma de **estado cognitivo integrado**.

---

# Integración completa en CPEA

Con todos los módulos añadidos, la arquitectura queda:

```
sensores
↓
predictive cortex
↓
conectoma dinámico
↓
memoria episódica (hipocampo)
↓
modelo generativo del mundo
↓
sistema de atención
↓
lenguaje interno simbólico
↓
workspace global
↓
acciones
```

---

# Ciclo cognitivo completo

En cada iteración:

```
1 percepción
2 predicción
3 cálculo de error
4 actualización del conectoma
5 recuperación de memoria
6 simulación del mundo
7 atención selectiva
8 representación simbólica
9 integración global
10 selección de acción
```

---

# Propiedades emergentes posibles

La arquitectura permite estudiar fenómenos como:

* atención dinámica
* aprendizaje contextual
* planificación
* representación conceptual
* integración global de información

---

# Alcance científico del sistema

Una plataforma que combine:

* conectoma humano real
* dinámica spiking
* plasticidad STDP
* metabolismo neuronal
* fisiología corporal
* predictive processing
* memoria episódica
* world model
* atención neuronal
* representación simbólica
* integración global

se aproxima a una **arquitectura cognitiva neuroinspirada completa**.

---

# Posicionamiento respecto a grandes proyectos

Iniciativas como:

* Blue Brain Project
* Human Brain Project

se centran principalmente en simulación biológica detallada.

La diferencia clave del enfoque CPEA sería:

```
neurodinámica
+
cognición funcional
+
aprendizaje continuo
+
interacción con EEG real
```

---

✅ Con estos tres módulos añadidos, **CPEA puede considerarse una arquitectura experimental de mente artificial basada en neurodinámica multiescala**.

---
