from avalanche.benchmarks.generators import nc_benchmark
from avalanche.training.supervised import Naive
from avalanche.training.plugins import EWCPlugin
from avalanche.evaluation.metrics import accuracy_metrics
from avalanche.logging import InteractiveLogger
from avalanche.training.plugins import EvaluationPlugin

import torch
import torch.nn as nn
import torch.optim as optim


def create_strategy(model):
    optimizer = optim.Adam(model.parameters(), lr=1e-3)
    criterion = nn.CrossEntropyLoss()

    ewc = EWCPlugin(ewc_lambda=0.4)

    eval_plugin = EvaluationPlugin(
        accuracy_metrics(epoch=True, experience=True),
        loggers=[InteractiveLogger()]
    )

    strategy = Naive(
        model,
        optimizer,
        criterion,
        train_mb_size=32,
        train_epochs=1,
        eval_mb_size=32,
        plugins=[ewc],
        evaluator=eval_plugin
    )

    return strategy
