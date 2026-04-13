import torch

def rate_encoding(features, time_steps=25):
    """
    Convierte features continuas en spikes
    """
    features = torch.tensor(features, dtype=torch.float32)
    spikes = []

    for t in range(time_steps):
        prob = torch.rand_like(features)
        spikes.append((prob < features).float())

    return torch.stack(spikes)
