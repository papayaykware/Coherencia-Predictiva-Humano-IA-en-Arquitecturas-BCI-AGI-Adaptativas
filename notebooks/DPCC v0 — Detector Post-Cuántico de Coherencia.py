# ==========================================
# DPCC v0 — Detector Post-Cuántico de Coherencia
# Repo listo para GitHub (single-file demo)
# ==========================================

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Generador de señales acopladas
# -----------------------------

def generate_signals(t, anomaly=False):
    x1 = np.sin(2 * np.pi * 0.5 * t)
    x2 = np.sin(2 * np.pi * 0.5 * t + 0.5)
    x3 = np.sin(2 * np.pi * 0.5 * t + 1.0)

    if anomaly:
        # romper coherencia en segmento
        mask = (t > 5) & (t < 7)
        x2[mask] += np.random.normal(0, 1.0, size=mask.sum())

    return np.vstack([x1, x2, x3])

# -----------------------------
# 2. Operador de coherencia (relacional)
# -----------------------------

def coherence_matrix(signals):
    n = signals.shape[0]
    C = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                C[i, j] = np.corrcoef(signals[i], signals[j])[0, 1]
    return C

# -----------------------------
# 3. Métrica de estabilidad (DPCC core)
# -----------------------------

def coherence_stability(C_series):
    diffs = []
    for i in range(1, len(C_series)):
        diffs.append(np.linalg.norm(C_series[i] - C_series[i-1]))
    return np.array(diffs)

# -----------------------------
# 4. Detector de excepciones
# -----------------------------

def detect_exceptions(stability, threshold=0.5):
    return stability > threshold

# -----------------------------
# 5. Simulación completa
# -----------------------------

def run_simulation():
    t = np.linspace(0, 10, 1000)

    signals = generate_signals(t, anomaly=True)

    window = 50
    C_series = []

    for i in range(len(t) - window):
        window_data = signals[:, i:i+window]
        C = coherence_matrix(window_data)
        C_series.append(C)

    stability = coherence_stability(C_series)
    anomalies = detect_exceptions(stability)

    return t[:-window-1], stability, anomalies

# -----------------------------
# 6. Visualización
# -----------------------------

def plot_results(t, stability, anomalies):
    plt.figure()

    plt.plot(t, stability, label="Coherence Stability")
    plt.scatter(t[anomalies], stability[anomalies], label="Exceptions")

    plt.title("DPCC v0 — Detection of Coherence Breakdown")
    plt.xlabel("Time")
    plt.ylabel("ΔCoherence")
    plt.legend()

    plt.show()

# -----------------------------
# 7. Main
# -----------------------------

if __name__ == "__main__":
    t, stability, anomalies = run_simulation()
    plot_results(t, stability, anomalies)

# ==========================================
# README (copiar a README.md en GitHub)
# ==========================================

"""
# DPCC v0 — Detector Post-Cuántico de Coherencia

## Descripción

Este repositorio implementa un prototipo mínimo del DPCC (Detector Post-Cuántico de Coherencia),
basado en la detección de rupturas de invariantes relacionales entre señales.

## Concepto clave

El sistema no detecta eventos directos, sino:

→ rupturas en la coherencia estructural entre variables

## Componentes

- Generador de señales acopladas
- Cálculo de matriz de coherencia
- Métrica de estabilidad temporal
- Detector de excepciones

## Ejecución

```bash
python dpcc_v0.py
```

