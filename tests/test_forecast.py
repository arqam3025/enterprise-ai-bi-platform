import unittest
from forecast import evaluate_forecast

class ForecastTests(unittest.TestCase):
    def test_chronological_holdout_and_baseline(self):
        rows=[(f"2025-{i:02d}",float(100+i*10)) for i in range(1,13)]
        result=evaluate_forecast(rows,test_months=3)
        self.assertEqual(result["holdout_months"],["2025-10","2025-11","2025-12"])
        self.assertEqual(result["train_months"],8)
        self.assertEqual(result["test_months"],3)
        self.assertEqual(result["persistence_prediction"],[190.0,200.0,210.0])
        self.assertGreaterEqual(result["ridge_mae"],0)
    def test_too_few_months(self):
        with self.assertRaises(ValueError):
            evaluate_forecast([("2025-01",100.0)])
if __name__=="__main__":
    unittest.main()
