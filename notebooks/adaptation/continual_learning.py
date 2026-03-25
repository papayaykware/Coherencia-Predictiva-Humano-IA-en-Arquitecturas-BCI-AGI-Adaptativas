"""
src/adaptation/continual_learning.py

Módulo para aprendizaje continuo en el clasificador EEG del pipeline CPEA.
Implementa técnicas de Experience Replay y Elastic Weight Consolidation (EWC)
para actualizar el modelo incrementalmente sin olvido catastrófico.
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from collections import deque
import random
from typing import Optional, List, Tuple, Dict, Any
import copy
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ExperienceReplayBuffer:
    """
    Buffer de replay para almacenar y muestrear experiencias pasadas.
    """
    def __init__(self, max_size: int = 2000):
        """
        Args:
            max_size: Número máximo de muestras a almacenar.
        """
        self.buffer = deque(maxlen=max_size)

    def add(self, x: np.ndarray, y: np.ndarray):
        """
        Añade una nueva experiencia (características y etiqueta) al buffer.
        """
        self.buffer.append((x.copy(), y.copy()))

    def sample(self, batch_size: int) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Muestrea un lote aleatorio de experiencias del buffer.
        """
        if len(self.buffer) < batch_size:
            batch_size = len(self.buffer)
        samples = random.sample(self.buffer, batch_size)
        x_batch = torch.tensor(np.array([s[0] for s in samples]), dtype=torch.float32)
        y_batch = torch.tensor(np.array([s[1] for s in samples]), dtype=torch.long)
        return x_batch, y_batch

    def __len__(self) -> int:
        return len(self.buffer)

class ElasticWeightConsolidation:
    """
    Implementación de Elastic Weight Consolidation (EWC) para regularización
    en aprendizaje continuo.
    """
    def __init__(self, model: nn.Module, fisher_sample_size: int = 1000,
                 fisher_batch_size: int = 32):
        """
        Args:
            model: Modelo PyTorch a regularizar.
            fisher_sample_size: Número de muestras para estimar la matriz Fisher.
            fisher_batch_size: Tamaño de lote para la estimación de Fisher.
        """
        self.model = model
        self.fisher_sample_size = fisher_sample_size
        self.fisher_batch_size = fisher_batch_size
        self.params = {n: p for n, p in model.named_parameters() if p.requires_grad}
        self._means = {}
        self._precision_matrices = {}

    def update_fisher_and_means(self, dataset: DataLoader):
        """
        Estima la matriz de Fisher diagonal y guarda los parámetros óptimos actuales.
        Se llama después de entrenar en una nueva tarea.
        """
        logger.info("Estimando matriz de Fisher para EWC...")
        self.model.eval()

        # Guardar parámetros actuales como referencia
        for n, p in self.params.items():
            self._means[n] = p.data.clone()

        # Inicializar precision matrices
        for n, p in self.params.items():
            self._precision_matrices[n] = torch.zeros_like(p.data)

        # Calcular gradientes al cuadrado (Fisher diagonal)
        # Usar un subset de datos representativo
        n_samples = 0
        for batch_x, batch_y in dataset:
            if n_samples >= self.fisher_sample_size:
                break
            self.model.zero_grad()
            outputs = self.model(batch_x)
            loss = nn.functional.cross_entropy(outputs, batch_y)
            loss.backward()

            for n, p in self.params.items():
                if p.grad is not None:
                    self._precision_matrices[n] += p.grad.data.clone().pow(2) / self.fisher_sample_size
            n_samples += batch_x.size(0)

        logger.info("Estimación de Fisher completada.")

    def ewc_loss(self, lambda_ewc: float = 0.1) -> torch.Tensor:
        """
        Calcula la pérdida de regularización EWC.
        """
        loss = 0.0
        for n, p in self.params.items():
            if n in self._means:
                # Diferencia entre parámetros actuales y los del mejor modelo anterior
                diff = p - self._means[n]
                loss += (self._precision_matrices[n] * diff.pow(2)).sum()
        return lambda_ewc * loss

class ContinualLearner:
    """
    Clase principal que combina Replay y EWC para aprendizaje continuo
    en el clasificador EEG.
    """
    def __init__(self, model: nn.Module, device: torch.device,
                 replay_buffer_size: int = 2000,
                 lambda_ewc: float = 0.1,
                 replay_batch_size: int = 32,
                 learning_rate: float = 1e-3,
                 ewc_update_interval: int = 100):
        """
        Args:
            model: Modelo PyTorch del clasificador EEG.
            device: Dispositivo (cpu o cuda).
            replay_buffer_size: Tamaño máximo del buffer de replay.
            lambda_ewc: Factor de regularización para EWC.
            replay_batch_size: Tamaño de lote para muestras de replay.
            learning_rate: Tasa de aprendizaje para el optimizador.
            ewc_update_interval: Cada cuántas actualizaciones se recalcula EWC.
        """
        self.model = model.to(device)
        self.device = device
        self.replay_buffer = ExperienceReplayBuffer(max_size=replay_buffer_size)
        self.ewc = None
        self.lambda_ewc = lambda_ewc
        self.replay_batch_size = replay_batch_size
        self.learning_rate = learning_rate
        self.ewc_update_interval = ewc_update_interval
        self.update_counter = 0

        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.criterion = nn.CrossEntropyLoss()

    def add_experience(self, x: np.ndarray, y: np.ndarray):
        """
        Almacena una nueva experiencia en el buffer de replay.
        Args:
            x: Características EEG (array numpy).
            y: Etiqueta de intent (array numpy con un entero).
        """
        self.replay_buffer.add(x, y)

    def update(self, new_x: np.ndarray, new_y: np.ndarray,
               epochs: int = 1, batch_size: int = 32,
               use_replay: bool = True, use_ewc: bool = True) -> Dict[str, float]:
        """
        Actualiza el modelo con nuevos datos, combinando replay y/o EWC.
        Args:
            new_x: Nuevas características EEG.
            new_y: Nuevas etiquetas.
            epochs: Número de épocas de entrenamiento.
            batch_size: Tamaño de lote para los datos nuevos.
            use_replay: Si usar experience replay.
            use_ewc: Si usar regularización EWC.
        Returns:
            Diccionario con métricas de pérdida durante la actualización.
        """
        logger.info("Iniciando actualización continua del clasificador...")

        # Preparar datos nuevos
        new_dataset = TensorDataset(torch.tensor(new_x, dtype=torch.float32),
                                    torch.tensor(new_y, dtype=torch.long))
        new_loader = DataLoader(new_dataset, batch_size=batch_size, shuffle=True)

        # Si es la primera actualización después de un lote de datos, inicializar EWC
        if use_ewc and self.ewc is None:
            logger.info("Inicializando EWC con datos nuevos...")
            self.ewc = ElasticWeightConsolidation(self.model)
            # Estimar Fisher con los datos nuevos como base
            self.ewc.update_fisher_and_means(new_loader)

        metrics = {'loss': [], 'replay_loss': [], 'ewc_loss': []}

        for epoch in range(epochs):
            self.model.train()
            epoch_loss = 0.0
            epoch_replay_loss = 0.0
            epoch_ewc_loss = 0.0

            # Entrenar con datos nuevos
            for batch_x, batch_y in new_loader:
                batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)

                self.optimizer.zero_grad()

                # Forward pass con datos nuevos
                outputs = self.model(batch_x)
                loss_new = self.criterion(outputs, batch_y)
                total_loss = loss_new

                # Replay: añadir pérdida de muestras pasadas
                if use_replay and len(self.replay_buffer) > 0:
                    replay_x, replay_y = self.replay_buffer.sample(self.replay_batch_size)
                    replay_x, replay_y = replay_x.to(self.device), replay_y.to(self.device)
                    outputs_replay = self.model(replay_x)
                    loss_replay = self.criterion(outputs_replay, replay_y)
                    total_loss += loss_replay
                    epoch_replay_loss += loss_replay.item()

                # EWC: añadir pérdida de regularización
                if use_ewc and self.ewc is not None:
                    loss_ewc = self.ewc.ewc_loss(self.lambda_ewc)
                    total_loss += loss_ewc
                    epoch_ewc_loss += loss_ewc.item()

                # Backward pass y optimización
                total_loss.backward()
                self.optimizer.step()

                epoch_loss += total_loss.item()

            # Registrar métricas por época
            metrics['loss'].append(epoch_loss / len(new_loader))
            if use_replay:
                metrics['replay_loss'].append(epoch_replay_loss / len(new_loader))
            if use_ewc:
                metrics['ewc_loss'].append(epoch_ewc_loss / len(new_loader))

            logger.info(f"Época {epoch+1}/{epochs} - Pérdida total: {metrics['loss'][-1]:.4f}")

        # Actualizar contador y potencialmente recalcular Fisher
        self.update_counter += 1
        if use_ewc and self.update_counter % self.ewc_update_interval == 0:
            logger.info("Recalculando matriz de Fisher con datos recientes...")
            # Recalcular Fisher con datos nuevos (o mezcla)
            self.ewc.update_fisher_and_means(new_loader)

        logger.info("Actualización continua completada.")
        return metrics

    def evaluate(self, x: np.ndarray, y: np.ndarray, batch_size: int = 32) -> float:
        """
        Evalúa el modelo actual en un conjunto de datos.
        Returns:
            Accuracy.
        """
        self.model.eval()
        dataset = TensorDataset(torch.tensor(x, dtype=torch.float32),
                                torch.tensor(y, dtype=torch.long))
        loader = DataLoader(dataset, batch_size=batch_size)
        correct = 0
        total = 0
        with torch.no_grad():
            for batch_x, batch_y in loader:
                batch_x, batch_y = batch_x.to(self.device), batch_y.to(self.device)
                outputs = self.model(batch_x)
                _, predicted = torch.max(outputs, 1)
                total += batch_y.size(0)
                correct += (predicted == batch_y).sum().item()
        return correct / total

# Ejemplo de uso integrado con pipeline
if __name__ == "__main__":
    # Simulación de modelo simple para prueba
    class SimpleClassifier(nn.Module):
        def __init__(self, input_dim=10, num_classes=3):
            super().__init__()
            self.fc = nn.Linear(input_dim, num_classes)

        def forward(self, x):
            return self.fc(x)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleClassifier()
    continual_learner = ContinualLearner(model, device)

    # Datos de ejemplo: 100 muestras iniciales (tarea base)
    X_base = np.random.rand(100, 10).astype(np.float32)
    y_base = np.random.randint(0, 3, size=100)
    continual_learner.update(X_base, y_base, epochs=2)

    # Almacenar experiencias en buffer (opcional)
    for i in range(50):
        continual_learner.add_experience(X_base[i], y_base[i])

    # Nuevos datos (nueva tarea o distribución)
    X_new = np.random.rand(50, 10).astype(np.float32)
    y_new = np.random.randint(0, 3, size=50)

    # Actualizar con replay y EWC
    metrics = continual_learner.update(X_new, y_new, epochs=2, use_replay=True, use_ewc=True)
    print("Métricas de actualización:", metrics)

    # Evaluación en datos base (para verificar que no hubo olvido)
    acc_base = continual_learner.evaluate(X_base, y_base)
    print(f"Accuracy en datos base después de actualización: {acc_base:.2f}")
