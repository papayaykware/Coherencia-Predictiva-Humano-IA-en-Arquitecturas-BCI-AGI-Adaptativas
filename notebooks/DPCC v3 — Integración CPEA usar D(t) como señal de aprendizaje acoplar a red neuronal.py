# ==========================================
# DPCC v2 + EEG PIPELINE (REAL DATA READY)
# ==========================================

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mutual_info_score

# OPTIONAL: EEG loading (EDF via MNE)
try:
    import mne
    MNE_AVAILABLE = True
except:
    MNE_AVAILABLE = False

# -----------------------------
# 1. LOAD EEG DATA
# -----------------------------

def load_eeg(file_path=None, duration=10):
    if MNE_AVAILABLE and file_path:
        raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
        raw.pick_types(eeg=True)
        raw.crop(tmin=0, tmax=duration)
        data = raw.get_data()
        sfreq = raw.info['sfreq']
        return data, sfreq
    else:
        # fallback synthetic EEG-like
        t = np.linspace(0, duration, duration * 100)
        x1 = np.sin(2 * np.pi * 10 * t)
        x2 = np.sin(2 * np.pi * 10 * t + 0.3)
        x3 = np.sin(2 * np.pi * 10 * t + 0.6)

        # anomaly
        mask = (t > duration/2 - 1) & (t < duration/2 + 1)
        x2[mask] = np.random.normal(0, 1, size=mask.sum())

        return np.vstack([x1, x2, x3]), 100

# -----------------------------
# 2. MUTUAL INFORMATION
# -----------------------------

def compute_mi(x, y, bins=16):
    x_binned = np.digitize(x, np.histogram_bin_edges(x, bins=bins))
    y_binned = np.digitize(y, np.histogram_bin_edges(y, bins=bins))
    return mutual_info_score(x_binned, y_binned)

# -----------------------------
# 3. RELATIONAL OPERATOR (MI)
# -----------------------------

def relational_operator(signals):
    n = signals.shape[0]
    R = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                R[i, j] = compute_mi(signals[i], signals[j])

    return R

# -----------------------------
# 4. INVARIANTS
# -----------------------------

def invariants(R):
    n = R.shape[0]
    inv = []

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and j != k and i != k:
                    inv.append(R[i, j] + R[j, k] - R[i, k])

    return np.array(inv)

# -----------------------------
# 5. DPCC CORE
# -----------------------------

def dpcc_operator(inv_series):
    return np.array([
        np.linalg.norm(inv_series[i] - inv_series[i-1])
        for i in range(1, len(inv_series))
    ])

# -----------------------------
# 6. EXCEPTION MEMORY
# -----------------------------

class ExceptionMemory:
    def __init__(self, persistence=5):
        self.persistence = persistence
        self.buffer = []
        self.threshold = None

    def fit(self, D):
        self.threshold = np.mean(D) + np.std(D)

    def update(self, value):
        self.buffer.append(value > self.threshold)
        if len(self.buffer) > self.persistence:
            self.buffer.pop(0)
        return all(self.buffer)

# -----------------------------
# 7. FULL PIPELINE
# -----------------------------

def run_dpcc_eeg(file_path=None):
    data, sfreq = load_eeg(file_path)

    window = int(sfreq * 1)  # 1-second window
    inv_series = []

    for i in range(data.shape[1] - window):
        segment = data[:, i:i+window]
        R = relational_operator(segment)
        inv = invariants(R)
        inv_series.append(inv)

    D = dpcc_operator(inv_series)

    memory = ExceptionMemory()
    memory.fit(D)
    exceptions = np.array([memory.update(d) for d in D])

    t = np.arange(len(D)) / sfreq

    return t, D, exceptions

# -----------------------------
# 8. FIGURES FOR PAPER
# -----------------------------

def plot_paper_figures(t, D, exceptions):
    # Figure 1: DPCC signal
    plt.figure()
    plt.plot(t, D)
    plt.title("DPCC Signal (Invariant Breakdown)")
    plt.xlabel("Time (s)")
    plt.ylabel("D(t)")
    plt.savefig("figure_dpcc_signal.png")

    # Figure 2: Exceptions
    plt.figure()
    plt.plot(t, D)
    plt.scatter(t[exceptions], D[exceptions])
    plt.title("Detected Persistent Exceptions")
    plt.xlabel("Time (s)")
    plt.ylabel("D(t)")
    plt.savefig("figure_exceptions.png")

# -----------------------------
# 9. MAIN
# -----------------------------

if __name__ == "__main__":
    # Put EDF path if available
    file_path = None

    t, D, exceptions = run_dpcc_eeg(file_path)
    plot_paper_figures(t, D, exceptions)

# ==========================================
# DPCC v3 — Integración con CPEA (Aprendizaje)
# ==========================================

import torch
import torch.nn as nn
import torch.optim as optim

# -----------------------------
# 10. MODELO NEURONAL (CPEA CORE)
# -----------------------------

class CPEAModel(nn.Module):
    def __init__(self, input_dim, hidden_dim=32):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, input_dim)
        )

    def forward(self, x):
        return self.net(x)

# -----------------------------
# 11. PREPARACIÓN DE DATOS
# -----------------------------

def prepare_dataset(inv_series):
    X = []
    Y = []
    for i in range(len(inv_series)-1):
        X.append(inv_series[i])
        Y.append(inv_series[i+1])
    return torch.tensor(X, dtype=torch.float32), torch.tensor(Y, dtype=torch.float32)

# -----------------------------
# 12. ENTRENAMIENTO CON SEÑAL DPCC
# -----------------------------

def train_cpea(inv_series, D, epochs=10):
    X, Y = prepare_dataset(inv_series)

    model = CPEAModel(input_dim=X.shape[1])
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss(reduction='none')

    losses = []

    for epoch in range(epochs):
        optimizer.zero_grad()

        preds = model(X)
        base_loss = criterion(preds, Y).mean(dim=1)

        # 🔥 CLAVE: ponderación por ruptura estructural
        weights = torch.tensor(D[:len(base_loss)], dtype=torch.float32)
        weights = (weights - weights.min()) / (weights.max() - weights.min() + 1e-8)

        loss = (base_loss * (1 + weights)).mean()

        loss.backward()
        optimizer.step()

        losses.append(loss.item())

    return model, losses

# -----------------------------
# 13. EJECUCIÓN COMPLETA v3
# -----------------------------

def run_dpcc_cpea():
    t = np.linspace(0, 10, 1000)
    signals = generate_signals(t, anomaly=True)

    window = 80
    inv_series = []

    for i in range(len(t) - window):
        segment = signals[:, i:i+window]
        R = relational_operator(segment)
        inv = invariants(R)
        inv_series.append(inv)

    D = dpcc_operator(inv_series)

    model, losses = train_cpea(inv_series, D)

    return t[:-window-1], D, losses

# -----------------------------
# 14. VISUALIZACIÓN APRENDIZAJE
# -----------------------------

def plot_learning(losses):
    plt.figure()
    plt.plot(losses)
    plt.title("CPEA Learning Curve (Weighted by DPCC)")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.show()

# -----------------------------
# 15. MAIN v3
# -----------------------------

if __name__ == "__main__":
    t, D, losses = run_dpcc_cpea()
    plot_learning(losses)

# ==========================================
# README.md
# ==========================================

"""
# DPCC v2 + EEG Pipeline

## Overview

Pipeline completo para:
- Cargar EEG real (EDF via MNE)
- Aplicar DPCC v2
- Detectar ruptura de coherencia
- Generar figuras para paper

## Uso

```bash
pip install mne numpy matplotlib scikit-learn
python dpcc_eeg_pipeline.py
```

## Input

- EDF EEG file (optional)
- Si no, genera señal sintética

## Output

- figure_dpcc_signal.png
- figure_exceptions.png

## Próximo nivel

- PhysioNet datasets
- Comparativa con métodos clásicos
- Integración PyTorch

"""
# ==========================================
# EXPERIMENTO DPCC vs BASELINE
# ==========================================

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import matplotlib.pyplot as plt

# =========================
# 1. MODELO
# =========================
class Model(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim)
        )

    def forward(self, x):
        return self.net(x)

# =========================
# 2. DATASET
# =========================
def prepare_dataset(inv_series):
    X, Y = [], []
    for i in range(len(inv_series)-1):
        X.append(inv_series[i])
        Y.append(inv_series[i+1])
    return torch.tensor(X, dtype=torch.float32), torch.tensor(Y, dtype=torch.float32)

X, Y = prepare_dataset(inv_series)

# dividir train/test
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
Y_train, Y_test = Y[:split], Y[split:]
D_train = torch.tensor(D[:split], dtype=torch.float32)
D_test = torch.tensor(D[split:], dtype=torch.float32)

# =========================
# 3. ENTRENAMIENTO
# =========================
def train_model(use_dpcc=False, epochs=20):
    model = Model(X.shape[1])
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss(reduction='none')

    losses = []

    for epoch in range(epochs):
        optimizer.zero_grad()

        preds = model(X_train)
        base_loss = criterion(preds, Y_train).mean(dim=1)

        if use_dpcc:
            weights = (D_train - D_train.min()) / (D_train.max() - D_train.min() + 1e-8)
            loss = (base_loss * (1 + weights)).mean()
        else:
            loss = base_loss.mean()

        loss.backward()
        optimizer.step()

        losses.append(loss.item())

    return model, losses

# =========================
# 4. ENTRENAR AMBOS
# =========================
model_base, loss_base = train_model(use_dpcc=False)
model_dpcc, loss_dpcc = train_model(use_dpcc=True)

# =========================
# 5. EVALUACIÓN
# =========================
def evaluate(model):
    preds = model(X_test)
    error = ((preds - Y_test)**2).mean(dim=1)
    return error.detach().numpy()

error_base = evaluate(model_base)
error_dpcc = evaluate(model_dpcc)

# =========================
# 6. FIGURA 1 — CONVERGENCIA
# =========================
plt.figure()
plt.plot(loss_base, label="Baseline")
plt.plot(loss_dpcc, label="DPCC")
plt.legend()
plt.title("Training Convergence")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.savefig("fig_convergence.png")
plt.show()

# =========================
# 7. FIGURA 2 — ERROR TEST
# =========================
plt.figure()
plt.plot(error_base, label="Baseline Error")
plt.plot(error_dpcc, label="DPCC Error")
plt.legend()
plt.title("Test Error Comparison")
plt.xlabel("Time Index")
plt.ylabel("Error")
plt.savefig("fig_test_error.png")
plt.show()

# =========================
# 8. FIGURA 3 — ERROR vs D(t)
# =========================
plt.figure()
plt.scatter(D_test.numpy(), error_base, label="Baseline", alpha=0.5)
plt.scatter(D_test.numpy(), error_dpcc, label="DPCC", alpha=0.5)
plt.legend()
plt.xlabel("D(t) — Invariant Breakdown")
plt.ylabel("Prediction Error")
plt.title("Error vs Structural Breakdown")
plt.savefig("fig_error_vs_dpcc.png")
plt.show()

# =========================
# 9. RESULTADOS NUMÉRICOS
# =========================
print("Baseline final loss:", loss_base[-1])
print("DPCC final loss:", loss_dpcc[-1])

print("Baseline mean error:", np.mean(error_base))
print("DPCC mean error:", np.mean(error_dpcc))
