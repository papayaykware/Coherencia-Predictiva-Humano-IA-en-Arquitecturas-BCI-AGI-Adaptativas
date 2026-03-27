# Integración en src/pipeline/run_pipeline.py (extensión)

from src.tae.exception_detector import TAEExceptionDetector, ExceptionEvent
from src.tae.anomaly_classifier import AnomalyClassifier

class CPEAPipeline:
    def __init__(self):
        # ... inicialización existente ...
        
        # Inicializar detector TAE
        self.tae_detector = TAEExceptionDetector(
            window_size=100,
            lambda_threshold=2.0
        )
        self.anomaly_classifier = AnomalyClassifier()
        
        # Callback para respuesta adaptativa
        self.on_exception_callback = self.handle_exception
    
    def process_trial(self, eeg_data, intent_correct=None):
        # ... procesamiento existente ...
        
        # Extraer características EEG
        eeg_features = self.extract_features(eeg_data)
        
        # Calcular ICP
        icp_value = self.calculate_icp(eeg_features, agi_response)
        
        # Actualizar detector TAE
        exception = self.tae_detector.update(
            eeg_features=eeg_features,
            icp_value=icp_value,
            agi_embedding=agi_embedding,
            intent_predicted=intent_predicted,
            intent_correct=intent_correct
        )
        
        # Si se detectó excepción, activar respuesta adaptativa
        if exception:
            self.handle_exception(exception)
        
        return results
    
    def handle_exception(self, exception: ExceptionEvent):
        """Maneja la excepción detectada."""
        # Clasificar anomalía
        anomaly_type = self.anomaly_classifier.classify(exception.context)
        exception.exception_type = anomaly_type
        
        # Incrementar contador
        self.anomaly_classifier.increment_count(anomaly_type)
        
        # Obtener respuesta sugerida
        response = self.anomaly_classifier.get_response(anomaly_type)
        
        # Ejecutar respuesta adaptativa
        if response == 'activar_filtro_adaptativo':
            self.activate_adaptive_filtering()
        elif response == 'activar_modo_calibracion':
            self.activate_calibration_mode()
        elif response == 'reducir_ganancia_adaptacion':
            self.reduce_adaptation_gain()
        elif response == 'reforzar_prompt':
            self.strengthen_agi_prompt()
        
        # Registrar evento
        self.log_exception(exception)
        
        # Si la severidad es alta, activar Safe-Switch
        if exception.severity > 0.8:
            self.activate_safe_switch()
