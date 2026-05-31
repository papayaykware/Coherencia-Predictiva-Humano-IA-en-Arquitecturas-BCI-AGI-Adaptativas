import numpy as np
from scipy.stats import kurtosis as scipy_kurtosis
from scipy.signal import welch
from collections import deque
from dataclasses import dataclass, field
from typing import List

@dataclass
class SQIResult:
    sqi_global: float          # 0.0 – 1.0
    sqi_per_channel: np.ndarray
    n_channels_ok: int
    n_channels_total: int
    variance_ok: np.ndarray    # bool por canal
    kurtosis_ok: np.ndarray    # bool por canal
    hf_ratio_ok: np.ndarray   # bool por canal
    jitter_ok: bool
    jitter_ms: float
    window_accepted: bool

class OnlineNoiseEstimator:
    """
    Estimador de SQI en línea sobre ventanas deslizantes de 1 segundo.
    
    Umbrales por defecto calibrados para EEG en reposo, sujetos adultos,
    hardware de investigación. Ajustables por configuración.
    """
    
    def __init__(
        self,
        n_channels: int,
        fs: int = 256,
        window_s: float = 1.0,
        var_min: float = 0.1,    # μV² — electrodo desconectado
        var_max: float = 500.0,  # μV² — artefacto de movimiento
        kurt_max: float = 7.0,   # kurtosis — EMG
        hf_ratio_max: float = 0.3,  # P(45-60Hz)/P(1-45Hz)
        jitter_max_ms: float = 2.0,
        sqi_threshold: float = 0.70
    ):
        self.n_channels = n_channels
        self.fs = fs
        self.window_samples = int(window_s * fs)
        self.var_min = var_min
        self.var_max = var_max
        self.kurt_max = kurt_max
        self.hf_ratio_max = hf_ratio_max
        self.jitter_max_ms = jitter_max_ms
        self.sqi_threshold = sqi_threshold
        
        # Buffer circular por canal
        self._buffers = [
            deque(maxlen=self.window_samples)
            for _ in range(n_channels)
        ]
        self._n_filled = 0
    
    def update(
        self,
        data: np.ndarray,     # (n_channels, n_new_samples)
        jitter_ms: float
    ) -> Optional[SQIResult]:
        """
        Actualiza los buffers y retorna SQIResult si hay ventana completa.
        Retorna None si el buffer no está lleno aún.
        """
        n_new = data.shape[1]
        for ch in range(self.n_channels):
            self._buffers[ch].extend(data[ch, :].tolist())
        
        self._n_filled = min(
            self._n_filled + n_new,
            self.window_samples
        )
        
        if self._n_filled < self.window_samples:
            return None
        
        # Construir array de ventana completa
        window = np.array([
            list(self._buffers[ch])
            for ch in range(self.n_channels)
        ])  # (n_channels, window_samples)
        
        return self._compute_sqi(window, jitter_ms)
    
    def _compute_sqi(
        self,
        window: np.ndarray,
        jitter_ms: float
    ) -> SQIResult:
        
        # SQI-1: Varianza por canal
        variances = np.var(window, axis=1)
        variance_ok = (variances >= self.var_min) & (variances <= self.var_max)
        
        # SQI-2: Exceso de kurtosis por canal
        kurt_values = np.array([
            scipy_kurtosis(window[ch], fisher=True)
            for ch in range(self.n_channels)
        ])
        kurtosis_ok = kurt_values <= self.kurt_max
        
        # SQI-3: Ratio de potencia de alta frecuencia
        hf_ratio_ok = np.ones(self.n_channels, dtype=bool)
        for ch in range(self.n_channels):
            freqs, psd = welch(
                window[ch],
                fs=self.fs,
                nperseg=self.window_samples // 4
            )
            p_signal = np.trapz(
                psd[(freqs >= 1) & (freqs <= 45)],
                freqs[(freqs >= 1) & (freqs <= 45)]
            )
            p_hf = np.trapz(
                psd[(freqs >= 45) & (freqs <= 60)],
                freqs[(freqs >= 45) & (freqs <= 60)]
            )
            ratio = p_hf / (p_signal + 1e-12)
            hf_ratio_ok[ch] = ratio <= self.hf_ratio_max
        
        # SQI-4: Jitter de timestamp
        jitter_ok = jitter_ms <= self.jitter_max_ms
        
        # SQI por canal (combinación de SQI-1, SQI-2, SQI-3)
        channel_ok = variance_ok & kurtosis_ok & hf_ratio_ok
        n_ok = int(np.sum(channel_ok))
        sqi_global = (n_ok / self.n_channels) * (1.0 if jitter_ok else 0.8)
        
        return SQIResult(
            sqi_global=sqi_global,
            sqi_per_channel=channel_ok.astype(float),
            n_channels_ok=n_ok,
            n_channels_total=self.n_channels,
            variance_ok=variance_ok,
            kurtosis_ok=kurtosis_ok,
            hf_ratio_ok=hf_ratio_ok,
            jitter_ok=jitter_ok,
            jitter_ms=jitter_ms,
            window_accepted=sqi_global >= self.sqi_threshold
        )
