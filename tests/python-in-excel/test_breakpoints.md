# Test: breakpoints

## Setup

1. Formulas → **Initialization** → paste `breakpoints` from `source/python-in-excel/functions/breakpoints.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Optional: 40 values with a mean shift (`1` twenty times, then `10` twenty times) in `A1:A40`.

## Cases (table)

In a PY cell, set output to **Excel value**. `y = [1]*20 + [10]*20` has a mean break after t=20.

| Python | Expected |
|--------|----------|
| `list(breakpoints([1]*20 + [10]*20).columns)` | `['metric', 'value', 'guidance']` |
| `str(breakpoints([1]*20 + [10]*20).loc[0, "value"])` | `cusum` |
| `str(breakpoints([1]*20 + [10]*20, method="chow", at=20).loc[0, "value"])` | `chow` |
| `float(breakpoints([1]*20 + [10]*20, method="chow", at=20).loc[breakpoints([1]*20 + [10]*20, method="chow", at=20)["metric"]=="pvalue", "value"].iloc[0]) < 0.05` | `True` |
| `str(breakpoints([1]*20 + [10]*20, method="baiperron").loc[0, "value"])` | `baiperron` |
| `float(breakpoints([1]*20 + [10]*20, method="baiperron").loc[breakpoints([1]*20 + [10]*20, method="baiperron")["metric"]=="n_breaks", "value"].iloc[0]) >= 1` | `True` |
| `breakpoints(list(range(9)), method="cusum")` | `#PYTHON!` — `Need at least 10 observations.` |

## Cases (plot)

Leave the PY cell as a **Python object**.

| Python | Expected |
|--------|----------|
| `type(breakpoints([1]*20 + [10]*20, plot=True)).__name__` | `Figure` |
| `len(breakpoints([1]*20 + [10]*20, plot=True).axes)` | `2` |
| `type(breakpoints([1]*20 + [10]*20, method="baiperron", plot=True)).__name__` | `Figure` |
