# Añadir estas importaciones al inicio
import yaml
from pathlib import Path
from src.agi_client import AGIFactory
import numpy as np

# Modificar la función principal o crear una nueva función run_with_agi
def run_pipeline_with_agi(config_path="config/agi_config.yaml", mode="online"):
    """
    Ejecuta el pipeline CPEA integrando AGI real.
    
    Args:
        config_path: Ruta al archivo de configuración AGI
        mode: 'baseline' (sin AGI) o 'online' (con AGI)
    """
    # Cargar configuración
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Inicializar cliente AGI
    agi_client = AGIFactory.create(config['agi'])
    logger.info(f"AGI cliente inicializado: {config['agi']['provider']} - {config['agi']['model']}")
    
    # Configuración del prompt template
    prompt_template = config['agi'].get('prompt_template', 
        "Características EEG: {features}. Responde como AGI.")
    
    # Simulación de obtención de features EEG (reemplazar con tu pipeline real)
    # Esto debería venir de tu clasificador EEG existente
    eeg_features = {
        'attention': 0.75,
        'relaxation': 0.32,
        'intent': 'motor_imagery_left',
        'features_summary': '[0.12, -0.45, 0.67, ...]'  # Resumen o vector completo
    }
    
    # Construir prompt con features
    prompt = prompt_template.format(**eeg_features)
    logger.info(f"Prompt enviado a AGI: {prompt[:100]}...")
    
    # Obtener respuesta del AGI
    response = agi_client.generate_response(
        prompt,
        temperature=config['agi'].get('temperature', 0.7),
        max_tokens=config['agi'].get('max_tokens', 150)
    )
    
    logger.info(f"Respuesta AGI: {response}")
    
    # Obtener embedding de la respuesta para métricas de coherencia
    response_embedding = agi_client.get_embedding(response)
    
    # Simular embedding EEG (esto debería venir de tu modelo EEG)
    eeg_embedding = np.random.randn(len(response_embedding))
    
    # Calcular coherencia predictiva (ejemplo simple)
    from scipy.spatial.distance import cosine
    coherence = 1 - cosine(eeg_embedding, response_embedding)
    logger.info(f"Índice de Coherencia Predictiva (simulado): {coherence:.4f}")
    
    # Aquí iría la integración con tu bucle adaptativo y métricas ICP
    return {
        'prompt': prompt,
        'response': response,
        'coherence': coherence,
        'eeg_features': eeg_features
    }

if __name__ == "__main__":
    # Ejecutar prueba
    result = run_pipeline_with_agi()
    print(json.dumps(result, indent=2, default=str))
