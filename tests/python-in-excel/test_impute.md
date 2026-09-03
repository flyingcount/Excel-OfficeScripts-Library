# Test: impute

## Setup

1. Formulas → **Initialization** → paste `impute` from `source/python-in-excel/functions/impute.py` after the default imports → Save. Or paste `init/TimeSeries.py`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(impute([1, None, 3], method="linear").columns)` | `['value', 'imputed', 'was_missing']` |
| `float(impute([1, None, 3], method="linear").loc[1, "imputed"])` | `2.0` |
| `float(impute([1, None, 3], method="linear").loc[1, "was_missing"])` | `1.0` |
| `float(impute([1, None, 3], method="ffill").loc[1, "imputed"])` | `1.0` |
| `float(impute([1, None, 3], method="mean").loc[1, "imputed"])` | `2.0` |
