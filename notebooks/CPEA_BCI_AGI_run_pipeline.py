#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CPEA: BCI–AGI Predictive Coherence Pipeline

Pipeline ejecutable end-to-end:
- Ingesta EEG (real o sintético)
- Filtrado
- Extracción de características
- Embeddings
- Clasificación
- Interfaz AGI (mock)

Modo:
    python CPEA_BCI_AGI_run_pipeline.py --baseline
"""

import os
import argparse
import logging
import numpy as np
from scipy import signal
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier

# -------------------------
# CONFIG LOGGING
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# -------------------------
# DATA INGEST
# -------------------------
def load_sample_eeg(path="data/sample_eeg.npy"):
    if os.path.exists(path):
        logging.info(f"Cargando datos EEG desde {path}")
        return np.load(path)
    else:
        logging.warning("No se encontró sample_eeg. Generando datos sintéticos...")
        return generate_synthetic_eeg()

def generate_synthetic_eeg(n_channels=8, n_samples=5000, fs=250):
    t = np.linspace(0, n_samples/fs, n_samples)
    eeg = []

    for ch in range(n_channels):
        signal_alpha = np.sin(2 * np.pi * 10 * t)
        signal_beta = np.sin(2 * np.pi * 20 * t)
        noise = np.random.normal(0, 0.5, size=n_samples)
        eeg.append(signal_alpha + signal_beta + noise)

    eeg = np.array(eeg)
    logging.info(f"EEG sintético generado: {eeg.shape}")
    return eeg

# -------------------------
# PREPROCESSING
# -------------------------
def bandpass_filter(data, fs=250, low=1, high=40):
    logging.info("Aplicando filtro bandpass...")
    sos = signal.butter(4, [low, high], btype='band', fs=fs, output='sos')
    return signal.sosfilt(sos, data)

# -------------------------
# FEATURE EXTRACTION
# -------------------------
def extract_features(eeg, fs=250):
    logging.info("Extrayendo características espectrales...")
    features = []

    for ch in eeg:
        freqs, psd = signal.welch(ch, fs)
        alpha_power = np.mean(psd[(freqs >= 8) & (freqs <= 12)])
        beta_power = np.mean(psd[(freqs >= 13) & (freqs <= 30)])
        theta_power = np.mean(psd[(freqs >= 4) & (freqs <= 7)])

        features.append([alpha_power, beta_power, theta_power])

    return np.array(features)

# -------------------------
# EMBEDDINGS
# -------------------------
def compute_embeddings(features, n_components=2):
    logging.info("Reduciendo dimensionalidad (embeddings)...")
    pca = PCA(n_components=n_components)
    return pca.fit_transform(features)

# -------------------------
# CLASSIFICATION
# -------------------------
def classify(embeddings):
    logging.info("Clasificando estado cognitivo...")
    clf = RandomForestClassifier()
    
    # etiquetas dummy (baseline)
    y = np.random.randint(0, 2, size=embeddings.shape[0])
    clf.fit(embeddings, y)

    preds = clf.predict(embeddings)
    return preds

# -------------------------
# AGI INTERFACE (MOCK)
# -------------------------
def agi_interface(predictions):
    logging.info("Enviando resultados a módulo AGI (mock)...")
    
    # Placeholder AGI
    interpretation = {
        0: "Estado estable",
        1: "Desviación detectada"
    }

    responses = [interpretation[p] for p in predictions]
    return responses

# -------------------------
# PIPELINE
# -------------------------
def run_pipeline(args):
    logging.info("===== INICIO PIPELINE CPEA =====")

    # 1. Ingesta
    eeg = load_sample_eeg() if args.baseline else load_sample_eeg(args.input)

    # 2. Filtrado
    eeg_filtered = bandpass_filter(eeg)

    # 3. Features
    features = extract_features(eeg_filtered)

    # 4. Embeddings
    embeddings = compute_embeddings(features)

    # 5. Clasificación
    predictions = classify(embeddings)

    # 6. AGI
    responses = agi_interface(predictions)

    logging.info("===== RESULTADOS =====")
    for i, r in enumerate(responses[:10]):
        logging.info(f"Canal {i}: {r}")

    logging.info("===== FIN PIPELINE =====")


# -------------------------
# MAIN
# -------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CPEA Pipeline")
    parser.add_argument("--baseline", action="store_true", help="Modo datos sintéticos")
    parser.add_argument("--input", type=str, help="Ruta a EEG real")

    args = parser.parse_args()
    run_pipeline(args)
