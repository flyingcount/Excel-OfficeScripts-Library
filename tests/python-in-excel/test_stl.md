# Test: stl

## Setup

1. Formulas → **Initialization** → paste `stl` from `source/python-in-excel/functions/stl.py` after the default imports → Save.
2. Put two copies of `1` … `12` in `A1:A24` (24 values, period 12).
3. Optional dates in `B1:B24` (monthly, 24 months).

STL is additive. Need at least two full seasons.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `stl("A1:A24", 12).shape` | `(24, 4)` |
| `list(stl("A1:A24", 12).columns)` | `['observed', 'trend', 'seasonal', 'resid']` |
| `(stl("A1:A24", 12).eval("trend + seasonal + resid") - stl("A1:A24", 12)["observed"]).abs().max() < 1e-8` | `True` |
| `stl("A1:A24", 12)["observed"].iloc[0]` | `1` |
| `stl("A1:A24", 12, dates="B1:B24").shape[1]` | `5` (adds `date`) |
| `stl([1, 2, 3, 4] * 6, 4).shape` | `(24, 4)` |
