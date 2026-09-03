# sarima_forecast

Seasonal ARIMA forecast. Spills actuals plus appended forecast rows.

Formula: `source/python-in-excel/functions/sarima_forecast.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
sarima_forecast("A1:A48", h=12, s=12)
sarima_forecast("A1:A48", h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `h` | No | Forecast horizon. Default `12`. |
| `p`, `d`, `q` | No | Non-seasonal orders. Default `(1, 1, 1)`. |
| `P`, `D`, `Q`, `s` | No | Seasonal orders and period. Default `(1, 1, 1)` and `s=12`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Columns: `t`, `value`, `label` (`Actual` / `Forecast SARIMA`).
