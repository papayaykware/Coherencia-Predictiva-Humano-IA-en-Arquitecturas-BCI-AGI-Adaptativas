"""
Generador de señales EEG sintéticas para pruebas de integración.
Simula una mejora gradual en la coherencia cuando el sistema está adaptándose.
"""

import numpy as np
import random

def generate_synthetic_trial(adaptive_mode=True, trial_index=0, session=0):
    """
    Genera señal EEG simulada con tendencia de mejora si el sistema es adaptativo.
    En modo adaptativo, la "calidad" de la señal aumenta con el trial y la sesión.
    """
    # Parámetros base
    fs = 256  # Hz
    duration = 2  # segundos
    t = np.linspace(0, duration, int(fs*duration))
    
    # Ruido base
    noise = np.random.randn(len(t)) * 0.5
    
    # Señal útil simulada: suma de senoides en bandas alfa y beta
    alpha_freq = 10  # Hz
    beta_freq = 20   # Hz
    alpha_amp = 0.3
    beta_amp = 0.2
    
    # Si es modo adaptativo, la amplitud de la señal aumenta con el progreso
    if adaptive_mode:
        # Progreso normalizado entre 0 y 1 (trial 0 a 2000, sesión 0 a 2)
        progress = (trial_index / 2000) + (session / 3)
        progress = min(progress, 1.0)
        alpha_amp += 0.5 * progress
        beta_amp += 0.3 * progress
    else:
        alpha_amp = 0.3
        beta_amp = 0.2
    
    signal = (alpha_amp * np.sin(2*np.pi*alpha_freq*t) +
              beta_amp * np.sin(2*np.pi*beta_freq*t) +
              noise)
    
    return signal
