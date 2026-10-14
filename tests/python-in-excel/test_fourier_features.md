# Test: fourier_features

## Setup

1. Formulas → **Initialization** → paste `fourier_features` from `source/python-in-excel/functions/fourier_features.py` after the default imports → Save. Or paste `init/TimeSeries.py`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(fourier_features([1, 2, 3, 4], period=4, order=1).columns)` | `['value', 'sin_1', 'cos_1']` |
| `fourier_features([1, 2, 3, 4], period=4, order=1).shape` | `(4, 3)` |
| `round(float(fourier_features([1, 2, 3, 4], period=4, order=1).loc[0, "sin_1"]), 6)` | `0.0` |
| `round(float(fourier_features([1, 2, 3, 4], period=4, order=1).loc[0, "cos_1"]), 6)` | `1.0` |
| `round(float(fourier_features([1, 2, 3, 4], period=4, order=1).loc[1, "sin_1"]), 6)` | `1.0` |
| `fourier_features([], period=4, order=1)` | `#PYTHON!` — `Need at least 1 value row.` |
