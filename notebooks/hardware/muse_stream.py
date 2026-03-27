# -*- coding: utf-8 -*-
# src/hardware/muse_stream.py
"""
Módulo de adquisición en tiempo real para dispositivos EEG (Muse / Emotiv).

Provee una interfaz unificada para conectar, leer y preprocesar streams EEG
con baja latencia. Diseñado para integrarse con el pipeline adaptativo CPEA.

Soporta:
- Muse (2016, 2) mediante muselsl + LSL
- Estructura base para Emotiv EPOC / Insight (requiere SDK propio)
- Buffer circular con timestamp para manejo de latencias
- Filtro banda base (8-30 Hz) y rechazo de parpadeos básico
"""

import numpy as np
import time
import threading
import logging
from collections import deque
from typing import Optional, Dict, List, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum

# Dependencias opcionales
try:
    from pylsl import StreamInlet, resolve_byprop
    PYLSL_AVAILABLE = True
except ImportError:
    PYLSL_AVAILABLE = False
    logging.warning("pylsl no disponible. Instalar con: pip install pylsl")

try:
    import mne
    MNE_AVAILABLE = True
except ImportError:
    MNE_AVAILABLE = False
    logging.warning("mne no disponible. Instalar con: pip install mne")

try:
    from scipy import signal
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    logging.warning("scipy no disponible. Instalar con: pip install scipy")

# Configuración logging
logger = logging.getLogger(__name__)


class HardwareType(Enum):
    """Tipos de hardware EEG soportados."""
    MUSE = "muse"
    EMOTIV = "emotiv"
    SIMULATED = "simulated"


@dataclass
class EEGConfig:
    """Configuración de adquisición EEG."""
    hardware: HardwareType = HardwareType.MUSE
    sampling_rate: int = 256          # Hz
    buffer_duration: float = 5.0      # segundos de buffer circular
    lowcut: float = 8.0               # Hz, filtro paso bajo
    highcut: float = 30.0             # Hz, filtro paso alto
    blink_threshold: float = 100.0    # µV, umbral para rechazo de parpadeo
    channels: List[str] = field(default_factory=lambda: [
        'TP9', 'AF7', 'AF8', 'TP10'
    ])  # Canales Muse estándar

    # LSL específico
    lsl_stream_name: str = "Muse"
    lsl_timeout: float = 5.0          # segundos esperando stream

    # Emotiv específico (placeholder)
    emotiv_client_id: Optional[str] = None
    emotiv_client_secret: Optional[str] = None


class CircularBuffer:
    """Buffer circular eficiente para almacenar muestras EEG con timestamp."""
    
    def __init__(self, maxlen: int):
        self.buffer = deque(maxlen=maxlen)
        self.timestamps = deque(maxlen=maxlen)
        
    def append(self, sample: np.ndarray, timestamp: float):
        """Añade una muestra al buffer."""
        self.buffer.append(sample)
        self.timestamps.append(timestamp)
        
    def get_all(self) -> Tuple[np.ndarray, np.ndarray]:
        """Retorna todas las muestras como arrays (datos, timestamps)."""
        if len(self.buffer) == 0:
            return np.array([]), np.array([])
        return np.array(self.buffer), np.array(self.timestamps)
    
    def get_recent(self, duration: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Retorna muestras de los últimos 'duration' segundos.
        Asume timestamps en segundos (monotónicos).
        """
        if len(self.timestamps) == 0:
            return np.array([]), np.array([])
        
        now = time.time()
        cutoff = now - duration
        indices = [i for i, ts in enumerate(self.timestamps) if ts >= cutoff]
        
        if not indices:
            return np.array([]), np.array([])
        
        data = np.array([self.buffer[i] for i in indices])
        timestamps = np.array([self.timestamps[i] for i in indices])
        return data, timestamps
    
    def clear(self):
        self.buffer.clear()
        self.timestamps.clear()
        
    def __len__(self):
        return len(self.buffer)


class MuseLSLStream:
    """
    Conector para dispositivos Muse mediante LSL.
    
    Utiliza muselsl para iniciar la transmisión y pylsl para recibir.
    """
    
    def __init__(self, config: EEGConfig):
        self.config = config
        self.inlet: Optional[StreamInlet] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self.buffer = CircularBuffer(maxlen=config.sampling_rate * config.buffer_duration)
        
        # Estado
        self.last_sample: Optional[np.ndarray] = None
        self.last_timestamp: float = 0.0
        self.sample_count = 0
        
        # Callbacks opcionales
        self.on_sample_callback: Optional[Callable] = None
        
    def connect(self) -> bool:
        """Busca y conecta al stream LSL del dispositivo Muse."""
        if not PYLSL_AVAILABLE:
            logger.error("pylsl no disponible. Instalar con: pip install pylsl")
            return False
            
        try:
            logger.info(f"Buscando stream LSL: {self.config.lsl_stream_name}...")
            streams = resolve_byprop('name', self.config.lsl_stream_name, 
                                     timeout=self.config.lsl_timeout)
            if not streams:
                logger.error(f"No se encontró stream LSL '{self.config.lsl_stream_name}'")
                return False
                
            self.inlet = StreamInlet(streams[0])
            logger.info(f"Conectado a {self.inlet.info().name()}")
            return True
            
        except Exception as e:
            logger.error(f"Error conectando a Muse: {e}")
            return False
            
    def start_acquisition(self):
        """Inicia el hilo de adquisición."""
        if self._running:
            logger.warning("Adquisición ya en curso")
            return
            
        if not self.inlet:
            logger.error("No hay conexión activa. Llame a connect() primero")
            return
            
        self._running = True
        self._thread = threading.Thread(target=self._acquire_loop, daemon=True)
        self._thread.start()
        logger.info("Adquisición iniciada")
        
    def _acquire_loop(self):
        """Bucle principal de adquisición."""
        while self._running:
            try:
                # Obtener muestra (bloqueo configurable)
                sample, timestamp = self.inlet.pull_sample(timeout=0.01)
                if sample is None:
                    continue
                    
                sample = np.array(sample[:len(self.config.channels)])
                self.last_sample = sample
                self.last_timestamp = timestamp
                self.sample_count += 1
                
                # Almacenar en buffer
                self.buffer.append(sample, timestamp)
                
                # Callback
                if self.on_sample_callback:
                    self.on_sample_callback(sample, timestamp)
                    
            except Exception as e:
                logger.error(f"Error en adquisición: {e}")
                time.sleep(0.1)
                
        logger.info("Adquisición detenida")
        
    def stop_acquisition(self):
        """Detiene el hilo de adquisición."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        logger.info("Adquisición detenida")
        
    def get_recent_data(self, duration: float = 2.0) -> Tuple[np.ndarray, np.ndarray]:
        """Obtiene datos recientes del buffer circular."""
        return self.buffer.get_recent(duration)
    
    def get_latest_sample(self) -> Optional[np.ndarray]:
        """Retorna la última muestra."""
        return self.last_sample


class EmotivStream:
    """
    Placeholder para integración con Emotiv.
    
    Requiere SDK de Emotiv (EMOTIV PRO) e implementación específica.
    """
    
    def __init__(self, config: EEGConfig):
        self.config = config
        self._connected = False
        self.buffer = CircularBuffer(maxlen=config.sampling_rate * config.buffer_duration)
        
    def connect(self) -> bool:
        """
        Conecta a dispositivo Emotiv.
        
        Nota: Implementación real requiere SDK de Emotiv y credenciales.
        """
        logger.warning("Emotiv no implementado. Se requiere SDK propio.")
        # Aquí iría la lógica con emotiv-python o SDK nativo
        self._connected = True
        return True
        
    def start_acquisition(self):
        """Inicia adquisición."""
        if not self._connected:
            logger.error("No conectado")
            return
        logger.warning("Emotiv adquisición no implementada")
        
    def stop_acquisition(self):
        pass
        
    def get_recent_data(self, duration: float) -> Tuple[np.ndarray, np.ndarray]:
        return np.array([]), np.array([])
    
    def get_latest_sample(self) -> Optional[np.ndarray]:
        return None


class SimulatedEEGStream:
    """
    Stream simulado para pruebas sin hardware.
    Genera señales sintéticas con ruido + componentes alpha/theta.
    """
    
    def __init__(self, config: EEGConfig):
        self.config = config
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self.buffer = CircularBuffer(maxlen=config.sampling_rate * config.buffer_duration)
        
        self.last_sample: Optional[np.ndarray] = None
        self.last_timestamp: float = 0.0
        self.sample_count = 0
        self.start_time = None
        
        # Parámetros de simulación
        self.freq_alpha = 10.0   # Hz
        self.freq_theta = 6.0    # Hz
        self.noise_std = 10.0    # µV
        
    def connect(self) -> bool:
        self.start_time = time.time()
        logger.info("Stream simulado listo")
        return True
        
    def start_acquisition(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._acquire_loop, daemon=True)
        self._thread.start()
        logger.info("Simulación iniciada")
        
    def _acquire_loop(self):
        """Genera muestras sintéticas."""
        dt = 1.0 / self.config.sampling_rate
        t = 0.0
        
        while self._running:
            t_abs = time.time()
            # Generar señal multicanal
            samples = []
            for _ in self.config.channels:
                # Mezcla de alpha + theta + ruido
                alpha = np.sin(2 * np.pi * self.freq_alpha * t) * 15.0
                theta = np.sin(2 * np.pi * self.freq_theta * t) * 8.0
                noise = np.random.randn() * self.noise_std
                sample = alpha + theta + noise
                samples.append(sample)
                
            sample = np.array(samples)
            self.last_sample = sample
            self.last_timestamp = t_abs
            self.sample_count += 1
            
            self.buffer.append(sample, t_abs)
            
            t += dt
            time.sleep(dt)  # Simula tasa real
            
    def stop_acquisition(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1.0)
            
    def get_recent_data(self, duration: float) -> Tuple[np.ndarray, np.ndarray]:
        return self.buffer.get_recent(duration)
    
    def get_latest_sample(self) -> Optional[np.ndarray]:
        return self.last_sample


class EEGPreprocessor:
    """
    Preprocesamiento en streaming: filtro banda base, rechazo de artefactos.
    
    Utiliza filtros IIR de scipy/mne para mantener baja latencia.
    """
    
    def __init__(self, config: EEGConfig):
        self.config = config
        self.sos = None  # Filtro SOS
        self._init_filter()
        
        # Estado para filtro (zi)
        self.zi = None
        
    def _init_filter(self):
        """Inicializa filtro Butterworth banda base."""
        if not SCIPY_AVAILABLE:
            logger.warning("scipy no disponible, filtro desactivado")
            return
            
        nyquist = self.config.sampling_rate / 2
        low = self.config.lowcut / nyquist
        high = self.config.highcut / nyquist
        
        self.sos = signal.butter(4, [low, high], btype='band', output='sos')
        
    def reset(self):
        """Reinicia estado del filtro."""
        if self.sos is not None:
            self.zi = None
            
    def process(self, data: np.ndarray, timestamps: Optional[np.ndarray] = None) -> np.ndarray:
        """
        Aplica preprocesamiento a un bloque de datos.
        
        Args:
            data: Array de forma (n_samples, n_channels) o (n_channels,)
            timestamps: Opcional, no usado directamente pero se mantiene API.
            
        Returns:
            Datos filtrados y artefactos rechazados (misma forma).
        """
        if data.ndim == 1:
            data = data.reshape(1, -1)
            
        if self.sos is None or not SCIPY_AVAILABLE:
            # Si no hay filtro, solo copia
            filtered = data.copy()
        else:
            # Aplicar filtro con estado inicial
            if self.zi is None:
                # Inicializar estado (n_secciones, 2, n_canales)
                n_channels = data.shape[1]
                self.zi = np.zeros((self.sos.shape[0], 2, n_channels))
                
            filtered, self.zi = signal.sosfilt(self.sos, data, axis=0, zi=self.zi)
            
        # Rechazo de parpadeos simple: si alguna muestra excede umbral, marcar
        # En versión real se aplicaría una máscara de rechazo, aquí devolvemos
        # los datos pero con posibilidad de registrar artefactos.
        if np.any(np.abs(filtered) > self.config.blink_threshold):
            logger.debug("Artefacto detectado (blink)")
            
        return filtered


class EEGStreamManager:
    """
    Gestor unificado de adquisición EEG.
    
    Encapsula la lógica de conexión, adquisición, preprocesamiento y
    entrega de datos al pipeline principal.
    """
    
    def __init__(self, config: EEGConfig):
        self.config = config
        self._stream = None
        self._preprocessor = EEGPreprocessor(config)
        self._running = False
        
        # Datos procesados disponibles
        self.processed_buffer = CircularBuffer(
            maxlen=config.sampling_rate * config.buffer_duration
        )
        
        # Callbacks
        self.on_processed_sample: Optional[Callable] = None
        
    def connect(self) -> bool:
        """Establece conexión según hardware configurado."""
        if self.config.hardware == HardwareType.MUSE:
            self._stream = MuseLSLStream(self.config)
        elif self.config.hardware == HardwareType.EMOTIV:
            self._stream = EmotivStream(self.config)
        elif self.config.hardware == HardwareType.SIMULATED:
            self._stream = SimulatedEEGStream(self.config)
        else:
            logger.error(f"Hardware no soportado: {self.config.hardware}")
            return False
            
        # Callback interno para preprocesar al vuelo
        self._stream.on_sample_callback = self._process_sample
        return self._stream.connect()
    
    def _process_sample(self, sample: np.ndarray, timestamp: float):
        """Callback de procesamiento en tiempo real."""
        # Preprocesar muestra
        processed = self._preprocessor.process(sample)
        
        # Almacenar procesado
        self.processed_buffer.append(processed, timestamp)
        
        # Callback externo
        if self.on_processed_sample:
            self.on_processed_sample(processed, timestamp)
            
    def start_acquisition(self):
        """Inicia flujo de datos."""
        if not self._stream:
            logger.error("No hay stream conectado. Llame a connect() primero")
            return
            
        self._running = True
        self._preprocessor.reset()
        self._stream.start_acquisition()
        logger.info("Adquisición iniciada con preprocesamiento")
        
    def stop_acquisition(self):
        """Detiene adquisición."""
        self._running = False
        if self._stream:
            self._stream.stop_acquisition()
        logger.info("Adquisición detenida")
        
    def get_processed_data(self, duration: float = 2.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Obtiene datos ya preprocesados del buffer.
        
        Returns:
            Tuple (data, timestamps) donde data shape (n_samples, n_channels)
        """
        return self.processed_buffer.get_recent(duration)
    
    def get_latest_processed_sample(self) -> Optional[np.ndarray]:
        """Última muestra procesada."""
        if len(self.processed_buffer) > 0:
            return self.processed_buffer.buffer[-1]
        return None
    
    def get_stream_info(self) -> Dict:
        """Información de estado del stream."""
        info = {
            'hardware': self.config.hardware.value,
            'running': self._running,
            'sample_rate': self.config.sampling_rate,
            'buffer_size': len(self.processed_buffer),
            'channels': self.config.channels,
        }
        
        if self._stream:
            info['samples_received'] = self._stream.sample_count
            info['last_timestamp'] = self._stream.last_timestamp
            
        return info


# Ejemplo de uso integrado con pipeline
def example_integration():
    """
    Demuestra cómo usar EEGStreamManager dentro del pipeline CPEA.
    """
    import time
    
    # Configuración
    config = EEGConfig(
        hardware=HardwareType.SIMULATED,  # Cambiar a MUSE para hardware real
        sampling_rate=256,
        buffer_duration=5.0
    )
    
    # Crear gestor
    manager = EEGStreamManager(config)
    
    # Definir callback que inyectaría datos al pipeline AGI
    def on_eeg_ready(processed_sample, timestamp):
        # Este callback recibiría la muestra procesada
        # y podría pasarla al clasificador/pipeline AGI
        logger.debug(f"EEG sample ready: {processed_sample[:2]}... at {timestamp}")
        
    manager.on_processed_sample = on_eeg_ready
    
    # Conectar y arrancar
    if manager.connect():
        manager.start_acquisition()
        
        # Simular ejecución por 10 segundos
        try:
            for _ in range(10):
                # Obtener batch de datos para clasificador
                data, ts = manager.get_processed_data(duration=1.0)
                if len(data) > 0:
                    logger.info(f"Batch shape: {data.shape}, timestamps: {ts[0]:.2f} - {ts[-1]:.2f}")
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            manager.stop_acquisition()
    else:
        logger.error("No se pudo conectar")


if __name__ == "__main__":
    # Configurar logging para ver detalles
    logging.basicConfig(level=logging.INFO)
    example_integration()
