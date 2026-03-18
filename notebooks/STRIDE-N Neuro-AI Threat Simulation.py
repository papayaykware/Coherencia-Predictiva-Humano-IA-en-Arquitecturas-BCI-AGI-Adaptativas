# STRIDE-N Neuro-AI Threat Simulation
# Reproducible PyTorch notebook-style script

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. Synthetic EEG Generator
# =========================

def generate_eeg(batch_size=32, seq_len=128, noise=0.1):
    t = torch.linspace(0, 1, seq_len)
    signals = []
    for _ in range(batch_size):
        freq = np.random.uniform(5, 15)
        signal = torch.sin(2 * np.pi * freq * t)
        signal += noise * torch.randn(seq_len)
        signals.append(signal)
    return torch.stack(signals)

# =========================
# 2. Encoder (Embedding)
# =========================

class Encoder(nn.Module):
    def __init__(self, input_dim=128, latent_dim=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, latent_dim)
        )
    
    def forward(self, x):
        return self.net(x)

# =========================
# 3. Decision Model
# =========================

class DecisionNet(nn.Module):
    def __init__(self, latent_dim=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 2)
        )
    
    def forward(self, x):
        return self.net(x)

# =========================
# 4. STRIDE-N Attack Modules
# =========================

# S: Signal Spoofing

def spoof_signal(x):
    return x + 0.5 * torch.sin(10 * x)

# T: Topological Tampering

def tamper_model(model, epsilon=0.01):
    with torch.no_grad():
        for p in model.parameters():
            p += epsilon * torch.randn_like(p)

# R: Reality Drift

def induce_drift(latent):
    return latent + 0.2 * torch.randn_like(latent)

# I: Information Leakage (simulated probe)

def probe_latent(latent):
    return latent.mean(dim=1)

# D: Denial of Cognition

def cognitive_overload(x):
    noise = torch.randn_like(x) * 2.0
    return x + noise

# E: Control Hijacking

def hijack_labels(labels):
    return 1 - labels

# =========================
# 5. Training Setup
# =========================

encoder = Encoder()
decision = DecisionNet()

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(list(encoder.parameters()) + list(decision.parameters()), lr=1e-3)

# =========================
# 6. Training Loop
# =========================

loss_history = []

for epoch in range(50):
    x = generate_eeg()
    labels = torch.randint(0, 2, (x.size(0),))
    
    # Apply random STRIDE-N attack
    attack_type = np.random.choice(['S','T','R','D','E','None'])
    
    if attack_type == 'S':
        x = spoof_signal(x)
    elif attack_type == 'D':
        x = cognitive_overload(x)
    
    latent = encoder(x)
    
    if attack_type == 'R':
        latent = induce_drift(latent)
    
    if attack_type == 'T':
        tamper_model(decision)
    
    if attack_type == 'E':
        labels = hijack_labels(labels)
    
    outputs = decision(latent)
    loss = criterion(outputs, labels)
    
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    loss_history.append(loss.item())
    
    if epoch % 10 == 0:
        print(f"Epoch {epoch}, Loss: {loss.item():.4f}, Attack: {attack_type}")

# =========================
# 7. Drift Monitoring
# =========================

x_clean = generate_eeg()
latent_clean = encoder(x_clean)
latent_drifted = induce_drift(latent_clean)

drift = torch.norm(latent_clean - latent_drifted, dim=1).mean().item()
print("\nAverage Latent Drift:", drift)

# =========================
# 8. Plot Loss
# =========================

plt.figure()
plt.plot(loss_history)
plt.title("Training Loss under STRIDE-N Attacks")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.show()

# =========================
# 9. Information Leakage Probe
# =========================

leak = probe_latent(latent_clean)
print("\nSample Leakage Signal:", leak[:5])
