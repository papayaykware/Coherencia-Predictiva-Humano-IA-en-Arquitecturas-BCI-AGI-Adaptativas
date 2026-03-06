# 1. Predictive Coherence Index (PCI)

## Definición conceptual

La hipótesis central de CPEA sostiene que puede emerger **coherencia predictiva** cuando un sistema artificial ajusta dinámicamente sus modelos internos a las estructuras temporales presentes en señales EEG.

Para formalizar este fenómeno se introduce el **Predictive Coherence Index (PCI)**.

El PCI mide **la convergencia entre tres variables dinámicas**:

1. precisión de predicción temporal del modelo
2. estabilidad del embedding neuronal
3. reducción del error ante anomalías

Este índice permite evaluar si el sistema está entrando en un **régimen de sincronización predictiva** con la señal neuronal.

---

## Formulación matemática

Sea:

* (x_t) señal EEG observada
* (\hat{x}_t) predicción del modelo
* (e_t = x_t - \hat{x}_t) error de predicción
* (z_t) embedding latente del modelo

Definimos tres métricas:

### 1 Error predictivo normalizado

[
PE = 1 - \frac{1}{T}\sum_{t=1}^{T} \frac{|x_t - \hat{x}_t|}{\sigma_x}
]

donde:

* ( \sigma_x ) es la desviación estándar de la señal EEG.

---

### 2 Estabilidad del embedding

Se mide mediante la autocorrelación del embedding latente:

[
ES = \frac{1}{T}\sum_{t=1}^{T} corr(z_t, z_{t-1})
]

Este término cuantifica **consistencia estructural en el espacio latente**.

---

### 3 Adaptación a excepciones

Se mide la reducción de error tras eventos de anomalía:

[
EA = 1 - \frac{E_{post}}{E_{pre}}
]

donde:

* (E_{pre}) error antes de la anomalía
* (E_{post}) error después de adaptación.

---

## Predictive Coherence Index

Finalmente:

[
PCI = \alpha PE + \beta ES + \gamma EA
]

con:

[
\alpha + \beta + \gamma = 1
]

Valores típicos:

```
α = 0.4
β = 0.3
γ = 0.3
```

---

## Interpretación

| PCI     | Régimen                        |
| ------- | ------------------------------ |
| <0.3    | acoplamiento débil             |
| 0.3–0.6 | sincronización parcial         |
| 0.6–0.8 | coherencia predictiva          |
| >0.8    | acoplamiento cognitivo estable |

---

# 2. Notebook reproducible con EEG real

Archivo recomendado:

```
notebooks/02_eeg_physionet_predictive_coherence.ipynb
```

Código base:

```python
import mne
import torch
import numpy as np
from sklearn.preprocessing import StandardScaler

# dataset EEG público
url = "https://physionet.org/files/eegmmidb/1.0.0/S001/S001R01.edf"

raw = mne.io.read_raw_edf(url, preload=True)

raw.filter(1.,40.)

data = raw.get_data()

signal = data[0]

scaler = StandardScaler()

signal = scaler.fit_transform(signal.reshape(-1,1)).flatten()

# tensor
x = torch.tensor(signal,dtype=torch.float32)

class Predictor(torch.nn.Module):

    def __init__(self):

        super().__init__()

        self.net = torch.nn.Sequential(
            torch.nn.Linear(1,64),
            torch.nn.ReLU(),
            torch.nn.Linear(64,1)
        )

    def forward(self,x):

        return self.net(x)

model = Predictor()

optimizer = torch.optim.Adam(model.parameters(),lr=1e-3)

loss_fn = torch.nn.MSELoss()

for epoch in range(200):

    inp = x[:-1].unsqueeze(1)

    target = x[1:].unsqueeze(1)

    pred = model(inp)

    loss = loss_fn(pred,target)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if epoch % 20 == 0:

        print("epoch",epoch,"loss",loss.item())
```

---

# 3. Cálculo de PCI

Añadir al notebook:

```python
def predictive_coherence(x,pred):

    error = torch.abs(x-pred)

    pe = 1 - torch.mean(error)

    pe = float(pe)

    es = np.corrcoef(pred[:-1].detach(),pred[1:].detach())[0,1]

    ea = 0.5  # placeholder adaptación anomalías

    pci = 0.4*pe + 0.3*es + 0.3*ea

    return pci
```

---

# 4. Figuras científicas del paper

El paper debería incluir **tres figuras principales**.

---

## Figura 1

### Arquitectura CPEA

```
EEG signals
     ↓
Neural Encoder
     ↓
Predictive Embedding
     ↓
Anomaly Detector
     ↓
Continual Learning
     ↓
Adaptive AGI
     ↺ feedback
```

---

## Figura 2

### Dinámica de coherencia

Gráfico temporal:

```
PCI
│
│        ──────────
│      ─
│    ─
│  ─
│─
└────────────────────
         tiempo
```

Representa la **convergencia del sistema hacia coherencia predictiva**.

---

## Figura 3

### Pipeline EEG-AGI

```
EEG acquisition
        ↓
Signal preprocessing
        ↓
Feature extraction
        ↓
Predictive model
        ↓
Exception detection
        ↓
AGI adaptation
```

---

# 5. Programas de seguimiento experimental

## Experimento 1

Evaluar PCI en señales EEG reales durante:

* reposo
* atención
* resolución de tareas

Objetivo:

determinar si la coherencia predictiva depende del estado cognitivo.

---

## Experimento 2

Closed-loop EEG-AGI.

El agente recibe:

```
EEG → predicción → adaptación
```

y genera estímulos adaptativos.

---

## Experimento 3

Comparación con BCI tradicionales.

Evaluar:

* precisión
* estabilidad temporal
* robustez a ruido.

---

# 6. Contribución conceptual del marco CPEA

El marco introduce tres aportaciones principales.

1. formalización cuantitativa de coherencia predictiva
2. integración de aprendizaje por excepción en BCI
3. arquitectura de acoplamiento cognitivo humano-IA.

El concepto central no es simplemente **decodificar la señal cerebral**, sino permitir que el sistema artificial **aprenda a anticipar su dinámica**.

Esta diferencia conceptual transforma el BCI en un **sistema cognitivo acoplado**.

---

# Resumen

* CPEA propone un marco de **coherencia predictiva EEG-AGI**.
* Se introduce una **métrica cuantitativa (PCI)** para medir el acoplamiento.
* Se desarrollan **notebooks reproducibles con EEG real**.
* El sistema se basa en **predicción temporal, detección de excepciones y aprendizaje continuo**.
* La arquitectura define un **bucle cognitivo bidireccional humano-IA**.

---

# Referencias comentadas

**Friston, Karl (2010)**
The Free Energy Principle.
Modelo teórico que describe el cerebro como sistema predictivo que minimiza sorpresa. Constituye una base conceptual para arquitecturas predictivas.

**Kirkpatrick et al. (2017)**
Overcoming catastrophic forgetting in neural networks.
Introduce Elastic Weight Consolidation, mecanismo clave para aprendizaje continuo en redes neuronales.

**Makeig et al. (2004)**
Mining event-related brain dynamics.
Trabajo fundamental sobre análisis de dinámica EEG y componentes independientes.

**Lake et al. (2017)**
Building Machines That Learn and Think Like People.
Propuesta influyente sobre la necesidad de arquitecturas cognitivas más flexibles en IA.

---
