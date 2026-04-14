"""
ICP (Índice de Coherencia Predictiva)
-------------------------------------

Métrica central del sistema CPEA (BCI–AGI).

Características:
- Vectorizado (PyTorch)
- Compatible con GPU
- Usable como métrica y como loss
- Soporte batch
- Preparado para streaming

Autor: CPEA framework
"""

import torch
import torch.nn.functional as F


# =========================================================
# 🔹 UTILIDADES BÁSICAS
# =========================================================

def normalize_signal(x, eps=1e-8):
    """
    Normaliza señal a media 0 y varianza 1
    """
    mean = x.mean(dim=-1, keepdim=True)
    std = x.std(dim=-1, keepdim=True) + eps
    return (x - mean) / std


# =========================================================
# 🔹 COMPONENTE 1: CORRELACIÓN TEMPORAL (C)
# =========================================================

def temporal_correlation(x, y, eps=1e-8):
    """
    Correlación de Pearson por batch
    
    x, y: (batch, time)
    """
    x = normalize_signal(x, eps)
    y = normalize_signal(y, eps)
    
    corr = torch.mean(x * y, dim=-1)  # (batch,)
    
    return torch.clamp(corr, -1.0, 1.0)


# =========================================================
# 🔹 COMPONENTE 2: ERROR NORMALIZADO (E)
# =========================================================

def normalized_mse(x, y, eps=1e-8):
    """
    MSE normalizado por varianza de x
    """
    var = torch.var(x, dim=-1, keepdim=True) + eps
    mse = torch.mean((x - y) ** 2, dim=-1, keepdim=True)
    
    norm_mse = mse / var
    return norm_mse.squeeze(-1)  # (batch,)


# =========================================================
# 🔹 COMPONENTE 3: COHERENCIA ESPECTRAL (P)
# =========================================================

def spectral_coherence(x, y, eps=1e-8):
    """
    Coherencia espectral basada en FFT
    
    x, y: (batch, time)
    """
    X = torch.fft.rfft(x, dim=-1)
    Y = torch.fft.rfft(y, dim=-1)

    PSD_x = torch.abs(X) ** 2
    PSD_y = torch.abs(Y) ** 2

    numerator = torch.sum(PSD_x * PSD_y, dim=-1)
    denominator = (
        torch.norm(PSD_x, dim=-1) *
        torch.norm(PSD_y, dim=-1) + eps
    )

    coherence = numerator / denominator
    return torch.clamp(coherence, 0.0, 1.0)


# =========================================================
# 🔹 ICP CORE
# =========================================================

def compute_icp(
    x,
    y,
    w1=0.4,
    w2=0.4,
    w3=0.2,
    return_components=False
):
    """
    Calcula ICP
    
    Parámetros:
    - x: señal real EEG (batch, time)
    - y: predicción AGI (batch, time)
    
    Retorna:
    - icp (batch,)
    """
    C = temporal_correlation(x, y)
    E = normalized_mse(x, y)
    P = spectral_coherence(x, y)

    icp = w1 * C + w2 * (1.0 - E) + w3 * P

    if return_components:
        return icp, C, E, P

    return icp


# =========================================================
# 🔹 ICP COMO LOSS (para entrenamiento)
# =========================================================

class ICPLoss(torch.nn.Module):
    """
    Loss basada en ICP (maximizar coherencia)
    """
    def __init__(self, w1=0.4, w2=0.4, w3=0.2):
        super().__init__()
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3

    def forward(self, x, y):
        icp = compute_icp(x, y, self.w1, self.w2, self.w3)
        return -icp.mean()  # maximizar ICP


# =========================================================
# 🔹 ICP ADAPTATIVO (pesos dinámicos)
# =========================================================

def adaptive_weights(C, E, P, alpha=(1.0, 1.0, 1.0)):
    """
    Softmax sobre métricas para ajustar pesos dinámicamente
    """
    m = torch.stack([
        C,
        (1.0 - E),
        P
    ], dim=-1)  # (batch, 3)

    alpha = torch.tensor(alpha, device=m.device)
    scores = m * alpha

    weights = F.softmax(scores, dim=-1)  # (batch, 3)

    return weights


def compute_icp_adaptive(x, y, alpha=(1.0, 1.0, 1.0)):
    """
    ICP con pesos adaptativos
    """
    C = temporal_correlation(x, y)
    E = normalized_mse(x, y)
    P = spectral_coherence(x, y)

    weights = adaptive_weights(C, E, P, alpha)

    icp = (
        weights[:, 0] * C +
        weights[:, 1] * (1.0 - E) +
        weights[:, 2] * P
    )

    return icp, weights


# =========================================================
# 🔹 ICP STREAMING (tiempo real)
# =========================================================

class ICPStreaming:
    """
    Calcula ICP en ventanas deslizantes
    """
    def __init__(self, window_size=256, stride=64):
        self.window_size = window_size
        self.stride = stride

    def compute(self, x, y):
        """
        x, y: (time,)
        """
        T = x.shape[0]
        icp_values = []

        for start in range(0, T - self.window_size + 1, self.stride):
            end = start + self.window_size

            x_win = x[start:end].unsqueeze(0)
            y_win = y[start:end].unsqueeze(0)

            icp = compute_icp(x_win, y_win)
            icp_values.append(icp.item())

        return icp_values


# =========================================================
# 🔹 TEST RÁPIDO
# =========================================================

if __name__ == "__main__":
    torch.manual_seed(42)

    batch = 4
    time = 512

    eeg = torch.randn(batch, time)
    pred = eeg + 0.1 * torch.randn(batch, time)

    icp, C, E, P = compute_icp(eeg, pred, return_components=True)

    print("ICP:", icp)
    print("C:", C)
    print("E:", E)
    print("P:", P)
