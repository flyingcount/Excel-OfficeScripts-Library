# Test: arima_forecast

## Setup

1. Formulas → **Initialization** → paste `arima_forecast` from `source/python-in-excel/functions/arima_forecast.py` after the default imports → Save. Or paste `init/TimeSeries.py`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(arima_forecast(list(range(1, 31)), h=3, p=1, d=1, q=0).columns)` | `['t', 'value', 'label']` |
| `arima_forecast(list(range(1, 31)), h=3, p=1, d=1, q=0).shape` | `(33, 3)` |
| `str(arima_forecast(list(range(1, 31)), h=3, p=1, d=1, q=0).iloc[-1]["label"])` | `Forecast ARIMA` |
| `int((arima_forecast(list(range(1, 31)), h=3, p=1, d=1, q=0)["label"] == "Forecast ARIMA").sum())` | `3` |
