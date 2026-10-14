# Test: check_collinearity

## Setup

1. Formulas → **Initialization** → paste `check_collinearity` from `source/python-in-excel/functions/check_collinearity.py` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.
2. Headers `a`, `b`, `c` in `A1:C1`.
3. Rows in `A2:C9`: `a` = `1`…`8`; `b` = `2,4,6,8,10,12,14,16`; `c` = `0,1,0,1,0,1,0,1`.

`b` is `2 * a`, so Pearson r(`a`,`b`) = 1 and VIF for `a` and `b` is infinite. `c` is weakly related to `a`/`b`.

## Cases

In a PY cell, set output to **Excel value**.

```python
df = pd.DataFrame({
    "a": [1, 2, 3, 4, 5, 6, 7, 8],
    "b": [2, 4, 6, 8, 10, 12, 14, 16],
    "c": [0, 1, 0, 1, 0, 1, 0, 1],
})
```

### Shape and flags (A1:C9)

| Python | Expected |
|--------|----------|
| `list(check_collinearity("A1:C9").columns)` | `['feature', 'vif', 'max_r', 'with', 'n_high', 'flag_corr', 'flag_vif', 'flag']` |
| `set(check_collinearity("A1:C9")["feature"])` | `{'a', 'b', 'c'}` |
| `check_collinearity("A1:C9").shape` | `(3, 8)` |
| `float(check_collinearity("A1:C9").set_index("feature").loc["a", "max_r"])` | `1.0` |
| `check_collinearity("A1:C9").set_index("feature").loc["a", "with"]` | `b` |
| `float(check_collinearity("A1:C9").set_index("feature").loc["a", "flag_corr"])` | `1.0` |
| `float(check_collinearity("A1:C9").set_index("feature").loc["a", "flag_vif"])` | `1.0` |
| `float(check_collinearity("A1:C9").set_index("feature").loc["a", "n_high"])` | `1.0` |
| `float(check_collinearity("A1:C9").set_index("feature").loc["c", "flag"])` | `0.0` |
| `not np.isfinite(check_collinearity("A1:C9").set_index("feature").loc["a", "vif"])` | `True` |

### Thresholds and DataFrame input

| Python | Expected |
|--------|----------|
| `float(check_collinearity(df, threshold=0.99).set_index("feature").loc["a", "flag_corr"])` | `1.0` |
| `check_collinearity(df.drop(columns=["b"]))` | `#PYTHON!` — `Need at least 2 numeric columns.` |

### Independent columns

| Python | Expected |
|--------|----------|
| `float(check_collinearity(pd.DataFrame({"x": [0, 0, 0, 1, 1, 1], "y": [0, 1, 0, 1, 0, 1]}))["flag"].sum())` | `0.0` |
| `round(float(check_collinearity(pd.DataFrame({"x": [1, 2, 3, 4, 5, 6], "y": [2, 4, 6, 8, 10, 12]}))["max_r"].iloc[0]), 6)` | `1.0` |

### Edge cases

| Python | Expected |
|--------|----------|
| `check_collinearity(pd.DataFrame({"x": [1, 2], "y": [2, 4]}))` | `#PYTHON!` — `Need at least 3 complete numeric rows.` |
| `check_collinearity(pd.DataFrame({"x": [1, 2, 3, 4], "y": [5, 6, 7, 8]}), threshold=0)` | `#PYTHON!` — `threshold must be in (0, 1].` |
| `check_collinearity(pd.DataFrame({"x": [1, 2, 3, 4], "y": [5, 6, 7, 8]}), vif_threshold=0)` | `#PYTHON!` — `vif_threshold must be > 0.` |
