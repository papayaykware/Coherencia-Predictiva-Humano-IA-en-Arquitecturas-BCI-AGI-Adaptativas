import numpy as np

class LatentProjector:
    def __init__(self, input_dim, latent_dim=128):
        self.W = np.random.randn(latent_dim, input_dim)

    def project(self, x):
        x_flat = x.flatten()
        return np.dot(self.W, x_flat)
