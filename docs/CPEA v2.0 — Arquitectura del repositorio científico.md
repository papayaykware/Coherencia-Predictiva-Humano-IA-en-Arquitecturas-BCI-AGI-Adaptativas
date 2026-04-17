# CPEA v2.0 — Arquitectura del repositorio científico

```
CPEA/
│
├── README.md
├── LICENSE
├── requirements.txt
├── environment.yml
├── setup.py
│
├── configs/
│   ├── model_config.yaml
│   ├── training_config.yaml
│   ├── experiment_registry.yaml
│   └── hcp_config.yaml
│
├── data/
│   ├── raw/
│   │   ├── hcp_connectome/
│   │   └── eeg_datasets/
│   │
│   ├── processed/
│   │   ├── adjacency_matrices/
│   │   ├── eeg_features/
│   │   └── embeddings/
│   │
│   └── loaders/
│       ├── hcp_loader.py
│       ├── eeg_loader.py
│       └── preprocessing.py
│
├── models/
│   ├── eeg_encoder.py
│   ├── connectome_gnn.py
│   ├── predictive_coding_module.py
│   ├── spiking_module.py
│   ├── cognitive_loop.py
│   └── agi_head.py
│
├── training/
│   ├── train_eeg_model.py
│   ├── continual_learning.py
│   ├── avalanche_integration.py
│   └── trainer.py
│
├── experiments/
│   ├── exp_connectome_simulation.py
│   ├── exp_eeg_coherence.py
│   ├── exp_brain_scale_model.py
│   └── experiment_runner.py
│
├── analysis/
│   ├── coherence_analysis.py
│   ├── graph_metrics.py
│   └── statistical_tests.py
│
├── visualization/
│   ├── connectome_3d.py
│   ├── eeg_topography.py
│   ├── coherence_plots.py
│   └── figure_generator.py
│
├── notebooks/
│   ├── 01_hcp_connectome_exploration.ipynb
│   ├── 02_eeg_embedding_learning.ipynb
│   ├── 03_brain_network_simulation.ipynb
│   └── 04_cpea_results_figures.ipynb
│
├── pipeline/
│   ├── reproducible_pipeline.py
│   ├── dataset_builder.py
│   └── experiment_registry.py
│
└── tests/
    ├── test_dataloaders.py
    ├── test_models.py
    └── test_pipeline.py
```

Este repositorio permite **tres escalas de investigación simultáneas**:

1. datos empíricos EEG
2. conectoma real HCP
3. simulación cognitiva

---

# 1. Integración del dataset HCP

El **Human Connectome Project** proporciona:

* matrices de conectividad estructural (DTI)
* conectividad funcional (fMRI)
* parcellations cerebrales (Glasser atlas)

En CPEA se usan para crear **grafo cerebral real**.

### hcp_loader.py

```python
import numpy as np
import networkx as nx

class HCPConnectomeLoader:

    def __init__(self, path):
        self.path = path

    def load_connectivity_matrix(self):

        matrix = np.load(self.path)

        return matrix

    def build_graph(self):

        matrix = self.load_connectivity_matrix()

        G = nx.from_numpy_array(matrix)

        return G
```

Salida:

```
Graph nodes: 360 cortical regions
Edges: weighted structural connectivity
```

Esto se convierte en **base para simulación cognitiva CPEA**.

---

# 2. Encoder EEG para aprendizaje AGI

El EEG se transforma en **embedding cognitivo dinámico**.

### eeg_encoder.py

Arquitectura:

```
EEG signal
   ↓
Conv1D temporal
   ↓
Transformer encoder
   ↓
Latent cognitive embedding
```

Código simplificado:

```python
import torch
import torch.nn as nn

class EEGEncoder(nn.Module):

    def __init__(self, channels=64, embedding_dim=128):

        super().__init__()

        self.conv = nn.Conv1d(channels, 128, kernel_size=5)

        self.transformer = nn.TransformerEncoder(
            nn.TransformerEncoderLayer(
                d_model=128,
                nhead=8
            ),
            num_layers=4
        )

        self.fc = nn.Linear(128, embedding_dim)

    def forward(self, x):

        x = self.conv(x)

        x = self.transformer(x)

        embedding = self.fc(x.mean(dim=2))

        return embedding
```

Salida:

```
EEG → vector cognitivo latente
```

---

# 3. Modelo conectómico (Graph Neural Network)

El cerebro se modela como **grafo dinámico**.

### connectome_gnn.py

```python
import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv

class ConnectomeGNN(nn.Module):

    def __init__(self, in_dim=128, hidden=256):

        super().__init__()

        self.conv1 = GCNConv(in_dim, hidden)
        self.conv2 = GCNConv(hidden, hidden)

    def forward(self, x, edge_index):

        x = self.conv1(x, edge_index)

        x = torch.relu(x)

        x = self.conv2(x, edge_index)

        return x
```

Este modelo permite:

* propagación de actividad neuronal
* simulación de dinámicas cognitivas
* predicción de estados cerebrales.

---

# 4. Bucle cognitivo CPEA

El núcleo del sistema.

### cognitive_loop.py

```python
class CognitiveLoop:

    def __init__(self, eeg_encoder, connectome_model):

        self.eeg_encoder = eeg_encoder
        self.connectome_model = connectome_model

    def step(self, eeg_signal, connectome_graph):

        embedding = self.eeg_encoder(eeg_signal)

        brain_state = self.connectome_model(
            embedding,
            connectome_graph.edge_index
        )

        return brain_state
```

El bucle implementa:

```
percepción EEG
→ representación latente
→ propagación conectómica
→ estado cognitivo emergente
```

---

# 5. Script de entrenamiento EEG

### train_eeg_model.py

```python
import torch
from torch.utils.data import DataLoader

def train(model, dataset):

    loader = DataLoader(dataset, batch_size=32)

    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

    for epoch in range(100):

        for x, y in loader:

            pred = model(x)

            loss = ((pred - y)**2).mean()

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

        print("epoch:", epoch, "loss:", loss.item())
```

---

# 6. Pipeline reproducible de experimentos

Un sistema **tipo NeurIPS reproducibility standard**.

### reproducible_pipeline.py

```python
class ExperimentPipeline:

    def __init__(self, config):

        self.config = config

    def run(self):

        dataset = build_dataset(self.config)

        model = build_model(self.config)

        trainer = Trainer(model, dataset)

        results = trainer.train()

        save_results(results)
```

Esto permite:

```
config.yaml → experimento reproducible
```

---

# 7. Visualización científica tipo Nature

### connectome_3d.py

Genera **conectoma 3D interactivo**.

```python
import plotly.graph_objects as go

def plot_connectome(coords, edges):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter3d(
            x=coords[:,0],
            y=coords[:,1],
            z=coords[:,2],
            mode='markers'
        )
    )

    fig.show()
```

Resultado:

* cerebro 3D
* nodos corticales
* conexiones dinámicas

---

# 8. Notebooks científicos incluidos

### 01_hcp_connectome_exploration.ipynb

Explora conectividad real:

```
degree distribution
small-worldness
modularidad
```

### 02_eeg_embedding_learning.ipynb

Visualiza:

```
embeddings EEG
clusters cognitivos
```

### 03_brain_network_simulation.ipynb

Simulación:

```
actividad neuronal en conectoma
```

### 04_cpea_results_figures.ipynb

Genera figuras:

* coherencia EEG-AGI
* dinámica conectómica
* mapas cerebrales

---

# 9. Pipeline completo del proyecto

Flujo total de CPEA v2.0:

```
EEG signals
   ↓
Encoder profundo
   ↓
Embeddings cognitivos
   ↓
Propagación en conectoma HCP
   ↓
Simulación estado cerebral
   ↓
Predicción cognitiva AGI
```

---

# 10. Métricas científicas incluidas

El repositorio calcula:

* **coherencia EEG**
* **centralidad conectómica**
* **entropía neuronal**
* **synchronization index**

Esto permite producir **figuras comparables a artículos de neurociencia computacional**.

---

# Resultado esperado del repositorio

Capacidades de **CPEA v2.0**:

* simulación conectómica realista
* entrenamiento EEG-AGI
* visualización cerebral 3D
* pipeline reproducible
* notebooks científicos
* integración HCP

Tamaño estimado:

```
~6500 líneas Python
~1000 líneas notebooks
~300 líneas configs
```

---
