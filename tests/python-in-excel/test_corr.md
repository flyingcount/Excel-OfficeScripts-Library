# Test: corr

## Setup

1. Formulas → **Initialization** → paste `corr` from `source/python-in-excel/functions/corr.py` after the default imports → Save.
2. Headers `X`, `Y` in `A1:B1`. Rows: `(1, 2)`, `(2, 4)`, `(3, 6)` in `A2:B4`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `corr("A1:B4").loc["X", "X"]` | `1` |
| `corr("A1:B4").loc["Y", "Y"]` | `1` |
| `corr("A1:B4").loc["X", "Y"]` | `1` |
| `corr("A1:B4", method="pearson").loc["Y", "X"]` | `1` |
