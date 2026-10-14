# Test: breakpoints

## Setup

1. Formulas → **Initialization** → paste `breakpoints` from `source/python-in-excel/functions/breakpoints.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Optional: 40 values with a mean shift (`1` twenty times, then `10` twenty times) in `A1:A40`.

## Cases (table)

In a PY cell, set output to **Excel value**. `y = [1]*20 + [10]*20` has a mean break after t=20. No dates → `break_date` is that 1-based t. Only detected breaks are rows (empty table if none).

| Python | Expected |
|--------|----------|
| `list(breakpoints([1]*20 + [10]*20).columns)` | `['break_date', 'confidence', 'type']` |
| `list(breakpoints([1]*20 + [10]*20, method="chow", at=20).columns)` | `['break_date', 'confidence', 'type']` |
| `int(breakpoints([1]*20 + [10]*20, method="chow", at=20)["break_date"].iloc[0])` | `20` |
| `str(breakpoints([1]*20 + [10]*20, method="chow", at=20)["type"].iloc[0])` | `Level shift` |
| `"%" in str(breakpoints([1]*20 + [10]*20, method="chow", at=20)["confidence"].iloc[0])` | `True` |
| `len(breakpoints([1]*20 + [10]*20, method="baiperron")) >= 1` | `True` |
| `str(breakpoints(pd.DataFrame({"Date": pd.date_range("2020-01-01", periods=40, freq="MS"), "y": [1]*20 + [10]*20}), method="chow", at=20)["break_date"].iloc[0])` | `2020-08` |
| `breakpoints(list(range(9)), method="cusum")` | `#PYTHON!` — `Need 10+ observations.` |

## Cases (plot)

Leave the PY cell as a **Python object**.

| Python | Expected |
|--------|----------|
| `type(breakpoints([1]*20 + [10]*20, plot=True)).__name__` | `Figure` |
| `len(breakpoints([1]*20 + [10]*20, plot=True).axes)` | `2` |
| `type(breakpoints([1]*20 + [10]*20, method="baiperron", plot=True)).__name__` | `Figure` |
