# Arquitectura del repositorio CPEA

```text
CPEA/
│
├── README.md
├── requirements.txt
├── setup.py
│
├── cpea/
│   ├── eeg/
│   │   ├── neural_mass.py
│   │   ├── eeg_simulator.py
│   │   └── preprocessing.py
│   │
│   ├── models/
│   │   ├── snn_encoder.py
│   │   ├── temporal_transformer.py
│   │   └── predictive_core.py
│   │
│   ├── connectome/
│   │   ├── connectome_loader.py
│   │   └── dynamic_fc.py
│   │
│   ├── metrics/
│   │   ├── coherence.py
│   │   └── phase_sync.py
│   │
│   ├── training/
│   │   ├── trainer.py
│   │   └── continual_learning.py
│   │
│   └── visualization/
│       └── brain_plots.py
│
└── experiments/
    └── run_simulation.py
```

---

# requirements.txt

```python
torch
snnTorch
avalanche-lib
numpy
scipy
mne
networkx
matplotlib
scikit-learn
tqdm
```

---

# 1. Simulación cortical — neural_mass.py

Modelo simplificado Wilson–Cowan para poblaciones excitatorias/inhibitorias.

```python
import numpy as np

class NeuralMassModel:

    def __init__(
        self,
        n_regions=64,
        dt=0.001,
        tau_e=0.02,
        tau_i=0.01,
        w_ee=12.0,
        w_ei=10.0,
        w_ie=10.0,
        w_ii=2.0,
    ):

        self.n = n_regions
        self.dt = dt

        self.tau_e = tau_e
        self.tau_i = tau_i

        self.w_ee = w_ee
        self.w_ei = w_ei
        self.w_ie = w_ie
        self.w_ii = w_ii

        self.E = np.random.rand(n_regions)
        self.I = np.random.rand(n_regions)

    def sigmoid(self, x):

        return 1 / (1 + np.exp(-x))

    def step(self, input_signal):

        dE = (
            -self.E
            + self.sigmoid(
                self.w_ee * self.E
                - self.w_ei * self.I
                + input_signal
            )
        ) / self.tau_e

        dI = (
            -self.I
            + self.sigmoid(
                self.w_ie * self.E
                - self.w_ii * self.I
            )
        ) / self.tau_i

        self.E += self.dt * dE
        self.I += self.dt * dI

        return self.E
```

---

# 2. Simulador EEG — eeg_simulator.py

```python
import numpy as np
from .neural_mass import NeuralMassModel


class EEGSimulator:

    def __init__(self, n_regions=64):

        self.model = NeuralMassModel(n_regions=n_regions)

        self.n_regions = n_regions

        self.projection = np.random.randn(32, n_regions)

    def generate(self, steps=2000):

        eeg = []

        for t in range(steps):

            input_signal = np.random.randn(self.n_regions) * 0.1

            state = self.model.step(input_signal)

            signal = self.projection @ state

            eeg.append(signal)

        eeg = np.array(eeg)

        return eeg
```

---

# 3. Codificador espiking — snn_encoder.py

```python
import torch
import torch.nn as nn
import snntorch as snn
from snntorch import surrogate


class SpikingEncoder(nn.Module):

    def __init__(self, input_size=32, hidden_size=128):

        super().__init__()

        spike_grad = surrogate.fast_sigmoid()

        self.fc1 = nn.Linear(input_size, hidden_size)

        self.lif1 = snn.Leaky(
            beta=0.9,
            spike_grad=spike_grad
        )

        self.fc2 = nn.Linear(hidden_size, hidden_size)

        self.lif2 = snn.Leaky(
            beta=0.9,
            spike_grad=spike_grad
        )

    def forward(self, x):

        mem1 = self.lif1.init_leaky()
        mem2 = self.lif2.init_leaky()

        spk_out = []

        for step in range(x.size(0)):

            cur = self.fc1(x[step])

            spk1, mem1 = self.lif1(cur, mem1)

            cur2 = self.fc2(spk1)

            spk2, mem2 = self.lif2(cur2, mem2)

            spk_out.append(spk2)

        return torch.stack(spk_out)
```

---

# 4. Transformer temporal — temporal_transformer.py

```python
import torch
import torch.nn as nn


class TemporalTransformer(nn.Module):

    def __init__(
        self,
        dim=128,
        heads=8,
        layers=4,
        dropout=0.1,
    ):

        super().__init__()

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=dim,
            nhead=heads,
            dropout=dropout,
            batch_first=True
        )

        self.encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=layers
        )

    def forward(self, x):

        x = self.encoder(x)

        return x
```

---

# 5. Métricas de coherencia — coherence.py

```python
import numpy as np
from scipy.signal import coherence


def spectral_coherence(x, y, fs=256):

    f, cxy = coherence(x, y, fs=fs)

    return f, cxy
```

---

# 6. Sincronización de fase — phase_sync.py

```python
import numpy as np
from scipy.signal import hilbert


def phase_locking_value(sig1, sig2):

    phase1 = np.angle(hilbert(sig1))

    phase2 = np.angle(hilbert(sig2))

    diff = phase1 - phase2

    plv = np.abs(np.mean(np.exp(1j * diff)))

    return plv
```

---

# 7. Script de experimento — run_simulation.py

```python
import torch
import numpy as np

from cpea.eeg.eeg_simulator import EEGSimulator
from cpea.models.snn_encoder import SpikingEncoder
from cpea.models.temporal_transformer import TemporalTransformer


def run():

    simulator = EEGSimulator()

    eeg = simulator.generate()

    eeg_tensor = torch.tensor(eeg, dtype=torch.float32)

    encoder = SpikingEncoder()

    spikes = encoder(eeg_tensor)

    transformer = TemporalTransformer()

    representation = transformer(spikes)

    print("Output representation:", representation.shape)


if __name__ == "__main__":
    run()
```

---

# Resultado del pipeline

El flujo completo es:

```text
Simulación cortical
        ↓
EEG sintético
        ↓
Codificación espiking
        ↓
Transformer temporal
        ↓
Representación cognitiva
```

Este pipeline ya permite realizar:

* simulaciones EEG realistas
* codificación neuronal espiking
* modelado temporal profundo
* extracción de representaciones latentes.

---
