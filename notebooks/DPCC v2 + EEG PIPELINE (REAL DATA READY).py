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
