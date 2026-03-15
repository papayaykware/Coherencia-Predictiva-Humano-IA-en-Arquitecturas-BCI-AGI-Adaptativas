# 🧠 CPEA Cognitive Field Simulation

### PyTorch Implementation

---

## Notebook Overview

Este notebook simula la dinámica de la ecuación:

[
\frac{\partial \Psi(x,t)}{\partial t}
=====================================

D\nabla^2 \Psi
+
\alpha P(x,t)
-------------

\beta E(x,t)
+
\gamma S(x,t)
+
\delta C(x,t)
]

donde:

* Ψ = campo cognitivo
* P = generación predictiva
* E = error de predicción
* S = sincronización
* C = acoplamiento cognitivo

---

# 1️⃣ Install Dependencies

```python
!pip install torch numpy matplotlib
```

---

# 2️⃣ Import Libraries

```python
import torch
import numpy as np
import matplotlib.pyplot as plt
```

---

# 3️⃣ Simulation Parameters

```python
grid_size = 100
time_steps = 300

D = 0.2      # difusión cognitiva
alpha = 0.6  # generación predictiva
beta = 0.4   # corrección error
gamma = 0.3  # sincronización
delta = 0.2  # acoplamiento agentes

device = "cuda" if torch.cuda.is_available() else "cpu"
```

---

# 4️⃣ Initialize Cognitive Field

```python
Psi = torch.randn(grid_size, grid_size, device=device) * 0.1
```

---

# 5️⃣ Laplacian Operator

Difusión espacial del campo cognitivo.

```python
def laplacian(field):

    return (
        -4 * field
        + torch.roll(field, 1, 0)
        + torch.roll(field, -1, 0)
        + torch.roll(field, 1, 1)
        + torch.roll(field, -1, 1)
    )
```

---

# 6️⃣ Predictive Generation Function

Simula generación de hipótesis internas.

```python
def predictive_drive(field):

    noise = torch.randn_like(field) * 0.05
    return torch.tanh(field) + noise
```

---

# 7️⃣ Prediction Error

Diferencia entre predicción y entrada sensorial.

```python
def prediction_error(field):

    sensory_input = torch.sin(field)
    return field - sensory_input
```

---

# 8️⃣ Synchronization Term

Modelo simple de sincronía neuronal.

```python
def synchronization(field):

    mean_phase = torch.mean(field)
    return mean_phase - field
```

---

# 9️⃣ Cognitive Coupling

Interacción entre múltiples agentes cognitivos.

```python
def coupling(field):

    shifted = torch.roll(field, shifts=5, dims=0)
    return shifted - field
```

---

# 🔟 Simulation Loop

```python
history = []

for t in range(time_steps):

    diffusion = D * laplacian(Psi)

    P = alpha * predictive_drive(Psi)

    E = -beta * prediction_error(Psi)

    S = gamma * synchronization(Psi)

    C = delta * coupling(Psi)

    dPsi = diffusion + P + E + S + C

    Psi = Psi + 0.05 * dPsi

    if t % 10 == 0:
        history.append(Psi.detach().cpu().numpy())
```

---

# 11️⃣ Visualization

```python
plt.figure(figsize=(6,6))
plt.imshow(history[-1], cmap="plasma")
plt.colorbar()
plt.title("Cognitive Field State")
plt.show()
```

---

# 12️⃣ Field Evolution Animation

```python
from matplotlib import animation

fig = plt.figure()

frames = []

for state in history:
    frame = plt.imshow(state, animated=True, cmap="plasma")
    frames.append([frame])

ani = animation.ArtistAnimation(fig, frames, interval=100)

plt.show()
```

---

# 13️⃣ Emergent Metrics

Medimos propiedades globales del campo.

```python
energy = []
entropy = []

for state in history:

    s = torch.tensor(state)

    energy.append(torch.mean(s**2).item())

    p = torch.softmax(s.flatten(), dim=0)

    entropy.append(-torch.sum(p * torch.log(p)).item())
```

---

# 14️⃣ Plot Dynamics

```python
plt.figure()

plt.plot(energy, label="Field Energy")
plt.plot(entropy, label="Cognitive Entropy")

plt.legend()
plt.title("Global Cognitive Metrics")

plt.show()
```

---

# 🧪 Possible Experiments

Puedes experimentar cambiando parámetros:

| Parámetro | Interpretación         |
| --------- | ---------------------- |
| D         | propagación cognitiva  |
| α         | creatividad/predicción |
| β         | estabilidad            |
| γ         | sincronía              |
| δ         | inteligencia colectiva |

---

# 🧠 Multi-Agent Extension

Simular múltiples agentes:

```python
agents = 5

fields = torch.randn(agents, grid_size, grid_size)
```

Campo global:

```python
global_field = torch.mean(fields, dim=0)
```

---

# 📊 Research Directions

Este modelo permite explorar:

* sincronización entre cerebros
* acoplamiento humano-AGI
* emergencia de inteligencia colectiva
* dinámica predictiva distribuida

---
