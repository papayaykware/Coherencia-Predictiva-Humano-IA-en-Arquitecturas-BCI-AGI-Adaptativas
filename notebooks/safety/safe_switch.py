"""
src/safety/safe_switch.py

Módulo Safe-Switch (versión simplificada) para CPEA.
Detecta caídas en el Índice de Coherencia Predictiva (ICP) y ejecuta
un reseteo parcial controlado del sistema para preservar la soberanía
neurodinámica y la estabilidad del bucle humano-AGI.

Basado en:
- Formalización del Safe-Switch como problema de control en sistemas dinámicos.md
- Safe-Switch + Sovereignty Engine.md
- Preprint CPEA con firewall cognitivo Safe-Switch
"""

import numpy as np
import logging
from typing import Optional, Dict, Any, List
from collections import deque
import time

# Configurar logging específico para el módulo de seguridad
logger = logging.getLogger(__name__)

class SafeSwitch:
    """
    Mecanismo de seguridad para detectar degradación de coherencia
    y ejecutar acciones de recuperación parcial del sistema.
    
    Parámetros
    ----------
    icp_threshold : float, default=0.35
        Umbral mínimo de ICP antes de activar alerta. 
        Por debajo de 0.35 se considera coherencia insuficiente.
    window_size : int, default=5
        Ventana de observación para suavizar detección de caídas.
    cooldown_seconds : int, default=30
        Tiempo mínimo entre reseteos para evitar oscilaciones.
    reset_level : str, default='partial'
        Nivel de reset: 'partial' (clasificador, contexto), 
        'full' (recalibración completa), 'none' (solo log).
    """
    
    def __init__(self, 
                 icp_threshold: float = 0.35,
                 window_size: int = 5,
                 cooldown_seconds: int = 30,
                 reset_level: str = 'partial'):
        
        self.icp_threshold = icp_threshold
        self.window_size = window_size
        self.cooldown_seconds = cooldown_seconds
        self.reset_level = reset_level
        
        # Buffer circular para almacenar últimos valores de ICP
        self.icp_buffer = deque(maxlen=window_size)
        
        # Estado interno
        self.last_reset_time = 0.0
        self.alert_active = False
        self.reset_count = 0
        self.consecutive_lows = 0
        
        # Métricas de diagnóstico
        self.diagnostics = {
            'total_resets': 0,
            'last_reset_reason': None,
            'last_icp_value': 0.0,
            'mean_icp_window': 0.0
        }
        
        logger.info(f"SafeSwitch inicializado | threshold={icp_threshold} "
                    f"window={window_size} cooldown={cooldown_seconds}s")
    
    def update(self, icp_value: float) -> Dict[str, Any]:
        """
        Actualiza el monitor con un nuevo valor de ICP y evalúa
        si es necesario activar el Safe-Switch.
        
        Parámetros
        ----------
        icp_value : float
            Valor actual del Índice de Coherencia Predictiva [0-1]
            
        Retorna
        -------
        dict
            Estado actual y acción recomendada
        """
        self.diagnostics['last_icp_value'] = icp_value
        self.icp_buffer.append(icp_value)
        
        # Calcular media móvil del ICP
        mean_icp = np.mean(self.icp_buffer) if self.icp_buffer else icp_value
        self.diagnostics['mean_icp_window'] = mean_icp
        
        # Detectar condición de caída sostenida
        is_low = mean_icp < self.icp_threshold
        
        if is_low:
            self.consecutive_lows += 1
        else:
            self.consecutive_lows = 0
            self.alert_active = False
        
        # Determinar si se activa la alerta (caída persistente)
        trigger_alert = (self.consecutive_lows >= self.window_size and 
                         not self.alert_active)
        
        # Evaluar si se ejecuta reset
        action = self._evaluate_action(trigger_alert)
        
        return {
            'alert_triggered': trigger_alert,
            'action': action,
            'mean_icp': mean_icp,
            'consecutive_lows': self.consecutive_lows,
            'reset_count': self.reset_count,
            'cooldown_active': (time.time() - self.last_reset_time) < self.cooldown_seconds
        }
    
    def _evaluate_action(self, trigger_alert: bool) -> Optional[str]:
        """Evalúa si se debe ejecutar un reset según estado y cooldown."""
        
        now = time.time()
        in_cooldown = (now - self.last_reset_time) < self.cooldown_seconds
        
        if not trigger_alert:
            return None
        
        if in_cooldown:
            logger.warning(f"Safe-Switch: alerta pero en cooldown "
                           f"(último reset hace {now - self.last_reset_time:.1f}s)")
            return 'cooldown'
        
        # Ejecutar reset según nivel configurado
        self.last_reset_time = now
        self.reset_count += 1
        self.diagnostics['total_resets'] = self.reset_count
        
        if self.reset_level == 'partial':
            action = self._partial_reset()
        elif self.reset_level == 'full':
            action = self._full_reset()
        else:
            action = 'none'
            
        logger.warning(f"Safe-Switch ACTIVADO | reset #{self.reset_count} | "
                       f"nivel={self.reset_level} | acción={action}")
        
        return action
    
    def _partial_reset(self) -> str:
        """
        Reseteo parcial del sistema:
        - Limpia caché de intents recientes
        - Reinicia acumuladores de adaptación (sin perder modelo base)
        - Notifica a módulos downstream que deben reestabilizarse
        """
        # En una implementación real, aquí se llamarían callbacks o se
        # enviarían eventos a otros módulos (pipeline, AGI, clasificador)
        self.diagnostics['last_reset_reason'] = 'partial_reset_icp_drop'
        
        # Simulación: marcar estado para que otros componentes actúen
        self.alert_active = True
        
        # Opcional: limpiar buffer de adaptación si existe un contexto externo
        # Ejemplo: if hasattr(self, 'adaptation_buffer'): self.adaptation_buffer.clear()
        
        return 'partial_reset_executed'
    
    def _full_reset(self) -> str:
        """
        Reseteo completo (reservado para caídas severas o persistentes):
        - Recalibración del clasificador EEG
        - Reinicio de ventanas de contexto AGI
        - Limpieza total de buffers adaptativos
        """
        self.diagnostics['last_reset_reason'] = 'full_reset_icp_critical'
        self.alert_active = True
        
        # En una implementación real, esto activaría un modo de recalibración
        # y posiblemente notificaría al usuario
        
        return 'full_reset_executed'
    
    def get_status(self) -> Dict[str, Any]:
        """Retorna estado completo del SafeSwitch para monitoreo."""
        now = time.time()
        return {
            'reset_level': self.reset_level,
            'icp_threshold': self.icp_threshold,
            'window_size': self.window_size,
            'cooldown_seconds': self.cooldown_seconds,
            'time_since_last_reset': now - self.last_reset_time if self.last_reset_time else None,
            **self.diagnostics,
            'buffer_content': list(self.icp_buffer),
            'alert_active': self.alert_active,
            'consecutive_lows': self.consecutive_lows
        }
    
    def reset(self, level: Optional[str] = None) -> str:
        """
        Permite un reset manual forzado desde otros módulos.
        
        Parámetros
        ----------
        level : str, opcional
            Nivel de reset a ejecutar ('partial', 'full'). 
            Si no se especifica, usa el configurado en __init__.
        """
        reset_level = level or self.reset_level
        now = time.time()
        self.last_reset_time = now
        self.reset_count += 1
        self.diagnostics['total_resets'] = self.reset_count
        self.diagnostics['last_reset_reason'] = 'manual_override'
        
        if reset_level == 'partial':
            action = self._partial_reset()
        elif reset_level == 'full':
            action = self._full_reset()
        else:
            action = 'none'
        
        logger.info(f"Safe-Switch: reset manual ({reset_level}) ejecutado")
        return f"manual_{action}"


# Ejemplo de uso integrado en pipeline de adaptación
if __name__ == "__main__":
    # Configurar logging básico para prueba
    logging.basicConfig(level=logging.INFO)
    
    # Instanciar SafeSwitch con parámetros realistas
    safety = SafeSwitch(icp_threshold=0.35, window_size=3, cooldown_seconds=10)
    
    # Simular una secuencia de valores de ICP (caída progresiva)
    test_icp_sequence = [0.52, 0.48, 0.41, 0.38, 0.33, 0.31, 0.30, 0.45, 0.50]
    
    print("=== Simulación de monitor Safe-Switch ===")
    for i, icp in enumerate(test_icp_sequence):
        result = safety.update(icp)
        print(f"ICP={icp:.3f} | media={result['mean_icp']:.3f} | "
              f"alert={result['alert_triggered']} | acción={result['action']}")
        time.sleep(1)  # Simular paso de tiempo entre muestras
    
    print("\n=== Estado final ===")
    print(safety.get_status())
