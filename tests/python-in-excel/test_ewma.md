# Test: ewma

## Setup

1. Formulas → **Initialization** → paste `ewma` from `source/python-in-excel/functions/ewma.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put `10, 12, 11, 13, 12` in `A1:A5`.

n=5, x̄=11.6, MR̄=1.5, σ=MR̄/1.128. λ=0.2, L=3. First EWMA = 0.2×10 + 0.8×11.6 = 11.28. First UCL≈12.40, LCL≈10.80. No outliers.

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

```python
vals = [10, 12, 11, 13, 12]
```

| Python | Expected |
|--------|----------|
| `list(ewma("A1:A5").columns)` | `['t', 'value', 'ewma', 'cl', 'ucl', 'lcl', 'is_outlier']` |
| `ewma("A1:A5").shape` | `(5, 7)` |
| `round(float(ewma(vals)["cl"].iloc[0]), 1)` | `11.6` |
| `round(float(ewma(vals)["ewma"].iloc[0]), 2)` | `11.28` |
| `round(float(ewma(vals)["ucl"].iloc[0]), 2)` | `12.40` |
| `round(float(ewma(vals)["lcl"].iloc[0]), 2)` | `10.80` |
| `ewma(vals)["is_outlier"].sum()` | `0.0` |
| `float(ewma([5, 5, 5])["ucl"].iloc[0])` | `5.0` |
| `type(ewma(vals, plot=True)).__name__` | `Figure` |
| `len(ewma(vals, plot=True).axes)` | `1` |
| `ewma(vals, plot=True, title="Test")._suptitle.get_text()` | `Test` |
| `ewma([1])` | `#PYTHON!` — `Need at least 2 numeric values.` |
| `ewma(vals, lambda_=0)` | `#PYTHON!` — `lambda_ must be in (0, 1].` |
| `ewma(vals, l=0)` | `#PYTHON!` — `l must be > 0.` |
