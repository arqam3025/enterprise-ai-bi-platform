import sqlite3
import tempfile
import unittest
from pathlib import Path
from seed import create_demo_db

class DemoDataTests(unittest.TestCase):
    def test_reproducible_relational_data(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"test.db"
            create_demo_db(path)
            with sqlite3.connect(path) as db:
                self.assertEqual(db.execute("SELECT COUNT(*) FROM invoices").fetchone()[0],1200)
                self.assertEqual(db.execute("SELECT COUNT(*) FROM tickets").fetchone()[0],400)
                self.assertEqual(db.execute("PRAGMA foreign_key_check").fetchall(),[])
                self.assertGreater(db.execute("SELECT SUM(amount) FROM invoices").fetchone()[0],0)

if __name__=="__main__":
    unittest.main()
