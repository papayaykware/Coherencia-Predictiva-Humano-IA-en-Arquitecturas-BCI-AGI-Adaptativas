# ==========================================
# DPCC v2 — Framework No Lineal de Coherencia
# Mutual Information + Transfer Entropy
# ==========================================

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import mutual_info_score

# -----------------------------
# 1. Generador de señales
# -----------------------------

def generate_signals(t, anomaly=False):
    x1 = np.sin(2 * np.pi * 0.5 * t)
    x2 = np.sin(2 * np.pi * 0.5 * t + 0.5)
    x3 = np.sin(2 * np.pi * 0.5 * t + 1.0)

    if anomaly:
        mask = (t > 5) & (t < 7)
        x2[mask] = np.random.normal(0, 1.0, size=mask.sum())  # ruptura no lineal

    return np.vstack([x1, x2, x3])

# -----------------------------
# 2. Mutual Information (discretización)
# -----------------------------

def compute_mi(x, y, bins=20):
    x_binned = np.digitize(x, np.histogram_bin_edges(x, bins=bins))
    y_binned = np.digitize(y, np.histogram_bin_edges(y, bins=bins))
    return mutual_info_score(x_binned, y_binned)

# -----------------------------
# 3. Transfer Entropy (simplificada)
# -----------------------------

def compute_te(x, y, lag=1):
    # aproximación simple basada en información condicional
    x_lag = x[:-lag]
    y_lag = y[:-lag]
    y_next = y[lag:]

    mi1 = compute_mi(y_next, y_lag)
    mi2 = compute_mi(y_next, np.vstack([y_lag, x_lag]).T.flatten())

    return mi2 - mi1

# -----------------------------
# 4. Operador relacional híbrido
# -----------------------------

def relational_operator(signals):
    n = signals.shape[0]
    R = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                mi = compute_mi(signals[i], signals[j])
                te = compute_te(signals[i], signals[j])
                R[i, j] = mi + te

    return R

# -----------------------------
# 5. Invariantes de orden superior
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
# 6. Operador DPCC
# -----------------------------

def dpcc_operator(inv_series):
    D = []
    for i in range(1, len(inv_series)):
        D.append(np.linalg.norm(inv_series[i] - inv_series[i-1]))
    return np.array(D)

# -----------------------------
# 7. Memoria de excepción (TAE)
# -----------------------------

class ExceptionMemory:
    def __init__(self, threshold=0.0, persistence=5):
        self.threshold = threshold
        self.persistence = persistence
        self.buffer = []

    def fit_threshold(self, values):
        self.threshold = np.mean(values) + np.std(values)

    def update(self, value):
        self.buffer.append(value > self.threshold)
        if len(self.buffer) > self.persistence:
            self.buffer.pop(0)
        return all(self.buffer)

# -----------------------------
# 8. Simulación
# -----------------------------

def run_simulation():
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

    memory = ExceptionMemory()
    memory.fit_threshold(D)
    exceptions = np.array([memory.update(d) for d in D])

    return t[:-window-1], D, exceptions

# -----------------------------
# 9. Visualización
# -----------------------------

def plot_results(t, D, exceptions):
    plt.figure()

    plt.plot(t, D, label="DPCC v2 (Nonlinear)")
    plt.scatter(t[exceptions], D[exceptions], label="Persistent Exceptions")

    plt.xlabel("Time")
    plt.ylabel("Invariant Breakdown")
    plt.title("DPCC v2 — Nonlinear Structural Detection")
    plt.legend()

    plt.show()

# -----------------------------
# 10. Main
# -----------------------------

if __name__ == "__main__":
    t, D, exceptions = run_simulation()
    plot_results(t, D, exceptions)

# ==========================================
# README.md
# ==========================================

"""
# DPCC v2 — Nonlinear Coherence Detection Framework

## Descripción

DPCC v2 introduce detección no lineal mediante:

- Mutual Information
- Transfer Entropy

El sistema ya no depende de fase ni de naturaleza de señal.

## Características

- Operador relacional híbrido (MI + TE)
- Invariantes estructurales
- Memoria adaptativa (TAE)
- Detección robusta de ruptura

## Ejecución

```bash
python dpcc_v2.py
```

## Próximos pasos

- GPU acceleration
- Integración PyTorch
- Datos reales (EEG, geomagnéticos)

"""
