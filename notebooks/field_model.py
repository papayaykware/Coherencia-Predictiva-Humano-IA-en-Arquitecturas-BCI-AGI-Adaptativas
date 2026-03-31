import torch

class GlobalField:
    def __init__(self, num_nodes, embedding_dim=1):
        self.num_nodes = num_nodes
        self.embedding_dim = embedding_dim
        
        # Estado global del campo
        self.field_state = torch.zeros((num_nodes, embedding_dim))

    def update(self, node_errors):
        """
        node_errors: tensor (num_nodes, time, dim)
        """
        # Promedio temporal → estado instantáneo
        aggregated = node_errors.mean(dim=1)

        # Actualización tipo relajación dinámica
        self.field_state = 0.9 * self.field_state + 0.1 * aggregated

        return self.field_state

    def get_field(self):
        return self.field_state
