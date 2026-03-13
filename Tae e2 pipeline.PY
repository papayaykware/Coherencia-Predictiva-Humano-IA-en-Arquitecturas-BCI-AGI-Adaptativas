"""
TAE-E2 Pipeline de Referencia
==============================
Detección de reorganización post-excepción en redes neuronales biológicas.
Firma TAE canónica: PE_max → ventana de reorganización → PE_post < PE_pre

Prioridad teórica (según corpus TAE):
  1. Pico de entropía de permutación (PE_max)
  2. Ventana temporal de la reorganización (Δt_reorg)
  3. Transición al nuevo atractor (PE_post < PE_pre)
  4. Calibración empírica de ε_c

Datasets soportados: EEGMMI (primario), DEAP (secundario), TUEG (terciario)

Dependencias:
  mne >= 1.7
  antropy >= 0.1.6
  ruptures >= 1.1.7
  scikit-learn >= 1.3
  numpy, scipy, matplotlib, h5py
"""

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import warnings
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

# Importaciones con fallback informativo
try:
    import mne
    MNE_AVAILABLE = True
except ImportError:
    MNE_AVAILABLE = False
    warnings.warn("MNE no disponible. Usar load_eeg_mock() para datos sintéticos.")

try:
    import antropy as ant
    ANTROPY_AVAILABLE = True
except ImportError:
    ANTROPY_AVAILABLE = False
    warnings.warn("antropy no disponible. PE calculada con implementación interna.")

try:
    import ruptures as rpt
    RUPTURES_AVAILABLE = True
except ImportError:
    RUPTURES_AVAILABLE = False
    warnings.warn("ruptures no disponible. PELT reemplazado por detector simplificado.")

try:
    from sklearn.mixture import GaussianMixture
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False


# ─────────────────────────────────────────────
# ESTRUCTURAS DE DATOS
# ─────────────────────────────────────────────

class Dataset(Enum):
    EEGMMI = "eegmmi"   # PhysioNet Motor Movement/Imagery — primario
    DEAP   = "deap"     # Emotion/EEG — secundario
    TUEG   = "tueg"     # Temple University Clinical — terciario


@dataclass
class TAESignature:
    """Resultado de detección de firma TAE en una época EEG."""
    subject_id: str
    channel: str
    dataset: Dataset

    # Prioridad 1: Pico PE
    pe_baseline: float = np.nan       # PE media en ventana pre-evento
    pe_max: float = np.nan            # Valor del pico PE_max
    pe_max_idx: int = -1              # Índice temporal del pico
    pe_max_zscore: float = np.nan     # Z-score del pico respecto a baseline

    # Prioridad 2: Ventana temporal de reorganización
    t_cp1: int = -1                   # Inicio de la fase excepcional (muestras PE)
    t_cp2: int = -1                   # Fin de la fase excepcional (muestras PE)
    delta_t_reorg_s: float = np.nan   # Duración de reorganización en segundos

    # Prioridad 3: Transición de atractor
    pe_post: float = np.nan           # PE media en ventana post-evento
    delta_pe: float = np.nan          # PE_post - PE_pre (negativo = confirmación TAE)
    attractor_distance: float = np.nan  # d_H(A0, A1) normalizada

    # Prioridad 4: ε_c calibrado
    epsilon_c: float = np.nan         # Umbral de excepción calibrado para este sujeto
    epsilon_c_norm: float = np.nan    # ε_c normalizado por σ de la distribución

    # Estado
    tae_positive: bool = False        # Firma TAE completa detectada
    confidence: float = 0.0          # Confianza [0, 1] basada en criterios satisfechos


@dataclass
class PipelineConfig:
    """Parámetros configurables del pipeline TAE-E2."""
    # --- Preprocesamiento ---
    bandpass_low: float = 1.0
    bandpass_high: float = 40.0
    notch_freq: float = 50.0
    target_sfreq: float = 128.0       # Downsampling objetivo (DEAP)

    # --- Entropía de permutación ---
    pe_order: int = 5                 # Dimensión de embedding m
    pe_delay: int = 1                 # Lag τ (en muestras; adaptativo si 0)
    window_s: float = 2.0            # Ventana deslizante (segundos)
    step_s: float = 0.25             # Paso de la ventana (segundos)
    n_scales: int = 4                # Escalas para MSPE: [1, 2, 4, 8]

    # --- PELT ---
    pelt_model: str = "rbf"          # Función de coste: "l2", "rbf", "l1"
    pelt_penalty: Optional[float] = None  # None = BIC automático
    min_reorg_s: float = 0.5         # Duración mínima de la fase excepcional
    max_reorg_s: float = 10.0        # Duración máxima

    # --- Criterios de detección TAE ---
    pe_peak_zscore_min: float = 2.0  # Z-score mínimo del pico PE_max
    delta_pe_max: float = -0.05      # ΔPE máximo para confirmar P3 (negativo)
    baseline_window_s: float = 1.0   # Ventana de línea de base pre-evento

    # --- Reconstrucción del atractor ---
    fnn_threshold: float = 0.01      # Umbral de falsos vecinos más próximos
    max_embed_dim: int = 10          # Dimensión máxima de búsqueda FNN

    # --- ε_c calibración ---
    epsilon_percentile: float = 90.0  # Percentil inicial para ε_c
    epsilon_validation_rate: float = 0.70  # Tasa mínima de concordancia PELT


# ─────────────────────────────────────────────
# MÓDULO 0: DATOS SINTÉTICOS (DEMO / TEST)
# ─────────────────────────────────────────────

def generate_tae_synthetic_eeg(
    sfreq: float = 128.0,
    duration_s: float = 30.0,
    exception_t: float = 15.0,
    seed: int = 42
) -> tuple[np.ndarray, np.ndarray, float]:
    """
    Genera una señal EEG sintética con firma TAE embebida.
    
    La señal simula:
      - Fase pre-excepción: oscilación alpha + ruido (PE moderada)
      - Evento excepcional en exception_t: spike de entropía
      - Fase post-excepción: nuevo atractor con frecuencia dominante distinta (PE reducida)
    
    Returns:
        signal: array (n_samples,)
        times: array (n_samples,)
        event_sample: índice de muestra del evento excepcional
    """
    rng = np.random.default_rng(seed)
    n = int(duration_s * sfreq)
    t = np.linspace(0, duration_s, n)
    exc_idx = int(exception_t * sfreq)

    # Fase pre-excepción: alpha 10 Hz + ruido gaussiano moderado
    pre = (
        1.5 * np.sin(2 * np.pi * 10 * t[:exc_idx]) +
        0.8 * np.sin(2 * np.pi * 8  * t[:exc_idx]) +
        rng.normal(0, 0.3, exc_idx)
    )

    # Evento excepcional: 500 ms de ruido de alta amplitud (pico PE)
    exc_duration = int(0.5 * sfreq)
    exc_window = rng.normal(0, 3.0, exc_duration)

    # Fase post-excepción: nuevo atractor (beta 18 Hz, menor ruido → PE reducida)
    post_start = exc_idx + exc_duration
    n_post = n - post_start
    post = (
        1.2 * np.sin(2 * np.pi * 18 * t[post_start:]) +
        0.4 * np.sin(2 * np.pi * 22 * t[post_start:]) +
        rng.normal(0, 0.15, n_post)        # menor ruido → PE_post < PE_pre
    )

    signal = np.concatenate([pre, exc_window, post])
    return signal, t, exc_idx


# ─────────────────────────────────────────────
# MÓDULO I: PREPROCESAMIENTO
# ─────────────────────────────────────────────

def preprocess_eeg(
    raw_signal: np.ndarray,
    sfreq: float,
    config: PipelineConfig,
    dataset: Dataset = Dataset.EEGMMI
) -> np.ndarray:
    """
    Preprocesamiento adaptativo por dataset.
    
    EEGMMI : filtrado + zero-phase Butterworth (1–40 Hz)
    DEAP   : ídem + downsampling a 128 Hz
    TUEG   : filtrado conservador (0.5–70 Hz) para preservar dinámica clínica
    """
    from scipy.signal import butter, sosfiltfilt, resample_poly
    from math import gcd

    if dataset == Dataset.TUEG:
        low, high = 0.5, 70.0
    else:
        low, high = config.bandpass_low, config.bandpass_high

    # Butterworth zero-phase
    nyq = sfreq / 2.0
    sos = butter(4, [low / nyq, high / nyq], btype='band', output='sos')
    filtered = sosfiltfilt(sos, raw_signal)

    # Downsampling para DEAP (512 → 128 Hz)
    if dataset == Dataset.DEAP and sfreq > config.target_sfreq:
        up = int(config.target_sfreq)
        down = int(sfreq)
        g = gcd(up, down)
        filtered = resample_poly(filtered, up // g, down // g)
        sfreq = config.target_sfreq

    # Normalización z-score por segmento
    filtered = (filtered - np.mean(filtered)) / (np.std(filtered) + 1e-12)
    return filtered


# ─────────────────────────────────────────────
# MÓDULO II: ENTROPÍA DE PERMUTACIÓN (PRIORIDAD 1 y 2)
# ─────────────────────────────────────────────

def _pe_internal(x: np.ndarray, order: int, delay: int) -> float:
    """
    Implementación interna de PE (Bandt & Pompe 2002) sin dependencias externas.
    PE_norm = H(patrones ordinales) / log2(m!)
    """
    n = len(x)
    if n < order * delay:
        return np.nan

    # Construir patrones ordinales
    patterns = []
    for i in range(n - (order - 1) * delay):
        window = x[i:i + order * delay:delay]
        pattern = tuple(np.argsort(np.argsort(window)))
        patterns.append(pattern)

    # Distribución de frecuencias de patrones
    unique, counts = np.unique(patterns, axis=0, return_counts=True)
    probs = counts / counts.sum()

    # Entropía de Shannon normalizada
    pe = -np.sum(probs * np.log2(probs + 1e-12))
    pe_norm = pe / np.log2(math.factorial(order))
    return pe_norm


def compute_pe_sliding(
    signal: np.ndarray,
    sfreq: float,
    config: PipelineConfig
) -> tuple[np.ndarray, np.ndarray]:
    """
    Calcula la entropía de permutación en ventana deslizante.
    
    Returns:
        pe_series : array de PE normalizada por ventana
        pe_times  : array de tiempos centrales de cada ventana (segundos)
    """
    window_n = int(config.window_s * sfreq)
    step_n   = int(config.step_s   * sfreq)
    n = len(signal)

    pe_values = []
    pe_times  = []

    for start in range(0, n - window_n + 1, step_n):
        end = start + window_n
        segment = signal[start:end]

        if ANTROPY_AVAILABLE:
            pe = ant.perm_entropy(segment, order=config.pe_order,
                                  delay=config.pe_delay, normalize=True)
        else:
            pe = _pe_internal(segment, config.pe_order, config.pe_delay)

        pe_values.append(pe)
        pe_times.append((start + window_n / 2) / sfreq)

    return np.array(pe_values), np.array(pe_times)


def compute_mspe(
    signal: np.ndarray,
    sfreq: float,
    config: PipelineConfig
) -> dict[int, np.ndarray]:
    """
    Entropía de permutación multiscala (MSPE) para factores s ∈ {1, 2, 4, 8}.
    Coarse-graining por promediado de bloques no solapados.
    
    Returns:
        dict {escala: array PE_norm}
    """
    scales = [1, 2, 4, 8][:config.n_scales]
    mspe = {}
    for s in scales:
        if s == 1:
            coarse = signal
        else:
            # Coarse-graining: media de bloques de tamaño s
            n_blocks = len(signal) // s
            coarse = signal[:n_blocks * s].reshape(n_blocks, s).mean(axis=1)
        sfreq_s = sfreq / s
        pe_s, _ = compute_pe_sliding(coarse, sfreq_s, config)
        mspe[s] = pe_s
    return mspe


# ─────────────────────────────────────────────
# MÓDULO III: DETECCIÓN DE PUNTOS DE CAMBIO PELT (PRIORIDAD 2)
# ─────────────────────────────────────────────

def _pelt_simple(signal: np.ndarray, min_size: int = 3) -> list[int]:
    """
    Detector de puntos de cambio simplificado (fallback sin ruptures).
    Busca los dos puntos donde la varianza local cambia más abruptamente.
    """
    n = len(signal)
    scores = np.zeros(n)
    hw = max(min_size, 3)

    for i in range(hw, n - hw):
        left  = signal[max(0, i - hw):i]
        right = signal[i:min(n, i + hw)]
        scores[i] = abs(np.var(right) - np.var(left))

    # Dos mejores picos no adyacentes
    peak1 = int(np.argmax(scores))
    scores_copy = scores.copy()
    scores_copy[max(0, peak1-hw):peak1+hw] = 0
    peak2 = int(np.argmax(scores_copy))
    return sorted([peak1, peak2])


def detect_changepoints(
    pe_series: np.ndarray,
    pe_times: np.ndarray,
    config: PipelineConfig,
    sfreq_pe: float = None
) -> list[int]:
    """
    Detecta puntos de cambio en la serie PE mediante PELT.
    
    Args:
        pe_series  : serie PE normalizada
        pe_times   : tiempos correspondientes (s)
        sfreq_pe   : frecuencia de muestreo de la serie PE (1/step_s)
    
    Returns:
        Lista de índices de puntos de cambio en pe_series.
    """
    if sfreq_pe is None:
        sfreq_pe = 1.0 / config.step_s

    if RUPTURES_AVAILABLE:
        model = rpt.Pelt(model=config.pelt_model, min_size=3, jump=1)
        model.fit(pe_series.reshape(-1, 1))

        # Penalización BIC si no se especifica
        if config.pelt_penalty is None:
            n = len(pe_series)
            penalty = np.log(n) * 2   # BIC para modelo gaussiano
        else:
            penalty = config.pelt_penalty

        try:
            bkps = model.predict(pen=penalty)
            # ruptures devuelve el último índice = len; excluirlo
            changepoints = [b for b in bkps if b < len(pe_series)]
        except Exception:
            changepoints = _pelt_simple(pe_series)
    else:
        changepoints = _pelt_simple(pe_series)

    return changepoints


def extract_tae_windows(
    pe_series: np.ndarray,
    pe_times: np.ndarray,
    changepoints: list[int],
    config: PipelineConfig
) -> tuple[int, int, float]:
    """
    A partir de los puntos de cambio, identifica la ventana [t_CP1, t_CP2]
    que delimita la fase de pico PE (excepción activa).
    
    Returns:
        (t_cp1_idx, t_cp2_idx, delta_t_reorg_s)
        Retorna (-1, -1, nan) si no se satisfacen los criterios TAE.
    """
    if len(changepoints) < 2:
        return -1, -1, np.nan

    # Evaluar todos los pares de puntos de cambio consecutivos
    best_pair = (-1, -1)
    best_score = -np.inf

    for i in range(len(changepoints) - 1):
        cp1 = changepoints[i]
        cp2 = changepoints[i + 1]

        # Duración de la ventana en segundos
        dt = pe_times[cp2 - 1] - pe_times[cp1] if cp2 > cp1 else np.nan
        if np.isnan(dt) or dt < config.min_reorg_s or dt > config.max_reorg_s:
            continue

        # PE media dentro de la ventana candidata
        pe_window = pe_series[cp1:cp2]
        pe_outside = np.concatenate([pe_series[:cp1], pe_series[cp2:]])

        if len(pe_outside) == 0:
            continue

        # Score: cuánto supera la ventana el nivel exterior
        score = np.mean(pe_window) - np.mean(pe_outside)
        if score > best_score:
            best_score = score
            best_pair = (cp1, cp2)

    cp1_idx, cp2_idx = best_pair
    if cp1_idx == -1:
        return -1, -1, np.nan

    dt_reorg = pe_times[min(cp2_idx, len(pe_times)-1)] - pe_times[cp1_idx]
    return cp1_idx, cp2_idx, dt_reorg


# ─────────────────────────────────────────────
# MÓDULO IV: RECONSTRUCCIÓN DEL ATRACTOR (PRIORIDAD 3)
# ─────────────────────────────────────────────

def mutual_information_delay(signal: np.ndarray, max_lag: int = 50) -> int:
    """
    Estima el retardo τ_Takens como el primer mínimo de la información mutua
    aproximada por binning uniforme.
    """
    mi_values = []
    bins = max(10, int(np.sqrt(len(signal))))

    for lag in range(1, max_lag + 1):
        x = signal[:-lag]
        y = signal[lag:]
        # Histograma 2D para estimar MI
        hist2d, _, _ = np.histogram2d(x, y, bins=bins)
        hist2d = hist2d / hist2d.sum()
        hx = hist2d.sum(axis=1)
        hy = hist2d.sum(axis=0)
        # MI = H(X) + H(Y) - H(X,Y)
        hx_val = -np.sum(hx[hx > 0] * np.log2(hx[hx > 0]))
        hy_val = -np.sum(hy[hy > 0] * np.log2(hy[hy > 0]))
        hxy_val = -np.sum(hist2d[hist2d > 0] * np.log2(hist2d[hist2d > 0]))
        mi_values.append(hx_val + hy_val - hxy_val)

    mi_values = np.array(mi_values)
    # Primer mínimo local
    for i in range(1, len(mi_values) - 1):
        if mi_values[i] < mi_values[i-1] and mi_values[i] < mi_values[i+1]:
            return i + 1  # lag es 1-indexed

    return int(np.argmin(mi_values)) + 1


def false_nearest_neighbors(
    signal: np.ndarray,
    tau: int,
    max_dim: int = 10,
    threshold: float = 0.01
) -> int:
    """
    Estima la dimensión de embedding óptima mediante FNN (Kennel et al. 1992).
    Retorna la primera dimensión donde la tasa FNN cae por debajo del umbral.
    """
    from scipy.spatial import KDTree

    n = len(signal)

    for d in range(1, max_dim):
        # Construir vectores de embedding en dimensión d
        n_pts = n - (d + 1) * tau
        if n_pts < 10:
            return d

        X_d   = np.array([signal[i:i + d*tau:tau]     for i in range(n_pts)])
        X_d1  = np.array([signal[i:i + (d+1)*tau:tau] for i in range(n_pts)])

        tree = KDTree(X_d)
        dists, indices = tree.query(X_d, k=2)  # k=2: el punto mismo + vecino

        fnn_count = 0
        for j in range(n_pts):
            nn_idx = indices[j, 1]
            r_d    = dists[j, 1] + 1e-12
            r_d1   = np.linalg.norm(X_d1[j] - X_d1[nn_idx])
            if r_d1 / r_d > 10.0:  # criterio de Kennel
                fnn_count += 1

        fnn_rate = fnn_count / n_pts
        if fnn_rate < threshold:
            return d + 1

    return max_dim


def reconstruct_attractor(
    signal: np.ndarray,
    tau: int,
    dim: int
) -> np.ndarray:
    """
    Reconstruye el atractor por embedding de Takens.
    Returns array (n_pts, dim) en el espacio de fase reconstruido.
    """
    n = len(signal)
    n_pts = n - (dim - 1) * tau
    if n_pts < 2:
        return np.empty((0, dim))
    X = np.array([signal[i:i + dim*tau:tau] for i in range(n_pts)])
    return X


def hausdorff_distance(A: np.ndarray, B: np.ndarray) -> float:
    """
    Distancia de Hausdorff entre dos conjuntos de puntos A y B.
    Normalizada por el diámetro medio de A para comparabilidad.
    """
    if len(A) == 0 or len(B) == 0:
        return np.nan

    from scipy.spatial import KDTree
    tree_B = KDTree(B)
    tree_A = KDTree(A)

    dists_A, _ = tree_B.query(A)
    dists_B, _ = tree_A.query(B)

    d_H = max(np.max(dists_A), np.max(dists_B))

    # Normalización por diámetro del atractor A
    diam_A = np.max(np.linalg.norm(A - A.mean(axis=0), axis=1)) + 1e-12
    return d_H / diam_A


# ─────────────────────────────────────────────
# MÓDULO V: CALIBRACIÓN EMPÍRICA DE ε_c (PRIORIDAD 4)
# ─────────────────────────────────────────────

def calibrate_epsilon_c(
    signal: np.ndarray,
    tau: int,
    dim: int,
    changepoints_pe: list[int],
    pe_times: np.ndarray,
    sfreq: float,
    config: PipelineConfig
) -> tuple[float, float]:
    """
    Calibración empírica de ε_c mediante análisis de la distribución
    de perturbaciones en el espacio de fase.
    
    Paso 1: Distribución de ‖δE‖ sobre la línea de base.
    Paso 2: GMM de dos componentes para separar ordinario vs. excepcional.
    Paso 3: ε_c = media aritmética de las dos medias del GMM.
    Paso 4: Normalización por σ de la distribución.
    
    Returns:
        (epsilon_c, epsilon_c_norm)
    """
    if len(signal) < 100:
        return np.nan, np.nan

    attractor = reconstruct_attractor(signal, tau, dim)
    if len(attractor) < 20:
        return np.nan, np.nan

    centroid = attractor.mean(axis=0)
    perturbations = np.linalg.norm(attractor - centroid, axis=1)

    if not SKLEARN_AVAILABLE or len(perturbations) < 10:
        # Fallback: percentil directo
        eps_c = np.percentile(perturbations, config.epsilon_percentile)
        eps_c_norm = (eps_c - np.mean(perturbations)) / (np.std(perturbations) + 1e-12)
        return eps_c, eps_c_norm

    # GMM de dos componentes
    gmm = GaussianMixture(n_components=2, random_state=42)
    gmm.fit(perturbations.reshape(-1, 1))
    means = gmm.means_.flatten()
    eps_c = float(np.mean(means))
    eps_c_norm = (eps_c - np.mean(perturbations)) / (np.std(perturbations) + 1e-12)

    return eps_c, eps_c_norm


# ─────────────────────────────────────────────
# ORQUESTADOR PRINCIPAL
# ─────────────────────────────────────────────

def run_tae_e2(
    signal: np.ndarray,
    sfreq: float,
    subject_id: str = "S01",
    channel: str = "Cz",
    dataset: Dataset = Dataset.EEGMMI,
    config: Optional[PipelineConfig] = None
) -> TAESignature:
    """
    Ejecuta el pipeline TAE-E2 completo sobre una señal EEG univariada.
    
    Args:
        signal     : señal EEG 1D, ya cargada y segmentada
        sfreq      : frecuencia de muestreo en Hz
        subject_id : identificador del sujeto
        channel    : canal EEG analizado
        dataset    : enum Dataset para preprocesamiento adaptativo
        config     : PipelineConfig (None → parámetros por defecto)
    
    Returns:
        TAESignature con todos los campos completados
    """
    if config is None:
        config = PipelineConfig()

    result = TAESignature(
        subject_id=subject_id,
        channel=channel,
        dataset=dataset
    )

    # ── Etapa I: Preprocesamiento ────────────────
    signal_proc = preprocess_eeg(signal, sfreq, config, dataset)

    # Actualizar sfreq si hubo downsampling (DEAP)
    if dataset == Dataset.DEAP and sfreq > config.target_sfreq:
        sfreq = config.target_sfreq

    # ── Etapa II: Entropía de permutación ────────
    pe_series, pe_times = compute_pe_sliding(signal_proc, sfreq, config)

    if len(pe_series) < 4:
        return result   # señal demasiado corta

    # Estadísticos de línea de base (primera mitad de pe_series)
    n_baseline = max(2, len(pe_series) // 3)
    pe_baseline = np.mean(pe_series[:n_baseline])
    pe_std      = np.std(pe_series[:n_baseline]) + 1e-12

    result.pe_baseline = float(pe_baseline)
    result.pe_max      = float(np.max(pe_series))
    result.pe_max_idx  = int(np.argmax(pe_series))
    result.pe_max_zscore = float((result.pe_max - pe_baseline) / pe_std)

    # ── Etapa III: PELT — ventana temporal ───────
    changepoints = detect_changepoints(pe_series, pe_times, config)
    cp1_idx, cp2_idx, dt_reorg = extract_tae_windows(
        pe_series, pe_times, changepoints, config
    )

    result.t_cp1 = cp1_idx
    result.t_cp2 = cp2_idx
    result.delta_t_reorg_s = float(dt_reorg) if not np.isnan(dt_reorg) else np.nan

    # PE pre y post ventana de reorganización
    if cp1_idx > 0 and cp2_idx > 0 and cp2_idx < len(pe_series):
        pre_window  = pe_series[max(0, cp1_idx - n_baseline):cp1_idx]
        post_window = pe_series[cp2_idx:min(len(pe_series), cp2_idx + n_baseline)]

        result.pe_baseline = float(np.mean(pre_window)) if len(pre_window) > 0 else pe_baseline
        result.pe_post     = float(np.mean(post_window)) if len(post_window) > 0 else np.nan
        result.delta_pe    = float(result.pe_post - result.pe_baseline) if not np.isnan(result.pe_post) else np.nan

    # ── Etapa IV: Reconstrucción del atractor ────
    tau_takens = mutual_information_delay(signal_proc, max_lag=min(50, len(signal_proc)//4))
    dim_embed  = false_nearest_neighbors(
        signal_proc, tau_takens,
        max_dim=config.max_embed_dim,
        threshold=config.fnn_threshold
    )

    # Segmentos pre y post excepción para comparar atractores
    exc_idx = int(result.pe_max_idx * config.step_s * sfreq)  # muestra en señal original
    n_seg = min(exc_idx, len(signal_proc) - exc_idx, int(5 * sfreq))

    if n_seg > dim_embed * tau_takens * 2:
        A0 = reconstruct_attractor(signal_proc[max(0, exc_idx-n_seg):exc_idx], tau_takens, dim_embed)
        A1 = reconstruct_attractor(signal_proc[exc_idx:exc_idx+n_seg], tau_takens, dim_embed)

        if len(A0) > 5 and len(A1) > 5:
            result.attractor_distance = float(hausdorff_distance(A0, A1))

    # ── Etapa V: Calibración ε_c ─────────────────
    result.epsilon_c, result.epsilon_c_norm = calibrate_epsilon_c(
        signal_proc, tau_takens, dim_embed,
        changepoints, pe_times, sfreq, config
    )

    # ── Evaluación de firma TAE completa ─────────
    criteria = {
        "P1_pico_pe":    result.pe_max_zscore >= config.pe_peak_zscore_min,
        "P2_ventana":    (cp1_idx > 0 and cp2_idx > 0 and
                         not np.isnan(dt_reorg) and
                         config.min_reorg_s <= dt_reorg <= config.max_reorg_s),
        "P3_delta_pe":   (not np.isnan(result.delta_pe) and
                         result.delta_pe <= config.delta_pe_max),
    }

    result.tae_positive = all(criteria.values())
    result.confidence   = sum(criteria.values()) / len(criteria)

    return result


# ─────────────────────────────────────────────
# VISUALIZACIÓN
# ─────────────────────────────────────────────

def plot_tae_signature(
    signal: np.ndarray,
    sfreq: float,
    result: TAESignature,
    config: Optional[PipelineConfig] = None,
    save_path: Optional[str] = None
) -> plt.Figure:
    """
    Visualización de cuatro paneles:
      (A) Señal EEG preprocesada
      (B) Serie PE con ventana de reorganización y picos marcados
      (C) Perfil PE por fases (pre/excepción/post)
      (D) Tabla resumen de criterios TAE
    """
    if config is None:
        config = PipelineConfig()

    signal_proc = preprocess_eeg(signal, sfreq, config, result.dataset)
    pe_series, pe_times = compute_pe_sliding(signal_proc, sfreq, config)
    times_eeg = np.arange(len(signal_proc)) / sfreq

    # Paleta TAE
    C_PRE  = "#2E86AB"   # azul — estado pre-excepción
    C_EXC  = "#E84855"   # rojo — ventana de excepción
    C_POST = "#3BB273"   # verde — estado post-excepción
    C_BG   = "#0D0D0D"
    C_TEXT = "#E8E8E8"

    fig = plt.figure(figsize=(14, 10), facecolor=C_BG)
    gs = gridspec.GridSpec(3, 2, figure=fig, hspace=0.45, wspace=0.35,
                           left=0.08, right=0.95, top=0.92, bottom=0.07)

    ax_eeg  = fig.add_subplot(gs[0, :])
    ax_pe   = fig.add_subplot(gs[1, :])
    ax_bar  = fig.add_subplot(gs[2, 0])
    ax_info = fig.add_subplot(gs[2, 1])

    for ax in [ax_eeg, ax_pe, ax_bar, ax_info]:
        ax.set_facecolor("#1A1A1A")
        for spine in ax.spines.values():
            spine.set_color("#444")

    # ── Panel A: Señal EEG ──────────────────────
    ax_eeg.plot(times_eeg, signal_proc, color="#888", linewidth=0.6, alpha=0.8)
    ax_eeg.set_title("Señal EEG preprocesada", color=C_TEXT, fontsize=10, pad=6)
    ax_eeg.set_xlabel("Tiempo (s)", color="#AAA", fontsize=8)
    ax_eeg.set_ylabel("Amplitud (z)", color="#AAA", fontsize=8)
    ax_eeg.tick_params(colors="#AAA", labelsize=7)

    # Marcar ventana de reorganización en señal
    if result.t_cp1 > 0 and result.t_cp2 > 0 and result.t_cp2 < len(pe_times):
        t1_s = pe_times[result.t_cp1]
        t2_s = pe_times[min(result.t_cp2, len(pe_times)-1)]
        ax_eeg.axvspan(t1_s, t2_s, color=C_EXC, alpha=0.15)

    # ── Panel B: Serie PE ───────────────────────
    ax_pe.plot(pe_times, pe_series, color=C_PRE, linewidth=1.5)
    ax_pe.set_title("Entropía de permutación deslizante (PE_norm)", color=C_TEXT,
                    fontsize=10, pad=6)
    ax_pe.set_xlabel("Tiempo (s)", color="#AAA", fontsize=8)
    ax_pe.set_ylabel("PE norm.", color="#AAA", fontsize=8)
    ax_pe.tick_params(colors="#AAA", labelsize=7)

    # Línea de baseline
    if not np.isnan(result.pe_baseline):
        ax_pe.axhline(result.pe_baseline, color=C_PRE, linestyle='--',
                      linewidth=0.8, alpha=0.6, label=f"PE_pre={result.pe_baseline:.3f}")

    # Pico PE_max
    if result.pe_max_idx >= 0 and result.pe_max_idx < len(pe_series):
        ax_pe.scatter(pe_times[result.pe_max_idx], pe_series[result.pe_max_idx],
                      color=C_EXC, s=80, zorder=5, label=f"PE_max={result.pe_max:.3f}")

    # Ventana de reorganización
    if result.t_cp1 > 0 and result.t_cp2 > 0 and result.t_cp2 < len(pe_times):
        t1_s = pe_times[result.t_cp1]
        t2_s = pe_times[min(result.t_cp2, len(pe_times)-1)]
        ax_pe.axvspan(t1_s, t2_s, color=C_EXC, alpha=0.18,
                      label=f"Δt={result.delta_t_reorg_s:.2f}s")

    # PE_post
    if not np.isnan(result.pe_post):
        ax_pe.axhline(result.pe_post, color=C_POST, linestyle='--',
                      linewidth=0.8, alpha=0.6, label=f"PE_post={result.pe_post:.3f}")

    ax_pe.legend(fontsize=7, facecolor="#1A1A1A", labelcolor=C_TEXT, framealpha=0.7)

    # ── Panel C: Barras por fase ─────────────────
    phases = ["Pre-excepción\n(PE_pre)", "Pico PE\n(PE_max)", "Post-excepción\n(PE_post)"]
    values = [result.pe_baseline, result.pe_max, result.pe_post]
    colors_bar = [C_PRE, C_EXC, C_POST]
    valid = [not np.isnan(v) for v in values]

    x_pos = [i for i, v in enumerate(valid) if v]
    y_val = [values[i] for i in x_pos]
    c_val = [colors_bar[i] for i in x_pos]
    l_val = [phases[i] for i in x_pos]

    if y_val:
        bars = ax_bar.bar(range(len(y_val)), y_val, color=c_val, width=0.5,
                          edgecolor="#333", linewidth=0.8)
        ax_bar.set_xticks(range(len(l_val)))
        ax_bar.set_xticklabels(l_val, color="#AAA", fontsize=7)
        ax_bar.set_ylabel("PE norm.", color="#AAA", fontsize=8)
        ax_bar.set_title("Perfil PE por fase", color=C_TEXT, fontsize=10, pad=6)
        ax_bar.tick_params(colors="#AAA", labelsize=7)

        # Flecha de ΔPE
        if not np.isnan(result.delta_pe) and len(y_val) >= 3:
            dy = result.delta_pe
            arrow_color = C_POST if dy < 0 else C_EXC
            ax_bar.annotate(
                f"ΔPE={dy:+.3f}",
                xy=(2, y_val[2] + 0.005),
                color=arrow_color, fontsize=8, ha='center', fontweight='bold'
            )

    # ── Panel D: Tabla de criterios ──────────────
    ax_info.axis('off')

    status_icon = "✓ POSITIVA" if result.tae_positive else "✗ NEGATIVA"
    status_color = C_POST if result.tae_positive else C_EXC

    info_lines = [
        (f"Firma TAE: {status_icon}", status_color, 12, True),
        (f"Confianza: {result.confidence*100:.0f}%", C_TEXT, 10, False),
        ("", C_TEXT, 8, False),
        (f"P1 – PE_max z-score: {result.pe_max_zscore:.2f}", C_TEXT, 9, False),
        (f"P2 – Δt reorganización: {result.delta_t_reorg_s:.2f}s"
         if not np.isnan(result.delta_t_reorg_s) else "P2 – Δt: no detectado",
         C_TEXT, 9, False),
        (f"P3 – ΔPE: {result.delta_pe:+.4f}"
         if not np.isnan(result.delta_pe) else "P3 – ΔPE: no calculable",
         C_TEXT, 9, False),
        ("", C_TEXT, 8, False),
        (f"d_H(A₀,A₁): {result.attractor_distance:.3f}"
         if not np.isnan(result.attractor_distance) else "d_H: no calculable",
         C_TEXT, 9, False),
        (f"ε_c: {result.epsilon_c:.4f} (norm: {result.epsilon_c_norm:.3f})"
         if not np.isnan(result.epsilon_c) else "ε_c: no calibrado",
         "#FFAA44", 9, False),
        ("", C_TEXT, 8, False),
        (f"Sujeto: {result.subject_id}  Canal: {result.channel}", "#888", 8, False),
        (f"Dataset: {result.dataset.value.upper()}", "#888", 8, False),
    ]

    y_cur = 0.97
    for text, color, size, bold in info_lines:
        ax_info.text(0.05, y_cur, text,
                     transform=ax_info.transAxes,
                     color=color, fontsize=size,
                     fontweight='bold' if bold else 'normal',
                     va='top', fontfamily='monospace')
        y_cur -= 0.085 if size >= 10 else 0.075

    # Título general
    fig.suptitle(
        f"TAE-E2 · Análisis de firma dinámica post-excepción · {result.subject_id} / {result.channel}",
        color=C_TEXT, fontsize=11, fontweight='bold', y=0.97
    )

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight', facecolor=C_BG)

    return fig


# ─────────────────────────────────────────────
# ANÁLISIS BATCH MULTI-SUJETO
# ─────────────────────────────────────────────

def batch_analysis(
    signals: list[np.ndarray],
    sfreq: float,
    subject_ids: list[str],
    channel: str = "Cz",
    dataset: Dataset = Dataset.EEGMMI,
    config: Optional[PipelineConfig] = None
) -> list[TAESignature]:
    """
    Ejecuta el pipeline sobre múltiples sujetos y devuelve lista de TAESignature.
    Adecuado para los n=109 sujetos de EEGMMI.
    """
    if config is None:
        config = PipelineConfig()
    results = []
    for sig, sid in zip(signals, subject_ids):
        r = run_tae_e2(sig, sfreq, sid, channel, dataset, config)
        results.append(r)
    return results


def summary_statistics(results: list[TAESignature]) -> dict:
    """
    Estadísticas de detección TAE sobre una cohorte de sujetos.
    Calcula tasas de detección, medias de los indicadores clave y distribución de ε_c_norm.
    """
    n = len(results)
    if n == 0:
        return {}

    positive = [r for r in results if r.tae_positive]
    rate = len(positive) / n

    pe_max_vals    = [r.pe_max          for r in results if not np.isnan(r.pe_max)]
    delta_pe_vals  = [r.delta_pe        for r in results if not np.isnan(r.delta_pe)]
    dt_vals        = [r.delta_t_reorg_s for r in results if not np.isnan(r.delta_t_reorg_s)]
    dH_vals        = [r.attractor_distance for r in results if not np.isnan(r.attractor_distance)]
    eps_norm_vals  = [r.epsilon_c_norm  for r in results if not np.isnan(r.epsilon_c_norm)]

    def safe_stats(arr):
        if not arr:
            return {"n": 0, "mean": np.nan, "std": np.nan, "median": np.nan}
        return {"n": len(arr), "mean": float(np.mean(arr)),
                "std": float(np.std(arr)), "median": float(np.median(arr))}

    return {
        "n_subjects": n,
        "tae_positive_rate": rate,
        "n_positive": len(positive),
        "pe_max": safe_stats(pe_max_vals),
        "delta_pe": safe_stats(delta_pe_vals),
        "delta_t_reorg_s": safe_stats(dt_vals),
        "hausdorff_distance": safe_stats(dH_vals),
        "epsilon_c_norm": safe_stats(eps_norm_vals),
    }


# ─────────────────────────────────────────────
# DEMO DE EJECUCIÓN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("TAE-E2 Pipeline de Referencia — Demo con datos sintéticos")
    print("github.com/papayaykware")
    print("=" * 60)

    # Generar señal sintética con firma TAE embebida
    signal, times, exc_idx = generate_tae_synthetic_eeg(
        sfreq=128.0, duration_s=30.0, exception_t=15.0, seed=42
    )
    print(f"\nSeñal generada: {len(signal)} muestras, {len(signal)/128:.1f}s")
    print(f"Evento excepcional en muestra {exc_idx} ({exc_idx/128:.2f}s)\n")

    # Configuración personalizada
    config = PipelineConfig(
        pe_order=5,
        window_s=2.0,
        step_s=0.25,
        pe_peak_zscore_min=2.0,
        delta_pe_max=-0.03
    )

    # Ejecutar pipeline
    result = run_tae_e2(
        signal=signal,
        sfreq=128.0,
        subject_id="DEMO_S01",
        channel="Cz_synth",
        dataset=Dataset.EEGMMI,
        config=config
    )

    # Resultados
    print("─── Resultados TAE-E2 ───────────────────────────")
    print(f"Firma TAE detectada : {'✓ SÍ' if result.tae_positive else '✗ NO'}")
    print(f"Confianza           : {result.confidence*100:.0f}%")
    print(f"\n[P1] PE_max         : {result.pe_max:.4f}  (z={result.pe_max_zscore:.2f})")
    print(f"[P2] Δt reorg.      : {result.delta_t_reorg_s:.3f}s")
    print(f"[P3] ΔPE (post-pre) : {result.delta_pe:+.4f}")
    print(f"\n[IV] d_H(A₀,A₁)    : {result.attractor_distance:.4f}")
    print(f"[V]  ε_c            : {result.epsilon_c:.4f}")
    print(f"     ε_c_norm       : {result.epsilon_c_norm:.4f}")

    # Estadísticas de cohorte simulada (3 réplicas con semillas distintas)
    print("\n─── Demo batch (3 sujetos sintéticos) ──────────")
    signals_batch = [generate_tae_synthetic_eeg(sfreq=128., duration_s=30.,
                     exception_t=15., seed=s)[0] for s in [42, 7, 99]]
    ids_batch = ["DEMO_S01", "DEMO_S02", "DEMO_S03"]
    batch_results = batch_analysis(signals_batch, 128., ids_batch, config=config)
    stats = summary_statistics(batch_results)
    print(f"Tasa de detección TAE positiva : {stats['tae_positive_rate']*100:.0f}%")
    print(f"PE_max medio                   : {stats['pe_max']['mean']:.4f}")
    print(f"ΔPE medio                      : {stats['delta_pe']['mean']:+.4f}")
    print(f"ε_c_norm medio                 : {stats['epsilon_c_norm']['mean']:.4f}")

    # Visualización
    print("\nGenerando visualización...")
    fig = plot_tae_signature(signal, 128., result, config, save_path="tae_e2_demo.png")
    plt.show()
    print("Figura guardada en tae_e2_demo.png")
    print("\nPipeline TAE-E2 completado.")
