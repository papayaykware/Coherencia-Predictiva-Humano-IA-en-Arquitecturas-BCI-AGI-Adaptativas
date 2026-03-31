import torch

def coherence_correlation(node_errors):
    """
    node_errors: (num_nodes, time, dim)
    """

    num_nodes = node_errors.shape[0]
    flat = node_errors.squeeze(-1)

    corr_matrix = torch.corrcoef(flat)

    # media de correlaciones (sin diagonal)
    coherence = (corr_matrix.sum() - num_nodes) / (num_nodes * (num_nodes - 1))

    return coherence.item()

def field_entropy(field_state):
    prob = torch.softmax(field_state, dim=0)
    entropy = -torch.sum(prob * torch.log(prob + 1e-8))
    return entropy.item()

def phase_synchronization(node_errors):
    """
    Aproximación simple basada en fase
    """

    phases = torch.angle(torch.fft.fft(node_errors.squeeze(-1)))
    sync = torch.mean(torch.cos(phases.unsqueeze(0) - phases.unsqueeze(1)))

    return sync.item()
