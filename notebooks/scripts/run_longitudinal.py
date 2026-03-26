#!/usr/bin/env python
"""
Ejecuta múltiples sesiones experimentales con el pipeline adaptativo.
Registra métricas y permite pausas entre sesiones.
"""

import argparse
import time
from src.pipeline.run_pipeline import CPEAPipeline
from src.data.simulated_eeg import generate_synthetic_trial  # Asumiendo que existe

def run_session(pipeline, session_id, num_trials=200, blocks=5):
    pipeline.start_experiment_session(session_id)
    trials_per_block = num_trials // blocks
    
    for block in range(blocks):
        print(f"Bloque {block+1}/{blocks}")
        for trial in range(trials_per_block):
            # Simular señal EEG (reemplazar con adquisición real)
            eeg = generate_synthetic_trial()  # Función a implementar
            _, icp = pipeline.process_trial(eeg, block=block)
            print(f"  Trial {trial+1}/{trials_per_block} - ICP: {icp:.4f}")
            time.sleep(0.5)  # Simular tiempo real
    
    pipeline.end_experiment_session()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--participant", default="P001")
    parser.add_argument("--sessions", type=int, default=3)
    parser.add_argument("--trials", type=int, default=200)
    args = parser.parse_args()
    
    pipeline = CPEAPipeline(participant_id=args.participant)
    
    for s in range(args.sessions):
        print(f"\n=== SESIÓN {s+1} ===")
        session_id = f"S{s+1:02d}"
        run_session(pipeline, session_id, num_trials=args.trials)
        if s < args.sessions - 1:
            print("Esperando 24 horas para la siguiente sesión...")
            time.sleep(86400)  # 24 horas (solo para simulación; en real se espera)
