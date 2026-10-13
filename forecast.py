"""Transparent monthly-revenue forecasting experiment on synthetic data.

Chronological holdout, one-step lag features, and persistence baseline.
No model-quality or business-value claims are made.
"""
import sqlite3
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error

def monthly_revenue(db):
    rows=db.execute("""
        SELECT substr(invoice_date,1,7), SUM(amount)
        FROM invoices GROUP BY substr(invoice_date,1,7)
        ORDER BY substr(invoice_date,1,7)
    """).fetchall()
    return [(str(month),float(revenue)) for month,revenue in rows]

def evaluate_forecast(rows, test_months=3):
    if len(rows) < test_months + 5:
        raise ValueError("At least test_months + 5 months are required")
    months=[r[0] for r in rows]
    values=np.asarray([r[1] for r in rows],dtype=float)
    if not np.all(np.isfinite(values)):
        raise ValueError("Revenue values must be finite")
    # One-step ahead: only the prior month's actual revenue is a feature.
    X=values[:-1].reshape(-1,1)
    y=values[1:]
    split=len(y)-test_months
    model=Ridge(alpha=1.0)
    model.fit(X[:split],y[:split])
    predicted=model.predict(X[split:])
    persistence=X[split:,0]
    return {
        "holdout_months":months[1+split:],
        "actual":y[split:].tolist(),
        "ridge_prediction":predicted.tolist(),
        "persistence_prediction":persistence.tolist(),
        "ridge_mae":float(mean_absolute_error(y[split:],predicted)),
        "persistence_mae":float(mean_absolute_error(y[split:],persistence)),
        "train_months":int(split),
        "test_months":int(test_months),
    }
