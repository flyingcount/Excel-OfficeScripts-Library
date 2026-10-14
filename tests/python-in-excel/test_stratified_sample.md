# Test: stratified_sample

## Setup

1. Formulas → **Initialization** → paste `stratified_sample` from `source/python-in-excel/functions/stratified_sample.py` after the default imports → Save. Or paste `init/Sampling.py`.
2. Headers `tier`, `value` in `A1:B1`. Rows: four `A` with values `1, 2, 3, 4` and two `B` with values `5, 6` in `A2:B7`.

Population `N=6`. `A` is 4/6, `B` is 2/6. For `total_n=3`: `A` gets 2 rows, `B` gets 1.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `len(stratified_sample("A1:B7", "tier", 3))` | `3` |
| `int(stratified_sample("A1:B7", "tier", 3)["tier"].value_counts().loc["A"])` | `2` |
| `int(stratified_sample("A1:B7", "tier", 3)["tier"].value_counts().loc["B"])` | `1` |
| `list(stratified_sample("A1:B7", "tier", 3).columns)` | `['tier', 'value']` |
| `len(stratified_sample("A1:B7", "tier", 100))` | `6` |
| `len(stratified_sample("A1:B7", "Tier", 3))` | `3` |
| `stratified_sample("A1:B7", "tier", 3).equals(stratified_sample("A1:B7", "tier", 3, 42))` | `True` |
| `len(stratified_sample(pd.DataFrame({"tier": ["A", "A", "A", "A", "B", "B"], "value": [1, 2, 3, 4, 5, 6]}), "tier", 3))` | `3` |
