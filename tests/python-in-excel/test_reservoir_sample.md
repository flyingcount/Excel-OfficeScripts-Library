# Test: reservoir_sample

## Setup

1. Formulas → **Initialization** → paste `reservoir_sample` from `source/python-in-excel/functions/reservoir_sample.py` after the default imports → Save. Or paste `init/Sampling.py`.
2. Header `x` in `A1`. Values `1` through `10` in `A2:A11`.
3. Headers `x`, `y` in `C1:D1`. `x` is `1` through `10` in `C2:C11`. `y` is `10` through `100` step `10` in `D2:D11`.

Population `N=10`. Algorithm R: if `k` is 10 or more, the result is every row in order. If `k` is 3, the result has 3 rows whose `x` values are a subset of `1..10`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `len(reservoir_sample("A1:A11", 3))` | `3` |
| `len(reservoir_sample("A1:A11", 10))` | `10` |
| `reservoir_sample("A1:A11", 10)["x"].tolist()` | `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]` |
| `len(reservoir_sample("A1:A11", 20))` | `10` |
| `set(reservoir_sample("A1:A11", 3)["x"]).issubset(set(range(1, 11)))` | `True` |
| `list(reservoir_sample("C1:D11", 4).columns)` | `['x', 'y']` |
| `reservoir_sample("A1:A11", 3).equals(reservoir_sample("A1:A11", 3, 42))` | `True` |
| `len(reservoir_sample(list(range(10)), 4, headers=False))` | `4` |
| `reservoir_sample(pd.DataFrame({"x": list(range(10))}), 10)["x"].tolist()` | `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]` |
