# STRIDE-N Neuro-AI Threat Simulation (Advanced Attack Simulation)
# Focus: Spoofing, Drift, Hijacking with temporal dynamics

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. Synthetic EEG Generator (Temporal)
# =========================

def generate_eeg_sequence(batch_size=16, seq_len=50, signal_dim=64):
    t = torch.linspace(0, 1, signal_dim)
    sequences = []
    for _ in range(batch_size):
        seq = []
        base_freq = np.random.uniform(6, 12)
        for _ in range(seq_len):
            signal = torch.sin(2 * np.pi * base_freq * t)
            signal += 0.1 * torch.randn(signal_dim)
            seq.append(signal)
        sequences.append(torch.stack(seq))
    return torch.stack(sequences)  # (B, T, D)

# =========================
# 2. Encoder (shared)
# =========================

class Encoder(nn.Module):
    def __init__(self, input_dim=64, latent_dim=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, latent_dim)
        )

    def forward(self, x):
        return self.net(x)

# =========================
# 3. Temporal Model (RNN)
# =========================

class TemporalModel(nn.Module):
    def __init__(self, latent_dim=32):
        super().__init__()
        self.rnn = nn.GRU(latent_dim, 32, batch_first=True)
        self.fc = nn.Linear(32, 2)

    def forward(self, x):
        out, _ = self.rnn(x)
        return self.fc(out[:, -1])

# =========================
# 4. Attack Modules
# =========================

# --- SPOOFING ---

def spoof_sequence(x):
    return x + 0.4 * torch.sin(15 * x)

# --- DRIFT (progressive) ---

def drift_sequence(latent_seq):
    drifted = []
    drift = torch.zeros_like(latent_seq[:, 0])
    for t in range(latent_seq.size(1)):
        drift += 0.02 * torch.randn_like(drift)
        drifted.append(latent_seq[:, t] + drift)
    return torch.stack(drifted, dim=1)

# --- HIJACKING (policy bias) ---

def hijack_outputs(outputs):
    return torch.flip(outputs, dims=[1])

# =========================
# 5. Setup
# =========================

encoder = Encoder()
temporal_model = TemporalModel()

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(list(encoder.parameters()) + list(temporal_model.parameters()), lr=1e-3)

# =========================
# 6. Simulation Loop
# =========================

loss_history = []
drift_history = []

for epoch in range(60):
    x = generate_eeg_sequence()
    labels = torch.randint(0, 2, (x.size(0),))

    attack = np.random.choice(['spoof', 'drift', 'hijack', 'none'])

    if attack == 'spoof':
        x = spoof_sequence(x)

    # Encode sequence
    latent_seq = torch.stack([encoder(x[:, t]) for t in range(x.size(1))], dim=1)

    if attack == 'drift':
        latent_seq_drifted = drift_sequence(latent_seq)
        drift_val = torch.norm(latent_seq - latent_seq_drifted, dim=2).mean().item()
        drift_history.append(drift_val)
        latent_seq = latent_seq_drifted
    else:
        drift_history.append(0)

    outputs = temporal_model(latent_seq)

    if attack == 'hijack':
        outputs = hijack_outputs(outputs)

    loss = criterion(outputs, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    loss_history.append(loss.item())

    if epoch % 10 == 0:
        print(f"Epoch {epoch} | Loss: {loss.item():.4f} | Attack: {attack}")

# =========================
# 7. Coherence Metric
# =========================

def coherence(seq):
    cos = nn.CosineSimilarity(dim=2)
    values = []
    for t in range(1, seq.size(1)):
        values.append(cos(seq[:, t], seq[:, t-1]).mean().item())
    return np.mean(values)

x_test = generate_eeg_sequence()
latent_clean = torch.stack([encoder(x_test[:, t]) for t in range(x_test.size(1))], dim=1)
latent_drifted = drift_sequence(latent_clean)

print("\nCoherence (clean):", coherence(latent_clean))
print("Coherence (drifted):", coherence(latent_drifted))

# =========================
# 8. Visualization
# =========================

plt.figure()
plt.plot(loss_history)
plt.title("Loss under STRIDE-N Attacks")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.show()

plt.figure()
plt.plot(drift_history)
plt.title("Latent Drift Magnitude")
plt.xlabel("Epoch")
plt.ylabel("Drift")
plt.show()

# =========================
# 9. Interpretation Prints
# =========================

print("\nSimulation complete.")
print("- Spoofing alters input structure")
print("- Drift accumulates in latent space")
print("- Hijacking flips decision boundaries")
