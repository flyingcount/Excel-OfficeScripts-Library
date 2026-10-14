# ets_forecast

Holt-Winters (ETS) forecast with a prediction interval. Spills actuals plus appended forecast rows, or `plot=True` for a chart.

Formula: `source/python-in-excel/functions/ets_forecast.py`

The point forecast is statsmodels `ExponentialSmoothing`. The interval is `value ± z * sigma * sqrt(v_h)`, where `sigma` is the RMSE of in-sample residuals and `v_h` uses Hyndman additive-error weights `c_j = alpha + j*beta + gamma * 1_{j mod m = 0}`. The band widens with the horizon. Multiplicative trend/seasonal intervals use the same additive-error approximation around the point forecast.

**Multiplicative `trend` / `seasonal`:** statsmodels requires every fitted value > 0. Zeros, negatives, and blanks (Excel often sends blanks as 0) are linearly interpolated for the fit only; the spilled Actual column keeps the original numbers. If the series still cannot be made strictly positive, use `trend="add"` and `seasonal="add"`, or fill the zeros first (for example `impute`).

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

Table (PY cell output **Excel value**):

```python
ets_forecast("A1:A48", h=12)
ets_forecast("A1:A48", h=6, trend="add", seasonal="mul", period=12)
ets_forecast("A1:A48", h=12, trend="mul", seasonal="mul", period=12)
ets_forecast("A1:A48", h=12, level=0.8)
```

Chart (leave as a **Python object**):

```python
ets_forecast("A1:A48", h=12, plot=True)
ets_forecast("A1:A48", h=6, trend="add", seasonal="none", plot=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `h` | No | Forecast horizon. Default `12`. |
| `trend` | No | `add`, `mul`, or `none`. Default `add`. |
| `seasonal` | No | `add`, `mul`, or `none`. Default `add`. |
| `period` | No | Seasonal length when seasonal is not `none`. Default `12`. |
| `level` | No | Prediction interval coverage between 0 and 1. Default `0.95`. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib chart. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result (table)

Columns: `t`, `value`, `lower`, `upper`, `label` (`Actual` / `Forecast ETS`). Set the PY cell to **Excel value** to spill. Actual rows leave `lower` / `upper` blank.

## Result (plot)

Actuals, point forecast, and a shaded interval. Leave the cell as a **Python object**, not Excel value.
