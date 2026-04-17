import numpy as np
import torch
import torch.nn as nn
import time


# =========================================================
# 1. EEG ENCODER
# =========================================================

class EEGEncoder(nn.Module):
    def __init__(self, input_dim=128, embed_dim=64):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Linear(128, embed_dim)
        )

    def forward(self, x):
        return self.model(x)


# =========================================================
# 2. AGI INTERFACE (SIMULADOR BASE)
# =========================================================

class AGISimulator(nn.Module):
    def __init__(self, embed_dim=64):
        super().__init__()
        self.state = torch.randn(embed_dim)

    def forward(self, input_embedding):
        # Simulación simple: mezcla estado interno + input
        self.state = 0.9 * self.state + 0.1 * input_embedding.detach()
        return self.state

    def act(self):
        # Acción abstracta hacia METFI
        return torch.tanh(self.state)


# =========================================================
# 3. COHERENCE (ICP)
# =========================================================

def compute_icp(eeg_emb, agi_emb):
    """
    Índice de Coherencia Predictiva (versión inicial)
    Cosine similarity + penalización de variabilidad
    """
    cos = nn.functional.cosine_similarity(eeg_emb, agi_emb, dim=0)
    stability = 1.0 / (1.0 + torch.std(eeg_emb - agi_emb))
    icp = 0.7 * cos + 0.3 * stability
    return icp


# =========================================================
# 4. TAE (MODULADOR)
# =========================================================

class TAEModule:
    def __init__(self):
        self.prev_icp = None

    def compute_signal(self, icp, prediction_error):
        if self.prev_icp is None:
            delta_icp = 0.0
        else:
            delta_icp = icp - self.prev_icp

        self.prev_icp = icp

        # Señal combinada
        tae_signal = (
            0.5 * prediction_error +
            0.3 * (1 - icp) +
            0.2 * abs(delta_icp)
        )

        return tae_signal.item()


# =========================================================
# 5. METFI ENVIRONMENT (SIMPLIFICADO)
# =========================================================

class METFIEnvironment:
    def __init__(self, dim=64):
        self.state = np.random.randn(dim)

    def step(self, action):
        """
        action: tensor AGI
        """
        action_np = action.detach().numpy()

        # Dinámica no lineal simplificada
        perturbation = np.sin(self.state) * 0.1
        self.state = self.state + action_np * 0.05 + perturbation

        return torch.tensor(self.state, dtype=torch.float32)


# =========================================================
# 6. CONTINUAL LEARNING HOOK (AVALANCHE READY)
# =========================================================

class ContinualLearner:
    def __init__(self, model, lr=1e-3):
        self.model = model
        self.optimizer = torch.optim.Adam(model.parameters(), lr=lr)

    def step(self, loss):
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()


# =========================================================
# 7. SYSTEM LOOP
# =========================================================

class CPEASystem:
    def __init__(self, input_dim=128, embed_dim=64):

        self.device = torch.device("cpu")

        self.eeg_encoder = EEGEncoder(input_dim, embed_dim).to(self.device)
        self.agi = AGISimulator(embed_dim).to(self.device)
        self.tae = TAEModule()
        self.env = METFIEnvironment(embed_dim)

        self.learner = ContinualLearner(self.eeg_encoder)

    def process_step(self, eeg_signal):
        """
        Ejecuta un ciclo completo del sistema
        """

        # ---------------------------
        # 1. EEG → Embedding
        # ---------------------------
        eeg_tensor = torch.tensor(eeg_signal, dtype=torch.float32)
        eeg_emb = self.eeg_encoder(eeg_tensor)

        # ---------------------------
        # 2. AGI forward
        # ---------------------------
        agi_emb = self.agi(eeg_emb)

        # ---------------------------
        # 3. ICP
        # ---------------------------
        icp = compute_icp(eeg_emb, agi_emb)

        # ---------------------------
        # 4. Error de predicción
        # ---------------------------
        prediction_error = torch.mean((eeg_emb - agi_emb) ** 2)

        # ---------------------------
        # 5. TAE
        # ---------------------------
        tae_signal = self.tae.compute_signal(icp.item(), prediction_error.item())

        # ---------------------------
        # 6. Acción AGI → METFI
        # ---------------------------
        action = self.agi.act()
        env_state = self.env.step(action)

        # ---------------------------
        # 7. Loss (objetivo: coherencia)
        # ---------------------------
        loss = prediction_error * (1 + tae_signal)

        # ---------------------------
        # 8. Aprendizaje continuo
        # ---------------------------
        self.learner.step(loss)

        return {
            "icp": icp.item(),
            "prediction_error": prediction_error.item(),
            "tae_signal": tae_signal,
            "env_state_mean": env_state.mean().item()
        }


# =========================================================
# 8. LOOP EJECUCIÓN
# =========================================================

def run_system(steps=100):

    system = CPEASystem()

    for step in range(steps):

        # Simulación EEG (ruido estructurado)
        eeg_signal = np.random.randn(128)

        output = system.process_step(eeg_signal)

        print(f"[{step}] ICP: {output['icp']:.3f} | "
              f"Err: {output['prediction_error']:.3f} | "
              f"TAE: {output['tae_signal']:.3f}")

        time.sleep(0.05)


if __name__ == "__main__":
    run_system(200)
