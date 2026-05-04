# En tu script de entrenamiento dpcc_train.py
from qbox_simulator import GeneradorQBox
import torch
import numpy as np

# Generar dataset grande
gen = GeneradorQBox(d=2, canales_meg=32, canales_geof=8)
X, y = gen.generar_dataset_etiquetado(n_muestras=10000, T=1000)

# Convertir a tensores de PyTorch (parte real solamente para simplificar)
X_real = np.real(X)  # shape (10000, 1000, 32, 32, 8, 8)
X_tensor = torch.tensor(X_real, dtype=torch.float32)
y_tensor = torch.tensor(y, dtype=torch.long)

# Ahora puedes usar esto para entrenar tu red DPCC
