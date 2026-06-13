"""
bci_horizon_to_cpea_stream.py
Adaptador: EEGMotorImagery (PhysioNet/BCI2000, EDF+) -> formato .cpea_stream (NEXUS-EEG)

Uso:
    python bci_horizon_to_cpea_stream.py --input <archivo.edf> --output <salida.cpea_stream> \
        --target_fs 250 --kp_source kp_history.csv
"""

import argparse
import hashlib
import json
import numpy as np
import mne  # lectura EDF+


# -----------------------------------------------------------------------
# FUNCIÓN 1: Ingesta y normalización de canales
# -----------------------------------------------------------------------
def load_and_normalize(edf_path):
    raw = mne.io.read_raw_edf(edf_path, preload=True)

    # Renombrar/verificar canales según sistema 10-10 (64 canales)
    raw = standardize_channel_names(raw)  # mapea nombres EDF -> nomenclatura interna

    # Filtro paso-banda 1-45 Hz (consistente con preprocesamiento NEXUS-EEG)
    raw.filter(l_freq=1.0, h_freq=45.0, fir_design='firwin')

    # Referencia común promedio (CAR)
    raw.set_eeg_reference('average')

    eeg_data = raw.get_data()        # shape: (n_channels, n_samples)
    fs_native = raw.info['sfreq']    # 160 Hz típicamente
    channel_names = raw.ch_names

    # Extraer anotaciones de evento (T0/T1/T2)
    events, event_id = mne.events_from_annotations(raw)
    event_markers = build_event_marker_array(events, n_samples=eeg_data.shape[1])

    return eeg_data, fs_native, channel_names, event_markers, raw.info


# -----------------------------------------------------------------------
# FUNCIÓN 2: Resampleo y alineación temporal
# -----------------------------------------------------------------------
def resample_with_event_preservation(eeg_data, fs_native, event_markers, target_fs):
    if fs_native == target_fs:
        return eeg_data, event_markers, fs_native

    # Resampleo de señal continua (interpolación tipo FFT/poly, vía mne o scipy)
    eeg_resampled = resample_signal(eeg_data, fs_native, target_fs)

    # Los event_markers son categóricos -> NO interpolar linealmente
    # Asignar cada marca al frame más cercano tras el resampleo
    ratio = target_fs / fs_native
    n_new_samples = eeg_resampled.shape[1]
    event_markers_resampled = np.zeros(n_new_samples, dtype=int)

    nonzero_idx = np.nonzero(event_markers)[0]
    for idx in nonzero_idx:
        new_idx = int(round(idx * ratio))
        new_idx = min(new_idx, n_new_samples - 1)
        event_markers_resampled[new_idx] = event_markers[idx]

    return eeg_resampled, event_markers_resampled, target_fs


# -----------------------------------------------------------------------
# FUNCIÓN 3: Inyección del canal geomagnético sintético-histórico
# -----------------------------------------------------------------------
def inject_synthetic_geo_channel(n_samples, target_fs, session_date, kp_source_csv):
    """
    session_date: fecha de adquisición (extraída de metadatos EDF/PhysioNet)
    kp_source_csv: tabla local con columnas [datetime, kp_index] (resolución 3h)
    """
    kp_table = load_kp_table(kp_source_csv)  # offline, evita dependencia de red

    # Seleccionar valores Kp correspondientes a la ventana temporal de la sesión
    kp_window = select_kp_window(kp_table, session_date)

    # Interpolación lineal de Kp (resolución 3h) a la resolución del frame (target_fs)
    timestamps_native = kp_window['datetime']      # bloques de 3h
    kp_values = kp_window['kp_index']

    session_duration_sec = n_samples / target_fs
    timestamps_frames = np.linspace(0, session_duration_sec, n_samples)

    geo_channel = np.interp(
        timestamps_frames,
        convert_to_seconds(timestamps_native),
        kp_values
    )

    geo_channel_synthetic_flag = True
    return geo_channel, geo_channel_synthetic_flag


# -----------------------------------------------------------------------
# FUNCIÓN 4: Serialización a .cpea_stream
# -----------------------------------------------------------------------
def serialize_to_cpea_stream(eeg_data, fs, event_markers, geo_channel,
                              geo_synthetic_flag, channel_names,
                              subject_id, session_id, output_path):
    n_channels, n_samples = eeg_data.shape

    with open(output_path, 'w') as f_out:
        for i in range(n_samples):
            frame = {
                "timestamp": i / fs,  # segundos relativos; reemplazar por epoch+offset si aplica
                "eeg_channels": eeg_data[:, i].tolist(),
                "channel_names": channel_names,
                "sampling_rate": fs,
                "event_marker": int(event_markers[i]),
                "geo_channel": float(geo_channel[i]),
                "geo_channel_synthetic": geo_synthetic_flag,
                "subject_id": subject_id,
                "session_id": session_id
            }
            f_out.write(json.dumps(frame) + "\n")  # formato JSON-lines


# -----------------------------------------------------------------------
# FUNCIÓN 5: Generación de manifiesto de procedencia (FAIR)
# -----------------------------------------------------------------------
def generate_manifest(edf_path, output_path, fs_native, target_fs,
                       subject_id, session_id, manifest_path):
    file_hash = compute_sha256(edf_path)

    manifest = {
        "source_dataset": "EEGMotorImagery (PhysioNet/BCI2000)",
        "source_file": edf_path,
        "source_file_sha256": file_hash,
        "adapter_version": "1.0",
        "preprocessing": {
            "bandpass_filter_hz": [1.0, 45.0],
            "reference": "common_average",
            "fs_native": fs_native,
            "fs_target": target_fs
        },
        "geo_channel_source": "Kp index (GFZ Potsdam, offline table)",
        "geo_channel_synthetic": True,
        "subject_id": subject_id,
        "session_id": session_id,
        "output_file": output_path
    }

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)


def compute_sha256(filepath):
    sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


# -----------------------------------------------------------------------
# MAIN: orquestación del pipeline completo
# -----------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--target_fs', type=int, default=250)
    parser.add_argument('--kp_source', required=True)
    args = parser.parse_args()

    subject_id, session_id, session_date = parse_metadata_from_filename(args.input)

    # Función 1
    eeg_data, fs_native, channel_names, event_markers, info = load_and_normalize(args.input)

    # Función 2
    eeg_resampled, event_markers_resampled, fs_final = resample_with_event_preservation(
        eeg_data, fs_native, event_markers, args.target_fs
    )

    # Función 3
    geo_channel, geo_flag = inject_synthetic_geo_channel(
        n_samples=eeg_resampled.shape[1],
        target_fs=fs_final,
        session_date=session_date,
        kp_source_csv=args.kp_source
    )

    # Función 4
    serialize_to_cpea_stream(
        eeg_resampled, fs_final, event_markers_resampled,
        geo_channel, geo_flag, channel_names,
        subject_id, session_id, args.output
    )

    # Función 5
    manifest_path = args.output.replace('.cpea_stream', '_manifest.json')
    generate_manifest(
        args.input, args.output, fs_native, fs_final,
        subject_id, session_id, manifest_path
    )

    print(f"Stream generado: {args.output}")
    print(f"Manifiesto: {manifest_path}")


if __name__ == "__main__":
    main()
