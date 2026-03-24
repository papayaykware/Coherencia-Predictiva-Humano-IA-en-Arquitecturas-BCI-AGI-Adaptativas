from src.metrics.icp import icp_from_data

# Después de cada trial o sesión
icp_value = icp_from_data(
    y_true=ground_truth_intents,
    y_pred=predicted_intents,
    X_eeg=eeg_features,
    expected_response=human_expected_embedding,
    actual_response=agi_response_embedding,
    weights=(0.4, 0.3, 0.3),
    error_metric='cosine'
)
