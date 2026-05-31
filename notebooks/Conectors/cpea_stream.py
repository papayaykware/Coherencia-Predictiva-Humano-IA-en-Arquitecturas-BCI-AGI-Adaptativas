import pylsl
import numpy as np
import json
from datetime import datetime
from typing import Dict, List

class CPEAStreamWriter:
    """
    Escribe el stream .cpea_stream sobre LSL.
    
    El stream tiene dimensión n_channels + n_metadata_channels:
    - Canales 0..n_channels-1: señal EEG normalizada (μV)
    - Canal n_channels: sqi_global (float)
    - Canal n_channels+1: coherence_score (float)
    - Canal n_channels+2: channel_mask_packed (float, bits empaquetados)
    - Canal n_channels+3: jitter_ms (float)
    
    Total: n_channels + 4 canales en el stream LSL.
    """
    
    STREAM_TYPE = 'CPEA'
    STREAM_FORMAT = pylsl.cf_double64
    
    def __init__(
        self,
        channel_names: List[str],
        fs: int = 256,
        hardware_id: str = 'unknown',
        corpus_version: str = 'NEXUS-2',
        session_id: str = None
    ):
        self.channel_names = channel_names
        self.n_eeg_channels = len(channel_names)
        self.n_total_channels = self.n_eeg_channels + 4
        self.fs = fs
        self.hardware_id = hardware_id
        self.session_id = session_id or datetime.utcnow().strftime(
            '%Y%m%dT%H%M%SZ'
        )
        
        # Crear StreamInfo LSL con metadatos extendidos
        self.info = pylsl.StreamInfo(
            name='NEXUS-EEG',
            type=self.STREAM_TYPE,
            channel_count=self.n_total_channels,
            nominal_srate=fs,
            channel_format=self.STREAM_FORMAT,
            source_id=f'cpea_{self.session_id}'
        )
        
        self._build_xml_header()
        self.outlet = pylsl.StreamOutlet(self.info)
    
    def _build_xml_header(self):
        """Construye el header XML extendido .cpea_stream"""
        desc = self.info.desc()
        
        # Metadata del corpus
        corpus = desc.append_child('corpus_papayaykware')
        corpus.append_child_value('document', 'NEXUS-2')
        corpus.append_child_value('series', 'CPEA')
        corpus.append_child_value('hardware_id', self.hardware_id)
        corpus.append_child_value('session_id', self.session_id)
        corpus.append_child_value('target_montage', 'CPEA-19')
        corpus.append_child_value('fs_normalized', str(self.fs))
        corpus.append_child_value('version', '1.0')
        
        # Descripción de canales EEG
        channels = desc.append_child('channels')
        for ch_name in self.channel_names:
            ch = channels.append_child('channel')
            ch.append_child_value('label', ch_name)
            ch.append_child_value('unit', 'microvolts')
            ch.append_child_value('type', 'EEG')
        
        # Canales de metadatos
        meta_channels = [
            ('sqi_global', 'SQI', 'normalized'),
            ('coherence_score', 'CPEA_COHERENCE', 'normalized'),
            ('channel_mask_packed', 'MASK', 'bits'),
            ('jitter_ms', 'TIMING', 'milliseconds')
        ]
        for label, ch_type, unit in meta_channels:
            ch = channels.append_child('channel')
            ch.append_child_value('label', label)
            ch.append_child_value('unit', unit)
            ch.append_child_value('type', ch_type)
    
    def push_window(
        self,
        eeg_window: np.ndarray,        # (n_channels, n_samples)
        timestamps: np.ndarray,        # (n_samples,)
        sqi_result: 'SQIResult',
        coherence_data: Dict,
        channel_mask: np.ndarray       # (n_channels,) bool/uint8
    ) -> bool:
        """
        Empuja una ventana completa al stream LSL.
        Retorna True si la ventana fue admitida (SQI >= threshold).
        """
        if not sqi_result.window_accepted:
            return False
        
        # Empaquetar channel_mask como entero de 32 bits en float64
        mask_packed = float(int(
            ''.join(str(int(b)) for b in channel_mask), 2
        ))
        
        # Construir array de salida: EEG + metadatos
        meta_row = np.array([
            sqi_result.sqi_global,
            coherence_data['coherence_score'],
            mask_packed,
            sqi_result.jitter_ms
        ])
        
        # Empujar muestra por muestra con timestamps corregidos
        for i in range(eeg_window.shape[1]):
            sample = np.concatenate([
                eeg_window[:, i],
                meta_row  # mismo valor de metadatos para toda la ventana
            ])
            self.outlet.push_sample(
                sample.tolist(),
                timestamp=timestamps[i]
            )
        
        return True
