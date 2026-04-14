import numpy as np

class BaseAGI:
    def __init__(self, embedding_dim=128):
        self.embedding_dim = embedding_dim

    def forward(self, x, label=None):
        raise NotImplementedError
