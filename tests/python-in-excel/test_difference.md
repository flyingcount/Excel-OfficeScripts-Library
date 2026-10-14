# Test: difference

## Setup

1. Formulas → **Initialization** → paste `difference` from `source/python-in-excel/functions/difference.py` after the default imports → Save. Or paste `init/TimeSeries.py`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(difference([10, 20, 30], lag=1).columns)` | `['value', 'diff']` |
| `pd.isna(difference([10, 20, 30], lag=1).loc[0, "diff"])` | `True` |
| `float(difference([10, 20, 30], lag=1).loc[1, "diff"])` | `10.0` |
| `float(difference([10, 20, 30], lag=1).loc[2, "diff"])` | `10.0` |
| `float(difference([10, 20, 30, 50], lag=2).loc[2, "diff"])` | `20.0` |
