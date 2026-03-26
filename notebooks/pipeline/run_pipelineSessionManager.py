from src.pipeline.session_manager import CPESessionManager

class CPEAPipeline:
    def __init__(self, config_path="config/agi_config.yaml", participant_id="P001"):
        # ... inicialización existente ...
        self.session_manager = CPESessionManager(participant_id=participant_id)
        self.current_trial = 0
        self.current_block = 0
