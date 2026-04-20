import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

# ============================================================
# 🔷 METFI — Entorno (simulación toroidal simplificada)
# ============================================================

class METFIEnvironment:
    def __init__(self, dim=16):
        self.dim = dim
        self.state = np.random.randn(dim)

    def step(self, action):
        """
        Dinámica no lineal simplificada (proxy toroidal)
        """
        noise = np.random.normal(0, 0.05, self.dim)

        # Dinámica tipo oscilador acoplado
        self.state = np.tanh(self.state + 0.1 * action + noise)

        return self.state


# ============================================================
# 🔵 CPEA — EEG → embeddings + coherencia
# ============================================================

class CPEAInterface:
    def __init__(self, input_dim=32, embed_dim=16):
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, embed_dim)
        )

    def encode(self, eeg_signal):
        eeg_tensor = torch.tensor(eeg_signal, dtype=torch.float32)
        return self.encoder(eeg_tensor)

    def compute_coherence(self, embedding, prediction):
        """
        Coherencia = similitud coseno
        """
        embedding = embedding.detach()
        prediction = prediction.detach()

        cos = nn.functional.cosine_similarity(embedding, prediction, dim=0)
        return cos.item()


# ============================================================
# 🔶 TAE — Aprendizaje por excepción
# ============================================================

class TAEEngine:
    def __init__(self, threshold=0.7):
        self.threshold = threshold

    def is_exception(self, coherence):
        """
        Detecta eventos relevantes
        """
        return coherence < self.threshold


# ============================================================
# 🤖 AGI Core (modelo simple)
# ============================================================

class AGICore(nn.Module):
    def __init__(self, dim=16):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(dim, 32),
            nn.ReLU(),
            nn.Linear(32, dim)
        )

    def forward(self, x):
        return self.model(x)


# ============================================================
# 🔄 SYSTEM LOOP
# ============================================================

class SystemLoop:
    def __init__(self):
        self.metfi = METFIEnvironment()
        self.cpea = CPEAInterface()
        self.tae = TAEEngine()
        self.agi = AGICore()

        self.optimizer = optim.Adam(self.agi.parameters(), lr=1e-3)
        self.loss_fn = nn.MSELoss()

        self.internal_state = torch.zeros(16)

    def simulate_eeg(self):
        """
        EEG simulado (placeholder realista)
        """
        return np.random.randn(32)

    def run_step(self, step_id):
        # ----------------------------------------------------
        # 1. Entrada humana (EEG)
        # ----------------------------------------------------
        eeg = self.simulate_eeg()
        embedding = self.cpea.encode(eeg)

        # ----------------------------------------------------
        # 2. Predicción AGI
        # ----------------------------------------------------
        prediction = self.agi(self.internal_state)

        # ----------------------------------------------------
        # 3. Coherencia
        # ----------------------------------------------------
        coherence = self.cpea.compute_coherence(embedding, prediction)

        # ----------------------------------------------------
        # 4. TAE — detección de excepción
        # ----------------------------------------------------
        exception = self.tae.is_exception(coherence)

        # ----------------------------------------------------
        # 5. Aprendizaje (solo si hay excepción)
        # ----------------------------------------------------
        if exception:
            loss = self.loss_fn(prediction, embedding)

            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
        else:
            loss = torch.tensor(0.0)

        # ----------------------------------------------------
        # 6. Acción hacia entorno (METFI)
        # ----------------------------------------------------
        action = prediction.detach().numpy()
        env_state = self.metfi.step(action)

        # ----------------------------------------------------
        # 7. Actualización estado interno
        # ----------------------------------------------------
        self.internal_state = torch.tensor(env_state, dtype=torch.float32)

        # ----------------------------------------------------
        # 8. Logging
        # ----------------------------------------------------
        print(f"[Step {step_id}] "
              f"Coherence={coherence:.3f} | "
              f"Exception={exception} | "
              f"Loss={loss.item():.4f}")

    def run(self, steps=100):
        for i in range(steps):
            self.run_step(i)


# ============================================================
# 🚀 MAIN
# ============================================================

if __name__ == "__main__":
    system = SystemLoop()
    system.run(steps=200)
