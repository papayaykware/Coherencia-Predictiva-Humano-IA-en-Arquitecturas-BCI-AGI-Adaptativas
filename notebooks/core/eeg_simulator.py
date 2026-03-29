import numpy as np

class EEGSimulator:
    def __init__(self, fs=256):
        self.fs = fs

    def generate(self, duration=10):
        t = np.linspace(0, duration, duration*self.fs)
        alpha = np.sin(2*np.pi*10*t)
        beta = 0.5*np.sin(2*np.pi*20*t)
        noise = np.random.normal(0, 0.2, len(t))
        return (alpha + beta + noise).reshape(-1, 1)
