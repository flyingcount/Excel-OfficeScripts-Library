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
4. Append the `def` and quoted call to **exactly one** library init file, and add a `contents()` row (`function`, brief `description`, `call`) in that same file in the **same change**. Every library init must have `contents()`. Cursor Agent: follow `.cursor/rules/python-in-excel-init-contents.mdc`.
   - **Sampling** (names often end in `_sample`) → `init/Sampling.py` only. Follow `.cursor/rules/python-in-excel-sampling.mdc`. `cluster_prep` is not a sampler.
   - **Time series** → `init/TimeSeries.py` only. Follow `.cursor/rules/python-in-excel-timeseries.mdc`. `describe`, `corr`, `normality_check`, `cluster_prep`, `detect_mixed_data_anomalies`, `rank_feature_importance`, `check_collinearity`, `confusion_matrix`, `classification_metrics`, `find_optimal_threshold`, and SPC functions are not time series.
   - **SPC** (control charts / process limits) → `init/SPC.py` only. Follow `.cursor/rules/python-in-excel-spc.mdc`.
   - **Otherwise general** → `init/PaulPythonLibrary.py` only. Paul holds functions that do not belong in another collection. If you later create a new collection init, move matching functions out of Paul into that file.
5. Do **not** duplicate the same public `def` across Paul and a specialized init.
6. Add a row to [PythonMap.md](PythonMap.md) and the README Python in Excel table.
7. Add a short note under **Added** in `CHANGELOG.md`.
8. Add `tests/python-in-excel/test_name.md` with a grid of PY-cell inputs and expected results.
9. If the function needs more than a one-line description, add `docs/python/name.md` and link it from [PythonMap.md](PythonMap.md).
10. Copy any new helper into `source/python-in-excel/shared/` and into the function file (no `import` from this repo), and into the one init file that owns that collection.
## Install in Excel

Python in Excel is Microsoft 365 only.

**General (preferred for mixed/non-series work):** Formulas → **Initialization** → replace the editor with `source/python-in-excel/init/PaulPythonLibrary.py` → Save. That paste is Excel defaults plus **general** functions only (`xl_df`, `describe`, `corr`, normality helpers, `cluster_prep`, `outlier_flag`, `detect_mixed_data_anomalies`, …). It does **not** include time series, sampling, or SPC. Then in a PY cell: `describe("Table1[#All]")`. Call `contents()` to spill names, descriptions, and call signatures.

**Sampling only:** paste `source/python-in-excel/init/Sampling.py` instead. That file is Excel defaults plus sampling functions (`stratified_sample`, `systematic_sample`, `two_stage_cluster_sample`, `reservoir_sample`, and any later samplers). `contents()` lists only the sampling functions.

**Time series only:** paste `source/python-in-excel/init/TimeSeries.py` instead. That file is Excel defaults plus time series functions (`expsmooth`, `stl`, `stl_plot`, `resid_analysis`, `acf_ljungbox`, `acf_pacf`, `adf_test`, `fft_spectrum`, `arima_order`, `arima_estimate`, `baseline_forecast`, `forecast_metrics`, `zscore_replace`, `date_features`, `lag_features`, `lead_features`, `fourier_features`, `difference`, `impute`, `seasonal_indices`, `seasonally_adjust`, `kpss_test`, `ets_forecast`, `arima_forecast`, `sarima_forecast`, `rolling_cv`, `detect_anomalies`, `breakpoints`, `forecast_plot`, and any later series tools). `contents()` lists only the time series functions.

**SPC only:** paste `source/python-in-excel/init/SPC.py` instead. That file is Excel defaults plus SPC functions (`xmr_spc` and any later control-chart tools). `contents()` lists only the SPC functions.

Init pastes are partitioned: a function lives in one of Paul, Sampling, TimeSeries, or SPC — not in Paul and a specialized file. For series work use `TimeSeries.py`; for sampling use `Sampling.py`; for control charts use `SPC.py`.
**One function:** paste that file’s `def` into Initialization after the default imports, or into a Python cell above and to the left of the cells that call it.

Excel limits for a pasted PY cell (`functions/*.py`):

| Limit | Maximum |
|-------|---------|
| Formula text | 8,192 characters (the whole function file) |
| Function arguments | 255 |
| Nested Excel functions | 64 levels |
| Cell value | 32,767 characters (each spilled cell) |

`init/PaulPythonLibrary.py`, `init/Sampling.py`, `init/TimeSeries.py`, and `init/SPC.py` can exceed 8,192 characters because they are Initialization, not a cell formula. Details: `.cursor/rules/python-in-excel-limits.mdc`.

**One-shot:** in a PY cell, paste a call such as `describe(xl("A1:D20", headers=True))` without installing the library.

Switch the cell to **Excel value** if the result should spill into the grid.

## Restore default Initialization

Excel’s default Initialization is stored at `source/python-in-excel/init/DefaultInitialization.py` (`numpy`, `pandas`, `matplotlib`, `seaborn`, `statsmodels`, `excel`, `warnings`, and the `xl` scalar/array conversion settings).

If those imports were deleted or edited:

1. Formulas → **Initialization**.
2. Select all in the editor and paste `DefaultInitialization.py`.
3. Save.

To restore defaults **and** general library functions in one step, paste `PaulPythonLibrary.py`. For sampling only, paste `Sampling.py`. For time series only, paste `TimeSeries.py`. For SPC only, paste `SPC.py`. Do not wrap these files in `=PY(...)`.

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
