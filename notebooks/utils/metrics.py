def compute_adaptation_effect(icp_history, window_size=10):
    """
    Calcula el efecto de la adaptación comparando ventanas inicial y final.
    """
    initial_icp = np.mean(icp_history[:window_size])
    final_icp = np.mean(icp_history[-window_size:])
    improvement = final_icp - initial_icp
    
    # Test estadístico (t-test)
    from scipy.stats import ttest_ind
    _, p_value = ttest_ind(icp_history[:window_size], icp_history[-window_size:])
    
    return {
        'initial_icp': initial_icp,
        'final_icp': final_icp,
        'absolute_improvement': improvement,
        'relative_improvement': improvement / max(initial_icp, 0.01),
        'p_value': p_value,
        'significant': p_value < 0.05
    }
