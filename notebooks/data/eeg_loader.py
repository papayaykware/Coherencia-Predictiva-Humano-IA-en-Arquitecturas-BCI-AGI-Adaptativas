import mne

def load_eeg(file):
    raw = mne.io.read_raw_edf(file, preload=True)
    data = raw.get_data().T
    return data
