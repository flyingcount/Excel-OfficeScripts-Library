# Test: expsmooth

## Setup

1. Formulas → **Initialization** → paste `expsmooth` from `source/python-in-excel/functions/expsmooth.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put `10`, `12`, `14` in `A1:A3`.
3. Optional: add LAMBDA `EXPSMOOTH` to cross-check.

## Cases

In a PY cell, set output to **Excel value**. Default alpha `0.2`. Result is `11.12` (same as `=EXPSMOOTH(A1:A3)`).

| Python | Expected |
|--------|----------|
| `expsmooth("A1:A3")` | `11.12` |
| `expsmooth("A1:A3", 0.2)` | `11.12` |
| `expsmooth([10, 12, 14])` | `11.12` |
| `expsmooth([10, 12, 14], 1)` | `14` |
