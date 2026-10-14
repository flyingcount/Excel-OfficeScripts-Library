# Test: rolling_cv

## Setup

1. Formulas → **Initialization** → paste `rolling_cv` from `source/python-in-excel/functions/rolling_cv.py` after the default imports → Save. Or paste `init/TimeSeries.py`.

For `[10, 20, 30, 40]`, `h=1`, `min_train=2`, `method='naive'`: origins 2 and 3 forecast 20 and 30 against actuals 30 and 40 → MAE = 10.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(rolling_cv([10, 20, 30, 40], h=1, min_train=2, method="naive").columns)` | `['metric', 'value', 'guidance']` |
| `float(rolling_cv([10, 20, 30, 40], h=1, min_train=2, method="naive").set_index("metric").loc["MAE", "value"])` | `10.0` |
| `int(rolling_cv([10, 20, 30, 40], h=1, min_train=2, method="naive").set_index("metric").loc["n_origins", "value"])` | `2` |
| `list(rolling_cv([10, 20, 30, 40], h=1, min_train=2, method="naive", full=True).columns)` | `['origin', 'horizon', 'actual', 'forecast', 'error']` |
| `rolling_cv([10, 20], h=1, min_train=2, method="naive")` | `#PYTHON!` — `Need at least min_train + h observations.` |
