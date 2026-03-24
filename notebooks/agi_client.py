"""
Módulo para conectar el pipeline CPEA con modelos AGI (Ollama/OpenAI).
Permite configuración unificada y paso de features EEG como prompt.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod

import numpy as np
import requests

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAGIClient(ABC):
    """Clase base abstracta para clientes AGI."""
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Genera respuesta a partir de un prompt."""
        pass
    
    @abstractmethod
    def get_embedding(self, text: str) -> np.ndarray:
        """Obtiene embedding de un texto (para métricas de coherencia)."""
        pass


class OllamaClient(BaseAGIClient):
    """Cliente para modelos AGI locales via Ollama."""
    
    def __init__(self, model: str = "llama3", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self._check_connection()
    
    def _check_connection(self):
        """Verifica que Ollama esté disponible."""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=2)
            if response.status_code == 200:
                models = [m['name'] for m in response.json().get('models', [])]
                if self.model not in models:
                    logger.warning(f"Modelo '{self.model}' no encontrado. Usando el primero disponible: {models[0] if models else 'N/A'}")
                    self.model = models[0] if models else self.model
                logger.info(f"Ollama conectado. Modelo: {self.model}")
            else:
                logger.error(f"Ollama no responde correctamente. Código: {response.status_code}")
        except Exception as e:
            logger.error(f"Error conectando con Ollama: {e}")
            logger.info("Asegúrate de que Ollama esté corriendo: `ollama serve`")
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Genera respuesta usando Ollama."""
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9),
                "max_tokens": kwargs.get("max_tokens", 150)
            }
        }
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=kwargs.get("timeout", 30)
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                logger.error(f"Error Ollama: {response.status_code} - {response.text}")
                return "[Error: No se pudo generar respuesta]"
        except Exception as e:
            logger.error(f"Excepción durante generación: {e}")
            return "[Error: Timeout o conexión fallida]"
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Obtiene embedding via Ollama (si el modelo soporta embeddings)."""
        # Nota: Algunos modelos en Ollama soportan embeddings via /api/embeddings
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=10
            )
            if response.status_code == 200:
                embedding = response.json().get("embedding", [])
                if embedding:
                    return np.array(embedding)
            logger.warning(f"No se pudo obtener embedding de Ollama. Usando fallback.")
        except Exception as e:
            logger.debug(f"Embedding no disponible: {e}")
        # Fallback: embedding simulado (para no romper pipeline)
        return np.random.randn(384)  # Dimensión típica


class OpenAIClient(BaseAGIClient):
    """Cliente para OpenAI API."""
    
    def __init__(self, model: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY no configurada. Configura la variable de entorno o pásala explícitamente.")
        try:
            import openai
            self.client = openai.OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError("openai no instalado. Ejecuta: pip install openai")
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Genera respuesta usando OpenAI."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 150),
                top_p=kwargs.get("top_p", 0.9)
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error OpenAI: {e}")
            return "[Error: No se pudo generar respuesta]"
    
    def get_embedding(self, text: str) -> np.ndarray:
        """Obtiene embedding usando OpenAI's embedding model."""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-ada-002",
                input=text
            )
            return np.array(response.data[0].embedding)
        except Exception as e:
            logger.error(f"Error obteniendo embedding: {e}")
            return np.random.randn(1536)  # Dimensión de ada-002


class AGIFactory:
    """Fábrica para crear clientes AGI según configuración."""
    
    @staticmethod
    def create(config: Dict[str, Any]) -> BaseAGIClient:
        provider = config.get("provider", "ollama").lower()
        
        if provider == "ollama":
            return OllamaClient(
                model=config.get("model", "llama3"),
                base_url=config.get("base_url", "http://localhost:11434")
            )
        elif provider == "openai":
            return OpenAIClient(
                model=config.get("model", "gpt-3.5-turbo"),
                api_key=config.get("api_key")
            )
        else:
            raise ValueError(f"Proveedor AGI no soportado: {provider}")
