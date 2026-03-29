import snntorch as snn
import torch.nn as nn

class SNNModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(1, 100)
        self.lif = snn.Leaky(beta=0.9)

    def forward(self, x):
        mem = None
        spk, mem = self.lif(self.fc(x), mem)
        return spk
