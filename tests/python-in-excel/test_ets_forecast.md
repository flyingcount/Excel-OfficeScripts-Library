# Test: ets_forecast

## Setup

1. Formulas → **Initialization** → paste `ets_forecast` from `source/python-in-excel/functions/ets_forecast.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put 24 seasonal values in `A1:A24` (e.g. repeat a mild monthly pattern twice).

## Cases (table)

In a PY cell, set output to **Excel value**. Default `level=0.95`. Use `trend="add", seasonal="none"` on a short series so the fit is cheap.

| Python | Expected |
|--------|----------|
| `list(ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none").columns)` | `['t', 'value', 'lower', 'upper', 'label']` |
| `ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none").shape` | `(27, 5)` |
| `str(ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none").iloc[0]["label"])` | `Actual` |
| `str(ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none").iloc[-1]["label"])` | `Forecast ETS` |
| `int((ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none")["label"] == "Forecast ETS").sum())` | `3` |
| `bool(pd.isna(ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none").iloc[0]["lower"]))` | `True` |
| `float(ets_forecast([10, 14, 9, 16, 11, 18, 13, 20], h=3, trend="add", seasonal="none").iloc[-1]["lower"]) < float(ets_forecast([10, 14, 9, 16, 11, 18, 13, 20], h=3, trend="add", seasonal="none").iloc[-1]["value"])` | `True` |
| `float(ets_forecast([10, 14, 9, 16, 11, 18, 13, 20], h=3, trend="add", seasonal="none").iloc[-1]["upper"]) > float(ets_forecast([10, 14, 9, 16, 11, 18, 13, 20], h=3, trend="add", seasonal="none").iloc[-1]["value"])` | `True` |
| `float(ets_forecast([10, 14, 9, 16, 11, 18, 13, 20], h=1, trend="add", seasonal="none", level=0.99).iloc[-1]["upper"]) > float(ets_forecast([10, 14, 9, 16, 11, 18, 13, 20], h=1, trend="add", seasonal="none", level=0.95).iloc[-1]["upper"])` | `True` |
| `ets_forecast(list(range(1, 25)), h=3, trend="mul", seasonal="mul", period=12).shape` | `(27, 5)` |
| `str(ets_forecast(list(range(1, 25)), h=3, trend="mul", seasonal="mul", period=12).iloc[-1]["label"])` | `Forecast ETS` |
| `str(ets_forecast([1, 2, 3, 0, 5, 6, 7, 8, 9, 10, 11, 12] * 2, h=3, trend="mul", seasonal="mul", period=12).iloc[-1]["label"])` | `Forecast ETS` |

## Cases (plot)

Leave the PY cell as a **Python object**.

| Python | Expected |
|--------|----------|
| `type(ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none", plot=True)).__name__` | `Figure` |
| `len(ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none", plot=True).axes)` | `1` |
| `ets_forecast(list(range(1, 25)), h=3, trend="add", seasonal="none", plot=True).axes[0].get_title()` | `ETS forecast` |
| `len(ets_forecast([10, 14, 9, 16, 11, 18, 13, 20], h=3, trend="add", seasonal="none", plot=True).axes[0].collections) >= 1` | `True` |
