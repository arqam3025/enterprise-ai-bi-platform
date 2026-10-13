"""Synthetic enterprise BI dashboard. Run: streamlit run app.py"""
import sqlite3
from pathlib import Path
import pandas as pd
import streamlit as st
from seed import create_demo_db

DB = Path(__file__).with_name("demo.db")
if not DB.exists():
    create_demo_db(DB)

st.set_page_config(page_title="Enterprise AI BI", layout="wide")
st.title("Enterprise AI Business Intelligence")
st.caption("Demonstration using synthetic business records; not connected to a real company.")
with sqlite3.connect(DB) as conn:
    kpis = pd.read_sql_query("""SELECT COUNT(*) AS invoices,
      ROUND(SUM(amount),2) AS revenue,
      SUM(CASE WHEN status='overdue' THEN 1 ELSE 0 END) AS overdue
      FROM invoices""", conn)
    monthly = pd.read_sql_query("""SELECT substr(invoice_date,1,7) AS month,
      ROUND(SUM(amount),2) AS revenue FROM invoices GROUP BY month ORDER BY month""", conn)
    service = pd.read_sql_query("""SELECT s.name AS service,
      ROUND(SUM(i.amount),2) AS revenue FROM invoices i
      JOIN contracts c ON i.contract_id=c.id
      JOIN services s ON c.service_id=s.id GROUP BY s.name ORDER BY revenue DESC""", conn)
    tickets = pd.read_sql_query("""SELECT priority, COUNT(*) AS tickets,
      SUM(CASE WHEN breached=1 THEN 1 ELSE 0 END) AS sla_breaches
      FROM tickets GROUP BY priority""", conn)
a,b,c=st.columns(3)
a.metric("Invoiced revenue", f"£{kpis.loc[0,'revenue']:,.2f}")
b.metric("Invoices", int(kpis.loc[0,'invoices']))
c.metric("Overdue invoices", int(kpis.loc[0,'overdue']))
st.subheader("Revenue trend")
st.line_chart(monthly.set_index("month"))
st.subheader("Revenue by service")
st.bar_chart(service.set_index("service"))
st.subheader("Service desk SLA performance")
st.dataframe(tickets, use_container_width=True)
st.caption("All records are generated locally and are for demonstration only.")

st.subheader("Predictive analytics — monthly revenue experiment")
st.caption("Chronological holdout on synthetic data; compare a simple Ridge model with persistence.")
from forecast import evaluate_forecast
with sqlite3.connect(DB) as conn:
    rows=conn.execute("""SELECT substr(invoice_date,1,7),SUM(amount)
      FROM invoices GROUP BY substr(invoice_date,1,7)
      ORDER BY substr(invoice_date,1,7)""").fetchall()
try:
    results=evaluate_forecast(rows)
    left,right=st.columns(2)
    left.metric("Ridge holdout MAE",f"£{results['ridge_mae']:,.0f}")
    right.metric("Persistence holdout MAE",f"£{results['persistence_mae']:,.0f}")
    comparison=pd.DataFrame({
        "month":results["holdout_months"],
        "actual":results["actual"],
        "ridge":results["ridge_prediction"],
        "persistence":results["persistence_prediction"]
    })
    st.line_chart(comparison.set_index("month"))
    st.caption(f"Training observations: {results['train_months']}; test months: {results['test_months']}. "
               "Synthetic data is randomly generated and may not contain learnable patterns.")
except ValueError as exc:
    st.info(str(exc))
