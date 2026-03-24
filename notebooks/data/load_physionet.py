#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module to load and preprocess the PhysioNet Motor Imagery dataset.

This module provides functions to automatically download the EEG Motor Movement/
Imagery Dataset (eegmmidb) from PhysioNet, load it with MNE, and apply standard
preprocessing steps (filtering, epoching, baseline correction, resampling).

The dataset contains 109 subjects, each with 14 runs. Typically, runs 3,4,7,8,11,12
are used for left/right motor imagery classification.
"""

import os
import warnings
import numpy as np
import mne
from mne.datasets import eegbci
from mne.io import concatenate_raws, read_raw_edf
from mne.epochs import Epochs


def download_physionet_data(
    subjects=None,
    runs=None,
    path=None,
    verbose=False,
):
    """
    Download the PhysioNet Motor Imagery dataset for given subjects and runs.

    Parameters
    ----------
    subjects : list of int, optional
        List of subject IDs (1 to 109). If None, all subjects are downloaded.
    runs : list of int, optional
        List of run numbers (1 to 14). If None, all runs are downloaded.
    path : str | None
        Directory where the data will be stored. If None, uses MNE's default path
        (~/mne_data).
    verbose : bool, default False
        Whether to print progress information.

    Returns
    -------
    list of str
        List of paths to the downloaded EDF files.
    """
    if subjects is None:
        subjects = list(range(1, 110))  # subjects 1..109
    if runs is None:
        runs = list(range(1, 15))       # runs 1..14

    # Use mne.datasets.eegbci.load_data to download files
    # This function returns a list of lists: one list per subject, each containing file paths.
    files = eegbci.load_data(subjects, runs, path=path, verbose=verbose)

    # Flatten the list of lists
    return [f for sub_files in files for f in sub_files]


def load_raw(
    subject,
    runs,
    path=None,
    verbose=False,
):
    """
    Load raw EEG data for a single subject and concatenate the selected runs.

    Parameters
    ----------
    subject : int
        Subject ID (1..109).
    runs : list of int
        List of run numbers to load.
    path : str | None
        Directory where the data is stored. If None, uses MNE's default path.
    verbose : bool, default False
        Whether to print progress information.

    Returns
    -------
    raw : mne.io.Raw
        Concatenated raw data object.
    """
    # Get the file paths for the given subject and runs
    files = eegbci.load_data(subject, runs, path=path, verbose=verbose)

    # Read each EDF file
    raws = []
    for f in files:
        raw = read_raw_edf(f, preload=True, verbose=verbose)
        raws.append(raw)

    # Concatenate all runs for this subject
    if len(raws) == 1:
        raw = raws[0]
    else:
        raw = concatenate_raws(raws, verbose=verbose)

    # Set the channel names to standard EEG 10-20 system (from dataset)
    # The dataset has 64 channels, but some are EOG and other non-EEG.
    # MNE's mapping can be used to keep only EEG channels if desired.
    # For now, keep all channels but standardize names.
    # The dataset already has channel names; we can just set the montage.
    montage = mne.channels.make_standard_montage('standard_1020')
    raw.set_montage(montage, match_case=False, verbose=verbose)

    # Add the standard event annotations (the EDF files contain annotations)
    # The events are already in raw.annotations. We'll extract them later.

    return raw


def preprocess_raw(
    raw,
    l_freq=8.0,
    h_freq=30.0,
    notch_freq=50.0,
    resample_sfreq=100.0,
    pick_channels=None,
    verbose=False,
):
    """
    Apply standard preprocessing to raw data.

    Steps:
        1. Apply bandpass filter (l_freq, h_freq).
        2. Optionally apply notch filter (notch_freq) if not None.
        3. Resample to resample_sfreq (if not None).
        4. Optionally pick only specified channels (e.g., EEG channels).

    Parameters
    ----------
    raw : mne.io.Raw
        Raw data to preprocess.
    l_freq : float, default 8.0
        Low cutoff frequency for bandpass filter (Hz). None means no lower bound.
    h_freq : float, default 30.0
        High cutoff frequency for bandpass filter (Hz). None means no upper bound.
    notch_freq : float | None, default 50.0
        Frequency for notch filter (Hz). If None, no notch filter is applied.
    resample_sfreq : float | None, default 100.0
        Target sampling frequency after resampling. If None, no resampling.
    pick_channels : list of str | None, default None
        List of channel names to keep. If None, keep all channels.
    verbose : bool, default False
        Whether to print progress information.

    Returns
    -------
    raw : mne.io.Raw
        Preprocessed raw data.
    """
    # Copy to avoid modifying original
    raw = raw.copy()

    # Apply notch filter (often needed for powerline noise)
    if notch_freq is not None:
        raw.notch_filter(notch_freq, verbose=verbose)

    # Apply bandpass filter
    if l_freq is not None or h_freq is not None:
        raw.filter(l_freq, h_freq, verbose=verbose)

    # Resample
    if resample_sfreq is not None:
        raw.resample(resample_sfreq, verbose=verbose)

    # Pick only desired channels
    if pick_channels is not None:
        raw.pick_channels(pick_channels, verbose=verbose)

    return raw


def extract_epochs(
    raw,
    event_id=None,
    tmin=-1.0,
    tmax=4.0,
    baseline=(None, 0),
    reject=None,
    verbose=False,
):
    """
    Extract epochs from raw data based on annotations.

    The dataset's annotations are encoded as strings: 'T0' (rest), 'T1' (left fist),
    'T2' (right fist), etc. By default, we keep only T1 and T2 for motor imagery.

    Parameters
    ----------
    raw : mne.io.Raw
        Raw data with annotations.
    event_id : dict | None, default None
        Mapping from event name to integer. If None, default is {'T1': 1, 'T2': 2}.
    tmin : float, default -1.0
        Start time (seconds) relative to event onset.
    tmax : float, default 4.0
        End time (seconds) relative to event onset.
    baseline : tuple | None, default (None, 0)
        Baseline correction interval. If None, no baseline correction.
        If tuple (start, end), baseline is subtracted. (None, 0) means from start to 0.
    reject : dict | None, default None
        Rejection criteria based on peak-to-peak amplitude. Example: {'eeg': 150e-6}
        for 150 µV peak-to-peak. If None, no rejection.
    verbose : bool, default False
        Whether to print progress information.

    Returns
    -------
    epochs : mne.Epochs
        Epochs object.
    """
    if event_id is None:
        event_id = {'T1': 1, 'T2': 2}   # left and right motor imagery

    # Find events from annotations
    events, event_dict = mne.events_from_annotations(raw, event_id=event_id, verbose=verbose)

    # Create epochs
    epochs = Epochs(
        raw,
        events,
        event_id,
        tmin,
        tmax,
        baseline=baseline,
        reject=reject,
        preload=True,
        verbose=verbose,
    )

    return epochs


def load_physionet(
    subjects=None,
    runs=None,
    path=None,
    l_freq=8.0,
    h_freq=30.0,
    notch_freq=50.0,
    resample_sfreq=100.0,
    pick_channels=None,
    tmin=-1.0,
    tmax=4.0,
    baseline=(None, 0),
    reject=None,
    event_id=None,
    return_raw=False,
    verbose=False,
):
    """
    Load and preprocess the PhysioNet Motor Imagery dataset in one call.

    This function downloads the data if not already present, loads it, applies
    standard preprocessing, and extracts epochs.

    Parameters
    ----------
    subjects : list of int | int, optional
        Subject ID(s) to load. If None, all subjects (1..109) are loaded.
        If int, loads a single subject.
    runs : list of int, optional
        Run numbers to load. If None, default is [3,4,7,8,11,12] (left/right imagery).
    path : str | None
        Directory where the data is stored. If None, uses MNE's default path.
    l_freq : float, default 8.0
        Low cutoff for bandpass filter (Hz).
    h_freq : float, default 30.0
        High cutoff for bandpass filter (Hz).
    notch_freq : float | None, default 50.0
        Notch filter frequency (Hz). Set to None to skip.
    resample_sfreq : float | None, default 100.0
        Target sampling frequency. Set to None to keep original (160 Hz).
    pick_channels : list of str | None, default None
        Channels to keep. If None, keep all. Common choice: eegbci.standard_1020_channels.
    tmin : float, default -1.0
        Epoch start time (s) relative to event.
    tmax : float, default 4.0
        Epoch end time (s) relative to event.
    baseline : tuple | None, default (None, 0)
        Baseline correction interval. None means no correction.
    reject : dict | None, default None
        Epoch rejection criteria. Example: {'eeg': 150e-6}.
    event_id : dict | None, default None
        Mapping of event names to integer codes. If None, uses {'T1':1, 'T2':2}.
    return_raw : bool, default False
        If True, return the raw data (after preprocessing) instead of epochs.
    verbose : bool, default False
        Whether to print progress information.

    Returns
    -------
    data : mne.Epochs | mne.io.Raw | list of mne.Epochs | list of mne.io.Raw
        Depending on `return_raw` and whether multiple subjects are loaded:
        - Single subject, return_raw=False: Epochs object
        - Single subject, return_raw=True: Raw object
        - Multiple subjects, return_raw=False: list of Epochs
        - Multiple subjects, return_raw=True: list of Raw
    """
    # Default runs: left/right motor imagery runs (T1 and T2)
    if runs is None:
        runs = [3, 4, 7, 8, 11, 12]

    # Normalize subjects input to a list
    if subjects is None:
        subjects = list(range(1, 110))
    elif isinstance(subjects, int):
        subjects = [subjects]

    # Predefined channel selection (optional)
    if pick_channels is None:
        # Use all channels (including EOG and other non-EEG)
        pick_channels = None
    else:
        # Ensure it's a list
        if not isinstance(pick_channels, list):
            pick_channels = [pick_channels]

    data_list = []

    for subj in subjects:
        # Load raw
        raw = load_raw(subj, runs, path=path, verbose=verbose)

        # Preprocess
        raw = preprocess_raw(
            raw,
            l_freq=l_freq,
            h_freq=h_freq,
            notch_freq=notch_freq,
            resample_sfreq=resample_sfreq,
            pick_channels=pick_channels,
            verbose=verbose,
        )

        if return_raw:
            data_list.append(raw)
        else:
            # Extract epochs
            epochs = extract_epochs(
                raw,
                event_id=event_id,
                tmin=tmin,
                tmax=tmax,
                baseline=baseline,
                reject=reject,
                verbose=verbose,
            )
            data_list.append(epochs)

    # Return appropriately
    if len(data_list) == 1:
        return data_list[0]
    else:
        return data_list


# Example usage (commented out)
if __name__ == "__main__":
    # Example: Load subject 1, runs 3,4,7,8,11,12, apply standard preprocessing,
    # and return epochs for left/right imagery.
    # epochs = load_physionet(subjects=1, verbose=True)

    # Example: Load subjects 1-3, return raw data (without epoching)
    # raws = load_physionet(subjects=[1,2,3], runs=[3,4], return_raw=True, verbose=True)
    pass
