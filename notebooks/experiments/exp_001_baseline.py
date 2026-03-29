from training.train import train
from core.cpea_loop import run_cpea_loop

model, tae = train()

# Simulación
import torch
from core.eeg_simulator import EEGSimulator

sim = EEGSimulator()
data = torch.tensor(sim.generate(), dtype=torch.float32).unsqueeze(0)

preds, anomalies, error = run_cpea_loop(model, tae, data)

print("Anomaly rate:", anomalies.float().mean().item())
