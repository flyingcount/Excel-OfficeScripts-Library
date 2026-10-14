# Test: seasonally_adjust

## Setup

1. Formulas → **Initialization** → paste `seasonally_adjust` from `source/python-in-excel/functions/seasonally_adjust.py` after the default imports → Save. Or paste `init/TimeSeries.py`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(seasonally_adjust([10, 20, 10, 20], period=2).columns)` | `['value', 'season', 'index', 'adjusted']` |
| `seasonally_adjust([10, 20, 10, 20], period=2).shape` | `(4, 4)` |
| `round(float(seasonally_adjust([10, 20, 10, 20], period=2).loc[0, "adjusted"]), 4)` | `15.0` |
| `round(float(seasonally_adjust([10, 20, 10, 20], period=2).loc[1, "adjusted"]), 4)` | `15.0` |
| `float(seasonally_adjust([10, 20, 10, 20], period=2, kind="additive").loc[0, "adjusted"])` | `15.0` |
