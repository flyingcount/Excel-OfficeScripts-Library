# stl_plot

Four-panel STL chart: **observed**, **trend**, **seasonal**, **resid**. Calls statsmodels `DecomposeResult.plot()`.

Formula: `source/python-in-excel/functions/stl_plot.py`

Same inputs as [stl](stl.md). Use `stl` when you want a spill table; use `stl_plot` when you want the figure.

## Install

Formulas → **Initialization** → paste `stl_fit` and `stl_plot` (or the whole `init/PaulPythonLibrary.py`) after the default imports → Save.

In a PY cell, leave the output as a **Python object** (do not switch to Excel value):

```python
stl_plot("B2:B49", 12)
stl_plot("A1:B49", 12, headers=True)
stl_plot("B2:B49", 12, dates="A2:A49", robust=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, or a date+value range/table. |
| `period` | Yes | Observations per season. `12` monthly, `7` weekly. |
| `dates` | No | Date column when dates are not in `data`. Used as the x-axis. |
| `robust` | No | `True` down-weights outliers. Default `False`. |
| `weights` | No | `True` adds the robust-LOESS weight panel. Use with `robust=True`. |
| `headers` | No | First row is headers when `data` or `dates` is a ref string. Default `False`. |

Need at least two full seasons (`2 * period` points).

## Result

A matplotlib `Figure` with four stacked panels (five if `weights=True`). Python in Excel draws it in the cell.
