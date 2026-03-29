import torch

class TAEModule:
    def __init__(self, threshold=0.1):
        self.threshold = threshold

    def detect(self, real, pred):
        error = torch.abs(real - pred)
        anomalies = error > self.threshold
        return anomalies, error
