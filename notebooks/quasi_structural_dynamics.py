# Quasi_structural_dynamics.py

import numpy as np
import torch
from sklearn.preprocessing import StandardScaler
from scipy.signal import butter, filtfilt

class QuasiStructuralDynamics:
    def __init__(self, fs=256, embedding_dim=5, delay=2):
        self.fs = fs
        self.embedding_dim = embedding_dim
        self.delay = delay

    # -----------------------------
    # 1. Preprocesado EEG
    # -----------------------------
    def bandpass_filter(self, signal, low=1.0, high=40.0):
        nyq = 0.5 * self.fs
        b, a = butter(4, [low/nyq, high/nyq], btype='band')
        return filtfilt(b, a, signal)

    def preprocess(self, eeg):
        eeg = np.array(eeg)
        eeg = self.bandpass_filter(eeg)
        eeg = StandardScaler().fit_transform(eeg)
        return eeg

    # -----------------------------
    # 2. Delay Embedding
    # -----------------------------
    def delay_embedding(self, signal):
        N = len(signal)
        M = self.embedding_dim
        tau = self.delay

        embedded = np.array([
            signal[i : i + M*tau : tau]
            for i in range(N - M*tau)
        ])
        return embedded

    # -----------------------------
    # 3. Proyección cuasicristalina
    # -----------------------------
    def cut_and_project(self, embedded):
        dim_high = embedded.shape[1]

        # matriz de proyección (aleatoria pero ortogonalizable)
        proj_matrix = np.random.randn(dim_high, 2)
        proj_matrix /= np.linalg.norm(proj_matrix, axis=0)

        projected = embedded @ proj_matrix

        # ventana (filtrado tipo cuasicristal)
        window_radius = np.percentile(np.linalg.norm(projected, axis=1), 50)
        mask = np.linalg.norm(projected, axis=1) < window_radius

        quasi_points = projected[mask]

        return quasi_points

    # -----------------------------
    # 4. Red de correlación
    # -----------------------------
    def correlation_graph(self, points, threshold=0.7):
        dist_matrix = np.linalg.norm(points[:, None] - points[None, :], axis=2)
        similarity = np.exp(-dist_matrix)

        adjacency = (similarity > threshold).astype(float)
        return adjacency

    # -----------------------------
    # 5. Métricas
    # -----------------------------
    def quasi_coherence_index(self, adjacency):
        # densidad de conexiones
        density = adjacency.sum() / adjacency.size

        # estabilidad estructural
        eigenvalues = np.linalg.eigvals(adjacency)
        spectral_entropy = -np.sum(
            np.abs(eigenvalues) * np.log(np.abs(eigenvalues) + 1e-8)
        )

        return {
            "density": density,
            "spectral_entropy": spectral_entropy,
            "QCI": density / (spectral_entropy + 1e-8)
        }

    # -----------------------------
    # Pipeline completo
    # -----------------------------
    def forward(self, eeg_signal):
        eeg_clean = self.preprocess(eeg_signal)
        embedded = self.delay_embedding(eeg_clean)
        quasi_points = self.cut_and_project(embedded)
        adjacency = self.correlation_graph(quasi_points)
        metrics = self.quasi_coherence_index(adjacency)

        return {
            "quasi_points": quasi_points,
            "adjacency": adjacency,
            "metrics": metrics
        }
