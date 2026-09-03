# Test: detect_anomalies

## Setup

1. Formulas → **Initialization** → paste `detect_anomalies` from `source/python-in-excel/functions/detect_anomalies.py` after the default imports → Save. Or paste `init/TimeSeries.py`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(detect_anomalies([1, 2, 3, 4, 100], method="zscore", z=2).columns)` | `['t', 'value', 'residual', 'score', 'is_anomaly']` |
| `detect_anomalies([1, 2, 3, 4, 100], method="zscore", z=2).shape` | `(5, 5)` |
| `float(detect_anomalies([1, 2, 3, 4, 100], method="zscore", z=2).loc[4, "is_anomaly"])` | `1.0` |
| `float(detect_anomalies([1, 2, 3, 4, 5], method="zscore", z=3).loc[0, "is_anomaly"])` | `0.0` |
| `float(detect_anomalies([1, 2, 3, 4, 100], method="iqr", z=1.5).loc[4, "is_anomaly"])` | `1.0` |
| `detect_anomalies([1, 2, 3], method="zscore")` | `#PYTHON!` — `Need at least 4 observations.` |
