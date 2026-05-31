import numpy as np
from typing import Dict, List, Optional, Tuple

# Coordenadas esféricas estándar sistema 10-20 (theta, phi en radianes)
# Subconjunto de 19 canales seleccionado como target CPEA
CPEA_MONTAGE_19 = {
    'Fp1': (-0.308, 1.571), 'Fp2': (0.308, 1.571),
    'F7':  (-0.524, 1.309), 'F3':  (-0.309, 1.047),
    'Fz':  (0.000, 0.785),  'F4':  (0.309, 1.047),
    'F8':  (0.524, 1.309),  'T7':  (-0.785, 0.785),
    'C3':  (-0.524, 0.524), 'Cz':  (0.000, 0.000),
    'C4':  (0.524, 0.524),  'T8':  (0.785, 0.785),
    'P7':  (-0.524, -0.524),'P3':  (-0.309, -0.524),
    'Pz':  (0.000, -0.524), 'P4':  (0.309, -0.524),
    'P8':  (0.524, -0.524), 'O1':  (-0.308, -1.047),
    'O2':  (0.308, -1.047)
}

class SensorTopologyManager:
    """
    Proyecta señal EEG de hardware heterogéneo al montaje target CPEA-19.
    
    Para canales disponibles: copia directa.
    Para canales ausentes: interpolación esférica (spline de superficie)
                          o flag de ausencia según configuración.
    """
    
    def __init__(
        self,
        available_channels: List[str],
        interpolate_missing: bool = True,
        target_montage: Dict = CPEA_MONTAGE_19
    ):
        self.target_montage = target_montage
        self.target_channels = list(target_montage.keys())
        self.n_target = len(self.target_channels)
        
        # Canales disponibles en el hardware actual
        self.available = [
            ch for ch in self.target_channels
            if ch in available_channels
        ]
        self.missing = [
            ch for ch in self.target_channels
            if ch not in available_channels
        ]
        
        self.interpolate = interpolate_missing and len(self.missing) > 0
        
        # Máscara binaria de disponibilidad (para metadatos SQI)
        self.channel_mask = np.array([
            1 if ch in self.available else 0
            for ch in self.target_channels
        ], dtype=np.uint8)
        
        # Precomputar pesos de interpolación si se requiere
        if self.interpolate:
            self._weights = self._compute_interpolation_weights()
    
    def _spherical_distance(
        self, ch1: str, ch2: str
    ) -> float:
        t1, p1 = self.target_montage[ch1]
        t2, p2 = self.target_montage[ch2]
        # Distancia angular sobre esfera unitaria
        return np.arccos(np.clip(
            np.sin(t1)*np.sin(t2) + np.cos(t1)*np.cos(t2)*np.cos(p1-p2),
            -1.0, 1.0
        ))
    
    def _compute_interpolation_weights(self) -> Dict[str, np.ndarray]:
        """
        Para cada canal missing, peso de cada canal available
        basado en distancia esférica inversa.
        """
        weights = {}
        for m_ch in self.missing:
            dists = np.array([
                self._spherical_distance(m_ch, a_ch)
                for a_ch in self.available
            ])
            # Interpolación IDW (Inverse Distance Weighting)
            # Exponente p=2 es estándar para señal EEG
            w = 1.0 / (dists**2 + 1e-6)
            weights[m_ch] = w / w.sum()
        return weights
    
    def project(
        self,
        data: np.ndarray,              # (n_available_ch, n_samples)
        available_channel_names: List[str]
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Retorna:
            projected: (19, n_samples) — espacio CPEA-19
            channel_mask: (19,) — 1=disponible, 0=interpolado/ausente
        """
        n_samples = data.shape[1]
        projected = np.zeros((self.n_target, n_samples))
        
        # Índices de canales disponibles en el array de entrada
        avail_idx = {ch: i for i, ch in enumerate(available_channel_names)}
        
        for i, target_ch in enumerate(self.target_channels):
            if target_ch in avail_idx:
                projected[i] = data[avail_idx[target_ch]]
            elif self.interpolate and target_ch in self._weights:
                # Interpolación esférica
                w = self._weights[target_ch]
                for j, a_ch in enumerate(self.available):
                    if a_ch in avail_idx:
                        projected[i] += w[j] * data[avail_idx[a_ch]]
            # Si no está disponible y no se interpola: queda en 0
            # channel_mask[i] == 0 indica al pipeline que lo ignore
        
        return projected, self.channel_mask
