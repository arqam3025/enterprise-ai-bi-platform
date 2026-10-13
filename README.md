# Enterprise AI Business Intelligence Platform

**Status:** Local portfolio demonstration using **synthetic data**, not a production business application.

A Streamlit dashboard with SQL reporting, a read-only FastAPI service and a transparent predictive analytics experiment. This repo demonstrates a small integrated business intelligence architecture without claiming real customer integration.

## Included

- Relational SQLite dataset: customers, services, contracts, invoices and tickets.
- Reproducible synthetic-data generator (`seed.py`).
- Streamlit KPIs, monthly revenue, service revenue and SLA reporting.
- Chronological holdout evaluation of a Ridge monthly revenue predictor **against a persistence baseline**.
- FastAPI read-only endpoints: `/health`, `/metrics`, `/services/revenue?limit=5`, `/tickets/summary`.
- Unit and API tests.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
streamlit run app.py
```

In another terminal, run the API:

```bash
uvicorn api:app --reload
```

Visit `http://127.0.0.1:8000/docs` for interactive API documentation.

## Tests

```bash
python -m unittest discover -s tests -v
```

## Architecture

Synthetic generator → SQLite relational tables → SQL analytics → Streamlit dashboard / read-only FastAPI.
Monthly invoice aggregates → lagged revenue features → chronological Ridge evaluation + persistence baseline.

## Evaluation limitations

The generated invoice amounts and dates are random. There is no reason to expect a predictive model to outperform a simple baseline on these data. Only 12 months of revenue are present, so a three-month holdout is too small for meaningful business conclusions. The holdout comparison is an **illustration of methodology**, not evidence of forecast accuracy in industry. In a real project, use longer historical data, rolling-origin validation and drift monitoring.

## Security and deployment limitations

This API has **no authentication, authorisation, rate limiting, audit logging or production security hardening**. Use locally only. Do not deploy with real customer records. Role-based access, integration with operational systems, and production deployment remain future work.

## Next milestones

- Realistic synthetic scenarios with temporal trends and customer churn labels.
- Rolling time-series validation and feature leakage checks.
- Authenticated data integration and secure deployment.
