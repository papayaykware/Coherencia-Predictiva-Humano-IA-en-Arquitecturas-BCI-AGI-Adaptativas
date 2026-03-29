from avalanche.training import Naive
from avalanche.benchmarks.generators import nc_benchmark

def setup_avalanche(model, optimizer, criterion, datasets):
    benchmark = nc_benchmark(datasets, datasets, n_experiences=3)

    strategy = Naive(
        model=model,
        optimizer=optimizer,
        criterion=criterion,
        train_mb_size=32,
        train_epochs=1
    )

    return strategy, benchmark
