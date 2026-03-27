import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

# =========================
# 1. EEG SINTÉTICO
# =========================

def generate_eeg(batch_size=32, seq_len=100, channels=8):
    t = torch.linspace(0, 10, seq_len)
    eeg = []

    for _ in range(batch_size):
        signal = []
        for c in range(channels):
            freq = torch.rand(1) * 5 + 1
            phase = torch.rand(1) * 2 * np.pi
            wave = torch.sin(freq * t + phase)

            # No linealidad + ruido
            nonlinear = torch.tanh(wave * 2)
            noise = 0.2 * torch.randn(seq_len)

            signal.append(nonlinear + noise)

        eeg.append(torch.stack(signal, dim=1))

    return torch.stack(eeg)  # [B, T, C]

# =========================
# 2. MODELO AGI (Predictor)
# =========================

class EEGPredictor(nn.Module):
    def __init__(self, channels, hidden_dim=64):
        super().__init__()
        self.lstm = nn.LSTM(channels, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, channels)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out)

# =========================
# 3. MÓDULO TAE
# =========================

def tae_loss(error, threshold=0.5, p=2):
    """
    Detecta excepciones (errores grandes)
    """
    mask = (torch.abs(error) > threshold).float()
    weights = 1.0 + 5.0 * mask  # amplificación
    return torch.mean(weights * (torch.abs(error) ** p))

# =========================
# 4. MÉTRICAS CPEA
# =========================

def entropy(x):
    var = torch.var(x, dim=[1,2])
    return torch.log(var + 1e-6).mean()

def mutual_info_proxy(x, x_pred):
    # Proxy simple: correlación negativa del error
    return -torch.mean((x - x_pred)**2)

def kl_divergence(x, x_pred):
    mu1 = x.mean()
    mu2 = x_pred.mean()
    var1 = x.var()
    var2 = x_pred.var()

    return torch.log(var2/var1 + 1e-6) + (var1 + (mu1-mu2)**2)/(var2 + 1e-6)

# =========================
# 5. ENTRENAMIENTO + Φ(t)
# =========================

device = "cuda" if torch.cuda.is_available() else "cpu"

model = EEGPredictor(channels=8).to(device)
optimizer = optim.Adam(model.parameters(), lr=1e-3)

alpha, beta, gamma, delta = 1.0, 0.5, 1.2, 0.3

for epoch in range(50):

    x = generate_eeg().to(device)
    
    x_pred = model(x)

    error = x - x_pred

    # Componentes ecuación
    I = mutual_info_proxy(x, x_pred)
    S = entropy(x)
    TAE = tae_loss(error)
    KL = kl_divergence(x, x_pred)

    # Ecuación CPEA (Φ)
    phi = alpha * I - beta * S + gamma * TAE - delta * KL

    loss = -phi  # maximizar Φ

    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    if epoch % 10 == 0:
        print(f"Epoch {epoch}")
        print(f"Φ: {phi.item():.4f}")
        print(f"I: {I.item():.4f} | S: {S.item():.4f} | TAE: {TAE.item():.4f} | KL: {KL.item():.4f}")
        print("------")
