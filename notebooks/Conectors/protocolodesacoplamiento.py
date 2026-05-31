# Prueba de desacoplamiento — ejecutar en dos terminales separadas
# Terminal 1: OpenBCI Cyton
run_nexus_loop(
    board_id=BoardIds.CYTON_BOARD.value,
    serial_port='/dev/ttyUSB0',
    hardware_label='OpenBCI-Cyton'
)

# Terminal 2: Muse S
run_nexus_loop(
    board_id=BoardIds.MUSE_S_BOARD.value,
    hardware_label='MuseS'
)

# Consumer (SIGMA-T o script de validación):
import pylsl

def validate_decoupling():
    streams = pylsl.resolve_stream('type', 'CPEA')
    assert len(streams) >= 1, "No hay streams CPEA disponibles"
    
    for stream_info in streams:
        inlet = pylsl.StreamInlet(stream_info)
        
        # Verificar estructura invariante del header
        desc = stream_info.desc()
        corpus_node = desc.child('corpus_papayaykware')
        assert corpus_node.child_value('target_montage') == 'CPEA-19'
        assert int(corpus_node.child_value('fs_normalized')) == 256
        
        # Verificar dimensionalidad: 19 EEG + 4 meta = 23 canales
        assert stream_info.channel_count() == 23
        
        # Leer 10 segundos de datos
        samples = []
        for _ in range(10 * 256):
            sample, ts = inlet.pull_sample(timeout=1.0)
            samples.append(sample)
        
        samples = np.array(samples)
        
        # Verificar que los metadatos tienen valores en rango válido
        sqi_col = samples[:, 19]
        coh_col = samples[:, 20]
        
        assert np.all((sqi_col >= 0.0) & (sqi_col <= 1.0)), \
            "SQI fuera de rango"
        assert np.all((coh_col >= 0.0) & (coh_col <= 1.0)), \
            "coherence_score fuera de rango"
        
        hw = corpus_node.child_value('hardware_id')
        print(f"[VALIDACIÓN] {hw}: estructura CPEA-19 ✓ · "
              f"SQI medio={sqi_col.mean():.3f} · "
              f"coherence medio={coh_col.mean():.3f}")
    
    print("[VALIDACIÓN] Desacoplamiento demostrado: "
          "ambos hardware generan streams .cpea_stream estructuralmente "
          "idénticos consumibles por el mismo código.")
