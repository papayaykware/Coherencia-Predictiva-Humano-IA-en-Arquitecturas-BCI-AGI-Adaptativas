"""
Módulo para calcular el Índice de Coherencia Predictiva (ICP)
según la definición formal del proyecto CPEA.

Fórmula:
    ICP = w1 * Accuracy + w2 * MI + w3 * (1 / (1 + Error_AGI))

Donde:
    - Accuracy: Precisión de clasificación de intención [0, 1]
    - MI: Información mutua entre EEG features e intención [0, ~]
    - Error_AGI: Error entre respuesta esperada y generada (≥ 0)
    - w1, w2, w3: pesos que suman 1 (por defecto [0.4, 0.3, 0.3])

Normalización:
    - MI se normaliza con un factor máximo teórico (log2(n_classes)) o empírico
    - Error_AGI se transforma con 1/(1+error) para mantener ICP en [0,1]
"""

import numpy as np
from typing import Union, Optional, Tuple
from sklearn.metrics import mutual_info_score


def compute_accuracy(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """
    Calcula la precisión de clasificación.

    Args:
        y_true: Etiquetas reales
        y_pred: Etiquetas predichas

    Returns:
        Accuracy en [0, 1]
    """
    if len(y_true) != len(y_pred):
        raise ValueError("y_true y y_pred deben tener la misma longitud")
    if len(y_true) == 0:
        return 0.0
    return np.mean(y_true == y_pred)


def compute_mutual_information(
    X: np.ndarray,
    y: np.ndarray,
    n_classes: Optional[int] = None,
    normalize: bool = True
) -> float:
    """
    Calcula la información mutua entre características EEG y etiquetas de intención.

    Args:
        X: Matriz de características (n_samples, n_features)
        y: Etiquetas de intención (n_samples,)
        n_classes: Número de clases posibles (para normalización)
        normalize: Si es True, normaliza por log2(n_classes)

    Returns:
        MI (normalizado si normalize=True) en [0, 1] si se normaliza
    """
    if len(X) != len(y):
        raise ValueError("X y y deben tener la misma longitud")
    if len(X) == 0:
        return 0.0

    # Discretizar X si es continua (usando bins por feature)
    # En una implementación real, podrías usar estimadores más avanzados
    n_bins = 10
    X_discrete = np.apply_along_axis(
        lambda col: np.digitize(col, np.percentile(col, np.linspace(0, 100, n_bins+1)[1:-1])),
        axis=0,
        arr=X
    )
    
    # Calcular MI para cada feature y promediar
    mi_values = []
    for i in range(X.shape[1]):
        mi = mutual_info_score(X_discrete[:, i], y)
        mi_values.append(mi)
    
    mi_avg = np.mean(mi_values)
    
    if normalize:
        if n_classes is None:
            n_classes = len(np.unique(y))
        max_mi = np.log2(n_classes)
        if max_mi > 0:
            return mi_avg / max_mi
        else:
            return 0.0
    return mi_avg


def compute_agi_error(
    expected_response: np.ndarray,
    actual_response: np.ndarray,
    metric: str = 'mse'
) -> float:
    """
    Calcula el error entre la respuesta esperada por el humano y la generada por la AGI.

    Args:
        expected_response: Vector de respuesta esperada (embedding o label)
        actual_response: Vector de respuesta generada por AGI
        metric: 'mse', 'mae', o 'cosine' (distancia angular)

    Returns:
        Error (≥ 0)
    """
    if len(expected_response) != len(actual_response):
        raise ValueError("Los vectores deben tener la misma longitud")
    
    if metric == 'mse':
        return np.mean((expected_response - actual_response) ** 2)
    elif metric == 'mae':
        return np.mean(np.abs(expected_response - actual_response))
    elif metric == 'cosine':
        # Distancia coseno: 1 - cos_sim
        dot = np.dot(expected_response, actual_response)
        norm_e = np.linalg.norm(expected_response)
        norm_a = np.linalg.norm(actual_response)
        if norm_e == 0 or norm_a == 0:
            return 1.0
        cos_sim = dot / (norm_e * norm_a)
        # Clipping por seguridad
        cos_sim = np.clip(cos_sim, -1.0, 1.0)
        return 1.0 - cos_sim
    else:
        raise ValueError(f"Métrica '{metric}' no soportada. Usa 'mse', 'mae' o 'cosine'.")


def compute_icp(
    accuracy: Union[float, np.ndarray],
    mutual_info: Union[float, np.ndarray],
    agi_error: Union[float, np.ndarray],
    weights: Tuple[float, float, float] = (0.4, 0.3, 0.3)
) -> float:
    """
    Calcula el Índice de Coherencia Predictiva (ICP).

    Args:
        accuracy: Precisión de clasificación (0–1)
        mutual_info: Información mutua normalizada (0–1)
        agi_error: Error AGI (≥ 0)
        weights: Pesos (w_accuracy, w_mi, w_error) que deben sumar 1

    Returns:
        ICP en [0, 1]
    """
    # Validación de pesos
    if abs(sum(weights) - 1.0) > 1e-6:
        raise ValueError(f"Los pesos deben sumar 1. Suma actual: {sum(weights)}")
    
    # Transformar error: f(error) = 1 / (1 + error) para que esté en (0,1]
    # Si error es muy grande, la contribución se aproxima a 0
    error_term = 1.0 / (1.0 + agi_error)
    
    # Asegurar rangos
    accuracy = np.clip(accuracy, 0.0, 1.0)
    mutual_info = np.clip(mutual_info, 0.0, 1.0)
    error_term = np.clip(error_term, 0.0, 1.0)
    
    icp = (weights[0] * accuracy +
           weights[1] * mutual_info +
           weights[2] * error_term)
    
    return float(np.clip(icp, 0.0, 1.0))


def icp_from_data(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    X_eeg: np.ndarray,
    expected_response: np.ndarray,
    actual_response: np.ndarray,
    weights: Tuple[float, float, float] = (0.4, 0.3, 0.3),
    mi_normalize: bool = True,
    error_metric: str = 'mse'
) -> float:
    """
    Calcula ICP directamente a partir de los datos crudos.

    Args:
        y_true: Etiquetas reales de intención
        y_pred: Etiquetas predichas por el clasificador
        X_eeg: Características EEG (n_samples, n_features)
        expected_response: Respuesta esperada por el humano
        actual_response: Respuesta generada por AGI
        weights: Pesos para cada componente
        mi_normalize: Si normalizar MI
        error_metric: Métrica para error AGI

    Returns:
        ICP value
    """
    acc = compute_accuracy(y_true, y_pred)
    
    n_classes = len(np.unique(y_true)) if mi_normalize else None
    mi = compute_mutual_information(X_eeg, y_true, n_classes=n_classes, normalize=mi_normalize)
    
    err = compute_agi_error(expected_response, actual_response, metric=error_metric)
    
    return compute_icp(acc, mi, err, weights)


# Versión vectorizada para múltiples trials/sesiones
def compute_icp_batch(
    accuracies: np.ndarray,
    mis: np.ndarray,
    errors: np.ndarray,
    weights: Tuple[float, float, float] = (0.4, 0.3, 0.3)
) -> np.ndarray:
    """
    Calcula ICP para múltiples observaciones.

    Args:
        accuracies: Array de accuracies
        mis: Array de MI normalizados
        errors: Array de errores AGI
        weights: Pesos

    Returns:
        Array de ICPs
    """
    error_terms = 1.0 / (1.0 + np.array(errors))
    icp = (weights[0] * np.clip(accuracies, 0, 1) +
           weights[1] * np.clip(mis, 0, 1) +
           weights[2] * np.clip(error_terms, 0, 1))
    return np.clip(icp, 0, 1)
