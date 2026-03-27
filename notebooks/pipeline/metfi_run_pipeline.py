# Extensión en src/pipeline/run_pipeline.py

from src.metfi.geomag_stream import GeomagneticDataStream, GeomagneticConfig
from src.metfi.correlation_analyzer import METFICorrelationAnalyzer
from src.metfi.schumann_detector import SchumannResonanceDetector

class CPEAPipeline:
    def __init__(self):
        # ... inicialización existente ...
        
        # Inicializar módulos METFI
        self.geomag_stream = GeomagneticDataStream(
            GeomagneticConfig(update_interval=30.0)
        )
        self.metfi_analyzer = METFICorrelationAnalyzer(
            window_size=1800,  # 30 minutos
            correlation_threshold=0.4
        )
        self.schumann_detector = SchumannResonanceDetector(
            eeg_sample_rate=256.0
        )
        
        # Métricas METFI
        self.metfi_metrics = {
            'geomagnetic_influence': 0.0,
            'schumann_coupling': 0.0,
            'icp_kp_correlation': 0.0,
            'last_geomagnetic_sample': None
        }
        
        # Iniciar stream geomagnético
        self.geomag_stream.start()
    
    def process_trial(self, eeg_data, intent_correct=None):
        # ... procesamiento existente ...
        
        # 1. Obtener datos geomagnéticos actuales
        geomag_sample = self.geomag_stream.get_current()
        if geomag_sample:
            self.metfi_metrics['last_geomagnetic_sample'] = geomag_sample
        
        # 2. Detectar resonancias Schumann en EEG
        if len(eeg_data) >= 256:  # Mínimo 1 segundo
            schumann_result = self.schumann_detector.detect_resonance(eeg_data)
            self.metfi_metrics['schumann_coupling'] = schumann_result.get('coupling_index', 0.0)
        
        # 3. Calcular potencia alpha (banda 8-12 Hz)
        alpha_power = self.calculate_alpha_power(eeg_data)
        
        # 4. Actualizar analizador de correlación
        if geomag_sample:
            correlation = self.metfi_analyzer.update(
                icp_value=icp_value,
                eeg_alpha_power=alpha_power,
                geomag_sample=geomag_sample
            )
            
            if correlation:
                self.metfi_metrics.update(correlation)
                self.metfi_metrics['geomagnetic_influence'] = \
                    self.metfi_analyzer.get_geomagnetic_influence_score()
        
        # 5. Ajustar ICP basado en influencia geomagnética (opcional)
        adjusted_icp = self._apply_geomagnetic_correction(icp_value)
        
        return results
    
    def _apply_geomagnetic_correction(self, icp: float) -> float:
        """Aplica corrección al ICP basada en influencia geomagnética."""
        influence = self.metfi_metrics.get('geomagnetic_influence', 0.5)
        
        # Si hay tormenta geomagnética, el ICP puede verse afectado
        if self.geomag_stream.is_geomagnetic_storm(threshold_kp=5.0):
            # Reducir confianza en ICP durante tormentas
            correction_factor = 0.8
        else:
            correction_factor = 1.0
        
        # Ajustar ICP por influencia geomagnética
        adjusted = icp * (1 - influence * 0.2) * correction_factor
        return max(0.0, min(1.0, adjusted))
    
    def shutdown(self):
        """Detiene streams y libera recursos."""
        self.geomag_stream.stop()
        # ... otros recursos ...
