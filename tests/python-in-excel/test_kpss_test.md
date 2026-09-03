# Test: kpss_test

## Setup

1. Formulas → **Initialization** → paste `kpss_test` from `source/python-in-excel/functions/kpss_test.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Optional: alternating series `[1, -1] * 12` (level-stationary). Trending `list(range(1, 25))` often rejects H0.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(kpss_test([1, -1] * 12).columns)` | `['metric', 'value', 'guidance']` |
| `"stationary" in set(kpss_test([1, -1] * 12)["metric"])` | `True` |
| `int(kpss_test([1, -1] * 12).set_index("metric").loc["n", "value"])` | `24` |
| `float(kpss_test([1, -1] * 12).set_index("metric").loc["alpha", "value"])` | `0.05` |
| `int(kpss_test([1, -1] * 12).set_index("metric").loc["stationary", "value"])` | `1` |
| `kpss_test([1, 2, 3])` | `#PYTHON!` — `Need at least 8 observations.` |
