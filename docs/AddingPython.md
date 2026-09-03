# Adding a Python in Excel function

One reusable function = one file under `source/python-in-excel/functions/`.

Cursor Agent: follow `.cursor/rules/python-in-excel.mdc` (same pattern as the existing PY-cell functions).

## Checklist

1. Add `source/python-in-excel/functions/name.py`. The file name (without extension) should match the Python function name.
2. Use this shape:

   ```python
   # Name: name
   # Description: One line.
   # Parameters: arg1, arg2=default

   def name(arg1, arg2=default):
       """One line."""
       ...

   "name(arg1, arg2=default)"
   ```

   The last line is a quoted call. When the file is pasted into a PY cell, Excel displays that signature so it can be copied into another cell.

3. The paste target is the `def` (and any helpers it needs). Do not wrap it in `=PY(...)`.
4. Append the same `def` and quoted call to `source/python-in-excel/init/PaulPythonLibrary.py`.
5. If it is a sampling function (draws a subset of rows or items; names often end in `_sample`), also append that `def` to `source/python-in-excel/init/Sampling.py`. Cursor Agent: follow `.cursor/rules/python-in-excel-sampling.mdc`. `cluster_prep` is not a sampler.
6. If it is a time series function (ordered series: smoothing, seasonal decomposition, ARIMA, residual diagnostics, outlier replacement on a series), also append that `def` to `source/python-in-excel/init/TimeSeries.py`. Cursor Agent: follow `.cursor/rules/python-in-excel-timeseries.mdc`. `describe`, `corr`, `normality_check`, and `cluster_prep` are not time series.
7. Add a row to [PythonMap.md](PythonMap.md) and the README Python in Excel table.
8. Add a short note under **Added** in `CHANGELOG.md`.
9. Add `tests/python-in-excel/test_name.md` with a grid of PY-cell inputs and expected results.
10. If the function needs more than a one-line description, add `docs/python/name.md` and link it from [PythonMap.md](PythonMap.md).
11. Copy any new helper into `source/python-in-excel/shared/` and into the function file (no `import` from this repo).

## Install in Excel

Python in Excel is Microsoft 365 only.

**Workbook-wide (preferred):** Formulas → **Initialization** → replace the editor with `source/python-in-excel/init/PaulPythonLibrary.py` → Save. That file includes the Excel default imports and the library functions. Then in a PY cell: `describe("Table1[#All]")`.

**Sampling only:** paste `source/python-in-excel/init/Sampling.py` instead. That file is Excel defaults plus sampling functions (`stratified_sample`, `systematic_sample`, `two_stage_cluster_sample`, `reservoir_sample`, and any later samplers). It does not include the rest of the library.

**Time series only:** paste `source/python-in-excel/init/TimeSeries.py` instead. That file is Excel defaults plus time series functions (`expsmooth`, `stl`, `stl_plot`, `resid_analysis`, `arima_order`, `zscore_replace`, `date_features`, and any later series tools). It does not include the rest of the library.

**One function:** paste that file’s `def` into Initialization after the default imports, or into a Python cell above and to the left of the cells that call it.

Excel limits for a pasted PY cell (`functions/*.py`):

| Limit | Maximum |
|-------|---------|
| Formula text | 8,192 characters (the whole function file) |
| Function arguments | 255 |
| Nested Excel functions | 64 levels |
| Cell value | 32,767 characters (each spilled cell) |

`init/PaulPythonLibrary.py`, `init/Sampling.py`, and `init/TimeSeries.py` can exceed 8,192 characters because they are Initialization, not a cell formula. Details: `.cursor/rules/python-in-excel-limits.mdc`.

**One-shot:** in a PY cell, paste a call such as `describe(xl("A1:D20", headers=True))` without installing the library.

Switch the cell to **Excel value** if the result should spill into the grid.

## Restore default Initialization

Excel’s default Initialization is stored at `source/python-in-excel/init/DefaultInitialization.py` (`numpy`, `pandas`, `matplotlib`, `seaborn`, `statsmodels`, `excel`, `warnings`, and the `xl` scalar/array conversion settings).

If those imports were deleted or edited:

1. Formulas → **Initialization**.
2. Select all in the editor and paste `DefaultInitialization.py`.
3. Save.

To restore defaults **and** the library functions in one step, paste `PaulPythonLibrary.py` instead. For sampling functions only, paste `Sampling.py`. For time series functions only, paste `TimeSeries.py`. Do not wrap these files in `=PY(...)`.

## Naming

- Python name: `snake_case` (`xl_df`, `expsmooth`). Avoid names that collide with pandas/numpy (`pd`, `np`, `xl`).
- File: `name.py` matching the function name.
- These are Python callables in PY cells, not Excel worksheet names like `ROUND2`.

## What not to add here

- Office Scripts (use `source/office-scripts/` and [AddingScripts.md](AddingScripts.md))
- Named `LAMBDA` formulas (use `source/lambda/` and [AddingLambdas.md](AddingLambdas.md))
- VBA modules (use [Excel-VBA-Library](https://github.com/flyingcount/Excel-VBA-Library))
- Power Query M (use [PowerQuery-Library](https://github.com/flyingcount/PowerQuery-Library))
- xlwings, PyXLL, or local CPython packages
- Secrets or personal data
