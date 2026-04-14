import torch
import numpy as np
from collections import deque


class SafetyLayer:
    """
    Safety Layer for CPEA (EEG–AGI system)

    Funciones:
    - Detectar deriva de señal EEG
    - Detectar deriva del modelo (embedding shift)
    - Calcular Índice de Riesgo Cognitivo (IRC)
    - Bloquear o modular aprendizaje
    """

    def __init__(
        self,
        eeg_window_size=100,
        embedding_window_size=100,
        drift_threshold=2.5,
        risk_threshold=0.7,
        device="cpu"
    ):
        self.device = device

        # Buffers históricos
        self.eeg_buffer = deque(maxlen=eeg_window_size)
        self.embedding_buffer = deque(maxlen=embedding_window_size)

        # Umbrales
        self.drift_threshold = drift_threshold
        self.risk_threshold = risk_threshold

        # Estado
        self.safe_mode = False

    # =========================
    # 1. UPDATE
    # =========================
    def update(self, eeg_sample, embedding):
        """
        eeg_sample: np.array o torch.Tensor
        embedding: torch.Tensor
        """

        eeg_sample = self._to_numpy(eeg_sample)
        embedding = embedding.detach().cpu().numpy()

        self.eeg_buffer.append(eeg_sample)
        self.embedding_buffer.append(embedding)

    # =========================
    # 2. DERIVA EEG
    # =========================
    def compute_eeg_drift(self):
        if len(self.eeg_buffer) < 10:
            return 0.0

        data = np.array(self.eeg_buffer)

        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0) + 1e-6

        z_scores = np.abs((data[-1] - mean) / std)

        drift = np.mean(z_scores)
        return drift

    # =========================
    # 3. DERIVA EMBEDDING
    # =========================
    def compute_embedding_drift(self):
        if len(self.embedding_buffer) < 10:
            return 0.0

        data = np.array(self.embedding_buffer)

        prev_mean = np.mean(data[:-1], axis=0)
        current = data[-1]

        drift = np.linalg.norm(current - prev_mean)
        return drift

    # =========================
    # 4. ÍNDICE DE RIESGO COGNITIVO (IRC)
    # =========================
    def compute_irc(self):
        eeg_drift = self.compute_eeg_drift()
        emb_drift = self.compute_embedding_drift()

        # Normalización simple (puedes calibrar empíricamente)
        eeg_score = np.tanh(eeg_drift / self.drift_threshold)
        emb_score = np.tanh(emb_drift / self.drift_threshold)

        # Peso relativo (ajustable)
        w1, w2 = 0.5, 0.5

        irc = w1 * eeg_score + w2 * emb_score

        return irc, eeg_drift, emb_drift

    # =========================
    # 5. DECISIÓN DE SEGURIDAD
    # =========================
    def check_safety(self):
        irc, eeg_drift, emb_drift = self.compute_irc()

        if irc > self.risk_threshold:
            self.safe_mode = True
        else:
            self.safe_mode = False

        return {
            "irc": irc,
            "eeg_drift": eeg_drift,
            "embedding_drift": emb_drift,
            "safe_mode": self.safe_mode
        }

    # =========================
    # 6. GATING DEL APRENDIZAJE
    # =========================
    def gate_learning(self, loss):
        """
        Modula el aprendizaje según el riesgo.
        """

        if self.safe_mode:
            # Bloqueo total
            return None

        # Atenuación progresiva
        irc, _, _ = self.compute_irc()
        scaling_factor = 1.0 - irc

        return loss * scaling_factor

    # =========================
    # 7. RESET SEGURO
    # =========================
    def reset(self):
        self.eeg_buffer.clear()
        self.embedding_buffer.clear()
        self.safe_mode = False

    # =========================
    # UTILS
    # =========================
    def _to_numpy(self, x):
        if isinstance(x, torch.Tensor):
            return x.detach().cpu().numpy()
        return x
