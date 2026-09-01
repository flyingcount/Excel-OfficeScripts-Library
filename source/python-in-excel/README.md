# Python in Excel

Each file under `functions/` is one reusable Python function for Microsoft 365 **Python in Excel** (`=PY` cells).

Excel cannot import this folder. Paste a function into **Formulas → Initialization** (workbook-wide) or into a Python cell that runs before the cells that call it. Each function file ends with a quoted call (for example `"arima_order(data, p_max=3, d_max=2, q_max=3, headers=False)"`) so that PY cell displays the signature for copying into another cell.

`init/PaulPythonLibrary.py` is a complete Initialization paste: Excel’s default imports plus every library function. `init/Sampling.py` is the same defaults plus sampling functions only (`stratified_sample`, `systematic_sample`, `two_stage_cluster_sample`, `reservoir_sample`, and later samplers). `init/DefaultInitialization.py` is the Excel default only — use it to restore `numpy` / `pandas` / `matplotlib` / `seaborn` / `statsmodels` / `excel` / `warnings` and the `xl` conversion settings if they were deleted or edited. `shared/` holds fragments you copy into a function file; the Excel Python runtime will not load that folder by itself.

These snippets use Excel’s `xl()` helper and the default initialization imports (`pandas` as `pd`, `numpy` as `np`). They are not a CPython package.
