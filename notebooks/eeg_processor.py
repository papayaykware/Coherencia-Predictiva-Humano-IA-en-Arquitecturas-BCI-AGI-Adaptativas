"""
EEG processing utilities: filtering, band power extraction, etc.

This module provides functions for common EEG preprocessing steps using MNE-Python,
including bandpass filtering and extraction of band power features from epochs.
"""

import numpy as np
from typing import Optional, List, Tuple, Union
import mne

# Define standard frequency bands (in Hz)
BANDS = {
    'delta': (0.5, 4),
    'theta': (4, 8),
    'alpha': (8, 13),
    'beta': (13, 30),
    'gamma': (30, 45),
}


def bandpass_filter(
    data: np.ndarray,
    sfreq: float,
    l_freq: float,
    h_freq: float,
    picks: Optional[Union[List[int], slice]] = None,
    verbose: bool = False
) -> np.ndarray:
    """
    Apply a zero-phase bandpass filter to EEG data using MNE.

    Parameters
    ----------
    data : np.ndarray, shape (n_channels, n_times) or (n_trials, n_channels, n_times)
        Input EEG data. If 3D, filtering is applied independently per trial.
    sfreq : float
        Sampling frequency in Hz.
    l_freq : float
        Lower bound of the bandpass filter (Hz). Use None for low-pass only.
    h_freq : float
        Upper bound of the bandpass filter (Hz). Use None for high-pass only.
    picks : list or slice, optional
        Indices of channels to filter. If None, all channels are filtered.
    verbose : bool, default=False
        Whether to print filter information.

    Returns
    -------
    filtered : np.ndarray
        Filtered data with same shape as input.
    """
    if data.ndim == 2:
        # Single trial: shape (n_channels, n_times)
        return _filter_2d(data, sfreq, l_freq, h_freq, picks, verbose)
    elif data.ndim == 3:
        # Multiple trials: shape (n_trials, n_channels, n_times)
        filtered_trials = []
        for i in range(data.shape[0]):
            filtered = _filter_2d(data[i], sfreq, l_freq, h_freq, picks, verbose)
            filtered_trials.append(filtered)
        return np.array(filtered_trials)
    else:
        raise ValueError("Data must be 2D (channels × times) or 3D (trials × channels × times)")


def _filter_2d(
    data: np.ndarray,
    sfreq: float,
    l_freq: float,
    h_freq: float,
    picks: Optional[Union[List[int], slice]] = None,
    verbose: bool = False
) -> np.ndarray:
    """
    Helper to filter a single 2D array (channels × times).
    """
    n_ch, n_times = data.shape
    if picks is not None:
        # Filter only selected channels, then copy back
        ch_indices = np.arange(n_ch)[picks] if isinstance(picks, slice) else picks
        data_sub = data[ch_indices, :]
        # Create Info object with channel names for filtering
        ch_names = [f'EEG{i:03d}' for i in range(len(ch_indices))]
        info = mne.create_info(ch_names, sfreq, ch_types='eeg')
        raw = mne.io.RawArray(data_sub, info, verbose=verbose)
        # Apply filter
        raw.filter(l_freq, h_freq, fir_design='firwin', verbose=verbose)
        filtered_sub = raw.get_data()
        # Copy back
        data_filtered = data.copy()
        data_filtered[ch_indices, :] = filtered_sub
        return data_filtered
    else:
        # Filter all channels
        ch_names = [f'EEG{i:03d}' for i in range(n_ch)]
        info = mne.create_info(ch_names, sfreq, ch_types='eeg')
        raw = mne.io.RawArray(data, info, verbose=verbose)
        raw.filter(l_freq, h_freq, fir_design='firwin', verbose=verbose)
        return raw.get_data()


def extract_band_power(
    data: np.ndarray,
    sfreq: float,
    bands: Optional[dict] = None,
    method: str = 'welch',
    window_duration: float = 1.0,
    overlap: float = 0.5,
    picks: Optional[Union[List[int], slice]] = None,
    average: bool = True
) -> np.ndarray:
    """
    Extract band power features from EEG epochs.

    Parameters
    ----------
    data : np.ndarray, shape (n_epochs, n_channels, n_times) or (n_channels, n_times)
        Input EEG data. If 2D, treated as a single epoch.
    sfreq : float
        Sampling frequency in Hz.
    bands : dict, optional
        Dictionary mapping band names to (low, high) frequency tuples.
        Default: BANDS (delta, theta, alpha, beta, gamma).
    method : str, default='welch'
        Method to compute power spectral density. Currently only 'welch' is supported.
    window_duration : float, default=1.0
        Length of Welch windows in seconds.
    overlap : float, default=0.5
        Overlap between windows (fraction of window length).
    picks : list or slice, optional
        Indices of channels to include. If None, all channels are used.
    average : bool, default=True
        If True, average power across channels; if False, return per-channel power.

    Returns
    -------
    features : np.ndarray
        If input is 2D (single epoch): shape (n_bands, n_channels) if average=False,
        else (n_bands,).
        If input is 3D: shape (n_epochs, n_bands, n_channels) if average=False,
        else (n_epochs, n_bands).
    """
    if bands is None:
        bands = BANDS

    # Ensure data is at least 2D
    if data.ndim == 2:
        data = data[np.newaxis, ...]  # add epoch dimension
    n_epochs, n_ch, n_times = data.shape

    if picks is not None:
        # Select subset of channels
        ch_indices = np.arange(n_ch)[picks] if isinstance(picks, slice) else picks
        data = data[:, ch_indices, :]
        n_ch = len(ch_indices)

    # Compute PSD for each epoch using Welch method
    # Convert window duration to samples
    nperseg = int(window_duration * sfreq)
    noverlap = int(overlap * nperseg)

    features = []
    for epoch in data:
        # epoch shape: (n_ch, n_times)
        freqs, psd = mne.time_frequency.psd_array_welch(
            epoch, sfreq, n_fft=None, n_per_seg=nperseg, n_overlap=noverlap,
            verbose=False
        )
        # psd shape: (n_ch, n_freqs)
        # For each band, compute average power over frequency range
        band_powers = []
        for band_name, (l_freq, h_freq) in bands.items():
            # Find indices within band
            idx = np.where((freqs >= l_freq) & (freqs <= h_freq))[0]
            if len(idx) == 0:
                # Band not represented in freqs
                band_power = np.zeros(n_ch)
            else:
                band_power = np.mean(psd[:, idx], axis=1)
            band_powers.append(band_power)
        # band_powers: list of arrays, each of length n_ch
        features.append(np.array(band_powers))  # shape (n_bands, n_ch)
    features = np.array(features)  # shape (n_epochs, n_bands, n_ch)

    if average:
        # Average across channels
        features = np.mean(features, axis=-1)  # shape (n_epochs, n_bands)

    # If input was 2D, remove the epoch dimension
    if features.shape[0] == 1 and data.ndim == 2:  # original input was 2D
        features = features.squeeze(0)

    return features
