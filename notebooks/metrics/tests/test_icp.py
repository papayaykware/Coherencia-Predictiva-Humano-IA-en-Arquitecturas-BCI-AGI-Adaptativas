import unittest
import numpy as np
from src.metrics.icp import (
    compute_accuracy,
    compute_mutual_information,
    compute_agi_error,
    compute_icp,
    icp_from_data,
    compute_icp_batch
)


class TestICPComponents(unittest.TestCase):
    
    def test_accuracy_perfect(self):
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        self.assertAlmostEqual(compute_accuracy(y_true, y_pred), 1.0)
    
    def test_accuracy_random(self):
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([1, 0, 1, 0])
        self.assertAlmostEqual(compute_accuracy(y_true, y_pred), 0.5)
    
    def test_accuracy_empty(self):
        self.assertEqual(compute_accuracy(np.array([]), np.array([])), 0.0)
    
    def test_mutual_information(self):
        X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
        y = np.array([0, 1, 0, 1])
        mi = compute_mutual_information(X, y, n_classes=2, normalize=True)
        self.assertGreaterEqual(mi, 0.0)
        self.assertLessEqual(mi, 1.0)
    
    def test_mutual_information_normalized(self):
        X = np.array([[0, 0], [1, 1], [0, 0], [1, 1]])
        y = np.array([0, 1, 0, 1])
        mi = compute_mutual_information(X, y, n_classes=2, normalize=True)
        self.assertAlmostEqual(mi, 1.0, places=5)
    
    def test_agi_error_mse(self):
        expected = np.array([1.0, 2.0, 3.0])
        actual = np.array([1.0, 2.0, 3.0])
        self.assertAlmostEqual(compute_agi_error(expected, actual, 'mse'), 0.0)
    
    def test_agi_error_mae(self):
        expected = np.array([1.0, 2.0, 3.0])
        actual = np.array([1.0, 4.0, 3.0])
        self.assertAlmostEqual(compute_agi_error(expected, actual, 'mae'), 2.0/3.0)
    
    def test_agi_error_cosine(self):
        expected = np.array([1.0, 0.0])
        actual = np.array([0.0, 1.0])
        # cos(90°) = 0 → error = 1 - 0 = 1
        self.assertAlmostEqual(compute_agi_error(expected, actual, 'cosine'), 1.0)
    
    def test_icp_perfect(self):
        icp = compute_icp(accuracy=1.0, mutual_info=1.0, agi_error=0.0)
        self.assertAlmostEqual(icp, 1.0)
    
    def test_icp_bad(self):
        icp = compute_icp(accuracy=0.0, mutual_info=0.0, agi_error=1e6)
        self.assertAlmostEqual(icp, 0.0)
    
    def test_icp_weight_validation(self):
        with self.assertRaises(ValueError):
            compute_icp(1.0, 1.0, 0.0, weights=(0.5, 0.5, 0.5))
    
    def test_icp_from_data(self):
        # Simular datos pequeños
        y_true = np.array([0, 1, 0, 1])
        y_pred = np.array([0, 1, 0, 1])
        X_eeg = np.random.rand(4, 10)
        expected = np.array([0.5, 0.5])
        actual = np.array([0.5, 0.5])
        
        icp = icp_from_data(y_true, y_pred, X_eeg, expected, actual)
        self.assertGreaterEqual(icp, 0.0)
        self.assertLessEqual(icp, 1.0)
    
    def test_icp_batch(self):
        accs = np.array([1.0, 0.5, 0.0])
        mis = np.array([1.0, 0.5, 0.0])
        errs = np.array([0.0, 1.0, 100.0])
        icps = compute_icp_batch(accs, mis, errs)
        
        # Primer trial perfecto
        self.assertAlmostEqual(icps[0], 1.0)
        # Último trial con error muy alto → error_term ~0
        expected_last = 0.4*0.0 + 0.3*0.0 + 0.3*(1/(1+100))
        self.assertAlmostEqual(icps[2], expected_last, places=5)


if __name__ == '__main__':
    unittest.main()
