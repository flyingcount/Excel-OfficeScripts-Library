# ets_forecast

Holt-Winters (ETS) forecast. Spills actuals plus appended forecast rows with labels.

Formula: `source/python-in-excel/functions/ets_forecast.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
ets_forecast("A1:A48", h=12)
ets_forecast("A1:A48", h=6, trend="add", seasonal="mul", period=12)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `h` | No | Forecast horizon. Default `12`. |
| `trend` | No | `add`, `mul`, or `none`. Default `add`. |
| `seasonal` | No | `add`, `mul`, or `none`. Default `add`. |
| `period` | No | Seasonal length when seasonal is not `none`. Default `12`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Columns: `t`, `value`, `label` (`Actual` / `Forecast ETS`).
