# Test: xl_df

## Setup

1. Formulas → **Initialization** → paste `xl_df` from `source/python-in-excel/functions/xl_df.py` after the default imports → Save.
2. Sheet **Data**: headers in row 1 (`Name`, `Value`), `A2:B4` = `a`, `1` / `b`, `2` / blank row.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `xl_df("A1:B4")` | DataFrame, columns Name and Value, two data rows (`a`/`1`, `b`/`2`); blank row dropped |
| `xl_df("A1:B4").shape` | `(2, 2)` |
| `xl_df("B2:B3", headers=False).iloc[0, 0]` | `1` |
