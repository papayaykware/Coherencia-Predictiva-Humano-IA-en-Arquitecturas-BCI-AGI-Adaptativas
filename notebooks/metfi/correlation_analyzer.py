# src/metfi/correlation_analyzer.py

"""
Analizador de correlación entre métricas CPEA y datos geomagnéticos.
Implementa análisis de coherencia espectral y correlación cruzada.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy import signal, stats
from scipy.fft import fft, fftfreq
from collections import deque
import logging

from .geomag_stream import GeomagneticSample

logger = logging.getLogger(__name__)

class METFICorrelationAnalyzer:
    """
    Analiza correlaciones entre actividad cerebral (ICP, EEG) y
    variables geomagnéticas (Kp, Dst, resonancias Schumann).
    """
    
    def __init__(self, 
                 window_size: int = 3600,      # Ventana en segundos
                 sample_rate: float = 1.0,     # Muestras por segundo
                 correlation_threshold: float = 0.5):
        """
        Args:
            window_size: Tamaño de la ventana de análisis (segundos)
            sample_rate: Frecuencia de muestreo de datos (Hz)
            correlation_threshold: Umbral para considerar correlación significativa
        """
        self.window_size = window_size
        self.sample_rate = sample_rate
        self.correlation_threshold = correlation_threshold
        
        # Buffers para datos sincronizados
        self.icp_buffer = deque(maxlen=int(window_size * sample_rate))
        self.eeg_alpha_buffer = deque(maxlen=int(window_size * sample_rate))
        self.geomag_buffer = deque(maxlen=int(window_size * sample_rate))
        
        # Resultados de correlación
        self.last_correlation: Optional[Dict] = None
        
        logger.info("METFICorrelationAnalyzer inicializado")
    
    def update(self, 
               icp_value: float,
               eeg_alpha_power: float,
               geomag_sample: GeomagneticSample) -> Optional[Dict]:
        """
        Actualiza los buffers y calcula correlaciones si hay suficientes datos.
        
        Returns:
            Diccionario con resultados de correlación o None
        """
        # Actualizar buffers
        self.icp_buffer.append(icp_value)
        self.eeg_alpha_buffer.append(eeg_alpha_power)
        self.geomag_buffer.append({
            'timestamp': geomag_sample.timestamp,
            'kp': geomag_sample.kp,
            'd_st': geomag_sample.d_st,
            'schumann_7_83': geomag_sample.schumann_7_83 or 0.0
        })
        
        # Calcular correlaciones si hay suficientes datos
        if len(self.icp_buffer) >= int(300 * self.sample_rate):  # Mínimo 5 minutos
            return self._compute_correlations()
        
        return None
    
    def _compute_correlations(self) -> Dict:
        """Calcula correlaciones entre variables."""
        # Convertir buffers a arrays
        icp_array = np.array(self.icp_buffer)
        alpha_array = np.array(self.eeg_alpha_buffer)
        kp_array = np.array([s['kp'] for s in self.geomag_buffer])
        dst_array = np.array([s['d_st'] for s in self.geomag_buffer])
        schumann_array = np.array([s['schumann_7_83'] for s in self.geomag_buffer])
        
        results = {
            'icp_vs_kp': self._pearson_correlation(icp_array, kp_array),
            'icp_vs_dst': self._pearson_correlation(icp_array, dst_array),
            'alpha_vs_schumann': self._pearson_correlation(alpha_array, schumann_array),
            'alpha_vs_kp': self._pearson_correlation(alpha_array, kp_array),
            'cross_correlation_icp_kp': self._cross_correlation(icp_array, kp_array),
            'coherence_alpha_schumann': self._spectral_coherence(alpha_array, schumann_array)
        }
        
        # Añadir significancia estadística
        for key in ['icp_vs_kp', 'alpha_vs_schumann']:
            if results[key]['correlation'] is not None:
                results[key]['significant'] = abs(results[key]['correlation']) > self.correlation_threshold
        
        self.last_correlation = results
        return results
    
    def _pearson_correlation(self, x: np.ndarray, y: np.ndarray) -> Dict:
        """Calcula correlación de Pearson y p-valor."""
        try:
            # Asegurar misma longitud
            min_len = min(len(x), len(y))
            x = x[-min_len:]
            y = y[-min_len:]
            
            corr, p_value = stats.pearsonr(x, y)
            return {
                'correlation': corr,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        except Exception as e:
            logger.warning(f"Error en correlación de Pearson: {e}")
            return {'correlation': None, 'p_value': 1.0, 'significant': False}
    
    def _cross_correlation(self, x: np.ndarray, y: np.ndarray, max_lag: int = 300) -> Dict:
        """Calcula correlación cruzada con desfases temporales."""
        try:
            min_len = min(len(x), len(y))
            x = x[-min_len:]
            y = y[-min_len:]
            
            # Normalizar
            x = (x - np.mean(x)) / np.std(x)
            y = (y - np.mean(y)) / np.std(y)
            
            # Correlación cruzada
            cross_corr = np.correlate(x, y, mode='full')
            lags = np.arange(-len(x)+1, len(x))
            
            # Encontrar máximo
            max_idx = np.argmax(np.abs(cross_corr))
            max_lag_actual = lags[max_idx] / self.sample_rate  # Convertir a segundos
            
            return {
                'max_correlation': cross_corr[max_idx],
                'lag_seconds': max_lag_actual,
                'significant': abs(cross_corr[max_idx]) > self.correlation_threshold
            }
        except Exception as e:
            logger.warning(f"Error en correlación cruzada: {e}")
            return {'max_correlation': 0, 'lag_seconds': 0, 'significant': False}
    
    def _spectral_coherence(self, x: np.ndarray, y: np.ndarray, fs: float = 1.0) -> Dict:
        """Calcula coherencia espectral entre dos señales."""
        try:
            # Asegurar misma longitud
            min_len = min(len(x), len(y))
            x = x[-min_len:]
            y = y[-min_len:]
            
            # Calcular coherencia
            f, Cxy = signal.coherence(x, y, fs=fs, nperseg=min(256, min_len//4))
            
            # Encontrar picos en bandas de interés
            schumann_bands = {
                '7.83hz': (7.5, 8.2),
                '14.3hz': (13.5, 15.0),
                '20.8hz': (19.5, 21.5)
            }
            
            coherence_peaks = {}
            for band_name, (low, high) in schumann_bands.items():
                band_mask = (f >= low) & (f <= high)
                if np.any(band_mask):
                    coherence_peaks[band_name] = np.mean(Cxy[band_mask])
                else:
                    coherence_peaks[band_name] = 0.0
            
            return {
                'frequencies': f.tolist(),
                'coherence': Cxy.tolist(),
                'band_coherence': coherence_peaks,
                'max_coherence': np.max(Cxy)
            }
        except Exception as e:
            logger.warning(f"Error en coherencia espectral: {e}")
            return {'frequencies': [], 'coherence': [], 'band_coherence': {}, 'max_coherence': 0}
    
    def get_geomagnetic_influence_score(self) -> float:
        """
        Calcula un puntaje de influencia geomagnética basado en correlaciones.
        Score alto = mayor influencia del campo geomagnético en la coherencia.
        """
        if not self.last_correlation:
            return 0.5  # Valor neutral
        
        score = 0.0
        weights = {
            'icp_vs_kp': 0.4,
            'alpha_vs_schumann': 0.4,
            'icp_vs_dst': 0.2
        }
        
        for key, weight in weights.items():
            if key in self.last_correlation:
                corr = self.last_correlation[key].get('correlation')
                if corr is not None:
                    score += weight * abs(corr)
        
        return min(1.0, score)
    
    def get_correlation_summary(self) -> Dict:
        """Devuelve un resumen de las correlaciones actuales."""
        if not self.last_correlation:
            return {'status': 'insufficient_data'}
        
        return {
            'status': 'active',
            'icp_kp_correlation': self.last_correlation['icp_vs_kp'].get('correlation'),
            'alpha_schumann_correlation': self.last_correlation['alpha_vs_schumann'].get('correlation'),
            'geomagnetic_influence_score': self.get_geomagnetic_influence_score(),
            'coherence_peaks': self.last_correlation.get('coherence_alpha_schumann', {}).get('band_coherence', {}),
            'significant_correlations': [
                k for k, v in self.last_correlation.items() 
                if isinstance(v, dict) and v.get('significant', False)
            ]
        }
