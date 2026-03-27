# -*- coding: utf-8 -*-
# src/ui/app.py
"""
Servidor web para visualización en tiempo real del pipeline CPEA.
Comunica datos EEG, clasificación y respuestas AGI mediante WebSockets.
"""

import eventlet
eventlet.monkey_patch()  # Necesario para SocketIO con concurrencia

from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
import logging
import threading
import time
import numpy as np
from typing import Dict, Any

# Importar gestor EEG y pipeline (asumiendo que existen)
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from hardware.muse_stream import EEGStreamManager, EEGConfig, HardwareType
from pipeline.agi_client import AGIClient  # Asumiendo que existe
from pipeline.eeg_classifier import EEGClassifier  # Asumiendo que existe

# Configuración logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar Flask y SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cpea-secret-key-change-in-production'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Estado global compartido entre hilos
class SharedState:
    def __init__(self):
        self.latest_eeg: np.ndarray = np.zeros((4,))  # Última muestra EEG
        self.eeg_buffer = []  # Buffer para gráfico (timestamp, datos)
        self.latest_intent: str = "Ninguno"
        self.intent_prob: float = 0.0
        self.latest_agi_response: str = ""
        self.latest_icp: float = 0.0
        self.stream_running: bool = False
        self.lock = threading.Lock()

state = SharedState()

# Inicializar componentes del pipeline
eeg_manager = None
classifier = None
agi_client = None

def init_pipeline(config_eeg: EEGConfig = None):
    """Inicializa el pipeline completo con hardware simulado o real."""
    global eeg_manager, classifier, agi_client
    
    if config_eeg is None:
        config_eeg = EEGConfig(hardware=HardwareType.SIMULATED)
    
    eeg_manager = EEGStreamManager(config_eeg)
    classifier = EEGClassifier()  # Asumimos que existe clase con método predict()
    agi_client = AGIClient()      # Asumimos que existe
    
    # Conectar y arrancar adquisición
    if eeg_manager.connect():
        eeg_manager.start_acquisition()
        logger.info("Pipeline inicializado correctamente")
    else:
        logger.error("Fallo al conectar hardware EEG")

def eeg_callback(processed_sample: np.ndarray, timestamp: float):
    """Callback que recibe muestras procesadas y actualiza estado."""
    global state
    
    # Clasificar intent (cada N muestras, por simplicidad cada muestra)
    # En real deberías acumular ventana, aquí ejemplo rápido
    intent, prob = classifier.predict(processed_sample)
    
    # Actualizar estado con lock
    with state.lock:
        state.latest_eeg = processed_sample
        # Mantener buffer para gráfico (últimos 5 segundos ~ 256*5 = 1280 muestras)
        state.eeg_buffer.append((timestamp, processed_sample.copy()))
        if len(state.eeg_buffer) > 1280:
            state.eeg_buffer.pop(0)
        state.latest_intent = intent
        state.intent_prob = prob
    
    # Emitir vía WebSocket solo si hay clientes conectados
    socketio.emit('eeg_update', {
        'timestamp': timestamp,
        'channels': processed_sample.tolist(),
        'intent': intent,
        'intent_prob': prob
    })

def agi_response_callback(agi_response: str, icp: float):
    """Callback cuando el AGI responde."""
    with state.lock:
        state.latest_agi_response = agi_response
        state.latest_icp = icp
    
    socketio.emit('agi_update', {
        'response': agi_response,
        'icp': icp
    })

def pipeline_loop():
    """Bucle que simula la lógica de envío a AGI cada cierto tiempo."""
    while state.stream_running:
        time.sleep(2.0)  # Enviar a AGI cada 2 segundos (ajustable)
        with state.lock:
            if len(state.eeg_buffer) > 0:
                # Tomar últimos datos EEG para contexto
                last_samples = np.array([s[1] for s in state.eeg_buffer[-10:]])
                features = np.mean(last_samples, axis=0)  # Feature simple
                intent = state.latest_intent
            else:
                features = np.zeros(4)
                intent = "desconocido"
        
        # Construir prompt y llamar a AGI
        prompt = f"EEG features: {features}, intent detected: {intent}. Respond briefly."
        try:
            agi_response = agi_client.query(prompt)
            icp = compute_icp(features, agi_response)  # Función aparte
            agi_response_callback(agi_response, icp)
        except Exception as e:
            logger.error(f"Error en AGI: {e}")

def compute_icp(eeg_features, agi_response):
    """Ejemplo de cálculo de ICP simplificado."""
    # En versión real usarías embeddings y correlación
    return np.random.random()  # Placeholder

# Rutas HTTP
@app.route('/')
def index():
    """Página principal."""
    return render_template('dashboard.html')

@app.route('/api/status')
def status():
    """Endpoint REST para estado actual."""
    with state.lock:
        return jsonify({
            'stream_running': state.stream_running,
            'latest_intent': state.latest_intent,
            'intent_prob': state.intent_prob,
            'latest_icp': state.latest_icp,
            'eeg_buffer_len': len(state.eeg_buffer)
        })

@app.route('/api/config', methods=['POST'])
def update_config():
    """Permite cambiar hardware o parámetros desde UI."""
    data = request.json
    # Aquí implementar cambio de hardware dinámico
    return jsonify({'status': 'ok'})

# Eventos SocketIO
@socketio.on('connect')
def handle_connect():
    logger.info('Cliente conectado')
    emit('connected', {'message': 'Conectado al servidor CPEA'})

@socketio.on('start_stream')
def handle_start_stream():
    """Inicia el flujo de datos si no está activo."""
    global state
    if not state.stream_running:
        state.stream_running = True
        # Arrancar hilo del pipeline AGI
        threading.Thread(target=pipeline_loop, daemon=True).start()
        # Registrar callback en eeg_manager
        if eeg_manager:
            eeg_manager.on_processed_sample = eeg_callback
        emit('stream_started', {'status': True})
    else:
        emit('stream_started', {'status': False, 'message': 'Ya activo'})

@socketio.on('stop_stream')
def handle_stop_stream():
    global state
    state.stream_running = False
    if eeg_manager:
        eeg_manager.stop_acquisition()
    emit('stream_stopped', {'status': True})

# Inicialización al arrancar
if __name__ == '__main__':
    init_pipeline()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
