import logging
import numpy as np

from snn_model import SNNModel
from spike_encoder import rate_encoding
from continual import create_strategy
from dataset import EEGDataset

import torch

logging.basicConfig(level=logging.INFO)


def generate_dummy_labels(n):
    return np.random.randint(0, 2, size=n)


def run_pipeline(features):
    logging.info("Inicializando SNN + Continual Learning...")

    model = SNNModel(input_size=features.shape[1])
    strategy = create_strategy(model)

    labels = generate_dummy_labels(len(features))

    dataset = EEGDataset(features, labels)

    # Simulación de experiencias (continual learning)
    experiences = [dataset]  # luego se pueden segmentar temporalmente

    for exp_id, exp in enumerate(experiences):
        logging.info(f"Training experience {exp_id}")

        strategy.train(exp)
        strategy.eval(exp)

    # Inferencia
    logging.info("Inferencia en tiempo real...")

    spikes = rate_encoding(features)
    spikes = spikes.mean(dim=0)  # simplificación

    output = model(spikes)
    prediction = output.sum(dim=0).argmax(dim=1)

    return prediction
