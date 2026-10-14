# Test: capability_report

## Setup

1. Formulas → **Initialization** → paste `capability_report` from `source/python-in-excel/functions/capability_report.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put `10, 12, 11, 13, 12` in `A1:A5`.

n=5, x̄=11.6, MR̄=1.5, σ_within=MR̄/1.128, σ_overall=√1.3. USL=16, LSL=8. Cpk uses the LSL side (x̄ − LSL = 3.6).

## Cases

In a PY cell, set output to **Excel value**.

```python
vals = [10, 12, 11, 13, 12]
r = capability_report(vals, 16, 8)
```

| Python | Expected |
|--------|----------|
| `list(capability_report("A1:A5", 16, 8).columns)` | `['mean', 'stdev_within', 'stdev_overall', 'cp', 'cpk', 'pp', 'ppk', 'ppm']` |
| `capability_report("A1:A5", 16, 8).shape` | `(1, 8)` |
| `round(float(r["mean"].iloc[0]), 1)` | `11.6` |
| `round(float(r["stdev_within"].iloc[0]), 4)` | `1.3298` |
| `round(float(r["stdev_overall"].iloc[0]), 4)` | `1.1402` |
| `round(float(r["cp"].iloc[0]), 2)` | `1.00` |
| `round(float(r["cpk"].iloc[0]), 2)` | `0.90` |
| `round(float(r["pp"].iloc[0]), 2)` | `1.17` |
| `round(float(r["ppk"].iloc[0]), 2)` | `1.05` |
| `round(float(r["ppm"].iloc[0]), 0)` | `853.0` |
| `float(capability_report([5, 5, 5], 10, 0)["stdev_within"].iloc[0])` | `0.0` |
| `float(capability_report([5, 5, 5], 10, 0)["ppm"].iloc[0])` | `0.0` |
| `pd.isna(capability_report([5, 5, 5], 10, 0)["cp"].iloc[0])` | `True` |
| `capability_report([1], 16, 8)` | `#PYTHON!` — `Need at least 2 numeric values.` |
| `capability_report(vals, 8, 16)` | `#PYTHON!` — `usl must be > lsl.` |
