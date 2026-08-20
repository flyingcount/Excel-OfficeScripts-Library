# Test: stl_plot

## Setup

1. Formulas → **Initialization** → paste `stl_fit` and `stl_plot` from `source/python-in-excel/functions/stl_plot.py` after the default imports → Save.
2. Put two copies of `1` … `12` in `A1:A24` (24 values, period 12).

Keep the PY cell as a **Python object** (not Excel value).

## Cases

| Python | Expected |
|--------|----------|
| `type(stl_plot("A1:A24", 12)).__name__` | `Figure` |
| `len(stl_plot("A1:A24", 12).axes)` | `4` |
| `len(stl_plot("A1:A24", 12, robust=True, weights=True).axes)` | `5` |
| `stl_plot([1, 2, 3, 4] * 6, 4).axes[0].get_ylabel().lower()` | contains `observed` |
| `stl_plot([1, 2, 3, 4] * 6, 4).axes[1].get_ylabel().lower()` | contains `trend` |
| `stl_plot([1, 2, 3, 4] * 6, 4).axes[2].get_ylabel().lower()` | contains `season` |
| `stl_plot([1, 2, 3, 4] * 6, 4).axes[3].get_ylabel().lower()` | contains `resid` |
