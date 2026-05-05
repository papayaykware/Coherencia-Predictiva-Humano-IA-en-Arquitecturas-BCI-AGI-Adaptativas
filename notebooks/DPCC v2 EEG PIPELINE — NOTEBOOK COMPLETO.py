# ==========================================
# DPCC v2 EEG PIPELINE — NOTEBOOK COMPLETO
# ==========================================

# =========================
# 1. INSTALACIÓN
# =========================
!pip install mne wfdb numpy matplotlib scikit-learn --quiet

# =========================
# 2. IMPORTS
# =========================
import numpy as np
import matplotlib.pyplot as plt
import mne
import wfdb
from sklearn.metrics import mutual_info_score

# =========================
# 3. DESCARGA DATASET (PhysioNet)
# =========================
# Usamos MIT-BIH EEG (ejemplo sencillo accesible vía WFDB)

record_name = "chb01_03"  # EEG ejemplo
wfdb.dl_database("chbmit", dl_dir="data", records=[record_name])

file_path = f"data/chbmit/{record_name}.edf"

# =========================
# 4. CARGA EEG
# =========================
raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
raw.pick_types(eeg=True)

# limitar duración (para rapidez)
raw.crop(tmin=0, tmax=60)

data = raw.get_data()
sfreq = raw.info['sfreq']
channels = raw.ch_names

print("Canales:", channels[:5])
print("Shape:", data.shape)

# =========================
# 5. SELECCIÓN DE CANALES
# =========================
# Seleccionamos 3 canales (puedes cambiar)
selected_idx = [0, 1, 2]
signals = data[selected_idx]

# =========================
# 6. MUTUAL INFORMATION
# =========================
def compute_mi(x, y, bins=16):
    x_binned = np.digitize(x, np.histogram_bin_edges(x, bins=bins))
    y_binned = np.digitize(y, np.histogram_bin_edges(y, bins=bins))
    return mutual_info_score(x_binned, y_binned)

# =========================
# 7. RELATIONAL OPERATOR (MI)
# =========================
def relational_operator(signals):
    n = signals.shape[0]
    R = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                R[i, j] = compute_mi(signals[i], signals[j])
    
    return R

# =========================
# 8. INVARIANTES
# =========================
def invariants(R):
    n = R.shape[0]
    inv = []
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and j != k and i != k:
                    inv.append(R[i,j] + R[j,k] - R[i,k])
    
    return np.array(inv)

# =========================
# 9. DPCC CORE
# =========================
def dpcc_operator(inv_series):
    return np.array([
        np.linalg.norm(inv_series[i] - inv_series[i-1])
        for i in range(1, len(inv_series))
    ])

# =========================
# 10. CORRELACIÓN CLÁSICA (baseline)
# =========================
def correlation_metric(signals):
    return np.corrcoef(signals)

# =========================
# 11. PIPELINE
# =========================
window = int(sfreq * 1)  # 1 segundo
inv_series = []
corr_series = []

for i in range(signals.shape[1] - window):
    segment = signals[:, i:i+window]
    
    # DPCC
    R = relational_operator(segment)
    inv = invariants(R)
    inv_series.append(inv)
    
    # Correlación
    C = correlation_metric(segment)
    corr_series.append(np.linalg.norm(C))

# Convertir
D = dpcc_operator(inv_series)
corr_series = np.array(corr_series[:-1])

t = np.arange(len(D)) / sfreq

# =========================
# 12. DETECCIÓN DE EXCEPCIONES (TAE)
# =========================
threshold = np.mean(D) + np.std(D)
exceptions = D > threshold

# =========================
# 13. FIGURA 1 — DPCC
# =========================
plt.figure()
plt.plot(t, D)
plt.title("DPCC Signal — Invariant Breakdown")
plt.xlabel("Time (s)")
plt.ylabel("D(t)")
plt.savefig("figure_dpcc_signal.png")
plt.show()

# =========================
# 14. FIGURA 2 — EXCEPCIONES
# =========================
plt.figure()
plt.plot(t, D)
plt.scatter(t[exceptions], D[exceptions])
plt.title("Detected Exceptions (DPCC)")
plt.xlabel("Time (s)")
plt.ylabel("D(t)")
plt.savefig("figure_exceptions.png")
plt.show()

# =========================
# 15. FIGURA 3 — COMPARATIVA
# =========================
plt.figure()
plt.plot(t, D, label="DPCC")
plt.plot(t, corr_series, label="Correlation (baseline)")
plt.legend()
plt.title("DPCC vs Classical Correlation")
plt.xlabel("Time (s)")
plt.ylabel("Signal")
plt.savefig("figure_comparison.png")
plt.show()

# =========================
# 16. RESULTADOS CLAVE
# =========================
print("Threshold:", threshold)
print("Número de excepciones detectadas:", np.sum(exceptions))
