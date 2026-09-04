# Test: c_chart

## Setup

1. Formulas → **Initialization** → paste `c_chart` from `source/python-in-excel/functions/c_chart.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put `10, 12, 8, 15, 9, 30` in `A1:A6`.

c̄ = 14, UCL = 14 + 3√14 ≈ 25.22, LCL ≈ 2.78. The 30 is above UCL.

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

```python
vals = [10, 12, 8, 15, 9, 30]
```

| Python | Expected |
|--------|----------|
| `list(c_chart("A1:A6").columns)` | `['t', 'defects', 'cl', 'ucl', 'lcl', 'is_outlier']` |
| `c_chart("A1:A6").shape` | `(6, 6)` |
| `float(c_chart(vals)["cl"].iloc[0])` | `14.0` |
| `round(float(c_chart(vals)["ucl"].iloc[0]), 2)` | `25.22` |
| `round(float(c_chart(vals)["lcl"].iloc[0]), 2)` | `2.78` |
| `float(c_chart(vals)["is_outlier"].iloc[5])` | `1.0` |
| `c_chart(vals)["is_outlier"].iloc[:5].sum()` | `0.0` |
| `float(c_chart([0, 0, 0])["ucl"].iloc[0])` | `0.0` |
| `float(c_chart([0, 0, 0])["lcl"].iloc[0])` | `0.0` |
| `type(c_chart(vals, plot=True)).__name__` | `Figure` |
| `len(c_chart(vals, plot=True).axes)` | `1` |
| `c_chart(vals, plot=True, title="Test")._suptitle.get_text()` | `Test` |
| `c_chart([1])` | `#PYTHON!` — `Need at least 2 numeric values.` |
| `c_chart([1, -1])` | `#PYTHON!` — `defects must be >= 0.` |
