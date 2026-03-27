# src/tae/exception_detector.py

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ExceptionEvent:
    """Estructura para eventos de excepción detectados."""
    timestamp: float
    exception_type: str  # 'eeg_anomaly', 'agi_mismatch', 'latency_spike', 'icp_collapse'
    severity: float      # 0.0 a 1.0
    theta_value: float   # Valor del parámetro de orden TAE
    context: Dict        # Contexto del evento (features, predicciones, etc.)

class TAEExceptionDetector:
    """
    Detector de excepciones basado en Aprendizaje por Excepción (TAE).
    Identifica anomalías en la dinámica EEG-AGI y activa respuestas adaptativas.
    """
    
    def __init__(self, 
                 window_size: int = 100,
                 prediction_horizon: int = 10,
                 lambda_threshold: float = 2.0,
                 learning_rate: float = 0.01):
        """
        Args:
            window_size: Tamaño de la ventana de historial para modelos predictivos
            prediction_horizon: Horizonte de predicción (número de pasos)
            lambda_threshold: Umbral de sensibilidad para detección de excepciones
            learning_rate: Tasa de actualización del modelo interno
        """
        self.window_size = window_size
        self.prediction_horizon = prediction_horizon
        self.lambda_threshold = lambda_threshold
        self.learning_rate = learning_rate
        
        # Buffer circular para datos históricos
        self.eeg_history = deque(maxlen=window_size)
        self.icp_history = deque(maxlen=window_size)
        self.agi_embedding_history = deque(maxlen=window_size)
        
        # Modelo interno predictivo (simplificado como media móvil + tendencia)
        self.predicted_eeg = None
        self.prediction_error = None
        self.prediction_uncertainty = None
        
        # Historial de excepciones
        self.exception_history = deque(maxlen=1000)
        
        logger.info("TAEExceptionDetector inicializado")
    
    def update(self, 
               eeg_features: np.ndarray, 
               icp_value: float, 
               agi_embedding: Optional[np.ndarray] = None,
               intent_predicted: Optional[int] = None,
               intent_correct: Optional[int] = None) -> Optional[ExceptionEvent]:
        """
        Actualiza el detector con una nueva observación.
        
        Args:
            eeg_features: Vector de características EEG (ej., band power, embeddings)
            icp_value: Índice de Coherencia Predictiva actual
            agi_embedding: Embedding de la respuesta AGI (opcional)
            intent_predicted: Intento predicho por el clasificador
            intent_correct: Intento real (si se conoce)
        
        Returns:
            ExceptionEvent si se detecta una excepción, None en caso contrario
        """
        # 1. Actualizar historiales
        self.eeg_history.append(eeg_features)
        self.icp_history.append(icp_value)
        if agi_embedding is not None:
            self.agi_embedding_history.append(agi_embedding)
        
        # 2. Actualizar modelo predictivo interno
        self._update_predictive_model()
        
        # 3. Calcular error de predicción
        if self.predicted_eeg is not None and len(self.eeg_history) > 1:
            # Error de predicción del EEG
            current_eeg = self.eeg_history[-1]
            self.prediction_error = np.linalg.norm(current_eeg - self.predicted_eeg)
        else:
            self.prediction_error = 0.0
        
        # 4. Calcular parámetro de orden TAE
        theta = self._calculate_theta()
        
        # 5. Detectar excepción si theta > 0
        if theta > 0:
            exception_type = self._classify_exception()
            severity = self._calculate_severity(theta)
            
            event = ExceptionEvent(
                timestamp=self._get_timestamp(),
                exception_type=exception_type,
                severity=severity,
                theta_value=theta,
                context={
                    'icp': icp_value,
                    'prediction_error': self.prediction_error,
                    'uncertainty': self.prediction_uncertainty,
                    'intent_predicted': intent_predicted,
                    'intent_correct': intent_correct,
                    'window_size': len(self.eeg_history)
                }
            )
            
            self.exception_history.append(event)
            logger.info(f"Excepción detectada: {exception_type} (severidad={severity:.3f}, θ={theta:.3f})")
            return event
        
        return None
    
    def _update_predictive_model(self):
        """Actualiza el modelo interno predictivo usando los datos históricos."""
        if len(self.eeg_history) < self.window_size:
            return
        
        # Modelo simplificado: media móvil + tendencia lineal
        eeg_array = np.array(self.eeg_history)
        
        # Predicción usando media móvil con ventana corta (ej., 10 muestras)
        short_window = min(10, len(eeg_array))
        self.predicted_eeg = np.mean(eeg_array[-short_window:], axis=0)
        
        # Calcular incertidumbre como desviación estándar de la predicción
        self.prediction_uncertainty = np.std(eeg_array[-short_window:], axis=0).mean()
    
    def _calculate_theta(self) -> float:
        """Calcula el parámetro de orden TAE Θ = ||e|| - λ·σ."""
        if self.prediction_uncertainty is None:
            return -1.0  # Sin datos suficientes
        
        theta = self.prediction_error - (self.lambda_threshold * self.prediction_uncertainty)
        return theta
    
    def _classify_exception(self) -> str:
        """Clasifica el tipo de excepción basado en el contexto actual."""
        # Verificar caída del ICP
        if len(self.icp_history) >= 5:
            recent_icp = list(self.icp_history)[-5:]
            if np.mean(recent_icp) < 0.4:
                return 'icp_collapse'
        
        # Verificar anomalía en EEG (prediction_error alto)
        if self.prediction_error > 2.0 * self.prediction_uncertainty:
            return 'eeg_anomaly'
        
        # Verificar latencia si está disponible
        # (se puede extender con métricas de latencia)
        
        # Verificar mismatch con AGI (si se tienen embeddings)
        if len(self.agi_embedding_history) >= 2:
            # Aquí se podría calcular similitud coseno entre embeddings consecutivos
            pass
        
        return 'unknown_anomaly'
    
    def _calculate_severity(self, theta: float) -> float:
        """Calcula la severidad de la excepción normalizada [0,1]."""
        # Severidad sigmoidea basada en theta
        severity = 1.0 / (1.0 + np.exp(-theta))
        return min(1.0, max(0.0, severity))
    
    def _get_timestamp(self) -> float:
        """Obtiene timestamp actual en segundos."""
        import time
        return time.time()
    
    def get_exception_rate(self, window_seconds: float = 60.0) -> float:
        """Calcula la tasa de excepciones en la ventana de tiempo especificada."""
        if not self.exception_history:
            return 0.0
        
        current_time = self._get_timestamp()
        recent_exceptions = [
            e for e in self.exception_history 
            if current_time - e.timestamp <= window_seconds
        ]
        return len(recent_exceptions) / window_seconds
    
    def reset(self):
        """Reinicia el estado del detector."""
        self.eeg_history.clear()
        self.icp_history.clear()
        self.agi_embedding_history.clear()
        self.exception_history.clear()
        self.predicted_eeg = None
        self.prediction_error = None
        self.prediction_uncertainty = None
        logger.info("TAEExceptionDetector reiniciado")
