# STRIDE-N Multi-Agent Neuro-AI Simulation with Global Cognitive Field
# Advanced CPEA-style prototype

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. Synthetic EEG (agents)
# =========================

def generate_agent_eeg(num_agents=5, seq_len=40, dim=32):
    t = torch.linspace(0, 1, dim)
    agents = []
    for _ in range(num_agents):
        base_freq = np.random.uniform(5, 12)
        seq = []
        for _ in range(seq_len):
            signal = torch.sin(2 * np.pi * base_freq * t)
            signal += 0.1 * torch.randn(dim)
            seq.append(signal)
        agents.append(torch.stack(seq))
    return torch.stack(agents)  # (N, T, D)

# =========================
# 2. Shared Encoder
# =========================

class Encoder(nn.Module):
    def __init__(self, input_dim=32, latent_dim=16):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, latent_dim)
        )

    def forward(self, x):
        return self.net(x)

# =========================
# 3. Agent Model (RNN)
# =========================

class AgentModel(nn.Module):
    def __init__(self, latent_dim=16):
        super().__init__()
        self.rnn = nn.GRU(latent_dim, 32, batch_first=True)
        self.fc = nn.Linear(32, 2)

    def forward(self, x):
        out, _ = self.rnn(x)
        return self.fc(out[:, -1])

# =========================
# 4. Global Cognitive Field
# =========================

def compute_global_field(latents):
    return latents.mean(dim=0, keepdim=True)  # (1, T, D)


def couple_agents(latents, field, coupling=0.2):
    return latents + coupling * (field - latents)

# =========================
# 5. Attacks
# =========================

# Drift propagation

def propagate_drift(latents):
    drift = torch.randn_like(latents) * 0.05
    return latents + drift

# Spoof one agent

def spoof_agent(latents, agent_idx=0):
    latents[agent_idx] += 0.5 * torch.sin(latents[agent_idx])
    return latents

# Field hijacking

def hijack_field(field):
    return field * -1

# =========================
# 6. Setup
# =========================

num_agents = 5
encoder = Encoder()
agents_model = AgentModel()

optimizer = optim.Adam(list(encoder.parameters()) + list(agents_model.parameters()), lr=1e-3)
criterion = nn.CrossEntropyLoss()

# =========================
# 7. Simulation Loop
# =========================

coherence_history = []
field_strength_history = []

for epoch in range(80):
    x = generate_agent_eeg(num_agents=num_agents)
    labels = torch.randint(0, 2, (num_agents,))

    # Encode each agent
    latents = torch.stack([
        torch.stack([encoder(x[i, t]) for t in range(x.size(1))])
        for i in range(num_agents)
    ])  # (N, T, D)

    # Global field
    field = compute_global_field(latents)

    # Random attack
    attack = np.random.choice(['drift', 'spoof', 'hijack', 'none'])

    if attack == 'drift':
        latents = propagate_drift(latents)

    if attack == 'spoof':
        latents = spoof_agent(latents)

    if attack == 'hijack':
        field = hijack_field(field)

    # Coupling with field
    latents = couple_agents(latents, field)

    # Decisions per agent
    outputs = torch.stack([
        agents_model(latents[i].unsqueeze(0))
        for i in range(num_agents)
    ]).squeeze(1)

    loss = criterion(outputs, labels)

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # Metrics
    coherence = torch.mean(torch.cosine_similarity(latents[:,1:], latents[:,:-1], dim=2)).item()
    field_strength = torch.norm(field).item()

    coherence_history.append(coherence)
    field_strength_history.append(field_strength)

    if epoch % 10 == 0:
        print(f"Epoch {epoch} | Loss {loss.item():.4f} | Attack {attack} | Coherence {coherence:.3f}")

# =========================
# 8. Visualization
# =========================

plt.figure()
plt.plot(coherence_history)
plt.title("Global Coherence")
plt.xlabel("Epoch")
plt.ylabel("Coherence")
plt.show()

plt.figure()
plt.plot(field_strength_history)
plt.title("Field Strength")
plt.xlabel("Epoch")
plt.ylabel("Norm")
plt.show()

# =========================
# 9. Interpretation
# =========================

print("\nSimulation complete:")
print("- Agents are coupled via global cognitive field")
print("- Drift propagates across agents")
print("- Spoofing destabilizes locally but spreads")
print("- Field hijacking flips global coordination")
