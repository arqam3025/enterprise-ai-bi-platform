"""Read-only demonstration REST API. Launch: uvicorn api:app --reload"""
import os
import sqlite3
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from seed import create_demo_db

app=FastAPI(title="Enterprise BI Demo API",version="0.2.0")
DB=Path(os.environ.get("BI_DB_PATH",str(Path(__file__).with_name("demo.db"))))

def ensure_database():
    if not DB.exists():
        create_demo_db(DB)

@app.get("/health")
def health():
    return {"status":"ok","data":"synthetic-demo"}

@app.get("/metrics")
def metrics():
    ensure_database()
    with sqlite3.connect(DB) as db:
        count,total,overdue=db.execute("""
          SELECT COUNT(*),COALESCE(SUM(amount),0),
          SUM(CASE WHEN status='overdue' THEN 1 ELSE 0 END)
          FROM invoices
        """).fetchone()
    return {"invoice_count":count,"invoiced_revenue":round(total,2),
            "overdue_invoices":overdue or 0}

@app.get("/services/revenue")
def service_revenue(limit:int=Query(default=10,ge=1,le=50)):
    ensure_database()
    with sqlite3.connect(DB) as db:
        rows=db.execute("""
          SELECT s.name,ROUND(SUM(i.amount),2) AS revenue
          FROM invoices i JOIN contracts c ON i.contract_id=c.id
          JOIN services s ON s.id=c.service_id
          GROUP BY s.id,s.name ORDER BY revenue DESC LIMIT ?
        """,(limit,)).fetchall()
    return [{"service":name,"revenue":revenue} for name,revenue in rows]

@app.get("/tickets/summary")
def ticket_summary():
    ensure_database()
    with sqlite3.connect(DB) as db:
        rows=db.execute("""
          SELECT priority,COUNT(*),SUM(breached) FROM tickets
          GROUP BY priority ORDER BY priority
        """).fetchall()
    return [{"priority":p,"tickets":n,"sla_breaches":b} for p,n,b in rows]
