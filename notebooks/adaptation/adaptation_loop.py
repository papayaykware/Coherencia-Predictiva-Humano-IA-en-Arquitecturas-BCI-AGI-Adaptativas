"""
src/adaptation/adaptation_loop.py

Bucle de adaptación principal para CPEA.
Orquesta el aprendizaje continuo del clasificador EEG basado en
el rendimiento del Índice de Coherencia Predictiva (ICP).

Flujo:
1. Monitoreo continuo del ICP en ventanas temporales
2. Detección de degradación o estancamiento del ICP
3. Activación selectiva del mecanismo de adaptación
4. Actualización del clasificador con replay/EWC
5. Validación post-adaptación
"""

import numpy as np
import torch
import torch.nn as nn
from collections import deque
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any, List
import logging
import time
from enum import Enum

from src.adaptation.continual_learning import ContinualLearner
from src.pipeline.eeg_classifier import EEGClassifier  # Asumiendo que existe
from src.metrics.icp_calculator import ICPCalculator   # Asumiendo que existe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AdaptationTrigger(Enum):
    """Tipos de triggers para activar la adaptación."""
    ICP_DROPPING = "icp_dropping"      # ICP está disminuyendo
    ICP_STAGNATION = "icp_stagnation"   # ICP estancado por mucho tiempo
    SCHEDULED = "scheduled"             # Actualización programada
    MANUAL = "manual"                   # Trigger manual externo


@dataclass
class AdaptationConfig:
    """Configuración del bucle de adaptación."""
    # Umbrales para triggers
    icp_drop_threshold: float = 0.05      # Caída mínima para activar (absoluta)
    icp_stagnation_window: int = 50       # Ventanas de estancamiento permitidas
    icp_stagnation_threshold: float = 0.02 # Variación máxima considerada estancamiento
    
    # Configuración de adaptación
    min_samples_for_adaptation: int = 100   # Mínimo de nuevas muestras para adaptar
    adaptation_cooldown: int = 10           # Ventanas de espera entre adaptaciones
    max_buffer_size: int = 5000             # Tamaño máximo del buffer de replay
    
    # Hiperparámetros de aprendizaje continuo
    lambda_ewc: float = 0.1                 # Fuerza de regularización EWC
    replay_batch_size: int = 32             # Tamaño de lote para replay
    learning_rate: float = 1e-3             # Tasa de aprendizaje
    ewc_update_interval: int = 100          # Frecuencia de actualización de Fisher
    
    # Métricas y logging
    log_interval: int = 10                  # Ventanas entre logs detallados
    save_checkpoint_interval: int = 100     # Ventanas entre checkpoints


class AdaptationLoop:
    """
    Bucle principal de adaptación para CPEA.
    Monitorea ICP y decide cuándo y cómo actualizar el clasificador EEG.
    """
    
    def __init__(
        self,
        classifier: nn.Module,
        input_dim: int,
        num_classes: int,
        config: AdaptationConfig,
        device: torch.device
    ):
        """
        Args:
            classifier: Modelo PyTorch del clasificador EEG.
            input_dim: Dimensión de características EEG.
            num_classes: Número de clases de intent.
            config: Configuración del bucle de adaptación.
            device: Dispositivo (cpu/cuda).
        """
        self.config = config
        self.device = device
        
        # Inicializar componentes
        self.classifier = classifier
        self.continual_learner = ContinualLearner(
            model=classifier,
            device=device,
            replay_buffer_size=config.max_buffer_size,
            lambda_ewc=config.lambda_ewc,
            replay_batch_size=config.replay_batch_size,
            learning_rate=config.learning_rate,
            ewc_update_interval=config.ewc_update_interval
        )
        
        # Buffer para datos recientes (características, etiquetas, ICP)
        self.recent_data = deque(maxlen=config.max_buffer_size)
        self.icp_history = deque(maxlen=1000)  # Historial de ICP por ventana
        
        # Estado interno
        self.window_counter = 0
        self.last_adaptation_window = -config.adaptation_cooldown
        self.adaptation_count = 0
        
        # Métricas de rendimiento
        self.performance_history = []
        
        logger.info("Bucle de adaptación inicializado correctamente")
    
    def process_window(
        self,
        features: np.ndarray,
        labels: np.ndarray,
        icp_value: float
    ) -> Dict[str, Any]:
        """
        Procesa una ventana temporal de datos.
        
        Args:
            features: Características EEG (N_samples x input_dim)
            labels: Etiquetas de intent (N_samples)
            icp_value: ICP promedio de la ventana
            
        Returns:
            Diccionario con resultados del procesamiento
        """
        self.window_counter += 1
        self.icp_history.append(icp_value)
        
        # Almacenar datos en buffer para posible adaptación futura
        for feat, lab in zip(features, labels):
            self.recent_data.append((feat, lab))
            self.continual_learner.add_experience(feat, lab)
        
        result = {
            'window': self.window_counter,
            'icp': icp_value,
            'adaptation_triggered': False,
            'reason': None,
            'pre_icp': None,
            'post_icp': None
        }
        
        # Evaluar si es necesario adaptar
        if self._should_adapt(icp_value):
            logger.info(f"Ventana {self.window_counter}: Activando adaptación...")
            result['adaptation_triggered'] = True
            result['pre_icp'] = icp_value
            
            # Ejecutar adaptación
            adaptation_result = self._execute_adaptation()
            result.update(adaptation_result)
            
            # Registrar métricas post-adaptación
            self.last_adaptation_window = self.window_counter
            self.adaptation_count += 1
            
            # Calcular mejora de ICP (si está disponible)
            if 'icp_after' in adaptation_result:
                icp_improvement = adaptation_result['icp_after'] - icp_value
                result['icp_improvement'] = icp_improvement
                logger.info(f"Mejora ICP: {icp_improvement:+.4f}")
        
        # Logging periódico
        if self.window_counter % self.config.log_interval == 0:
            self._log_status(icp_value)
        
        # Checkpoint periódico
        if self.window_counter % self.config.save_checkpoint_interval == 0:
            self._save_checkpoint()
        
        return result
    
    def _should_adapt(self, current_icp: float) -> bool:
        """
        Decide si se debe activar la adaptación basado en múltiples criterios.
        
        Política:
        1. ICP está cayendo significativamente
        2. ICP está estancado por mucho tiempo
        3. Suficientes nuevas muestras acumuladas
        4. Respetar cooldown entre adaptaciones
        """
        # Verificar cooldown
        if self.window_counter - self.last_adaptation_window < self.config.adaptation_cooldown:
            return False
        
        # Verificar suficientes datos nuevos
        if len(self.recent_data) < self.config.min_samples_for_adaptation:
            return False
        
        # Criterio 1: Caída significativa de ICP
        if len(self.icp_history) > 5:
            recent_icp = list(self.icp_history)[-5:]
            icp_trend = recent_icp[-1] - recent_icp[0]
            if icp_trend < -self.config.icp_drop_threshold:
                logger.debug(f"ICP dropping detected: {icp_trend:.4f}")
                return True
        
        # Criterio 2: Estancamiento prolongado
        if len(self.icp_history) >= self.config.icp_stagnation_window:
            recent_window = list(self.icp_history)[-self.config.icp_stagnation_window:]
            icp_range = max(recent_window) - min(recent_window)
            if icp_range < self.config.icp_stagnation_threshold:
                logger.debug(f"ICP stagnation detected: range={icp_range:.4f}")
                return True
        
        return False
    
    def _execute_adaptation(self) -> Dict[str, Any]:
        """
        Ejecuta el proceso de adaptación:
        1. Recopilar datos recientes
        2. Actualizar clasificador con replay/EWC
        3. Validar mejora
        """
        logger.info("=" * 50)
        logger.info("INICIANDO ADAPTACIÓN DEL CLASIFICADOR")
        logger.info("=" * 50)
        
        # Preparar datos para actualización
        recent_samples = list(self.recent_data)
        if len(recent_samples) == 0:
            return {'adaptation_success': False, 'error': 'No data available'}
        
        X_recent = np.array([s[0] for s in recent_samples])
        y_recent = np.array([s[1] for s in recent_samples])
        
        # Medir ICP antes de adaptación (si es posible)
        icp_before = self._estimate_current_icp()
        
        # Ejecutar actualización continua
        try:
            start_time = time.time()
            metrics = self.continual_learner.update(
                X_recent,
                y_recent,
                epochs=3,  # Número de épocas de fine-tuning
                batch_size=32,
                use_replay=True,
                use_ewc=True
            )
            adaptation_time = time.time() - start_time
            
            logger.info(f"Adaptación completada en {adaptation_time:.2f} segundos")
            logger.info(f"Métricas de entrenamiento: {metrics}")
            
            # Limpiar datos recientes después de adaptación
            self.recent_data.clear()
            
            # Medir ICP después de adaptación
            icp_after = self._estimate_current_icp()
            
            # Registrar rendimiento
            self.performance_history.append({
                'window': self.window_counter,
                'icp_before': icp_before,
                'icp_after': icp_after,
                'adaptation_time': adaptation_time,
                'samples_used': len(X_recent)
            })
            
            return {
                'adaptation_success': True,
                'icp_before': icp_before,
                'icp_after': icp_after,
                'adaptation_time': adaptation_time,
                'samples_used': len(X_recent),
                'training_metrics': metrics
            }
            
        except Exception as e:
            logger.error(f"Error durante adaptación: {e}")
            return {'adaptation_success': False, 'error': str(e)}
    
    def _estimate_current_icp(self) -> float:
        """
        Estima el ICP actual basado en el historial reciente.
        En producción, esto se calcularía con datos reales del pipeline.
        """
        if len(self.icp_history) > 0:
            return np.mean(list(self.icp_history)[-10:])  # Promedio últimas 10 ventanas
        return 0.5  # Valor por defecto
    
    def _log_status(self, current_icp: float):
        """
        Registra estado actual del sistema.
        """
        avg_icp = np.mean(list(self.icp_history)[-50:]) if len(self.icp_history) > 0 else 0
        logger.info(f"--- Estado Ventana {self.window_counter} ---")
        logger.info(f"ICP actual: {current_icp:.4f} | ICP promedio (50 ventanas): {avg_icp:.4f}")
        logger.info(f"Buffer size: {len(self.recent_data)} | Adaptaciones realizadas: {self.adaptation_count}")
        logger.info(f"Última adaptación: hace {self.window_counter - self.last_adaptation_window} ventanas")
    
    def _save_checkpoint(self):
        """
        Guarda checkpoint del estado actual.
        """
        checkpoint_path = f"checkpoints/adaptation_checkpoint_{self.window_counter}.pt"
        torch.save({
            'model_state_dict': self.classifier.state_dict(),
            'window_counter': self.window_counter,
            'adaptation_count': self.adaptation_count,
            'performance_history': self.performance_history
        }, checkpoint_path)
        logger.info(f"Checkpoint guardado en {checkpoint_path}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Retorna estadísticas resumidas del bucle de adaptación.
        """
        return {
            'total_windows': self.window_counter,
            'total_adaptations': self.adaptation_count,
            'adaptation_rate': self.adaptation_count / max(1, self.window_counter),
            'current_buffer_size': len(self.recent_data),
            'avg_icp': np.mean(list(self.icp_history)) if self.icp_history else 0,
            'icp_trend': self._calculate_icp_trend(),
            'performance': self.performance_history[-10:] if self.performance_history else []
        }
    
    def _calculate_icp_trend(self) -> float:
        """
        Calcula tendencia de ICP usando regresión lineal simple.
        """
        if len(self.icp_history) < 10:
            return 0.0
        
        x = np.arange(len(self.icp_history))
        y = np.array(list(self.icp_history))
        slope = np.polyfit(x, y, 1)[0]
        return slope


class ICPOptimizer:
    """
    Optimizador avanzado que ajusta dinámicamente los parámetros de adaptación
    basado en el rendimiento histórico del ICP.
    """
    
    def __init__(self, adaptation_loop: AdaptationLoop):
        self.loop = adaptation_loop
        self.optimization_history = []
        
    def optimize_parameters(self) -> Dict[str, Any]:
        """
        Analiza el historial de adaptaciones y ajusta parámetros.
        """
        if len(self.loop.performance_history) < 5:
            return {'status': 'insufficient_data'}
        
        # Analizar mejoras de ICP post-adaptación
        improvements = [p['icp_after'] - p['icp_before'] 
                       for p in self.loop.performance_history 
                       if 'icp_before' in p and 'icp_after' in p]
        
        avg_improvement = np.mean(improvements) if improvements else 0
        
        # Ajustar parámetros basado en rendimiento
        adjustments = {}
        
        if avg_improvement < 0.01:  # Mejora insuficiente
            logger.warning("Mejora de ICP insuficiente, ajustando parámetros...")
            
            # Aumentar fuerza de EWC para mejor preservación
            self.loop.config.lambda_ewc *= 1.2
            adjustments['lambda_ewc'] = self.loop.config.lambda_ewc
            
            # Reducir cooldown para adaptaciones más frecuentes
            self.loop.config.adaptation_cooldown = max(3, self.loop.config.adaptation_cooldown - 1)
            adjustments['adaptation_cooldown'] = self.loop.config.adaptation_cooldown
            
            # Aumentar tamaño de buffer
            self.loop.config.max_buffer_size = int(self.loop.config.max_buffer_size * 1.2)
            adjustments['max_buffer_size'] = self.loop.config.max_buffer_size
            
            # Actualizar configuración en continual_learner
            self.loop.continual_learner.lambda_ewc = self.loop.config.lambda_ewc
            
        elif avg_improvement > 0.05:  # Excelente mejora
            logger.info("Excelente mejora de ICP, manteniendo parámetros")
            adjustments['status'] = 'good_performance'
        
        self.optimization_history.append({
            'timestamp': time.time(),
            'avg_improvement': avg_improvement,
            'adjustments': adjustments
        })
        
        return {
            'avg_improvement': avg_improvement,
            'adjustments': adjustments
        }


# ============================================================================
# INTEGRACIÓN CON PIPELINE PRINCIPAL
# ============================================================================

class PipelineIntegrator:
    """
    Integra el bucle de adaptación en el pipeline principal de CPEA.
    Esta clase orquesta la comunicación entre:
    - Adquisición EEG
    - Clasificador
    - AGI
    - Módulo de adaptación
    """
    
    def __init__(
        self,
        classifier: nn.Module,
        input_dim: int,
        num_classes: int,
        config_path: Optional[str] = None
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Configuración
        self.config = AdaptationConfig()
        if config_path:
            self._load_config(config_path)
        
        # Inicializar bucle de adaptación
        self.adaptation_loop = AdaptationLoop(
            classifier=classifier,
            input_dim=input_dim,
            num_classes=num_classes,
            config=self.config,
            device=self.device
        )
        
        # Optimizador avanzado
        self.icp_optimizer = ICPOptimizer(self.adaptation_loop)
        
        # Métricas en tiempo real
        self.window_metrics = []
        
        logger.info("Pipeline integrado con bucle de adaptación")
    
    def _load_config(self, config_path: str):
        """Carga configuración desde archivo YAML."""
        import yaml
        with open(config_path, 'r') as f:
            config_dict = yaml.safe_load(f)
            for key, value in config_dict.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
    
    def process_eeg_window(
        self,
        eeg_features: np.ndarray,
        intent_labels: np.ndarray,
        agi_embedding: Optional[np.ndarray] = None
    ) -> Dict[str, Any]:
        """
        Procesa una ventana de datos EEG completa.
        
        Args:
            eeg_features: Características extraídas del EEG
            intent_labels: Etiquetas de intent (ground truth o inferidas)
            agi_embedding: Embedding de respuesta AGI (para calcular ICP)
            
        Returns:
            Diccionario con resultados completos del pipeline
        """
        # Calcular ICP si tenemos embedding AGI
        icp_value = self._calculate_icp(eeg_features, agi_embedding) if agi_embedding is not None else 0.5
        
        # Procesar ventana en bucle de adaptación
        adaptation_result = self.adaptation_loop.process_window(
            features=eeg_features,
            labels=intent_labels,
            icp_value=icp_value
        )
        
        # Optimización periódica
        if self.adaptation_loop.window_counter % 50 == 0:
            optimization_result = self.icp_optimizer.optimize_parameters()
            adaptation_result['optimization'] = optimization_result
        
        # Almacenar métricas
        self.window_metrics.append({
            'window': self.adaptation_loop.window_counter,
            'icp': icp_value,
            'adaptation': adaptation_result['adaptation_triggered']
        })
        
        return adaptation_result
    
    def _calculate_icp(self, eeg_features: np.ndarray, agi_embedding: np.ndarray) -> float:
        """
        Calcula ICP entre características EEG y embeddings AGI.
        Implementación simplificada - en producción usaría el módulo de métricas.
        """
        # Normalizar
        eeg_norm = (eeg_features - eeg_features.mean()) / (eeg_features.std() + 1e-8)
        agi_norm = (agi_embedding - agi_embedding.mean()) / (agi_embedding.std() + 1e-8)
        
        # Correlación como proxy de coherencia
        correlation = np.corrcoef(eeg_norm.flatten(), agi_norm.flatten())[0, 1]
        
        # Escalar a [0, 1]
        icp = (correlation + 1) / 2
        
        return np.clip(icp, 0, 1)
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Retorna estado completo del sistema.
        """
        return {
            'adaptation_stats': self.adaptation_loop.get_statistics(),
            'total_windows_processed': len(self.window_metrics),
            'avg_icp_recent': np.mean([m['icp'] for m in self.window_metrics[-100:]]) if self.window_metrics else 0,
            'optimization_history': self.icp_optimizer.optimization_history[-5:]
        }


# ============================================================================
# EJEMPLO DE USO COMPLETO
# ============================================================================

if __name__ == "__main__":
    # Simulación de pipeline completo
    
    # 1. Definir clasificador simple
    class SimpleEEGClassifier(nn.Module):
        def __init__(self, input_dim=64, num_classes=3):
            super().__init__()
            self.net = nn.Sequential(
                nn.Linear(input_dim, 128),
                nn.ReLU(),
                nn.Dropout(0.3),
                nn.Linear(128, num_classes)
            )
        
        def forward(self, x):
            return self.net(x)
    
    # 2. Inicializar pipeline integrado
    classifier = SimpleEEGClassifier(input_dim=64, num_classes=3)
    pipeline = PipelineIntegrator(
        classifier=classifier,
        input_dim=64,
        num_classes=3
    )
    
    # 3. Simular procesamiento de 200 ventanas
    print("Iniciando simulación del pipeline adaptativo...")
    print("=" * 60)
    
    for window in range(200):
        # Simular datos EEG
        eeg_features = np.random.randn(50, 64).astype(np.float32)  # 50 muestras
        intent_labels = np.random.randint(0, 3, size=50)
        
        # Simular embedding AGI
        agi_embedding = np.random.randn(50, 128).astype(np.float32)
        
        # Procesar ventana
        result = pipeline.process_eeg_window(eeg_features, intent_labels, agi_embedding)
        
        # Mostrar adaptaciones
        if result['adaptation_triggered']:
            print(f"\n*** Ventana {window+1}: ADAPTACIÓN ACTIVADA ***")
            print(f"ICP antes: {result.get('icp_before', 'N/A'):.4f}")
            print(f"ICP después: {result.get('icp_after', 'N/A'):.4f}")
            if 'icp_improvement' in result:
                print(f"Mejora: {result['icp_improvement']:+.4f}")
            print("-" * 40)
    
    # 4. Mostrar estadísticas finales
    print("\n" + "=" * 60)
    print("ESTADÍSTICAS FINALES DEL SISTEMA")
    print("=" * 60)
    status = pipeline.get_system_status()
    print(f"Total ventanas procesadas: {status['total_windows_processed']}")
    print(f"Total adaptaciones: {status['adaptation_stats']['total_adaptations']}")
    print(f"Tasa de adaptación: {status['adaptation_stats']['adaptation_rate']:.2%}")
    print(f"ICP promedio reciente: {status['avg_icp_recent']:.4f}")
    print(f"Tendencia ICP: {status['adaptation_stats']['icp_trend']:+.4f} por ventana")
