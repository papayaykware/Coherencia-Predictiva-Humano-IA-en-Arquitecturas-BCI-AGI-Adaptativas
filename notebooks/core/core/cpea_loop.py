import torch

def run_cpea_loop(model, tae, data):
    preds = model(data)
    anomalies, error = tae.detect(data, preds)
    return preds, anomalies, error
