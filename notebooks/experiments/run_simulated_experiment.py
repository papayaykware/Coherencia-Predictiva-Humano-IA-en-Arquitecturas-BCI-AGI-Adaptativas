"""
src/experiments/run_simulated_experiment.py

Ejecuta un experimento simulado para el pipeline CPEA.
Genera datos para N sujetos sintéticos con condiciones baseline y adaptativa.
Guarda resultados agregados y por sujeto en la carpeta results/.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
import time
import json
from datetime import datetime

# Configuración del experimento
N_SUBJECTS = 10
N_TRIALS = 200  # Por condición, por sujeto (total 400 por sujeto)
CONDITIONS = ['baseline', 'adaptive']
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

# Parámetros de simulación (basados en literatura de BCI)
# Accuracy baseline ~65-75%, adaptativa mejora ~10-15%
BASELINE_ACC_MEAN = 0.70
BASELINE_ACC_STD = 0.05
ADAPTIVE_ACC_GAIN_MEAN = 0.12  # Mejora absoluta
ADAPTIVE_ACC_GAIN_STD = 0.03

# Latencia: baseline ~2-3s, adaptativa reduce ~0.5s
BASELINE_LAT_MEAN = 2.5  # segundos
BASELINE_LAT_STD = 0.3
ADAPTIVE_LAT_REDUCTION_MEAN = 0.6
ADAPTIVE_LAT_REDUCTION_STD = 0.2

# Información Mutua (MI): baseline ~0.3 bits, adaptativa ~0.45 bits
BASELINE_MI_MEAN = 0.30
BASELINE_MI_STD = 0.05
ADAPTIVE_MI_GAIN_MEAN = 0.15
ADAPTIVE_MI_GAIN_STD = 0.04

# Pesos para el ICP (según tu definición)
ICP_WEIGHTS = {'accuracy': 0.4, 'mi': 0.4, 'latency': 0.2}
# La latencia se transforma: 1/error (normalizado). Usaremos 1/(latencia) escalado
# para que esté en rango similar. Asumimos latencia máxima esperada ~4s.
MAX_LATENCY = 4.0

def calculate_icp(accuracy, mi, latency):
    """Calcula el Índice de Coherencia Predictiva (ICP) normalizado [0-1]."""
    latency_score = 1.0 - (latency / MAX_LATENCY)  # Invertido: menor latencia, mayor score
    icp = (ICP_WEIGHTS['accuracy'] * accuracy +
           ICP_WEIGHTS['mi'] * mi +
           ICP_WEIGHTS['latency'] * latency_score)
    # Normalización empírica para que esté en [0,1]
    # Asumiendo rangos: acc[0.5-1], mi[0.2-0.6], latency_score[0.5-1]
    # Esto daría ICP entre ~0.45 y 0.95. Re-escalamos:
    icp_normalized = np.clip((icp - 0.45) / 0.5, 0, 1)
    return icp_normalized

def simulate_subject(subject_id, condition):
    """Simula un sujeto para una condición específica."""
    np.random.seed(RANDOM_SEED + subject_id + (0 if condition == 'baseline' else 1000))

    if condition == 'baseline':
        acc_mean = BASELINE_ACC_MEAN
        acc_std = BASELINE_ACC_STD
        lat_mean = BASELINE_LAT_MEAN
        lat_std = BASELINE_LAT_STD
        mi_mean = BASELINE_MI_MEAN
        mi_std = BASELINE_MI_STD
    else:  # adaptive
        # La mejora es específica por sujeto
        acc_gain = np.random.normal(ADAPTIVE_ACC_GAIN_MEAN, ADAPTIVE_ACC_GAIN_STD)
        acc_mean = BASELINE_ACC_MEAN + acc_gain
        acc_std = BASELINE_ACC_STD * 0.8  # Menor varianza en adaptativa

        lat_reduction = np.random.normal(ADAPTIVE_LAT_REDUCTION_MEAN, ADAPTIVE_LAT_REDUCTION_STD)
        lat_mean = max(0.5, BASELINE_LAT_MEAN - lat_reduction)
        lat_std = BASELINE_LAT_STD * 0.7

        mi_gain = np.random.normal(ADAPTIVE_MI_GAIN_MEAN, ADAPTIVE_MI_GAIN_STD)
        mi_mean = BASELINE_MI_MEAN + mi_gain
        mi_std = BASELINE_MI_STD * 0.7

    # Generar trials con variabilidad intra-sujeto
    acc_trials = np.clip(np.random.normal(acc_mean, acc_std, N_TRIALS), 0.5, 1.0)
    latency_trials = np.clip(np.random.normal(lat_mean, lat_std, N_TRIALS), 0.8, 4.0)
    mi_trials = np.clip(np.random.normal(mi_mean, mi_std, N_TRIALS), 0.1, 0.7)

    # Calcular métricas agregadas
    metrics = {
        'subject_id': subject_id,
        'condition': condition,
        'accuracy_mean': np.mean(acc_trials),
        'accuracy_std': np.std(acc_trials),
        'latency_mean': np.mean(latency_trials),
        'latency_std': np.std(latency_trials),
        'mi_mean': np.mean(mi_trials),
        'mi_std': np.std(mi_trials),
        'trials': N_TRIALS
    }

    # Calcular ICP
    icp = calculate_icp(metrics['accuracy_mean'], metrics['mi_mean'], metrics['latency_mean'])
    metrics['icp'] = icp

    # Guardar trials individuales para análisis detallado (opcional)
    trials_df = pd.DataFrame({
        'subject_id': subject_id,
        'condition': condition,
        'trial': range(N_TRIALS),
        'accuracy': acc_trials,
        'latency': latency_trials,
        'mi': mi_trials
    })

    return metrics, trials_df

def run_experiment():
    """Ejecuta el experimento completo para todos los sujetos y condiciones."""
    print(f"Iniciando experimento simulado: {N_SUBJECTS} sujetos, {N_TRIALS} trials por condición.")
    start_time = time.time()

    all_metrics = []
    all_trials = []

    for subj in range(1, N_SUBJECTS + 1):
        for cond in CONDITIONS:
            print(f"Simulando sujeto {subj:02d}, condición: {cond}...")
            metrics, trials_df = simulate_subject(subj, cond)
            all_metrics.append(metrics)
            all_trials.append(trials_df)

    # Crear dataframes
    metrics_df = pd.DataFrame(all_metrics)
    trials_df = pd.concat(all_trials, ignore_index=True)

    # Guardar resultados
    results_dir = Path('results')
    results_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    metrics_path = results_dir / f'experiment_metrics_{timestamp}.csv'
    trials_path = results_dir / f'experiment_trials_{timestamp}.csv'
    config_path = results_dir / f'experiment_config_{timestamp}.json'

    metrics_df.to_csv(metrics_path, index=False)
    trials_df.to_csv(trials_path, index=False)

    # Guardar configuración
    config = {
        'n_subjects': N_SUBJECTS,
        'n_trials_per_condition': N_TRIALS,
        'conditions': CONDITIONS,
        'random_seed': RANDOM_SEED,
        'icp_weights': ICP_WEIGHTS,
        'max_latency': MAX_LATENCY,
        'baseline_params': {
            'accuracy_mean': BASELINE_ACC_MEAN,
            'latency_mean': BASELINE_LAT_MEAN,
            'mi_mean': BASELINE_MI_MEAN
        },
        'adaptive_gains': {
            'accuracy_mean': ADAPTIVE_ACC_GAIN_MEAN,
            'latency_reduction': ADAPTIVE_LAT_REDUCTION_MEAN,
            'mi_gain': ADAPTIVE_MI_GAIN_MEAN
        }
    }
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

    elapsed = time.time() - start_time
    print(f"Experimento completado en {elapsed:.2f} segundos.")
    print(f"Resultados guardados en: {results_dir}")
    print(f"  - Métricas agregadas: {metrics_path.name}")
    print(f"  - Trials individuales: {trials_path.name}")
    print(f"  - Configuración: {config_path.name}")

    return metrics_df, trials_df

if __name__ == "__main__":
    run_experiment()
