import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import numpy as np
import time

def create_nexus_pipeline(
    board_id: int,           # BoardIds.CYTON_BOARD o MUSE_S_BOARD
    serial_port: str = '',
    hardware_label: str = 'unknown'
):
    """
    Crea y retorna el pipeline NEXUS-EEG configurado para el hardware dado.
    El código aguas abajo (SIGMA-T) no necesita saber qué hardware es.
    """
    
    # --- BrainFlow: inicialización de hardware ---
    params = BrainFlowInputParams()
    params.serial_port = serial_port
    
    board = BoardShim(board_id, params)
    board.prepare_session()
    
    fs_native = BoardShim.get_sampling_rate(board_id)
    eeg_channels_raw = BoardShim.get_eeg_channels(board_id)
    eeg_names_raw = BoardShim.get_eeg_names(board_id)
    
    # --- Instanciar módulos NEXUS-EEG ---
    normalizer = TemporalNormalizer(source_fs=fs_native)
    topology_mgr = SensorTopologyManager(available_channels=eeg_names_raw)
    
    noise_estimator = OnlineNoiseEstimator(
        n_channels=len(CPEA_MONTAGE_19),
        fs=256
    )
    
    coherence_scorer = CoherenceScorer(
        channel_names=list(CPEA_MONTAGE_19.keys()),
        fs=256,
        channel_mask=topology_mgr.channel_mask
    )
    
    stream_writer = CPEAStreamWriter(
        channel_names=list(CPEA_MONTAGE_19.keys()),
        fs=256,
        hardware_id=hardware_label
    )
    
    return board, normalizer, topology_mgr, noise_estimator, \
           coherence_scorer, stream_writer, eeg_channels_raw, eeg_names_raw

def run_nexus_loop(board_id, serial_port='', hardware_label='unknown'):
    
    (board, normalizer, topology_mgr, noise_estimator,
     coherence_scorer, stream_writer,
     eeg_ch_raw, eeg_names_raw) = create_nexus_pipeline(
        board_id, serial_port, hardware_label
    )
    
    board.start_stream()
    print(f"[NEXUS-EEG] Stream iniciado · hardware: {hardware_label}")
    
    try:
        while True:
            # Leer buffer de BrainFlow (tramas acumuladas)
            data_raw = board.get_board_data()
            if data_raw.shape[1] == 0:
                time.sleep(0.01)
                continue
            
            eeg_raw = data_raw[eeg_ch_raw, :]
            ts_raw = data_raw[
                BoardShim.get_timestamp_channel(board_id), :
            ]
            
            # M1: Normalización temporal
            eeg_norm, ts_corr, jitter_ms = normalizer.process(
                eeg_raw, ts_raw
            )
            
            # M2: Proyección topológica
            eeg_proj, ch_mask = topology_mgr.project(
                eeg_norm, eeg_names_raw
            )
            
            # M3: Estimación de ruido → SQI
            sqi = noise_estimator.update(eeg_proj, jitter_ms)
            if sqi is None:
                continue  # Buffer no lleno aún
            
            # M4: Coherence score (solo si SQI admite la ventana)
            if sqi.window_accepted:
                window = np.array([
                    list(noise_estimator._buffers[i])
                    for i in range(eeg_proj.shape[0])
                ])
                coherence = coherence_scorer.compute(window, sqi)
            else:
                coherence = {'coherence_score': 0.0, 'band_scores': {},
                            'pair_coherences': {}, 'n_pairs_computed': 0,
                            'active_channels': []}
            
            # M5: Escritura al stream .cpea_stream
            window_ts = ts_corr[-noise_estimator.window_samples:]
            admitted = stream_writer.push_window(
                eeg_proj[:, -noise_estimator.window_samples:],
                window_ts,
                sqi,
                coherence,
                ch_mask
            )
            
            status = "✓ ADMIT" if admitted else "✗ REJECT"
            print(
                f"[{hardware_label}] SQI={sqi.sqi_global:.3f} "
                f"| coherence={coherence['coherence_score']:.3f} "
                f"| jitter={jitter_ms:.2f}ms | {status}"
            )
            
    except KeyboardInterrupt:
        print("[NEXUS-EEG] Detención manual.")
    finally:
        board.stop_stream()
        board.release_session()
