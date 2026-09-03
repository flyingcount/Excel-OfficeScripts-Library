# Test: seasonal_indices

## Setup

1. Formulas → **Initialization** → paste `seasonal_indices` from `source/python-in-excel/functions/seasonal_indices.py` after the default imports → Save. Or paste `init/TimeSeries.py`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(seasonal_indices([10, 20, 10, 20], period=2).columns)` | `['season', 'index', 'kind']` |
| `seasonal_indices([10, 20, 10, 20], period=2).shape` | `(2, 3)` |
| `round(float(seasonal_indices([10, 20, 10, 20], period=2).loc[0, "index"]), 4)` | `0.6667` |
| `round(float(seasonal_indices([10, 20, 10, 20], period=2).loc[1, "index"]), 4)` | `1.3333` |
| `str(seasonal_indices([10, 20, 10, 20], period=2, kind="additive").loc[0, "kind"])` | `additive` |
| `float(seasonal_indices([10, 20, 10, 20], period=2, kind="additive").loc[0, "index"])` | `-5.0` |
