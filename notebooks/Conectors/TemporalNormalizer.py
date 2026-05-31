import numpy as np
from scipy.signal import resample_poly
from collections import deque
from typing import Tuple
import time

class TemporalNormalizer:
    """
    Normaliza timestamps y tasa de muestreo de tramas BrainFlow crudas.
    
    Parámetros:
        source_fs: tasa de muestreo nominal del hardware (Hz)
        target_fs: tasa de muestreo de salida (Hz), default 256
        pll_alpha: ganancia del PLL para corrección de jitter (0.01–0.1)
        max_jitter_ms: umbral de jitter máximo admisible (ms)
    """
    
    TARGET_FS = 256  # Hz — tasa normalizada del corpus CPEA
    
    def __init__(
        self,
        source_fs: float,
        target_fs: int = TARGET_FS,
        pll_alpha: float = 0.05,
        max_jitter_ms: float = 2.0
    ):
        self.source_fs = source_fs
        self.target_fs = target_fs
        self.pll_alpha = pll_alpha
        self.max_jitter_ms = max_jitter_ms
        
        # Estado del PLL
        self._phase_error = 0.0
        self._freq_estimate = source_fs
        self._last_timestamp = None
        self._timestamp_buffer = deque(maxlen=256)  # ~1s de historia
        
        # Ratio de remuestreo (fracción exacta para resample_poly)
        from math import gcd
        g = gcd(int(target_fs), int(source_fs))
        self.up = int(target_fs) // g
        self.down = int(source_fs) // g
    
    def process(
        self,
        data: np.ndarray,          # (n_channels, n_samples) — crudo de BF
        timestamps: np.ndarray     # (n_samples,) — timestamps BrainFlow
    ) -> Tuple[np.ndarray, np.ndarray, float]:
        """
        Retorna: (data_resampled, timestamps_corrected, jitter_ms_estimated)
        """
        # --- 1. Estimación de jitter mediante PLL ---
        if self._last_timestamp is not None:
            dt_nominal = len(timestamps) / self.source_fs
            dt_actual = timestamps[-1] - self._last_timestamp
            phase_error = dt_actual - dt_nominal
            
            # Actualización PLL (integrador de primer orden)
            self._phase_error += self.pll_alpha * phase_error
            jitter_ms = abs(phase_error) * 1000.0
        else:
            jitter_ms = 0.0
        
        self._last_timestamp = timestamps[-1]
        self._timestamp_buffer.extend(timestamps)
        
        # --- 2. Corrección de timestamps ---
        # Reconstrucción de timestamps ideales anclados al primer punto
        t_start_corrected = timestamps[0] - self._phase_error
        n_samples = len(timestamps)
        timestamps_corrected = (
            t_start_corrected
            + np.arange(n_samples) / self.source_fs
        )
        
        # --- 3. Remuestreo de señal (si source_fs != target_fs) ---
        if self.source_fs != self.target_fs:
            data_resampled = resample_poly(
                data, self.up, self.down, axis=1
            )
            # Reconstruir timestamps a la nueva tasa
            n_resampled = data_resampled.shape[1]
            timestamps_corrected = (
                t_start_corrected
                + np.arange(n_resampled) / self.target_fs
            )
        else:
            data_resampled = data
        
        return data_resampled, timestamps_corrected, jitter_ms
