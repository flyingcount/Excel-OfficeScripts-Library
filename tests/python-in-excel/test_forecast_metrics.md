# Test: forecast_metrics

## Setup

1. Formulas → **Initialization** → paste `forecast_metrics` from `source/python-in-excel/functions/forecast_metrics.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put this table in `A1:B4`:

   | Actual | Forecast |
   |--------|----------|
   | 10 | 12 |
   | 20 | 18 |
   | 30 | 33 |

Errors are −2, 2, −3. ME = −1. MAE = 7/3. RMSE = √(17/3). MAPE = 13.333…%.

## Cases

In a PY cell, set output to **Excel value**.

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(forecast_metrics("A1:B4", "Actual", "Forecast").columns)` | `['metric', 'value', 'guidance']` |
| `forecast_metrics("A1:B4", "Actual", "Forecast").shape` | `(10, 3)` |
| `list(forecast_metrics("A1:B4", "Actual", "Forecast")["metric"])` | `['n', 'ME', 'MAE', 'MSE', 'RMSE', 'MAPE', 'sMAPE', 'MdAPE', 'MASE', 'R2']` |

### Values

| Python | Expected |
|--------|----------|
| `int(forecast_metrics("A1:B4", "Actual", "Forecast").set_index("metric").loc["n", "value"])` | `3` |
| `float(forecast_metrics("A1:B4", "Actual", "Forecast").set_index("metric").loc["ME", "value"])` | `-1.0` |
| `round(float(forecast_metrics("A1:B4", "Actual", "Forecast").set_index("metric").loc["MAE", "value"]), 4)` | `2.3333` |
| `round(float(forecast_metrics("A1:B4", "Actual", "Forecast").set_index("metric").loc["MSE", "value"]), 4)` | `5.6667` |
| `round(float(forecast_metrics("A1:B4", "Actual", "Forecast").set_index("metric").loc["RMSE", "value"]), 4)` | `2.3805` |
| `round(float(forecast_metrics("A1:B4", "Actual", "Forecast").set_index("metric").loc["MAPE", "value"]), 4)` | `13.3333` |
| `float(forecast_metrics("A1:B4", "Actual", "Forecast").set_index("metric").loc["MdAPE", "value"])` | `10.0` |
| `round(float(forecast_metrics("A1:B4", "Actual", "Forecast").set_index("metric").loc["MASE", "value"]), 4)` | `0.2333` |
| `round(float(forecast_metrics("A1:B4", "Actual", "Forecast").set_index("metric").loc["R2", "value"]), 4)` | `0.915` |

### Perfect forecast and DataFrame

| Python | Expected |
|--------|----------|
| `float(forecast_metrics(pd.DataFrame({"y": [1, 2, 3], "f": [1, 2, 3]}), "y", "f").set_index("metric").loc["MAE", "value"])` | `0.0` |
| `float(forecast_metrics(pd.DataFrame({"y": [1, 2, 3], "f": [1, 2, 3]}), "y", "f").set_index("metric").loc["R2", "value"])` | `1.0` |

### Edge cases

| Python | Expected |
|--------|----------|
| `forecast_metrics("A1:B4", "Missing", "Forecast")` | `#PYTHON!` — `Column 'Missing' not found` |
| `forecast_metrics(pd.DataFrame({"y": [None], "f": [1]}), "y", "f")` | `#PYTHON!` — `Need at least 1 row with both actual and forecast.` |
