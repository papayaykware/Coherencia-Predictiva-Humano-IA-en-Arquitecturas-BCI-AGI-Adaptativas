import torch
from core.eeg_simulator import EEGSimulator
from models.lstm_model import LSTMPredictor
from tae.tae_module import TAEModule
from training.loss import get_loss

def train():
    sim = EEGSimulator()
    data = sim.generate()

    data = torch.tensor(data, dtype=torch.float32).unsqueeze(0)

    model = LSTMPredictor()
    tae = TAEModule()

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = get_loss()

    for epoch in range(10):
        pred = model(data)
        loss = loss_fn(pred, data)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch} Loss: {loss.item()}")

    return model, tae
