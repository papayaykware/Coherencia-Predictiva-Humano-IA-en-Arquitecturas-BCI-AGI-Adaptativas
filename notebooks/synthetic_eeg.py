"""
Synthetic EEG generator for motor imagery tasks.

This module simulates EEG signals with realistic noise (pink noise filtered
to the EEG band) and event-related desynchronization (ERD) patterns
typically observed during motor imagery. It generates labeled trials that
can be used for testing BCI pipelines or deep learning models.
"""

import numpy as np
from scipy import signal
from typing import Optional, Tuple, List


def _generate_pink_noise(n_samples: int, n_channels: int, rng: np.random.Generator) -> np.ndarray:
    """
    Generate pink noise (1/f spectrum) using the Voss-McCartney algorithm.

    Parameters
    ----------
    n_samples : int
        Number of samples per channel.
    n_channels : int
        Number of channels.
    rng : np.random.Generator
        Random number generator.

    Returns
    -------
    noise : np.ndarray, shape (n_channels, n_samples)
        Pink noise signals.
    """
    # Number of octaves (determines frequency range)
    n_octaves = 16
    # Generate white noise for each octave
    white = rng.normal(0, 1, (n_channels, n_samples, n_octaves))
    # Apply 1/f amplitude scaling and sum over octaves
    pink = np.sum(white / np.sqrt(2.0) ** np.arange(n_octaves), axis=-1)
    # Normalize to unit variance
    pink = pink / np.std(pink, axis=-1, keepdims=True)
    return pink


def _bandpass_filter(data: np.ndarray, sfreq: float, lowcut: float = 0.5, highcut: float = 40.0,
                     order: int = 4) -> np.ndarray:
    """
    Apply a Butterworth bandpass filter to the data.

    Parameters
    ----------
    data : np.ndarray, shape (n_channels, n_samples)
        Input signals.
    sfreq : float
        Sampling frequency in Hz.
    lowcut : float
        Lower cutoff frequency.
    highcut : float
        Upper cutoff frequency.
    order : int
        Filter order.

    Returns
    -------
    filtered : np.ndarray, shape (n_channels, n_samples)
        Filtered signals.
    """
    nyquist = 0.5 * sfreq
    low = lowcut / nyquist
    high = highcut / nyquist
    sos = signal.butter(order, [low, high], btype='band', output='sos')
    filtered = signal.sosfiltfilt(sos, data, axis=-1)
    return filtered


def _add_motor_imagery_event(trial: np.ndarray, sfreq: float, event_class: int,
                             channel_indices: List[int], event_duration: float = 1.0,
                             erd_strength: float = 0.5, rng: np.random.Generator) -> np.ndarray:
    """
    Add an event-related desynchronization (ERD) pattern to a trial.

    For motor imagery, the event is simulated by a transient decrease in mu (8-12 Hz)
    and beta (13-30 Hz) power over central channels. The event onset is placed at
    the center of the trial by default.

    Parameters
    ----------
    trial : np.ndarray, shape (n_channels, n_samples)
        Original trial (baseline + noise).
    sfreq : float
        Sampling frequency.
    event_class : int
        Class label (0 = left, 1 = right, etc.). Used to determine which channels
        are modulated (e.g., contralateral). For simplicity, we always modulate
        the provided channel indices.
    channel_indices : List[int]
        Indices of channels to which the event pattern is applied.
    event_duration : float
        Duration of the event in seconds.
    erd_strength : float
        Strength of the desynchronization (0 to 1). 0 means no change,
        1 means maximum suppression.
    rng : np.random.Generator
        Random number generator.

    Returns
    -------
    trial_mod : np.ndarray, shape (n_channels, n_samples)
        Trial with event added.
    """
    n_samples = trial.shape[1]
    center = n_samples // 2
    event_samples = int(event_duration * sfreq)
    onset = center - event_samples // 2
    offset = onset + event_samples

    # Ensure onset and offset are within bounds
    if onset < 0:
        onset = 0
        offset = event_samples
    if offset > n_samples:
        offset = n_samples
        onset = offset - event_samples

    # Create a temporal envelope (raised cosine) for smooth modulation
    t = np.linspace(0, np.pi, offset - onset)
    envelope = 0.5 * (1 - np.cos(t))  # shape: (event_samples,)
    # Scale by ERD strength: envelope goes from 0 to 1, then multiply by strength
    envelope = erd_strength * envelope

    # For each selected channel, we suppress power by multiplying the signal
    # with (1 - envelope). This simulates event-related desynchronization.
    for ch in channel_indices:
        trial[ch, onset:offset] *= (1 - envelope)

    return trial


def _add_eog_artifact(trial: np.ndarray, sfreq: float, artifact_channels: List[int],
                      probability: float = 0.3, rng: np.random.Generator) -> np.ndarray:
    """
    Add a blink-like artifact to specified channels.

    The artifact is a transient pulse (a Gaussian-shaped spike) that simulates
    an eye blink.

    Parameters
    ----------
    trial : np.ndarray, shape (n_channels, n_samples)
        Input trial.
    sfreq : float
        Sampling frequency.
    artifact_channels : List[int]
        Indices of channels where artifact is added (e.g., frontal channels).
    probability : float
        Probability of adding an artifact to each trial.
    rng : np.random.Generator
        Random number generator.

    Returns
    -------
    trial_art : np.ndarray, shape (n_channels, n_samples)
        Trial with optional artifact.
    """
    if rng.random() > probability:
        return trial

    n_samples = trial.shape[1]
    # Random onset (avoid edges)
    onset = rng.randint(int(0.2 * sfreq), int(0.8 * sfreq))
    duration = int(0.2 * sfreq)  # 200 ms blink
    t = np.linspace(-2, 2, duration)
    blink = np.exp(-t ** 2)  # Gaussian shape
    blink = blink / np.max(blink)  # normalize to 1
    amplitude = rng.uniform(50, 150)  # arbitrary amplitude in µV

    for ch in artifact_channels:
        if onset + duration <= n_samples:
            trial[ch, onset:onset + duration] += amplitude * blink

    return trial


def generate_synthetic_eeg(
    n_trials: int,
    n_channels: int,
    duration: float,
    sfreq: float,
    n_classes: int = 2,
    channel_indices_event: Optional[List[int]] = None,
    channel_indices_artifact: Optional[List[int]] = None,
    event_duration: float = 1.0,
    erd_strength: float = 0.5,
    artifact_probability: float = 0.3,
    random_state: Optional[int] = None
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic EEG trials with motor imagery events and realistic noise.

    Each trial consists of bandpass-filtered pink noise (0.5–40 Hz) simulating
    background EEG. A motor imagery event (ERD pattern) is added to the central
    channels for a random class. Optionally, blink artifacts can be added to
    frontal channels.

    Parameters
    ----------
    n_trials : int
        Number of trials to generate.
    n_channels : int
        Number of EEG channels.
    duration : float
        Trial duration in seconds.
    sfreq : float
        Sampling frequency in Hz.
    n_classes : int, default=2
        Number of motor imagery classes. Labels are drawn uniformly from
        0 to n_classes-1.
    channel_indices_event : List[int], optional
        Indices of channels (0-based) where the event is applied.
        Default: the first 3 channels (C3, Cz, C4-like).
    channel_indices_artifact : List[int], optional
        Indices of channels where blink artifacts may be added.
        Default: the last channel (e.g., Fpz-like).
    event_duration : float, default=1.0
        Duration of the motor imagery event in seconds.
    erd_strength : float, default=0.5
        Strength of the event-related desynchronization (0 to 1).
    artifact_probability : float, default=0.3
        Probability of adding a blink artifact to each trial.
    random_state : int, optional
        Seed for the random number generator.

    Returns
    -------
    X : np.ndarray, shape (n_trials, n_channels, n_samples)
        Synthetic EEG data.
    y : np.ndarray, shape (n_trials,)
        Class labels for each trial (0, 1, ..., n_classes-1).
    """
    # Set up random number generator
    rng = np.random.default_rng(random_state)

    n_samples = int(duration * sfreq)

    # Default channel groups if not provided
    if channel_indices_event is None:
        # Assume first 3 channels correspond to central region (C3, Cz, C4)
        channel_indices_event = list(range(min(3, n_channels)))
    if channel_indices_artifact is None:
        # Assume last channel is frontal (Fpz-like)
        channel_indices_artifact = [n_channels - 1] if n_channels > 0 else []

    X = np.zeros((n_trials, n_channels, n_samples))
    y = np.zeros(n_trials, dtype=int)

    for trial_idx in range(n_trials):
        # Generate pink noise for all channels
        noise = _generate_pink_noise(n_samples, n_channels, rng)
        # Bandpass filter to EEG range (0.5–40 Hz)
        eeg = _bandpass_filter(noise, sfreq)

        # Assign a random class label
        label = rng.integers(0, n_classes)
        y[trial_idx] = label

        # Add motor imagery event
        eeg = _add_motor_imagery_event(
            eeg, sfreq, label, channel_indices_event,
            event_duration=event_duration, erd_strength=erd_strength,
            rng=rng
        )

        # Optionally add blink artifact
        eeg = _add_eog_artifact(
            eeg, sfreq, channel_indices_artifact,
            probability=artifact_probability, rng=rng
        )

        X[trial_idx] = eeg

    return X, y


if __name__ == "__main__":
    # Example usage
    n_trials = 10
    n_channels = 8
    duration = 4.0  # seconds
    sfreq = 250.0   # Hz

    X, y = generate_synthetic_eeg(
        n_trials=n_trials,
        n_channels=n_channels,
        duration=duration,
        sfreq=sfreq,
        n_classes=2,
        random_state=42
    )

    print(f"Generated {X.shape[0]} trials, each with {X.shape[1]} channels and {X.shape[2]} samples.")
    print(f"Class labels: {y}")
