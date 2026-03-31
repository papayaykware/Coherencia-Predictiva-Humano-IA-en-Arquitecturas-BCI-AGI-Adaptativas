import torch

class FieldCoupling:
    def __init__(self, strength=0.05):
        self.strength = strength

    def apply(self, node_states, global_field):
        """
        node_states: (num_nodes, time, dim)
        global_field: (num_nodes, dim)
        """

        # Expandimos field al tiempo
        field_expanded = global_field.unsqueeze(1)

        # Influencia del campo
        coupled = node_states + self.strength * field_expanded

        return coupled

  class NonLinearCoupling:
    def __init__(self, strength=0.05):
        self.strength = strength

    def apply(self, node_states, global_field):
        field_expanded = global_field.unsqueeze(1)

        # acoplamiento tipo resonancia
        coupled = node_states + self.strength * torch.tanh(field_expanded)

        return coupled
