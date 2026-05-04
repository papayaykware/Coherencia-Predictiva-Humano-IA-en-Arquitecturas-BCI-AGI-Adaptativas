# ==========================================
# DPCC v1 — Framework de Detección de Coherencia
# Sistema operativo de detección de invariantes
# ==========================================

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

# -----------------------------
# 1. Generador de señales (multiescala + anomalía estructural)
# -----------------------------

def generate_signals(t, anomaly=False):
    x1 = np.sin(2 * np.pi * 0.5 * t)
    x2 = np.sin(2 * np.pi * 0.5 * t + 0.5)
    x3 = np.sin(2 * np.pi * 0.5 * t + 1.0)

    if anomaly:
        mask = (t > 5) & (t < 7)
        x2[mask] = np.sin(2 * np.pi * 0.8 * t[mask])  # cambio estructural

    return np.vstack([x1, x2, x3])

# -----------------------------
# 2. Operador relacional (fase)
# -----------------------------

def phase_relation(signals):
    analytic = hilbert(signals)
    phase = np.angle(analytic)

    n = signals.shape[0]
    R = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                R[i, j] = np.mean(np.unwrap(phase[i] - phase[j]))

    return R

# -----------------------------
# 3. Invariantes de orden superior
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
# 4. Operador DPCC (núcleo)
# -----------------------------

def dpcc_operator(inv_series):
    D = []
    for i in range(1, len(inv_series)):
        D.append(np.linalg.norm(inv_series[i] - inv_series[i-1]))
    return np.array(D)

# -----------------------------
# 5. Memoria de excepción (TAE)
# -----------------------------

class ExceptionMemory:
    def __init__(self, threshold=0.5, persistence=5):
        self.threshold = threshold
        self.persistence = persistence
        self.buffer = []

    def update(self, value):
        self.buffer.append(value > self.threshold)
        if len(self.buffer) > self.persistence:
            self.buffer.pop(0)

        return all(self.buffer)

# -----------------------------
# 6. Simulación completa
# -----------------------------

def run_simulation():
    t = np.linspace(0, 10, 1000)
    signals = generate_signals(t, anomaly=True)

    window = 80
    inv_series = []

    for i in range(len(t) - window):
        segment = signals[:, i:i+window]
        R = phase_relation(segment)
        inv = invariants(R)
        inv_series.append(inv)

    D = dpcc_operator(inv_series)

    memory = ExceptionMemory(threshold=np.mean(D) * 1.5)
    exceptions = np.array([memory.update(d) for d in D])

    return t[:-window-1], D, exceptions

# -----------------------------
# 7. Visualización avanzada
# -----------------------------

def plot_results(t, D, exceptions):
    plt.figure()

    plt.plot(t, D, label="DPCC Operator")
    plt.scatter(t[exceptions], D[exceptions], label="Persistent Exceptions")

    plt.xlabel("Time")
    plt.ylabel("Invariant Breakdown")
    plt.title("DPCC v1 — Structural Coherence Detection")
    plt.legend()

    plt.show()

# -----------------------------
# 8. Main
# -----------------------------

if __name__ == "__main__":
    t, D, exceptions = run_simulation()
    plot_results(t, D, exceptions)

# ==========================================
# README.md
# ==========================================

"""
# DPCC v1 — Framework de Detección de Coherencia

## Descripción

DPCC v1 implementa un sistema de detección de rupturas estructurales basado en invariantes relacionales.

## Características clave

- Operador relacional basado en fase
- Invariantes de orden superior
- Detección dinámica de ruptura estructural
- Memoria de excepción (TAE)

## Ejecución

```bash
python dpcc_v1.py
```

## Roadmap

- Integración con PyTorch
- Entrada EEG real
- Multiescala jerárquico
- Visualización topológica

"""
