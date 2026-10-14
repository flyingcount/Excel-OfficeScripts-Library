# Test: xbar_r

## Setup

1. Formulas → **Initialization** → paste `xbar_r` from `source/python-in-excel/functions/xbar_r.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put this value stream in `A1:A20` (four subgroups of 5): `10,12,11,13,10, 11,11,12,10,11, 12,13,12,14,13, 10,11,10,12,11`.
3. Put the same four subgroups as rows in `C1:G4` (no headers).

n=5, k=4. Means 11.2, 11.0, 12.8, 10.8. Ranges 3, 2, 2, 2. X̄̄=11.45, R̄=2.25, A2=0.577, D4=2.114, D3=0. X-bar UCL≈12.75, LCL≈10.15. Subgroup 3 is an X-bar outlier. No R outliers.

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
| `list(xbar_r("A1:A20", 5).columns)` | `['subgroup', 'n', 'xbar', 'r', 'cl', 'ucl', 'lcl', 'r_cl', 'r_ucl', 'r_lcl', 'is_outlier', 'is_r_outlier']` |
| `xbar_r("A1:A20", 5).shape` | `(4, 12)` |
| `xbar_r(vals, 5).shape` | `(4, 12)` |
| `xbar_r(wide, 5).shape` | `(4, 12)` |
| `float(xbar_r(vals, 5)["n"].iloc[0])` | `5.0` |
| `xbar_r(vals + [99], 5).shape[0]` | `4` |

### Limits (n=5)

| Python | Expected |
|--------|----------|
| `round(float(xbar_r(vals, 5)["cl"].iloc[0]), 2)` | `11.45` |
| `round(float(xbar_r(vals, 5)["r_cl"].iloc[0]), 2)` | `2.25` |
| `round(float(xbar_r(vals, 5)["ucl"].iloc[0]), 2)` | `12.75` |
| `round(float(xbar_r(vals, 5)["lcl"].iloc[0]), 2)` | `10.15` |
| `round(float(xbar_r(vals, 5)["r_ucl"].iloc[0]), 2)` | `4.76` |
| `float(xbar_r(vals, 5)["r_lcl"].iloc[0])` | `0.0` |
| `round(float(xbar_r(vals, 5)["xbar"].iloc[2]), 1)` | `12.8` |
| `float(xbar_r(vals, 5)["is_outlier"].iloc[2])` | `1.0` |
| `xbar_r(vals, 5)["is_outlier"].iloc[[0, 1, 3]].sum()` | `0.0` |
| `xbar_r(vals, 5)["is_r_outlier"].sum()` | `0.0` |
| `round(float(xbar_r(wide, 5)["cl"].iloc[0]), 2)` | `11.45` |

### Plot

Leave as a **Python object**.

| Python | Expected |
|--------|----------|
| `type(xbar_r(vals, 5, plot=True)).__name__` | `Figure` |
| `len(xbar_r(vals, 5, plot=True).axes)` | `2` |
| `xbar_r(vals, 5, plot=True, title="Test")._suptitle.get_text()` | `Test` |

### Edge cases

| Python | Expected |
|--------|----------|
| `xbar_r([1, 2, 3], 1)` | `#PYTHON!` — `subgroup_size must be 2 to 10.` |
| `xbar_r([1, 2, 3], 11)` | `#PYTHON!` — `subgroup_size must be 2 to 10.` |
| `xbar_r([1, 2, 3, 4, 5], 5)` | `#PYTHON!` — `Need at least 2 complete subgroups.` |
| `float(xbar_r([5, 5, 5, 5], 2)["ucl"].iloc[0])` | `5.0` |
| `float(xbar_r([5, 5, 5, 5], 2)["r_cl"].iloc[0])` | `0.0` |
