def process_trial(self, eeg_signal, block=None):
    features = self.extract_eeg_features(eeg_signal)
    prompt = self.build_prompt(features)
    response = self.agi_finetuner.generate_response(prompt, features)
    icp = self.compute_icp(eeg_signal, response)
    
    # Registrar
    self.session_manager.log_trial(
        trial_id=self.current_trial,
        eeg_features=features,
        response=response,
        icp=icp,
        block=block if block is not None else self.current_block
    )
    
    self.current_trial += 1
    return response, icp
