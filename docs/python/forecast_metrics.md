# forecast_metrics

Accuracy scores for paired **actual** and **forecast** columns. Error is **actual − forecast**. Spills a metric table (MAE, RMSE, MAPE, MASE, and related).

Formula: `source/python-in-excel/functions/forecast_metrics.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` or `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
forecast_metrics("A1:B50", "Actual", "Forecast")
forecast_metrics("Table1[#All]", "Sales", "Pred")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Table/range, DataFrame, or ref string with both columns. |
| `actual_col` | Yes | Header of the actual values (e.g. `"Actual"`). |
| `forecast_col` | Yes | Header of the forecast values (e.g. `"Forecast"`). |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Rows with a blank in either column are dropped. Need at least one complete pair.

## Result

| Metric | Notes |
|--------|-------|
| `n` | Complete pairs. |
| `ME` | Mean error. Positive means the forecast is too low. |
| `MAE` | Mean absolute error. Same units as the series. |
| `MSE` | Mean squared error. |
| `RMSE` | Square root of MSE. Same units as the series. |
| `MAPE` | Mean \|error\|/\|actual\| as a percent. Skips zero actuals. |
| `sMAPE` | Symmetric MAPE (%). Denominator is \|actual\| + \|forecast\|. |
| `MdAPE` | Median absolute percentage error. |
| `MASE` | MAE divided by the mean \|change\| of actuals. Below 1 beats a naive walk. Need n ≥ 2. |
| `R2` | 1 − SS_error / SS_actual. 1 is a perfect fit. |

Use this on holdout rows where both actuals and forecasts exist. `baseline_forecast` appends future rows without actuals — those rows are dropped here.
