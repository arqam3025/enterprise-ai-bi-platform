# Enterprise AI Business Intelligence Platform

**Status:** Working local BI demonstration (synthetic data). Predictive analytics and production API integration are **not yet implemented**.

A portfolio project aligned with enterprise reporting, data integration and business intelligence. Includes a reproducible relational SQLite data generator and Streamlit dashboard showing invoiced revenue, overdue invoices, service revenue and SLA breaches.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python seed.py
streamlit run app.py
```

## Tests

```bash
python -m unittest discover -s tests -v
```

## Architecture

Synthetic data generator → SQLite (customers, services, contracts, invoices, tickets) → SQL aggregation → Streamlit visualisations.

## Next milestones

- Add train/test-separated customer-risk and revenue forecasting baselines.
- Add read-only REST API and validation.
- Add role-based access and deployment documentation.

No real customer data, company integration, trained predictive model or production deployment is claimed.
