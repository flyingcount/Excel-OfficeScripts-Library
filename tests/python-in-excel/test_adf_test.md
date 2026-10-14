# Test: adf_test

## Setup

1. Formulas → **Initialization** → paste `adf_test` from `source/python-in-excel/functions/adf_test.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put `1, 2, 3, …, 24` in `A1:A24` (trending / unit-root-like).
3. Optional: mean-reverting series in `B1:B24` such as `1, -1, 1, -1, …`.

Set the PY cell to **Excel value**.

## Cases

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(adf_test("A1:A24").columns)` | `['metric', 'value', 'guidance']` |
| `adf_test("A1:A24").shape` | `(12, 3)` |
| `list(adf_test("A1:A24")["metric"])` | `['n', 'adf_stat', 'pvalue', 'usedlag', 'nobs', 'crit_1', 'crit_5', 'crit_10', 'alpha', 'regression', 'stationary', 'interpretation']` |

### Values

A linear trend typically fails to reject the unit root at 5%.

| Python | Expected |
|--------|----------|
| `int(adf_test("A1:A24").set_index("metric").loc["n", "value"])` | `24` |
| `float(adf_test("A1:A24").set_index("metric").loc["alpha", "value"])` | `0.05` |
| `str(adf_test("A1:A24").set_index("metric").loc["regression", "value"])` | `c` |
| `int(adf_test("A1:A24").set_index("metric").loc["stationary", "value"])` | `0` |
| `float(adf_test("A1:A24").set_index("metric").loc["pvalue", "value"]) > 0.05` | `True` |
| `np.isfinite(adf_test("A1:A24").set_index("metric").loc["adf_stat", "value"])` | `True` |
| `int(adf_test([1, -1] * 12).set_index("metric").loc["stationary", "value"])` | `1` |

### Options

| Python | Expected |
|--------|----------|
| `str(adf_test("A1:A24", regression="ct").set_index("metric").loc["regression", "value"])` | `ct` |
| `float(adf_test("A1:A24", alpha=0.01).set_index("metric").loc["alpha", "value"])` | `0.01` |

### Edge cases

| Python | Expected |
|--------|----------|
| `adf_test([1, 2, 3])` | `#PYTHON!` — `Need at least 4 observations.` |
| `adf_test("A1:A24", regression="foo")` | `#PYTHON!` — `regression must be 'c', 'ct', 'n', or 'ctt'.` |
