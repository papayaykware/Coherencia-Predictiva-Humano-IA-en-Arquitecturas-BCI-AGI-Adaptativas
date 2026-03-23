"""
Tests for the EEG processing module.
"""

import numpy as np
import pytest
from src.utils import eeg_processor  # adjust import according to your package structure


def test_bandpass_filter_2d():
    """Test bandpass filtering on a 2D array."""
    sfreq = 250.0
    duration = 2.0
    n_ch = 4
    n_times = int(duration * sfreq)
    # Create synthetic signal: white noise
    np.random.seed(42)
    data = np.random.randn(n_ch, n_times)

    # Apply bandpass filter (1-30 Hz)
    filtered = eeg_processor.bandpass_filter(data, sfreq, 1.0, 30.0)
    assert filtered.shape == (n_ch, n_times)
    # Check that filtering did not change dimensions
    assert not np.allclose(filtered, data)  # should have changed


def test_bandpass_filter_3d():
    """Test bandpass filtering on a 3D array (multiple epochs)."""
    n_epochs = 5
    n_ch = 4
    n_times = 500
    sfreq = 250.0
    np.random.seed(42)
    data = np.random.randn(n_epochs, n_ch, n_times)

    filtered = eeg_processor.bandpass_filter(data, sfreq, 1.0, 30.0)
    assert filtered.shape == (n_epochs, n_ch, n_times)
    # Check that each epoch is different
    for i in range(n_epochs):
        assert not np.allclose(filtered[i], data[i])


def test_bandpass_filter_with_picks():
    """Test filtering with selected channels."""
    sfreq = 250.0
    n_ch = 4
    n_times = 500
    data = np.random.randn(n_ch, n_times)
    picks = [0, 2]  # filter only these channels

    filtered = eeg_processor.bandpass_filter(data, sfreq, 1.0, 30.0, picks=picks)
    # Check that filtered channels are modified
    for ch in picks:
        assert not np.allclose(filtered[ch], data[ch])
    # Check that other channels remain unchanged (since picks=None)
    other = [1, 3]
    for ch in other:
        assert np.allclose(filtered[ch], data[ch])


def test_extract_band_power_2d():
    """Test band power extraction from a single epoch."""
    sfreq = 250.0
    duration = 2.0
    n_ch = 4
    n_times = int(duration * sfreq)
    # Create synthetic data with known power in certain bands? Use random.
    data = np.random.randn(n_ch, n_times)

    # Extract band powers with default bands, average over channels
    features = eeg_processor.extract_band_power(data, sfreq, average=True)
    assert features.shape == (len(eeg_processor.BANDS),)  # (n_bands,)
    assert features.dtype == np.float64

    # Extract without averaging (per-channel)
    features_per_ch = eeg_processor.extract_band_power(data, sfreq, average=False)
    assert features_per_ch.shape == (len(eeg_processor.BANDS), n_ch)


def test_extract_band_power_3d():
    """Test band power extraction from multiple epochs."""
    n_epochs = 5
    n_ch = 4
    n_times = 500
    sfreq = 250.0
    data = np.random.randn(n_epochs, n_ch, n_times)

    features_avg = eeg_processor.extract_band_power(data, sfreq, average=True)
    assert features_avg.shape == (n_epochs, len(eeg_processor.BANDS))

    features_per_ch = eeg_processor.extract_band_power(data, sfreq, average=False)
    assert features_per_ch.shape == (n_epochs, len(eeg_processor.BANDS), n_ch)


def test_extract_band_power_custom_bands():
    """Test extraction with custom frequency bands."""
    data = np.random.randn(4, 500)
    sfreq = 250.0
    custom_bands = {'mu': (8, 12), 'beta': (13, 30)}
    features = eeg_processor.extract_band_power(data, sfreq, bands=custom_bands, average=True)
    assert features.shape == (2,)  # two bands


def test_extract_band_power_with_picks():
    """Test band power extraction on selected channels."""
    n_epochs = 3
    n_ch = 5
    n_times = 500
    sfreq = 250.0
    data = np.random.randn(n_epochs, n_ch, n_times)
    picks = [0, 2, 4]
    features = eeg_processor.extract_band_power(data, sfreq, picks=picks, average=True)
    assert features.shape == (n_epochs, len(eeg_processor.BANDS))
    # For per-channel, we should get n_bands × len(picks)
    features_per_ch = eeg_processor.extract_band_power(data, sfreq, picks=picks, average=False)
    assert features_per_ch.shape == (n_epochs, len(eeg_processor.BANDS), len(picks))
