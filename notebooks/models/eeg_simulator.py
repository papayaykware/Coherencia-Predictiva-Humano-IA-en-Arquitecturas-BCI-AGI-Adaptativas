import numpy as np

class EEGSimulator:
    def __init__(self, n_channels=8, signal_length=256, noise_level=0.1):
        self.n_channels = n_channels
        self.signal_length = signal_length
        self.noise_level = noise_level

    def generate(self, intent=0):
        t = np.linspace(0, 1, self.signal_length)

        signal = []

        for ch in range(self.n_channels):
            freq = 10 + intent * 5  # diferencia por intención
            wave = np.sin(2 * np.pi * freq * t)

            noise = np.random.randn(self.signal_length) * self.noise_level
            signal.append(wave + noise)

        return np.array(signal)
