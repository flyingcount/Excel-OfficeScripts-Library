# Test: sarima_forecast

## Setup

1. Formulas → **Initialization** → paste `sarima_forecast` from `source/python-in-excel/functions/sarima_forecast.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Prefer at least 2–3 full seasons (e.g. 36 monthly points).

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).columns)` | `['t', 'value', 'label']` |
| `sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).shape` | `(39, 3)` |
| `str(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).iloc[-1]["label"])` | `Forecast SARIMA` |
| `int((sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12)["label"] == "Forecast SARIMA").sum())` | `3` |
