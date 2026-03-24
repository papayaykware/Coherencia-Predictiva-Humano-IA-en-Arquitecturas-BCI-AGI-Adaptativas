"""
Script de prueba para verificar la integración AGI.
Ejecutar: python tests/test_agi_integration.py
"""

import sys
sys.path.append('.')

from src.agi_client import AGIFactory
import yaml

def test_ollama():
    """Prueba conexión con Ollama."""
    config = {
        'provider': 'ollama',
        'model': 'llama3',
        'base_url': 'http://localhost:11434'
    }
    client = AGIFactory.create(config)
    
    prompt = "Describe brevemente qué es la coherencia predictiva entre EEG y AGI."
    response = client.generate_response(prompt)
    print(f"Ollama response: {response}")
    
    # Probar embedding
    emb = client.get_embedding(prompt)
    print(f"Embedding shape: {emb.shape}")

def test_openai():
    """Prueba conexión con OpenAI (requiere API key configurada)."""
    config = {
        'provider': 'openai',
        'model': 'gpt-3.5-turbo'
    }
    try:
        client = AGIFactory.create(config)
        prompt = "Define coherencia predictiva en BCI-AGI systems."
        response = client.generate_response(prompt)
        print(f"OpenAI response: {response}")
    except Exception as e:
        print(f"OpenAI test skipped: {e}")

if __name__ == "__main__":
    print("=== Testing AGI Integration ===")
    test_ollama()
    test_openai()
