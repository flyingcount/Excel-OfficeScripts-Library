# Test: systematic_sample

## Setup

1. Formulas → **Initialization** → paste `systematic_sample` from `source/python-in-excel/functions/systematic_sample.py` after the default imports → Save. Or paste `init/Sampling.py`.
2. Header `x` in `A1`. Values `1` through `10` in `A2:A11`.
3. Headers `x`, `y` in `C1:D1`. `x` is `1` through `10` in `C2:C11`. `y` is `10` through `100` step `10` in `D2:D11`.

Population `N=10`. For `sample_size=5`, interval `k=2`. Selected `x` values are all odd or all even (random start 0 or 1). `sample_size=10` returns every row in order.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `len(systematic_sample("A1:A11", 5))` | `5` |
| `len(systematic_sample("A1:A11", 10))` | `10` |
| `systematic_sample("A1:A11", 10)["x"].tolist()` | `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` |
| `int(systematic_sample("A1:A11", 5)["x"].diff().dropna().min())` | `2` |
| `int(systematic_sample("A1:A11", 5)["x"].diff().dropna().max())` | `2` |
| `list(systematic_sample("C1:D11", 5).columns)` | `['x', 'y']` |
| `systematic_sample("A1:A11", 5).equals(systematic_sample("A1:A11", 5, 42))` | `True` |
| `len(systematic_sample(list(range(10)), 5, headers=False))` | `5` |
| `systematic_sample(pd.DataFrame({"x": list(range(10))}), 10)["x"].tolist()` | `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]` |
