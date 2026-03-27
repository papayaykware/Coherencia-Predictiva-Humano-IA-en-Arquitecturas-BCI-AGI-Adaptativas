# src/metfi/schumann_detector.py

"""
Detector de resonancias Schumann en señales EEG.
Identifica acoplamiento entre actividad neural y campo geomagnético.
"""

import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class SchumannResonanceDetector:
    """
    Detecta resonancias Schumann en datos EEG y calcula métricas de acoplamiento.
    Frecuencias de interés: 7.83 Hz, 14.3 Hz, 20.8 Hz.
    """
    
    # Frecuencias de resonancia Schumann (Hz)
    SCHUMANN_FREQUENCIES = {
        'fundamental': 7.83,
        'first_overtone': 14.3,
        'second_overtone': 20.8,
        'third_overtone': 27.3,
        'fourth_overtone': 33.8
    }
    
    # Bandas de frecuencia con tolerancia
    BAND_TOLERANCE = 0.5  # Hz
    
    def __init__(self, eeg_sample_rate: float = 256.0):
        """
        Args:
            eeg_sample_rate: Frecuencia de muestreo del EEG (Hz)
        """
        self.eeg_sample_rate = eeg_sample_rate
        self.last_power_ratios: Optional[Dict] = None
        
        # Crear filtros para cada banda
        self._create_filters()
        
        logger.info("SchumannResonanceDetector inicializado")
    
    def _create_filters(self):
        """Crea filtros Butterworth para cada banda de resonancia."""
        self.filters = {}
        nyquist = self.eeg_sample_rate / 2
        
        for name, freq in self.SCHUMANN_FREQUENCIES.items():
            low = max(0.5, freq - self.BAND_TOLERANCE)
            high = min(nyquist - 1, freq + self.BAND_TOLERANCE)
            
            if low < high:
                b, a = signal.butter(4, [low/nyquist, high/nyquist], btype='band')
                self.filters[name] = (b, a)
    
    def detect_resonance(self, 
                         eeg_channel: np.ndarray, 
                         return_spectrum: bool = False) -> Dict:
        """
        Detecta resonancias Schumann en un canal EEG.
        
        Args:
            eeg_channel: Señal EEG (vector 1D)
            return_spectrum: Si es True, devuelve espectro completo
        
        Returns:
            Diccionario con métricas de resonancia
        """
        if len(eeg_channel) < self.eeg_sample_rate:  # Mínimo 1 segundo
            return {'error': 'insufficient_data'}
        
        # Calcular espectro de potencia
        freqs, psd = signal.welch(
            eeg_channel, 
            fs=self.eeg_sample_rate,
            nperseg=min(512, len(eeg_channel)//2),
            noverlap=256
        )
        
        # Calcular potencia en bandas de resonancia
        resonance_powers = {}
        total_power = np.sum(psd)
        
        for name, freq in self.SCHUMANN_FREQUENCIES.items():
            # Encontrar índice más cercano
            idx = np.argmin(np.abs(freqs - freq))
            
            # Potencia en un entorno de ±0.5 Hz
            band_mask = (freqs >= freq - self.BAND_TOLERANCE) & (freqs <= freq + self.BAND_TOLERANCE)
            band_power = np.sum(psd[band_mask])
            
            # Potencia relativa
            relative_power = band_power / total_power if total_power > 0 else 0
            
            # SNR (potencia en banda vs. potencia en bandas vecinas)
            neighbor_mask = (freqs >= freq - 2) & (freqs <= freq + 2) & (~band_mask)
            neighbor_power = np.sum(psd[neighbor_mask]) if np.any(neighbor_mask) else 1e-10
            snr = 10 * np.log10(band_power / neighbor_power)
            
            resonance_powers[name] = {
                'absolute_power': band_power,
                'relative_power': relative_power,
                'snr_db': snr,
                'frequency': freq,
                'detected': snr > 3.0  # Umbral de detección
            }
        
        self.last_power_ratios = resonance_powers
        
        # Calcular índice de acoplamiento Schumann-EEG
        coupling_index = self._calculate_coupling_index(resonance_powers)
        
        result = {
            'resonance_powers': resonance_powers,
            'coupling_index': coupling_index,
            'primary_resonance': self._get_primary_resonance(resonance_powers),
            'timestamp': time.time()
        }
        
        if return_spectrum:
            result['frequencies'] = freqs.tolist()
            result['psd'] = psd.tolist()
        
        return result
    
    def _calculate_coupling_index(self, resonance_powers: Dict) -> float:
        """Calcula índice de acoplamiento entre EEG y resonancias Schumann."""
        # Basado en suma ponderada de SNR en bandas relevantes
        weights = {
            'fundamental': 0.5,
            'first_overtone': 0.3,
            'second_overtone': 0.2
        }
        
        coupling = 0.0
        total_weight = 0.0
        
        for name, weight in weights.items():
            if name in resonance_powers:
                snr = resonance_powers[name]['snr_db']
                # Normalizar SNR a [0,1] (asumiendo rango 0-15 dB)
                normalized_snr = min(1.0, max(0.0, snr / 15.0))
                coupling += weight * normalized_snr
                total_weight += weight
        
        return coupling / total_weight if total_weight > 0 else 0.0
    
    def _get_primary_resonance(self, resonance_powers: Dict) -> str:
        """Identifica la resonancia dominante."""
        best_resonance = 'fundamental'
        best_snr = 0
        
        for name, data in resonance_powers.items():
            if data['snr_db'] > best_snr:
                best_snr = data['snr_db']
                best_resonance = name
        
        return best_resonance
    
    def detect_temporal_evolution(self, 
                                  eeg_stream: List[np.ndarray],
                                  window_seconds: float = 10.0) -> List[Dict]:
        """
        Detecta evolución temporal de resonancias en un stream de EEG.
        
        Args:
            eeg_stream: Lista de segmentos EEG
            window_seconds: Ventana de análisis (segundos)
        
        Returns:
            Lista de resultados por ventana
        """
        samples_per_window = int(self.eeg_sample_rate * window_seconds)
        results = []
        
        for i in range(0, len(eeg_stream), samples_per_window):
            window_data = eeg_stream[i:i+samples_per_window]
            if len(window_data) >= samples_per_window:
                window_array = np.concatenate(window_data)
                result = self.detect_resonance(window_array)
                result['window_index'] = i // samples_per_window
                results.append(result)
        
        return results
    
    def get_acoplamiento_score(self) -> float:
        """Devuelve el último índice de acoplamiento calculado."""
        if self.last_power_ratios:
            return self._calculate_coupling_index(self.last_power_ratios)
        return 0.0
