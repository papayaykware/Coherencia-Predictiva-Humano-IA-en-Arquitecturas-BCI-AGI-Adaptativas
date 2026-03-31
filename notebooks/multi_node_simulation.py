import torch
from core.eeg_simulator import EEGSimulator
from models.lstm_model import LSTMPredictor
from tae.tae_module import TAEModule

from global_field.field_model import GlobalField
from global_field.coupling import FieldCoupling
from global_field.coherence_metric import coherence_correlation

NUM_NODES = 3

# Inicialización
simulators = [EEGSimulator() for _ in range(NUM_NODES)]
models = [LSTMPredictor() for _ in range(NUM_NODES)]
tae_modules = [TAEModule() for _ in range(NUM_NODES)]

field = GlobalField(num_nodes=NUM_NODES)
coupling = FieldCoupling()

node_errors = []

# Generación y procesamiento
for i in range(NUM_NODES):
    data = torch.tensor(simulators[i].generate(), dtype=torch.float32).unsqueeze(0)
    pred = models[i](data)
    _, error = tae_modules[i].detect(data, pred)
    node_errors.append(error)

node_errors = torch.stack(node_errors)

# 🔵 Actualizar campo global
field_state = field.update(node_errors)

# 🟣 Aplicar acoplamiento
coupled_states = coupling.apply(node_errors, field_state)

# 🟡 Métrica de coherencia
coherence = coherence_correlation(node_errors)

print("Field state:", field_state)
print("Coherence:", coherence)
