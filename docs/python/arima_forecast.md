# arima_forecast

ARIMA(p,d,q) forecast. Spills actuals plus appended forecast rows.

Formula: `source/python-in-excel/functions/arima_forecast.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
arima_forecast("A1:A50", h=12)
arima_forecast("A1:A50", h=6, p=1, d=1, q=1)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `h` | No | Forecast horizon. Default `12`. |
| `p`, `d`, `q` | No | ARIMA orders. Default `(1, 1, 1)`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Columns: `t`, `value`, `label` (`Actual` / `Forecast ARIMA`).
