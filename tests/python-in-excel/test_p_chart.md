# Test: p_chart

## Setup

1. Formulas → **Initialization** → paste `p_chart` from `source/python-in-excel/functions/p_chart.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put `5, 8, 3, 20` in `A1:A4` and `50` in each of `B1:B4`.

p̄ = 36/200 = 0.18. n = 50. UCL ≈ 0.343, LCL = 0. The last p = 0.4 is above UCL.

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

```python
d = [5, 8, 3, 20]
```

| Python | Expected |
|--------|----------|
| `list(p_chart("A1:A4", "B1:B4").columns)` | `['t', 'defectives', 'sample_size', 'p', 'cl', 'ucl', 'lcl', 'is_outlier']` |
| `p_chart("A1:A4", "B1:B4").shape` | `(4, 8)` |
| `round(float(p_chart(d, 50)["cl"].iloc[0]), 2)` | `0.18` |
| `float(p_chart(d, 50)["p"].iloc[0])` | `0.1` |
| `round(float(p_chart(d, 50)["ucl"].iloc[0]), 3)` | `0.343` |
| `float(p_chart(d, 50)["lcl"].iloc[0])` | `0.0` |
| `float(p_chart(d, 50)["is_outlier"].iloc[3])` | `1.0` |
| `p_chart(d, 50)["is_outlier"].iloc[:3].sum()` | `0.0` |
| `float(p_chart([0, 0, 0], 10)["ucl"].iloc[0])` | `0.0` |
| `type(p_chart(d, 50, plot=True)).__name__` | `Figure` |
| `len(p_chart(d, 50, plot=True).axes)` | `1` |
| `p_chart(d, 50, plot=True, title="Test")._suptitle.get_text()` | `Test` |
| `p_chart([1], 10)` | `#PYTHON!` — `Need at least 2 numeric values.` |
| `p_chart([1, -1], 10)` | `#PYTHON!` — `defectives must be >= 0.` |
| `p_chart([1, 2], [10, 0])` | `#PYTHON!` — `sample_size must be > 0.` |
| `p_chart([1, 12], 10)` | `#PYTHON!` — `defectives cannot exceed sample_size.` |
