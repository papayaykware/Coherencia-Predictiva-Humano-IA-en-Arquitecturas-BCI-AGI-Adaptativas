# ==========================================
# DPCC v4 — EEG + GEOMAGNETIC (MULTISCALE)
# ==========================================

# =========================
# 1. INSTALL
# =========================
!pip install mne wfdb pandas requests numpy matplotlib scikit-learn --quiet

# =========================
# 2. IMPORTS
# =========================
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mne, wfdb, requests
from sklearn.metrics import mutual_info_score

# =========================
# 3. LOAD EEG (PhysioNet)
# =========================
record = "chb01_03"
wfdb.dl_database("chbmit", dl_dir="data", records=[record])

file_path = f"data/chbmit/{record}.edf"
raw = mne.io.read_raw_edf(file_path, preload=True, verbose=False)
raw.pick_types(eeg=True)
raw.crop(tmin=0, tmax=120)

eeg = raw.get_data()
sfreq = raw.info['sfreq']

# select 3 channels
eeg = eeg[[0,1,2]]

t_eeg = np.arange(eeg.shape[1]) / sfreq

# =========================
# 4. LOAD GEOMAGNETIC DATA (NOAA)
# =========================
url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
geo_json = requests.get(url).json()

geo_df = pd.DataFrame(geo_json)
geo_df['time_tag'] = pd.to_datetime(geo_df['time_tag'])
geo_df['kp'] = pd.to_numeric(geo_df['kp'], errors='coerce')
geo_df = geo_df.dropna()

# normalize time to seconds
geo_time = (geo_df['time_tag'] - geo_df['time_tag'].iloc[0]).dt.total_seconds().values
geo_signal = geo_df['kp'].values

# =========================
# 5. ALIGN EEG + GEO
# =========================
geo_interp = np.interp(t_eeg, geo_time, geo_signal)

# =========================
# 6. MUTUAL INFORMATION
# =========================
def compute_mi(x, y, bins=16):
    x_b = np.digitize(x, np.histogram_bin_edges(x, bins=bins))
    y_b = np.digitize(y, np.histogram_bin_edges(y, bins=bins))
    return mutual_info_score(x_b, y_b)

# =========================
# 7. RELATIONAL OPERATOR
# =========================
def relational_operator(signals):
    n = signals.shape[0]
    R = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            if i != j:
                R[i,j] = compute_mi(signals[i], signals[j])
    return R

# =========================
# 8. INVARIANTS
# =========================
def invariants(R):
    n = R.shape[0]
    inv = []
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i!=j and j!=k and i!=k:
                    inv.append(R[i,j] + R[j,k] - R[i,k])
    return np.array(inv)

# =========================
# 9. DPCC
# =========================
def dpcc(inv_series):
    return np.array([
        np.linalg.norm(inv_series[i]-inv_series[i-1])
        for i in range(1,len(inv_series))
    ])

# =========================
# 10. RUN PIPELINES
# =========================
def run_pipeline(signals):
    window = int(sfreq * 1)
    inv_series = []
    
    for i in range(signals.shape[1]-window):
        seg = signals[:, i:i+window]
        R = relational_operator(seg)
        inv = invariants(R)
        inv_series.append(inv)
    
    return dpcc(inv_series)

# EEG only
D_eeg = run_pipeline(eeg)

# EEG + GEO
signals_multi = np.vstack([eeg, geo_interp])
D_multi = run_pipeline(signals_multi)

t = np.arange(len(D_eeg)) / sfreq

# =========================
# 11. FIGURES
# =========================

# Fig 1 — EEG vs Multiscale
plt.figure()
plt.plot(t, D_eeg, label="EEG only")
plt.plot(t, D_multi, label="EEG + Geo")
plt.legend()
plt.title("DPCC Multiscale Comparison")
plt.xlabel("Time (s)")
plt.ylabel("D(t)")
plt.savefig("fig_multiscale.png")
plt.show()

# Fig 2 — Difference
plt.figure()
plt.plot(t, D_multi - D_eeg)
plt.title("Multiscale Contribution (Geo influence)")
plt.xlabel("Time (s)")
plt.ylabel("ΔD")
plt.savefig("fig_difference.png")
plt.show()

# Fig 3 — Exceptions
thr = np.mean(D_multi) + np.std(D_multi)
exc = D_multi > thr

plt.figure()
plt.plot(t, D_multi)
plt.scatter(t[exc], D_multi[exc])
plt.title("Multiscale Exceptions")
plt.savefig("fig_exceptions_multiscale.png")
plt.show()

# =========================
# 12. METRICS
# =========================
print("EEG mean D:", np.mean(D_eeg))
print("Multiscale mean D:", np.mean(D_multi))
print("Exception count:", np.sum(exc))
