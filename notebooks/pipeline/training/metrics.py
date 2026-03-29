import torch

def anomaly_rate(anomalies):
    return anomalies.float().mean().item()

def mse(real, pred):
    return torch.mean((real - pred) ** 2).item()
