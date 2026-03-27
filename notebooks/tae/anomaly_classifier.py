# src/tae/anomaly_classifier.py

import numpy as np
from typing import Dict, Any

class AnomalyClassifier:
    """
    Clasifica el tipo específico de anomalía detectada por el sistema TAE.
    Permite activar respuestas adaptativas específicas.
    """
    
    ANOMALY_TYPES = {
        'eeg_anomaly': {
            'description': 'Señal EEG anómala (ruido excesivo, artefactos, desconexión)',
            'suggested_response': 'activar_filtro_adaptativo'
        },
        'agi_mismatch': {
            'description': 'Respuesta AGI incoherente con el contexto EEG',
            'suggested_response': 'reforzar_prompt'
        },
        'latency_spike': {
            'description': 'Aumento anómalo en latencia de procesamiento',
            'suggested_response': 'reducir_complejidad_agi'
        },
        'icp_collapse': {
            'description': 'Caída sostenida del Índice de Coherencia Predictiva',
            'suggested_response': 'activar_modo_calibracion'
        },
        'intent_drift': {
            'description': 'Deriva gradual en la decodificación de intenciones',
            'suggested_response': 'recalibrar_clasificador'
        },
        'neurofeedback_loop': {
            'description': 'Bucle de retroalimentación inestable',
            'suggested_response': 'reducir_ganancia_adaptacion'
        }
    }
    
    def __init__(self):
        self.anomaly_counts = {t: 0 for t in self.ANOMALY_TYPES}
    
    def classify(self, context: Dict[str, Any]) -> str:
        """
        Clasifica la anomalía basada en el contexto proporcionado.
        
        Args:
            context: Diccionario con métricas actuales (icp, prediction_error, latencia, etc.)
        
        Returns:
            Tipo de anomalía detectada
        """
        icp = context.get('icp', 0.5)
        prediction_error = context.get('prediction_error', 0.0)
        uncertainty = context.get('uncertainty', 1.0)
        latency = context.get('latency', 0.0)
        intent_drift = context.get('intent_drift', 0.0)
        
        # Reglas de clasificación
        if icp < 0.3:
            return 'icp_collapse'
        elif prediction_error > 3.0 * uncertainty:
            return 'eeg_anomaly'
        elif latency > 2.0:  # >2 segundos
            return 'latency_spike'
        elif intent_drift > 0.2:
            return 'intent_drift'
        elif context.get('agi_embedding_similarity', 1.0) < 0.5:
            return 'agi_mismatch'
        
        return 'unknown_anomaly'
    
    def get_response(self, anomaly_type: str) -> str:
        """Obtiene la respuesta adaptativa sugerida para el tipo de anomalía."""
        return self.ANOMALY_TYPES.get(anomaly_type, {}).get('suggested_response', 'none')
    
    def increment_count(self, anomaly_type: str):
        """Incrementa el contador para el tipo de anomalía."""
        if anomaly_type in self.anomaly_counts:
            self.anomaly_counts[anomaly_type] += 1
    
    def get_summary(self) -> Dict[str, int]:
        """Devuelve un resumen de las anomalías detectadas."""
        return self.anomaly_counts.copy()
