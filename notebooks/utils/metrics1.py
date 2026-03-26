def compute_sustained_coherence(icp_series, window_ratio=0.2):
    """
    Calcula ICP sostenido como media de la última ventana de trials.
    """
    n = len(icp_series)
    window_size = int(n * window_ratio)
    return np.mean(icp_series[-window_size:])

def compute_retention_rate(icp_end_session1, icp_start_session2):
    """
    Tasa de retención de coherencia entre sesiones.
    """
    return icp_start_session2 / icp_end_session1 if icp_end_session1 != 0 else 0

def compute_learning_rate(icp_series):
    """
    Calcula la pendiente de la regresión lineal del ICP.
    """
    x = np.arange(len(icp_series))
    slope, _, r_value, _, _ = stats.linregress(x, icp_series)
    return slope, r_value**2
