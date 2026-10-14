# sarima_forecast

Seasonal ARIMA forecast with a prediction interval. Spills actuals plus appended forecast rows, or `plot=True` for a chart.

Formula: `source/python-in-excel/functions/sarima_forecast.py`

The point forecast and interval come from statsmodels `ARIMA.get_forecast` at coverage `level` (default 0.95). The band widens with the horizon.

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

Table (PY cell output **Excel value**):

```python
sarima_forecast("A1:A48", h=12, s=12)
sarima_forecast("A1:A48", h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12)
sarima_forecast("A1:A48", h=6, s=12, level=0.8)
```

Chart (leave as a **Python object**):

```python
sarima_forecast("A1:A48", h=12, s=12, plot=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `h` | No | Forecast horizon. Default `12`. |
| `p`, `d`, `q` | No | Non-seasonal orders. Default `(1, 1, 1)`. |
| `P`, `D`, `Q`, `s` | No | Seasonal orders and period. Default `(1, 1, 1)` and `s=12`. |
| `level` | No | Prediction interval coverage between 0 and 1. Default `0.95`. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib chart. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result (table)

Columns: `t`, `value`, `lower`, `upper`, `label` (`Actual` / `Forecast SARIMA`). Set the PY cell to **Excel value** to spill. Actual rows leave `lower` / `upper` blank.

## Result (plot)

Actuals, point forecast, and a shaded interval. Leave the cell as a **Python object**, not Excel value.
