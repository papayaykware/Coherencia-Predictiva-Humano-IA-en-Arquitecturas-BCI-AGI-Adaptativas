#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Módulo para el modelo EEGNet: definición, entrenamiento, validación y carga de pesos.

EEGNet es una arquitectura convolucional compacta para clasificación de EEG,
propuesta por Lawhern et al. (2018): https://doi.org/10.1088/1741-2552/aace8c

Este módulo proporciona:
- Modelo EEGNet con parámetros configurables.
- Funciones de entrenamiento y validación con Keras.
- Guardado y carga de pesos preentrenados.
- Integración con datos cargados desde src.data.load_physionet.
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models, backend as K
from tensorflow.keras.callbacks import (
    EarlyStopping, ReduceLROnPlateau, ModelCheckpoint, CSVLogger
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import mne

# Para importar la función de carga de datos del módulo anterior
# Se asume que el módulo load_physionet está en src.data
from src.data.load_physionet import load_physionet


def build_eegnet(
    n_channels,
    n_samples,
    n_classes=2,
    dropout_rate=0.5,
    kern_length=64,
    F1=8,
    D=2,
    F2=16,
    norm_rate=0.25,
    activation='elu',
    include_top=True,
    verbose=False
):
    """
    Construye el modelo EEGNet según la arquitectura original.

    Parámetros
    ----------
    n_channels : int
        Número de canales EEG.
    n_samples : int
        Número de puntos temporales por muestra (epoch).
    n_classes : int, default=2
        Número de clases (para clasificación binaria o multiclase).
    dropout_rate : float, default=0.5
        Dropout después de las capas densas.
    kern_length : int, default=64
        Longitud del kernel en la convolución temporal.
    F1 : int, default=8
        Número de filtros temporales.
    D : int, default=2
        Profundidad de la convolución por profundidad (depthwise).
    F2 : int, default=16
        Número de filtros pointwise (separables).
    norm_rate : float, default=0.25
        Tasa de normalización para los batch normalization (momentum = 1 - norm_rate).
    activation : str, default='elu'
        Función de activación.
    include_top : bool, default=True
        Si es False, no incluye la capa final de clasificación (útil para extraer características).
    verbose : bool, default=False
        Si imprime resumen del modelo.

    Retorna
    -------
    model : tf.keras.Model
        Modelo EEGNet compilado (si include_top=True, con softmax; si no, sin capa final).
    """
    # Entrada
    input_layer = layers.Input(shape=(n_channels, n_samples, 1), name='input')

    # Bloque 1: convolución temporal + profundidad
    # Capa 1: convolución temporal (sobre el eje tiempo)
    block1 = layers.Conv2D(
        F1,
        (1, kern_length),
        padding='same',
        use_bias=False,
        name='conv2d_temporal'
    )(input_layer)
    block1 = layers.BatchNormalization(momentum=norm_rate, name='bn_temporal')(block1)
    block1 = layers.Activation(activation, name='act_temporal')(block1)

    # Capa 2: convolución por profundidad (depthwise) sobre canales
    block1 = layers.DepthwiseConv2D(
        (n_channels, 1),
        depth_multiplier=D,
        use_bias=False,
        depthwise_constraint=None,
        name='depthwise_conv'
    )(block1)
    block1 = layers.BatchNormalization(momentum=norm_rate, name='bn_depthwise')(block1)
    block1 = layers.Activation(activation, name='act_depthwise')(block1)
    block1 = layers.AveragePooling2D((1, 4), name='avg_pool_depthwise')(block1)
    block1 = layers.Dropout(dropout_rate, name='dropout_depthwise')(block1)

    # Bloque 2: convolución separable
    # Capa 3: convolución separable (pointwise)
    block2 = layers.SeparableConv2D(
        F2,
        (1, 16),
        use_bias=False,
        padding='same',
        name='separable_conv'
    )(block1)
    block2 = layers.BatchNormalization(momentum=norm_rate, name='bn_separable')(block2)
    block2 = layers.Activation(activation, name='act_separable')(block2)
    block2 = layers.AveragePooling2D((1, 8), name='avg_pool_separable')(block2)
    block2 = layers.Dropout(dropout_rate, name='dropout_separable')(block2)

    # Aplanar y capa densa final
    flatten = layers.Flatten(name='flatten')(block2)

    if include_top:
        # Capa densa con softmax para clasificación
        dense = layers.Dense(n_classes, name='dense', activation='softmax')(flatten)
        model = models.Model(inputs=input_layer, outputs=dense, name='eegnet')
    else:
        model = models.Model(inputs=input_layer, outputs=flatten, name='eegnet_feature')

    if verbose:
        model.summary()

    return model


def compile_model(model, learning_rate=0.001):
    """
    Compila el modelo con el optimizador Adam y pérdida categórica.

    Parámetros
    ----------
    model : tf.keras.Model
        Modelo EEGNet (sin compilar).
    learning_rate : float, default=0.001
        Tasa de aprendizaje inicial.

    Retorna
    -------
    model : tf.keras.Model
        Modelo compilado.
    """
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(
        optimizer=optimizer,
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model


def prepare_data_from_epochs(
    epochs,
    n_classes=2,
    test_size=0.2,
    random_state=42,
    shuffle=True
):
    """
    Convierte objetos mne.Epochs en arrays de numpy listos para entrenamiento.

    Parámetros
    ----------
    epochs : mne.Epochs
        Epochs con datos EEG (debe contener eventos y etiquetas).
    n_classes : int, default=2
        Número de clases (para codificar one-hot).
    test_size : float, default=0.2
        Proporción para conjunto de prueba.
    random_state : int, default=42
        Semilla aleatoria.
    shuffle : bool, default=True
        Si se mezclan los datos antes de dividir.

    Retorna
    -------
    X_train, X_test, y_train, y_test : tuple
        Conjuntos de datos de entrenamiento y prueba.
        X es (n_samples, n_channels, n_times) y se expande a (..., 1) para CNN.
        y es one-hot encoded.
    """
    # Obtener datos y etiquetas
    X = epochs.get_data()  # shape: (n_epochs, n_channels, n_times)
    y = epochs.events[:, -1]  # última columna son los códigos de evento (enteros)

    # Codificar etiquetas a one-hot
    y_onehot = tf.keras.utils.to_categorical(y - 1, num_classes=n_classes)  # restamos 1 si eventos empiezan en 1

    # Dividir en train/test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_onehot, test_size=test_size, random_state=random_state, shuffle=shuffle, stratify=y
    )

    # Expandir dimensión de canal para convolución 2D (canales, tiempo, 1)
    X_train = X_train[..., np.newaxis]
    X_test = X_test[..., np.newaxis]

    return X_train, X_test, y_train, y_test


def train_eegnet(
    X_train,
    y_train,
    X_val=None,
    y_val=None,
    n_channels=None,
    n_samples=None,
    n_classes=2,
    model=None,
    batch_size=64,
    epochs=200,
    learning_rate=0.001,
    callbacks=None,
    verbose=1,
    model_save_path=None
):
    """
    Entrena un modelo EEGNet con los datos proporcionados.

    Parámetros
    ----------
    X_train : np.ndarray
        Datos de entrenamiento con forma (n_samples, n_channels, n_times, 1).
    y_train : np.ndarray
        Etiquetas one-hot de entrenamiento.
    X_val : np.ndarray, opcional
        Datos de validación. Si se proporciona, se usa como conjunto de validación.
    y_val : np.ndarray, opcional
        Etiquetas one-hot de validación.
    n_channels : int, opcional
        Número de canales (si no se pasa, se infiere de X_train).
    n_samples : int, opcional
        Número de puntos temporales (si no se pasa, se infiere de X_train).
    n_classes : int, default=2
        Número de clases.
    model : tf.keras.Model, opcional
        Modelo predefinido; si es None, se construye uno nuevo.
    batch_size : int, default=64
        Tamaño del lote.
    epochs : int, default=200
        Número máximo de épocas.
    learning_rate : float, default=0.001
        Tasa de aprendizaje.
    callbacks : list, opcional
        Lista de callbacks de Keras. Si es None, se usan los por defecto.
    verbose : int, default=1
        Nivel de verbosidad (0=sin salida, 1=progreso, 2=una línea por época).
    model_save_path : str, opcional
        Ruta donde guardar el mejor modelo (pesos y arquitectura). Si se proporciona,
        se añade un ModelCheckpoint para guardar el mejor según val_loss.

    Retorna
    -------
    history : tf.keras.callbacks.History
        Historial de entrenamiento.
    model : tf.keras.Model
        Modelo entrenado.
    """
    # Inferir dimensiones si no se dan
    if n_channels is None:
        n_channels = X_train.shape[1]
    if n_samples is None:
        n_samples = X_train.shape[2]

    # Construir modelo si no se proporciona
    if model is None:
        model = build_eegnet(n_channels, n_samples, n_classes=n_classes, verbose=verbose > 0)
        model = compile_model(model, learning_rate=learning_rate)

    # Callbacks por defecto
    if callbacks is None:
        callbacks = []
        # Early stopping
        callbacks.append(EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True, verbose=verbose))
        # Reducción de LR
        callbacks.append(ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, min_lr=1e-6, verbose=verbose))

    # Si se especifica ruta de guardado, añadir ModelCheckpoint
    if model_save_path is not None:
        os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
        checkpoint = ModelCheckpoint(
            model_save_path,
            monitor='val_loss',
            save_best_only=True,
            save_weights_only=False,
            verbose=verbose
        )
        callbacks.append(checkpoint)

    # Configurar validación
    validation_data = (X_val, y_val) if X_val is not None else None

    # Entrenar
    history = model.fit(
        X_train, y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_data=validation_data,
        callbacks=callbacks,
        verbose=verbose
    )

    return history, model


def load_pretrained_weights(model, weights_path, by_name=False):
    """
    Carga pesos preentrenados en un modelo.

    Parámetros
    ----------
    model : tf.keras.Model
        Modelo al que se le cargarán los pesos.
    weights_path : str
        Ruta del archivo de pesos (.h5 o .keras).
    by_name : bool, default=False
        Si True, carga pesos por nombre de capa (útil si la arquitectura no coincide exactamente).

    Retorna
    -------
    model : tf.keras.Model
        Modelo con los pesos cargados.
    """
    model.load_weights(weights_path, by_name=by_name)
    print(f"Pesos cargados desde {weights_path}")
    return model


def run_training_pipeline(
    subject_id=1,
    runs=None,
    n_classes=2,
    test_size=0.2,
    batch_size=64,
    epochs=200,
    model_save_path='models/eegnet_weights.h5',
    preprocess_params=None,
    verbose=1
):
    """
    Función completa que carga datos, prepara, entrena y guarda el modelo.

    Parámetros
    ----------
    subject_id : int, default=1
        ID del sujeto a usar para entrenamiento (se puede extender para múltiples).
    runs : list, opcional
        Runs a cargar; por defecto los de imaginería motora izquierda/derecha.
    n_classes : int, default=2
        Número de clases (2 para izquierda/derecha).
    test_size : float, default=0.2
        Proporción de datos para prueba.
    batch_size : int, default=64
        Tamaño del lote.
    epochs : int, default=200
        Número máximo de épocas.
    model_save_path : str, default='models/eegnet_weights.h5'
        Ruta donde guardar el modelo entrenado.
    preprocess_params : dict, opcional
        Parámetros para la carga de datos (filtros, etc.).
    verbose : int, default=1
        Nivel de verbosidad.

    Retorna
    -------
    model : tf.keras.Model
        Modelo entrenado.
    history : tf.keras.callbacks.History
        Historial de entrenamiento.
    """
    # Parámetros por defecto para preprocesamiento
    if preprocess_params is None:
        preprocess_params = {
            'l_freq': 8.0,
            'h_freq': 30.0,
            'notch_freq': 50.0,
            'resample_sfreq': 100.0,
            'tmin': -1.0,
            'tmax': 4.0,
            'baseline': (None, 0),
            'reject': None,
            'return_raw': False
        }

    # Cargar epochs para el sujeto
    print(f"Cargando datos del sujeto {subject_id}...")
    epochs = load_physionet(
        subjects=subject_id,
        runs=runs,
        **preprocess_params,
        verbose=verbose > 0
    )

    # Verificar que tenemos los eventos esperados
    if n_classes == 2:
        # Por defecto, se usan T1 y T2. Verificar que existan.
        event_ids = epochs.event_id
        if set(event_ids.keys()) != {'T1', 'T2'}:
            print("Advertencia: los eventos no son solo T1 y T2. Se tomarán los primeros n_classes.")
            # Si hay más eventos, seleccionar los primeros n_classes
            # Pero normalmente load_physionet ya filtra por event_id en extract_epochs.
            # Asegurar que solo se tienen dos clases.
            epochs = epochs[['T1', 'T2']]

    # Preparar datos
    print("Preparando datos para entrenamiento...")
    X_train, X_test, y_train, y_test = prepare_data_from_epochs(
        epochs,
        n_classes=n_classes,
        test_size=test_size,
        random_state=42,
        shuffle=True
    )

    # Dimensiones
    n_channels = X_train.shape[1]
    n_samples = X_train.shape[2]

    print(f"Dimensiones: {n_channels} canales, {n_samples} muestras, {X_train.shape[0]} epochs de entrenamiento, {X_test.shape[0]} de prueba.")

    # Construir y compilar modelo
    model = build_eegnet(n_channels, n_samples, n_classes=n_classes, verbose=verbose > 0)
    model = compile_model(model, learning_rate=0.001)

    # Entrenar
    history, model = train_eegnet(
        X_train, y_train,
        X_val=X_test, y_val=y_test,
        model=model,
        batch_size=batch_size,
        epochs=epochs,
        learning_rate=0.001,
        verbose=verbose,
        model_save_path=model_save_path
    )

    print(f"Entrenamiento completado. Mejor modelo guardado en {model_save_path}")

    # Evaluar en test
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    print(f"Precisión en conjunto de prueba: {test_acc:.4f}")

    return model, history


if __name__ == "__main__":
    # Ejemplo de uso: entrenar un EEGNet con datos del sujeto 1
    model, history = run_training_pipeline(
        subject_id=1,
        runs=[3, 4, 7, 8, 11, 12],  # runs estándar para izquierda/derecha
        n_classes=2,
        test_size=0.2,
        batch_size=32,
        epochs=100,
        model_save_path='models/eegnet_subject1.h5',
        verbose=1
    )
