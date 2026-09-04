# Test: np_chart

## Setup

1. Formulas → **Initialization** → paste `np_chart` from `source/python-in-excel/functions/np_chart.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put `5, 8, 3, 20` in `A1:A4`.

p̄ = 0.18, n = 50, np̄ = 9. UCL ≈ 17.15, LCL = 0. The last count (20) is above UCL.

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

```python
d = [5, 8, 3, 20]
```

| Python | Expected |
|--------|----------|
| `list(np_chart("A1:A4", 50).columns)` | `['t', 'defectives', 'sample_size', 'cl', 'ucl', 'lcl', 'is_outlier']` |
| `np_chart("A1:A4", 50).shape` | `(4, 7)` |
| `float(np_chart(d, 50)["cl"].iloc[0])` | `9.0` |
| `round(float(np_chart(d, 50)["ucl"].iloc[0]), 2)` | `17.15` |
| `float(np_chart(d, 50)["lcl"].iloc[0])` | `0.0` |
| `float(np_chart(d, 50)["is_outlier"].iloc[3])` | `1.0` |
| `np_chart(d, 50)["is_outlier"].iloc[:3].sum()` | `0.0` |
| `float(np_chart([0, 0, 0], 10)["ucl"].iloc[0])` | `0.0` |
| `type(np_chart(d, 50, plot=True)).__name__` | `Figure` |
| `len(np_chart(d, 50, plot=True).axes)` | `1` |
| `np_chart(d, 50, plot=True, title="Test")._suptitle.get_text()` | `Test` |
| `np_chart([1], 10)` | `#PYTHON!` — `Need at least 2 numeric values.` |
| `np_chart([1, -1], 10)` | `#PYTHON!` — `defectives must be >= 0.` |
| `np_chart([1, 2], [10, 0])` | `#PYTHON!` — `sample_size must be > 0.` |
| `np_chart([1, 12], 10)` | `#PYTHON!` — `defectives cannot exceed sample_size.` |
