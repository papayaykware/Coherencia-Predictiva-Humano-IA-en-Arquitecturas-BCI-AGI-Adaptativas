# ============================================
# CPEA–METFI SIMULATION NOTEBOOK (REPRODUCIBLE)
# ============================================

# This notebook implements a coupled system:
# - Electromagnetic vacuum field (Phi)
# - Cognitive field (Psi)
# - Multi-agent cognitive network

# Dependencies
import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

# Device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# PARAMETERS
# =========================

GRID_SIZE = 64
DT = 0.01
STEPS = 500

alpha = -0.1
beta = 0.05
gamma = 0.1

D = 0.2
kappa = 0.3

NUM_AGENTS = 50
omega = 0.1
xi = 0.2

# =========================
# UTILS
# =========================

def laplacian(field):
    return (
        -4 * field
        + torch.roll(field, 1, 0)
        + torch.roll(field, -1, 0)
        + torch.roll(field, 1, 1)
        + torch.roll(field, -1, 1)
    )

# =========================
# VACUUM FIELD MODEL
# =========================

class VacuumField(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, Phi, E, B):
        return (
            laplacian(Phi)
            + alpha * Phi
            + beta * Phi**3
            - gamma * (E**2 - B**2)
        )

# =========================
# COGNITIVE FIELD MODEL
# =========================

class CognitiveField(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, Psi, Phi):
        return (
            D * laplacian(Psi)
            + Psi * (1 - Psi**2)  # non-linear term
            + kappa * Phi * Psi
        )

# =========================
# AGENT MODEL
# =========================

class AgentSystem:
    def __init__(self, num_agents):
        self.num_agents = num_agents
        self.states = torch.randn(num_agents, device=DEVICE)
        self.W = torch.randn(num_agents, num_agents, device=DEVICE) * 0.1

    def step(self, Phi_field):
        new_states = []
        for i in range(self.num_agents):
            interaction = torch.sum(self.W[i] * self.states)
            field_influence = xi * Phi_field.mean()
            dpsi = -omega * self.states[i] + interaction + field_influence
            new_states.append(self.states[i] + DT * dpsi)
        self.states = torch.stack(new_states)

# =========================
# INITIALIZATION
# =========================

Phi = torch.randn(GRID_SIZE, GRID_SIZE, device=DEVICE) * 0.1
Psi = torch.randn(GRID_SIZE, GRID_SIZE, device=DEVICE) * 0.1

E = torch.randn(GRID_SIZE, GRID_SIZE, device=DEVICE) * 0.1
B = torch.randn(GRID_SIZE, GRID_SIZE, device=DEVICE) * 0.1

vacuum_model = VacuumField().to(DEVICE)
cognitive_model = CognitiveField().to(DEVICE)
agents = AgentSystem(NUM_AGENTS)

# =========================
# SIMULATION LOOP
# =========================

phi_history = []
psi_history = []
coherence_history = []

for step in range(STEPS):
    dPhi = vacuum_model(Phi, E, B)
    dPsi = cognitive_model(Psi, Phi)

    Phi = Phi + DT * dPhi
    Psi = Psi + DT * dPsi

    agents.step(Phi)

    # coherence metric
    coherence = torch.std(agents.states).item()

    if step % 10 == 0:
        phi_history.append(Phi.mean().item())
        psi_history.append(Psi.mean().item())
        coherence_history.append(coherence)

# =========================
# VISUALIZATION
# =========================

plt.figure()
plt.plot(phi_history)
plt.title("Vacuum Field Mean")
plt.show()

plt.figure()
plt.plot(psi_history)
plt.title("Cognitive Field Mean")
plt.show()

plt.figure()
plt.plot(coherence_history)
plt.title("Agent Coherence")
plt.show()

# =========================
# FINAL STATE SNAPSHOT
# =========================

plt.figure()
plt.imshow(Phi.detach().cpu().numpy())
plt.title("Final Phi Field")
plt.colorbar()
plt.show()

plt.figure()
plt.imshow(Psi.detach().cpu().numpy())
plt.title("Final Psi Field")
plt.colorbar()
plt.show()

print("Simulation complete.")
