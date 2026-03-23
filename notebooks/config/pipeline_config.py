"""
Configuration file for the AGI pipeline.
"""

# AGI Configuration
AGI_CONFIG = {
    "name": "DummyAGI_V1",
    "version": "1.0.0",
    "learning_rate": 0.01,
    "accuracy_base": 0.85
}

# ICP Calculator Configuration
ICP_WEIGHTS = {
    'complexity': 0.4,
    'performance': 0.4,
    'resources': 0.2
}

# Pipeline Configuration
PIPELINE_CONFIG = {
    "default_trials": 10,
    "save_results": True,
    "results_file": "pipeline_results.json",
    "verbose": True,
    "random_seed": 42  # For reproducibility
}

# Task Generation Configuration
TASK_CONFIG = {
    "min_features": 5,
    "max_features": 50,
    "min_data_size": 100,
    "max_data_size": 10000,
    "complexity_distribution": "beta",  # 'uniform' or 'beta'
    "beta_params": [2, 2]  # For beta distribution
}
