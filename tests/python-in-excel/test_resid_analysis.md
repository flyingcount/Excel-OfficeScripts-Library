# Test: resid_analysis

## Setup

1. Formulas → **Initialization** → paste `resid_analysis` from `source/python-in-excel/functions/resid_analysis.py` after the default imports → Save.
2. Put `1`, `2`, `3`, `4`, `5` in `A1:A5`.
3. Optional: 24 seasonal values in `B1:B24` for the `stl` cross-check.

## Cases

Table: set the PY cell to **Excel value**. Plot: leave as a **Python object**.

| Python | Expected |
|--------|----------|
| `resid_analysis("A1:A5").set_index("metric").loc["n", "value"]` | `5` |
| `resid_analysis("A1:A5").set_index("metric").loc["sum", "value"]` | `15` |
| `resid_analysis("A1:A5").set_index("metric").loc["mean", "value"]` | `3` |
| `abs(resid_analysis("A1:A5").set_index("metric").loc["slope_vs_order", "value"] - 1) < 1e-12` | `True` |
| `abs(resid_analysis("A1:A5").set_index("metric").loc["intercept_vs_order", "value"]) < 1e-12` | `True` |
| `abs(resid_analysis("A1:A5").set_index("metric").loc["rsq_vs_order", "value"] - 1) < 1e-12` | `True` |
| `resid_analysis([0, 0, 0, 0]).set_index("metric").loc["n", "value"]` | `4` |
| `resid_analysis(stl([1, 2, 3, 4] * 6, 4)).set_index("metric").loc["n", "value"]` | `24` |
| `type(resid_analysis("A1:A5", plot=True)).__name__` | `Figure` |
| `len(resid_analysis("A1:A5", plot=True).axes)` | at least `4` |
