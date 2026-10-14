# Test: u_chart

## Setup

1. Formulas → **Initialization** → paste `u_chart` from `source/python-in-excel/functions/u_chart.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put `10, 12, 8, 15` in `A1:A4` and `50` in each of `B1:B4`.

ū = 45/200 = 0.225. Constant n = 50. UCL ≈ 0.426, LCL ≈ 0.024. No outliers.

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

```python
c = [10, 12, 8, 15]
n = [50, 50, 50, 50]
```

| Python | Expected |
|--------|----------|
| `list(u_chart("A1:A4", "B1:B4").columns)` | `['t', 'defects', 'units', 'u', 'cl', 'ucl', 'lcl', 'is_outlier']` |
| `u_chart("A1:A4", "B1:B4").shape` | `(4, 8)` |
| `round(float(u_chart(c, 50)["cl"].iloc[0]), 3)` | `0.225` |
| `float(u_chart(c, 50)["u"].iloc[0])` | `0.2` |
| `round(float(u_chart(c, 50)["ucl"].iloc[0]), 3)` | `0.426` |
| `round(float(u_chart(c, 50)["lcl"].iloc[0]), 3)` | `0.024` |
| `u_chart(c, 50)["is_outlier"].sum()` | `0.0` |
| `float(u_chart([2, 8, 3], [10, 100, 20])["u"].iloc[0])` | `0.2` |
| `float(u_chart([2, 8, 3], [10, 100, 20])["lcl"].iloc[0])` | `0.0` |
| `round(float(u_chart([2, 8, 3], [10, 100, 20])["ucl"].iloc[0]), 1)` | `0.4` |
| `type(u_chart(c, 50, plot=True)).__name__` | `Figure` |
| `len(u_chart(c, 50, plot=True).axes)` | `1` |
| `u_chart(c, 50, plot=True, title="Test")._suptitle.get_text()` | `Test` |
| `u_chart([1], 10)` | `#PYTHON!` — `Need at least 2 numeric values.` |
| `u_chart([1, -1], 10)` | `#PYTHON!` — `defects must be >= 0.` |
| `u_chart([1, 2], [10, 0])` | `#PYTHON!` — `units must be > 0.` |
