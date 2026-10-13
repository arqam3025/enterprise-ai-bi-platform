import tempfile
import unittest
from pathlib import Path
from fastapi.testclient import TestClient
import api

class ApiTests(unittest.TestCase):
    def test_read_only_metrics_and_validation(self):
        old=api.DB
        with tempfile.TemporaryDirectory() as temp:
            api.DB=Path(temp)/"api-test.db"
            try:
                client=TestClient(api.app)
                self.assertEqual(client.get("/health").status_code,200)
                result=client.get("/metrics")
                self.assertEqual(result.status_code,200)
                self.assertEqual(result.json()["invoice_count"],1200)
                self.assertEqual(len(client.get("/services/revenue?limit=2").json()),2)
                self.assertEqual(client.get("/services/revenue?limit=0").status_code,422)
                self.assertEqual(len(client.get("/tickets/summary").json()),3)
            finally:
                api.DB=old
if __name__=="__main__":
    unittest.main()
