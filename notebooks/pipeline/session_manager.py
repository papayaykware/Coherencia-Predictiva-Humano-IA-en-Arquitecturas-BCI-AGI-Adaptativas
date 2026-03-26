"""
Gestión de sesiones prolongadas para CPEA.
Mantiene el estado del modelo AGI (pesos LoRA) entre sesiones y registra métricas longitudinales.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
import pandas as pd

from src.models.agi_finetuner import AGIOnlineFinetuner
from src.utils.metrics import compute_icp, compute_adaptation_effect

logger = logging.getLogger(__name__)

class CPESessionManager:
    """
    Administra sesiones múltiples, persistencia del modelo y análisis longitudinal.
    """
    
    def __init__(self, base_path: str = "./experiments", participant_id: str = "P001"):
        self.base_path = base_path
        self.participant_id = participant_id
        self.session_path = os.path.join(base_path, participant_id)
        os.makedirs(self.session_path, exist_ok=True)
        
        # Archivos de registro
        self.metrics_file = os.path.join(self.session_path, "metrics.csv")
        self.config_file = os.path.join(self.session_path, "config.json")
        
        # Inicializar o cargar modelo adaptativo
        self.agi = AGIOnlineFinetuner("config/agi_config.yaml")
        
        # Cargar pesos LoRA si existen (continuación)
        self._load_lora_if_exists()
        
        # Registro de sesiones
        self.current_session_id = None
        self.session_start = None
        
    def _load_lora_if_exists(self):
        """Carga los pesos LoRA más recientes de la carpeta de experimentos."""
        lora_path = os.path.join(self.session_path, "lora_weights")
        if os.path.exists(lora_path):
            self.agi.load_lora_weights(lora_path)
            logger.info(f"Pesos LoRA cargados desde {lora_path}")
    
    def start_session(self, session_id: Optional[str] = None):
        """Inicia una nueva sesión de registro."""
        if session_id is None:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.current_session_id = session_id
        self.session_start = datetime.now()
        
        # Crear subcarpeta para esta sesión
        self.session_dir = os.path.join(self.session_path, session_id)
        os.makedirs(self.session_dir, exist_ok=True)
        
        # Archivo de log de trials
        self.trials_log = os.path.join(self.session_dir, "trials.csv")
        self.icp_log = os.path.join(self.session_dir, "icp.csv")
        
        # Inicializar archivos con cabeceras
        with open(self.trials_log, 'w') as f:
            f.write("trial_id,timestamp,eeg_features,response,icp\n")
        with open(self.icp_log, 'w') as f:
            f.write("trial_id,icp,block\n")
        
        logger.info(f"Sesión {session_id} iniciada para {self.participant_id}")
    
    def end_session(self):
        """Finaliza la sesión actual, guarda estado y calcula métricas."""
        if self.current_session_id is None:
            return
        
        # Guardar pesos LoRA actuales
        lora_save_path = os.path.join(self.session_path, "lora_weights")
        self.agi.save_lora_weights(lora_save_path)
        
        # Guardar resumen de sesión
        summary = self._compute_session_summary()
        with open(os.path.join(self.session_dir, "summary.json"), 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Sesión {self.current_session_id} finalizada. Resumen guardado.")
        self.current_session_id = None
    
    def log_trial(self, trial_id: int, eeg_features: Dict, response: str, icp: float, block: int):
        """Registra un trial completo en los logs."""
        timestamp = datetime.now().isoformat()
        
        # Guardar trial
        with open(self.trials_log, 'a') as f:
            f.write(f"{trial_id},{timestamp},{json.dumps(eeg_features)},{response},{icp}\n")
        
        # Guardar ICP por separado para análisis rápido
        with open(self.icp_log, 'a') as f:
            f.write(f"{trial_id},{icp},{block}\n")
    
    def _compute_session_summary(self) -> Dict:
        """Calcula métricas resumen de la sesión a partir de los logs."""
        df = pd.read_csv(self.icp_log)
        icp_array = df['icp'].values
        blocks = df['block'].values
        
        # Métricas básicas
        initial_icp = np.mean(icp_array[:20])  # primeros 20 trials
        final_icp = np.mean(icp_array[-20:])   # últimos 20 trials
        improvement = final_icp - initial_icp
        
        # Pendiente de regresión lineal
        if len(icp_array) > 5:
            x = np.arange(len(icp_array))
            slope, _ = np.polyfit(x, icp_array, 1)
        else:
            slope = np.nan
        
        # Desviación estándar por bloque
        block_means = [np.mean(icp_array[blocks == b]) for b in np.unique(blocks)]
        
        return {
            "session_id": self.current_session_id,
            "num_trials": len(icp_array),
            "initial_icp": initial_icp,
            "final_icp": final_icp,
            "absolute_improvement": improvement,
            "relative_improvement": improvement / max(initial_icp, 0.01),
            "slope": slope,
            "block_means": block_means,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_longitudinal_data(self) -> pd.DataFrame:
        """Recupera métricas de todas las sesiones para análisis longitudinal."""
        summaries = []
        for session_dir in os.listdir(self.session_path):
            summary_file = os.path.join(self.session_path, session_dir, "summary.json")
            if os.path.exists(summary_file):
                with open(summary_file) as f:
                    summaries.append(json.load(f))
        return pd.DataFrame(summaries)
