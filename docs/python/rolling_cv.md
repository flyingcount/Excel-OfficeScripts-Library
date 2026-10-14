# rolling_cv

Walk-forward (rolling-origin) cross-validation for baseline methods. At each origin, forecast `h` steps from history only.

Formula: `source/python-in-excel/functions/rolling_cv.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
rolling_cv("A1:A50", h=1, method="naive")
rolling_cv("A1:A48", h=1, method="seasonal_naive", period=12, full=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `h` | No | Forecast horizon per origin. Default `1`. |
| `min_train` | No | Smallest training length. Default `max(h * 2, period + 1)`. |
| `step` | No | Origin stride. Default `1`. |
| `method` | No | `naive`, `seasonal_naive` / `snaive`, or `drift`. Default `naive`. |
| `period` | No | Seasonal period for seasonal_naive. Default `12`. |
| `full` | No | `False` (default) spills MAE/RMSE/MAPE summary. `True` spills each origin. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Summary: `metric` / `value` / `guidance` (MAE, RMSE, MAPE, …). With `full=True`: per-origin forecast errors.
