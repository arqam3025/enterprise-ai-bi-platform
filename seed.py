"""Create reproducible, synthetic relational business data."""
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

def create_demo_db(path="demo.db", seed=42):
    rng = random.Random(seed)
    path = Path(path)
    with sqlite3.connect(path) as db:
        db.executescript("""
        DROP TABLE IF EXISTS tickets;
        DROP TABLE IF EXISTS invoices;
        DROP TABLE IF EXISTS contracts;
        DROP TABLE IF EXISTS services;
        DROP TABLE IF EXISTS customers;
        CREATE TABLE customers(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE services(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
        CREATE TABLE contracts(id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL,
          service_id INTEGER NOT NULL, FOREIGN KEY(customer_id) REFERENCES customers(id),
          FOREIGN KEY(service_id) REFERENCES services(id));
        CREATE TABLE invoices(id INTEGER PRIMARY KEY, contract_id INTEGER NOT NULL,
          invoice_date TEXT NOT NULL, amount REAL NOT NULL, status TEXT NOT NULL,
          FOREIGN KEY(contract_id) REFERENCES contracts(id));
        CREATE TABLE tickets(id INTEGER PRIMARY KEY, contract_id INTEGER NOT NULL,
          priority TEXT NOT NULL, breached INTEGER NOT NULL,
          FOREIGN KEY(contract_id) REFERENCES contracts(id));
        """)
        db.executemany("INSERT INTO customers VALUES (?,?)",
                       [(i, f"Demo Customer {i:03d}") for i in range(1,101)])
        names=["Cloud Hosting","Managed IT","Cybersecurity","Connectivity","Backup"]
        db.executemany("INSERT INTO services VALUES (?,?)",list(enumerate(names,1)))
        contracts=[(i,rng.randint(1,100),rng.randint(1,5)) for i in range(1,201)]
        db.executemany("INSERT INTO contracts VALUES (?,?,?)",contracts)
        start=date(2025,1,1)
        invoices=[(i,rng.randint(1,200),(start+timedelta(days=rng.randint(0,364))).isoformat(),
                   round(rng.uniform(100,5000),2),rng.choices(["paid","open","overdue"],[.72,.18,.10])[0])
                  for i in range(1,1201)]
        db.executemany("INSERT INTO invoices VALUES (?,?,?,?,?)",invoices)
        tickets=[(i,rng.randint(1,200),rng.choice(["P1","P2","P3"]),int(rng.random()<.15))
                 for i in range(1,401)]
        db.executemany("INSERT INTO tickets VALUES (?,?,?,?)",tickets)
    return path

if __name__=="__main__":
    print("Created:",create_demo_db())
