# forecast_plot

Chart of historical actuals, a point forecast that continues after the last actual, and an optional prediction interval.

Formula: `source/python-in-excel/functions/forecast_plot.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

Leave the PY cell as a **Python object** (not Excel value):

```python
forecast_plot("A1:A24", "B1:B6")
forecast_plot("A1:A24", "B1:B6", lower="C1:C6", upper="D1:D6")
forecast_plot([10, 12, 11, 13], [14, 15], lower=[13, 13.5], upper=[15, 16.5])
```

Pair with `ets_forecast`, `arima_forecast`, `sarima_forecast`, or `baseline_forecast` by splitting Actual vs Forecast rows, or pass any history and horizon columns.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `actual` | Yes | History: column, ref string, Series, list, or DataFrame (first numeric col). |
| `forecast` | Yes | Future point forecasts (same shapes). Plotted on `t = n+1..n+h`. |
| `lower` | No | Lower interval bound; same length as `forecast`. |
| `upper` | No | Upper interval bound; same length as `forecast`. |
| `headers` | No | First row is headers when any argument is a ref string. Default `False`. |

Both `lower` and `upper` shade a band. One alone is drawn as a dotted line.

## Result

A matplotlib `Figure` with Actual, Forecast, an origin marker, and optional Interval.
