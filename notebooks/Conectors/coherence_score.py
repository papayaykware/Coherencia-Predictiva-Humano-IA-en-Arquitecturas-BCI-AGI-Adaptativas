import numpy as np
from scipy.signal import csd, welch
from itertools import combinations
from typing import Dict, List, Tuple

class CoherenceScorer:
    """
    Calcula coherence_score como proxy de calidad de señal y estimador
    de primer orden de coherencia corticotalámica.
    
    Implementa coherencia espectral de Welch entre pares de canales
    en bandas de interés CPEA: theta (4-8Hz), alpha (8-13Hz),
    beta_low (13-20Hz), gamma_low (30-45Hz).
    
    El coherence_score NO es Φ_TICAM. Es un indicador de si la señal
    contiene estructura de coherencia explotable por el pipeline.
    """
    
    BANDS = {
        'theta':     (4.0,  8.0),
        'alpha':     (8.0,  13.0),
        'beta_low':  (13.0, 20.0),
        'gamma_low': (30.0, 45.0),
    }
    
    # Pares de canales de interés para coherencia talamocortical
    # (frontal-parietal, interhemisférico, temporal-occipital)
    PRIORITY_PAIRS_19CH = [
        ('F3', 'P3'), ('F4', 'P4'),   # frontoparietal ipsilateral
        ('Fz', 'Pz'),                  # frontoparietal medial
        ('F3', 'F4'), ('P3', 'P4'),   # interhemisférico
        ('T7', 'T8'),                  # temporal interhemisférico
        ('C3', 'C4'),                  # central interhemisférico
        ('F3', 'O1'), ('F4', 'O2'),   # frontooccipital
    ]
    
    def __init__(
        self,
        channel_names: List[str],
        fs: int = 256,
        window_samples: int = 256,
        channel_mask: np.ndarray = None
    ):
        self.channel_names = channel_names
        self.fs = fs
        self.window_samples = window_samples
        self.channel_mask = channel_mask
        
        # Filtrar pares disponibles según canales activos y máscara
        ch_set = set(channel_names)
        if channel_mask is not None:
            ch_set = {
                ch for ch, m in zip(channel_names, channel_mask)
                if m == 1
            }
        
        self.active_pairs = [
            (a, b) for a, b in self.PRIORITY_PAIRS_19CH
            if a in ch_set and b in ch_set
        ]
    
    def compute(
        self,
        window: np.ndarray,    # (n_channels, n_samples)
        sqi_result: 'SQIResult'
    ) -> Dict:
        """
        Retorna diccionario con coherence_score global y por banda/par.
        Solo opera sobre canales con SQI-per-channel == 1.
        """
        ch_idx = {ch: i for i, ch in enumerate(self.channel_names)}
        
        band_scores = {}
        pair_coherences = {}
        
        for band_name, (f_low, f_high) in self.BANDS.items():
            band_vals = []
            
            for ch_a, ch_b in self.active_pairs:
                idx_a = ch_idx.get(ch_a)
                idx_b = ch_idx.get(ch_b)
                
                if idx_a is None or idx_b is None:
                    continue
                
                # Solo canales con SQI bueno
                if (sqi_result.sqi_per_channel[idx_a] == 0 or
                        sqi_result.sqi_per_channel[idx_b] == 0):
                    continue
                
                sig_a = window[idx_a]
                sig_b = window[idx_b]
                
                # Densidad espectral cruzada
                freqs, Pxy = csd(
                    sig_a, sig_b,
                    fs=self.fs,
                    nperseg=self.window_samples // 2
                )
                _, Pxx = welch(sig_a, fs=self.fs,
                               nperseg=self.window_samples // 2)
                _, Pyy = welch(sig_b, fs=self.fs,
                               nperseg=self.window_samples // 2)
                
                # Coherencia de magnitud cuadrada (MSC)
                msc = np.abs(Pxy)**2 / (Pxx * Pyy + 1e-12)
                
                # Media en la banda
                band_mask = (freqs >= f_low) & (freqs <= f_high)
                if band_mask.sum() == 0:
                    continue
                
                coherence_band = float(np.mean(msc[band_mask]))
                
                pair_key = f"{ch_a}-{ch_b}"
                if pair_key not in pair_coherences:
                    pair_coherences[pair_key] = {}
                pair_coherences[pair_key][band_name] = coherence_band
                band_vals.append(coherence_band)
            
            band_scores[band_name] = (
                float(np.mean(band_vals)) if band_vals else 0.0
            )
        
        # coherence_score global: media ponderada entre bandas
        # Alpha y theta tienen mayor peso en el contexto CPEA/TICAM
        weights = {
            'theta': 0.30,
            'alpha': 0.35,
            'beta_low': 0.20,
            'gamma_low': 0.15
        }
        coherence_score = sum(
            band_scores.get(b, 0.0) * w
            for b, w in weights.items()
        )
        
        return {
            'coherence_score': coherence_score,
            'band_scores': band_scores,
            'pair_coherences': pair_coherences,
            'n_pairs_computed': len([
                v for v in pair_coherences.values() if v
            ]),
            'active_channels': [
                ch for ch in self.channel_names
                if ch_idx.get(ch) is not None and
                sqi_result.sqi_per_channel[ch_idx[ch]] == 1
            ]
        }
