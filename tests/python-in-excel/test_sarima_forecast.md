# Test: sarima_forecast

## Setup

1. Formulas → **Initialization** → paste `sarima_forecast` from `source/python-in-excel/functions/sarima_forecast.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Prefer at least 2–3 full seasons (e.g. 36 monthly points).

## Cases (table)

In a PY cell, set output to **Excel value**. Default `level=0.95`. The cheap spec `p=0, d=1, q=0, P=0, D=1, Q=0, s=12` is seasonal differencing of a trend.

| Python | Expected |
|--------|----------|
| `list(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).columns)` | `['t', 'value', 'lower', 'upper', 'label']` |
| `sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).shape` | `(39, 5)` |
| `str(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).iloc[-1]["label"])` | `Forecast SARIMA` |
| `int((sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12)["label"] == "Forecast SARIMA").sum())` | `3` |
| `bool(pd.isna(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).iloc[0]["lower"]))` | `True` |
| `float(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).iloc[-1]["lower"]) <= float(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).iloc[-1]["value"])` | `True` |
| `float(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).iloc[-1]["upper"]) >= float(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12).iloc[-1]["value"])` | `True` |

## Cases (plot)

Leave the PY cell as a **Python object**.

| Python | Expected |
|--------|----------|
| `type(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12, plot=True)).__name__` | `Figure` |
| `len(sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12, plot=True).axes)` | `1` |
| `sarima_forecast(list(range(1, 37)), h=3, p=0, d=1, q=0, P=0, D=1, Q=0, s=12, plot=True).axes[0].get_title()` | `SARIMA forecast` |
