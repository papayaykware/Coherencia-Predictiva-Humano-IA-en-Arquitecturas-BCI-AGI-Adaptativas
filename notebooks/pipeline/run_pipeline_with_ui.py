# src/pipeline/run_pipeline_with_ui.py
from ui.app import socketio, app, init_pipeline
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    init_pipeline()  # Usa configuración por defecto (simulada)
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
