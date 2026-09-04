# Test: process_shift_detection

## Setup

1. Formulas → **Initialization** → paste `process_shift_detection` from `source/python-in-excel/functions/process_shift_detection.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put eight `10`s then four `20`s in `A1:A12`.

Default CUSUM matches `cusum`: `is_low` at the second 10; `is_high` at the first 20. EWMA (λ=0.2, L=3) flags the first point low. XmR flags the first 10 as low (below 3σ).

## Cases

In a PY cell, set output to **Excel value**.

```python
vals = [10] * 8 + [20] * 4
cols = ['t', 'value', 'method', 'is_shift', 'is_high', 'is_low']
```

| Python | Expected |
|--------|----------|
| `list(process_shift_detection("A1:A12").columns)` | `['t', 'value', 'method', 'is_shift', 'is_high', 'is_low']` |
| `process_shift_detection("A1:A12").shape` | `(12, 6)` |
| `process_shift_detection(vals)["method"].iloc[0]` | `cusum` |
| `float(process_shift_detection(vals)["is_low"].iloc[0])` | `0.0` |
| `float(process_shift_detection(vals)["is_low"].iloc[1])` | `1.0` |
| `float(process_shift_detection(vals)["is_high"].iloc[7])` | `0.0` |
| `float(process_shift_detection(vals)["is_high"].iloc[8])` | `1.0` |
| `float(process_shift_detection(vals)["is_shift"].iloc[1])` | `1.0` |
| `process_shift_detection(vals, method="ewma")["method"].iloc[0]` | `ewma` |
| `float(process_shift_detection(vals, method="ewma")["is_low"].iloc[0])` | `1.0` |
| `process_shift_detection(vals, method="xmr")["method"].iloc[0]` | `xmr` |
| `float(process_shift_detection(vals, method="xmr")["is_low"].iloc[0])` | `1.0` |
| `process_shift_detection(vals, method="shewhart")["method"].iloc[0]` | `xmr` |
| `process_shift_detection([5, 5, 5])["is_shift"].sum()` | `0.0` |
| `process_shift_detection([1])` | `#PYTHON!` — `Need at least 2 numeric values.` |
| `process_shift_detection(vals, method="chow")` | `#PYTHON!` — `method must be cusum, ewma, or xmr.` |
