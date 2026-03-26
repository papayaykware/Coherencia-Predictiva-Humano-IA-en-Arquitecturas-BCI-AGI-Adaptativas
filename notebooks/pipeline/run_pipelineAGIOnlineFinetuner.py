# ... imports existentes ...
from src.models.agi_finetuner import AGIOnlineFinetuner

class CPEAPipeline:
    def __init__(self, config_path="config/agi_config.yaml"):
        # ... inicialización existente ...
        
        # Reemplazar AGI estático por finetuner adaptativo
        self.agi_finetuner = AGIOnlineFinetuner(config_path)
        
        # Buffer para tracking de ICP
        self.icp_history = []
        
    def process_trial(self, eeg_signal):
        """
        Procesa un trial completo: decodificación EEG, consulta a AGI, cálculo de ICP,
        y almacena para adaptación.
        """
        # 1. Preprocesar EEG
        features = self.extract_eeg_features(eeg_signal)
        
        # 2. Construir prompt con features
        prompt = self.build_prompt(features)
        
        # 3. Obtener respuesta AGI (con adaptación implícita)
        response = self.agi_finetuner.generate_response(prompt, features)
        
        # 4. Calcular ICP (usando tu módulo existente)
        icp = self.compute_icp(eeg_signal, response)
        self.icp_history.append(icp)
        
        # 5. Logging y almacenamiento
        self.log_trial(features, response, icp)
        
        return response, icp

    def build_prompt(self, features):
        """Construye prompt con formato específico para el modelo AGI."""
        return f"""EEG features: attention={features['attention']:.3f}, intent={features['intent']}, alpha_theta_ratio={features.get('alpha_theta_ratio', 0.5):.3f}
        
Based on these neural correlates, your response:"""
