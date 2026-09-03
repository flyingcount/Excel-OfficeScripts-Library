# Test: ets_forecast

## Setup

1. Formulas → **Initialization** → paste `ets_forecast` from `source/python-in-excel/functions/ets_forecast.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put 24 seasonal values in `A1:A24` (e.g. repeat a mild monthly pattern twice).

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none").columns)` | `['t', 'value', 'label']` |
| `ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none").shape` | `(27, 3)` |
| `str(ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none").iloc[0]["label"])` | `Actual` |
| `str(ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none").iloc[-1]["label"])` | `Forecast ETS` |
| `int((ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none")["label"] == "Forecast ETS").sum())` | `3` |
