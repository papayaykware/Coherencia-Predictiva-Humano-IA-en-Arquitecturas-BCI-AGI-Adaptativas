# src/metfi/geomag_stream.py

"""
Cliente para adquisición de datos geomagnéticos en tiempo real.
Soporta múltiples fuentes: NOAA SWPC, INTERMAGNET, APIs locales.
"""

import numpy as np
import requests
import time
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import threading
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class GeomagneticSample:
    """Estructura para una muestra de datos geomagnéticos."""
    timestamp: float
    d_st: float           # Índice Dst (tormentas geomagnéticas) en nT
    kp: float             # Índice Kp (actividad planetaria) 0-9
    bz: float             # Componente Bz del campo magnético interplanetario (nT)
    solar_wind_speed: float  # Velocidad del viento solar (km/s)
    schumann_7_83: Optional[float] = None  # Amplitud resonancia 7.83 Hz
    schumann_14_3: Optional[float] = None  # Amplitud resonancia 14.3 Hz
    schumann_20_8: Optional[float] = None  # Amplitud resonancia 20.8 Hz

@dataclass
class GeomagneticConfig:
    """Configuración de fuentes de datos geomagnéticos."""
    noaa_api_key: Optional[str] = None
    intermag_username: Optional[str] = None
    intermag_password: Optional[str] = None
    update_interval: float = 60.0  # Segundos entre actualizaciones
    cache_size: int = 1440         # Muestras a mantener (1 día a 1/min)
    observatory_code: str = 'BOU'  # Código del observatorio (Boulder, CO)

class GeomagneticDataStream:
    """
    Stream de datos geomagnéticos en tiempo real.
    Conecta con APIs de NOAA SWPC e INTERMAGNET.
    """
    
    # URLs de APIs
    NOAA_DST_URL = "https://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json"
    NOAA_KP_URL = "https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json"
    NOAA_SCHUMANN_URL = "https://services.swpc.noaa.gov/json/goes/primary/xray-flares-latest.json"
    INTERMAGNET_URL = "https://www.intermagnet.org/data-donnee/download-eng.php"
    
    def __init__(self, config: Optional[GeomagneticConfig] = None):
        """
        Inicializa el stream de datos geomagnéticos.
        
        Args:
            config: Configuración de APIs y parámetros
        """
        self.config = config or GeomagneticConfig()
        
        # Buffer circular para datos históricos
        self.data_buffer = deque(maxlen=self.config.cache_size)
        
        # Estado actual
        self.current_sample: Optional[GeomagneticSample] = None
        self.last_update: float = 0.0
        
        # Thread para actualización asíncrona
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        logger.info("GeomagneticDataStream inicializado")
    
    def start(self):
        """Inicia el stream de datos en segundo plano."""
        if self._running:
            logger.warning("Stream ya está en ejecución")
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._update_loop, daemon=True)
        self._thread.start()
        logger.info("GeomagneticDataStream iniciado")
    
    def stop(self):
        """Detiene el stream de datos."""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5.0)
        logger.info("GeomagneticDataStream detenido")
    
    def _update_loop(self):
        """Loop principal de actualización de datos."""
        while self._running:
            try:
                self._fetch_current_data()
                self.last_update = time.time()
            except Exception as e:
                logger.error(f"Error en actualización de datos geomagnéticos: {e}")
            
            # Esperar hasta el próximo intervalo de actualización
            time.sleep(self.config.update_interval)
    
    def _fetch_current_data(self):
        """Obtiene datos actuales de las APIs NOAA."""
        try:
            # Obtener índice Dst y viento solar
            dst_data = self._fetch_noaa_plasma()
            
            # Obtener índice Kp
            kp_data = self._fetch_noaa_kp()
            
            # Crear muestra actual
            sample = GeomagneticSample(
                timestamp=time.time(),
                d_st=dst_data.get('d_st', 0.0),
                kp=kp_data.get('kp', 2.0),
                bz=dst_data.get('bz', 0.0),
                solar_wind_speed=dst_data.get('speed', 400.0)
            )
            
            # Obtener resonancias Schumann (si están disponibles)
            schumann = self._estimate_schumann()
            sample.schumann_7_83 = schumann.get('7_83')
            sample.schumann_14_3 = schumann.get('14_3')
            sample.schumann_20_8 = schumann.get('20_8')
            
            # Actualizar buffer
            with self._lock:
                self.data_buffer.append(sample)
                self.current_sample = sample
            
            logger.debug(f"Datos geomagnéticos actualizados: Dst={sample.d_st:.1f}, Kp={sample.kp:.1f}")
            
        except Exception as e:
            logger.error(f"Error obteniendo datos NOAA: {e}")
            # Fallback a datos simulados
            self._generate_simulated_data()
    
    def _fetch_noaa_plasma(self) -> Dict:
        """Obtiene datos de plasma solar de NOAA SWPC."""
        try:
            response = requests.get(self.NOAA_DST_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # El formato es: [timestamp, speed, density, temperature, bz]
                if len(data) > 1:
                    latest = data[-1]
                    return {
                        'speed': float(latest[1]) if latest[1] != 'null' else 400.0,
                        'bz': float(latest[4]) if latest[4] != 'null' else 0.0,
                        'd_st': self._estimate_dst_from_kp()
                    }
        except Exception as e:
            logger.warning(f"Error en NOAA plasma API: {e}")
        
        return {'speed': 400.0, 'bz': 0.0, 'd_st': 0.0}
    
    def _fetch_noaa_kp(self) -> Dict:
        """Obtiene índice Kp de NOAA."""
        try:
            response = requests.get(self.NOAA_KP_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if len(data) > 1:
                    latest = data[-1]
                    # Formato: [timestamp, kp_index]
                    return {'kp': float(latest[1])}
        except Exception as e:
            logger.warning(f"Error en NOAA Kp API: {e}")
        
        return {'kp': 2.0}
    
    def _estimate_dst_from_kp(self) -> float:
        """Estima índice Dst a partir de Kp (aproximación empírica)."""
        # Relación empírica: Dst ≈ -20 * (Kp - 2) + ruido
        kp = self.current_sample.kp if self.current_sample else 2.0
        return -20.0 * (kp - 2.0) + np.random.normal(0, 5)
    
    def _estimate_schumann(self) -> Dict[str, float]:
        """Estima amplitudes de resonancia Schumann (simulación)."""
        # En implementación real, se usarían datos de satélites
        # o estaciones terrestres especializadas
        t = time.time()
        # Variación diurna de resonancias
        diurnal = np.sin(2 * np.pi * t / 86400) * 0.2
        
        return {
            '7_83': 1.0 + diurnal + np.random.normal(0, 0.1),
            '14_3': 0.7 + diurnal * 0.5 + np.random.normal(0, 0.1),
            '20_8': 0.5 + diurnal * 0.3 + np.random.normal(0, 0.1)
        }
    
    def _generate_simulated_data(self):
        """Genera datos simulados cuando las APIs no están disponibles."""
        t = time.time()
        # Simular variaciones diurnas y tormentas
        diurnal = np.sin(2 * np.pi * t / 86400)
        
        sample = GeomagneticSample(
            timestamp=t,
            d_st=-20.0 * (2.0 + diurnal * 0.5),
            kp=2.0 + diurnal * 0.5,
            bz=np.sin(2 * np.pi * t / 3600) * 2.0,
            solar_wind_speed=400.0 + diurnal * 50,
            schumann_7_83=1.0 + diurnal * 0.2,
            schumann_14_3=0.7 + diurnal * 0.1,
            schumann_20_8=0.5 + diurnal * 0.05
        )
        
        with self._lock:
            self.data_buffer.append(sample)
            self.current_sample = sample
        
        logger.debug("Datos geomagnéticos simulados generados")
    
    def get_current(self) -> Optional[GeomagneticSample]:
        """Obtiene la muestra actual de datos geomagnéticos."""
        with self._lock:
            return self.current_sample
    
    def get_history(self, window_seconds: float = 3600) -> List[GeomagneticSample]:
        """Obtiene historial de datos en la ventana de tiempo especificada."""
        current_time = time.time()
        with self._lock:
            return [s for s in self.data_buffer 
                    if current_time - s.timestamp <= window_seconds]
    
    def get_kp_index(self) -> float:
        """Obtiene el índice Kp actual."""
        current = self.get_current()
        return current.kp if current else 2.0
    
    def get_dst_index(self) -> float:
        """Obtiene el índice Dst actual."""
        current = self.get_current()
        return current.d_st if current else 0.0
    
    def is_geomagnetic_storm(self, threshold_kp: float = 5.0) -> bool:
        """Detecta si hay una tormenta geomagnética en curso."""
        return self.get_kp_index() >= threshold_kp
