# Test: lead_features

## Setup

1. Formulas → **Initialization** → paste `lead_features` from `source/python-in-excel/functions/lead_features.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put `10, 20, 30, 40, 50` in `A1:A5`.

Leads are `y.shift(-k)`. For `10, 20, 30, 40, 50` with `leads=2`: `lead_1` is 20, 30, 40, 50, blank.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(lead_features([10, 20, 30, 40, 50], leads=2).columns)` | `['value', 'lead_1', 'lead_2']` |
| `lead_features([10, 20, 30, 40, 50], leads=2).shape` | `(5, 3)` |
| `list(lead_features([10, 20, 30, 40], leads=1).columns)` | `['value', 'lead_1']` |
| `list(lead_features([10, 20, 30, 40], leads="1,3").columns)` | `['value', 'lead_1', 'lead_3']` |
| `float(lead_features([10, 20, 30, 40, 50], leads=2).loc[0, "lead_1"])` | `20.0` |
| `float(lead_features([10, 20, 30, 40, 50], leads=2).loc[0, "lead_2"])` | `30.0` |
| `pd.isna(lead_features([10, 20, 30, 40, 50], leads=2).loc[4, "lead_1"])` | `True` |
| `lead_features([10, 20], leads=0)` | `#PYTHON!` — `Provide at least one lead.` |
