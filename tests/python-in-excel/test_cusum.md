# Test: cusum

## Setup

1. Formulas → **Initialization** → paste `cusum` from `source/python-in-excel/functions/cusum.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put eight `10`s then four `20`s in `A1:A12`.

x̄ = 13.333…, σ from MR̄/1.128. Default k=0.5, h=5. The low run turns `is_low` on by the second point. The jump to 20 turns `is_high` on.

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

```python
vals = [10] * 8 + [20] * 4
```

| Python | Expected |
|--------|----------|
| `list(cusum("A1:A12").columns)` | `['t', 'value', 's_high', 's_low', 'h_limit', 'is_high', 'is_low']` |
| `cusum("A1:A12").shape` | `(12, 7)` |
| `float(cusum(vals)["is_low"].iloc[0])` | `0.0` |
| `float(cusum(vals)["is_low"].iloc[1])` | `1.0` |
| `float(cusum(vals)["is_high"].iloc[7])` | `0.0` |
| `float(cusum(vals)["is_high"].iloc[8])` | `1.0` |
| `cusum([5, 5, 5])["s_high"].sum()` | `0.0` |
| `cusum([5, 5, 5])["is_high"].sum()` | `0.0` |
| `type(cusum(vals, plot=True)).__name__` | `Figure` |
| `len(cusum(vals, plot=True).axes)` | `1` |
| `cusum(vals, plot=True, title="Test")._suptitle.get_text()` | `Test` |
| `cusum([1])` | `#PYTHON!` — `Need at least 2 numeric values.` |
| `cusum(vals, k=0)` | `#PYTHON!` — `k must be > 0.` |
| `cusum(vals, h=0)` | `#PYTHON!` — `h must be > 0.` |
