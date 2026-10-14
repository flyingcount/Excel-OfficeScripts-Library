# Test: xbar_s

## Setup

1. Formulas → **Initialization** → paste `xbar_s` from `source/python-in-excel/functions/xbar_s.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put this value stream in `A1:A20` (four subgroups of 5): `10,12,11,13,10, 11,11,12,10,11, 12,13,12,14,13, 10,11,10,12,11`.
3. Put the same four subgroups as rows in `C1:G4` (no headers).

n=5, k=4. Means 11.2, 11.0, 12.8, 10.8. X̄̄=11.45. Sample S ≈ 1.304, 0.707, 0.831, 0.831; s̄≈0.92. A3≈1.427, B4≈2.089, B3=0. X-bar UCL≈12.76, LCL≈10.14. Subgroup 3 is an X-bar outlier. No S outliers.

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

```python
vals = [
    10, 12, 11, 13, 10,
    11, 11, 12, 10, 11,
    12, 13, 12, 14, 13,
    10, 11, 10, 12, 11,
]
wide = pd.DataFrame([
    [10, 12, 11, 13, 10],
    [11, 11, 12, 10, 11],
    [12, 13, 12, 14, 13],
    [10, 11, 10, 12, 11],
])
```

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(xbar_s("A1:A20", 5).columns)` | `['subgroup', 'n', 'xbar', 's', 'cl', 'ucl', 'lcl', 's_cl', 's_ucl', 's_lcl', 'is_outlier', 'is_s_outlier']` |
| `xbar_s("A1:A20", 5).shape` | `(4, 12)` |
| `xbar_s(vals, 5).shape` | `(4, 12)` |
| `xbar_s(wide, 5).shape` | `(4, 12)` |
| `float(xbar_s(vals, 5)["n"].iloc[0])` | `5.0` |
| `xbar_s(vals + [99], 5).shape[0]` | `4` |

### Limits (n=5)

| Python | Expected |
|--------|----------|
| `round(float(xbar_s(vals, 5)["cl"].iloc[0]), 2)` | `11.45` |
| `round(float(xbar_s(vals, 5)["s_cl"].iloc[0]), 2)` | `0.92` |
| `round(float(xbar_s(vals, 5)["ucl"].iloc[0]), 2)` | `12.76` |
| `round(float(xbar_s(vals, 5)["lcl"].iloc[0]), 2)` | `10.14` |
| `round(float(xbar_s(vals, 5)["s_ucl"].iloc[0]), 2)` | `1.92` |
| `float(xbar_s(vals, 5)["s_lcl"].iloc[0])` | `0.0` |
| `round(float(xbar_s(vals, 5)["xbar"].iloc[2]), 1)` | `12.8` |
| `float(xbar_s(vals, 5)["is_outlier"].iloc[2])` | `1.0` |
| `xbar_s(vals, 5)["is_outlier"].iloc[[0, 1, 3]].sum()` | `0.0` |
| `xbar_s(vals, 5)["is_s_outlier"].sum()` | `0.0` |
| `round(float(xbar_s(wide, 5)["cl"].iloc[0]), 2)` | `11.45` |
| `xbar_s(list(range(22)), 11).shape[0]` | `2` |

### Plot

Leave as a **Python object**.

| Python | Expected |
|--------|----------|
| `type(xbar_s(vals, 5, plot=True)).__name__` | `Figure` |
| `len(xbar_s(vals, 5, plot=True).axes)` | `2` |
| `xbar_s(vals, 5, plot=True, title="Test")._suptitle.get_text()` | `Test` |

### Edge cases

| Python | Expected |
|--------|----------|
| `xbar_s([1, 2, 3], 1)` | `#PYTHON!` — `subgroup_size must be 2 to 25.` |
| `xbar_s([1, 2, 3], 26)` | `#PYTHON!` — `subgroup_size must be 2 to 25.` |
| `xbar_s([1, 2, 3, 4, 5], 5)` | `#PYTHON!` — `Need at least 2 complete subgroups.` |
| `float(xbar_s([5, 5, 5, 5], 2)["ucl"].iloc[0])` | `5.0` |
| `float(xbar_s([5, 5, 5, 5], 2)["s_cl"].iloc[0])` | `0.0` |
