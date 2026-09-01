# Python in Excel map

Inventory of reusable Python functions. Add a row when you add a file under `source/python-in-excel/functions/`. After pasting `init/PaulPythonLibrary.py` or `init/Sampling.py`, call `contents()` in a PY cell to spill the public names and a brief explanation for that Initialization. New public functions in those init files must get a `contents()` row (see `.cursor/rules/python-in-excel-init-contents.mdc`).

| Name | File | Call | Notes |
|------|------|------|--------|
| `xl_df` | `source/python-in-excel/functions/xl_df.py` | `xl_df("Table1[#All]")` | DataFrame from a range, table, or name. Drops all-empty rows. |
| `describe` | `source/python-in-excel/functions/describe.py` | `describe("A1:D20")` | pandas `describe()`. Accepts a ref string or a DataFrame. |
| `corr` | `source/python-in-excel/functions/corr.py` | `corr("A1:D20")` | Numeric correlation matrix. `method` pearson / kendall / spearman. |
| `expsmooth` | `source/python-in-excel/functions/expsmooth.py` | `expsmooth("A1:A3")` | Last SES value, default α 0.2. Matches LAMBDA `EXPSMOOTH`. |
| `stl` | `source/python-in-excel/functions/stl.py` | `stl("A1:A24", 12)` | STL trend / seasonal / resid table. See [docs/python/stl.md](python/stl.md). |
| `stl_plot` | `source/python-in-excel/functions/stl_plot.py` | `stl_plot("A1:A24", 12)` | Same fit as `stl`, as `DecomposeResult.plot()`. See [docs/python/stl_plot.md](python/stl_plot.md). |
| `resid_analysis` | `source/python-in-excel/functions/resid_analysis.py` | `resid_analysis("C2:C25")` | Residual diagnostics table (Ljung-Box, Durbin–Watson, Jarque-Bera, Shapiro–Wilk, z-scored residuals), or `plot=True` for vs-order / hist / QQ / ACF. See [docs/python/resid_analysis.md](python/resid_analysis.md). |
| `normality_check` | `source/python-in-excel/functions/normality_check.py` | `normality_check("A1:A10")` | One paste: Q-Q plot (`normality_check` / `qq_norm`), `shapiro("A1:A10", "pvalue")`, `anderson("A1:A10", "stat")`. See [docs/python/normality_check.md](python/normality_check.md). |
| `arima_order` | `source/python-in-excel/functions/arima_order.py` | `arima_order("A1:A50")` | AIC grid search for ARIMA(p, d, q). See [docs/python/arima_order.md](python/arima_order.md). |
| `zscore_replace` | `source/python-in-excel/functions/zscore_replace.py` | `zscore_replace("A1:A9", z=2)` | Replace points outside a z-score cutoff by interpolation. See [docs/python/zscore_replace.md](python/zscore_replace.md). |
| `cluster_prep` | `source/python-in-excel/functions/cluster_prep.py` | `cluster_prep("A1:D20")` | Scale numeric columns and one-hot encode categoricals for clustering. See [docs/python/cluster_prep.md](python/cluster_prep.md). |
| `stratified_sample` | `source/python-in-excel/functions/stratified_sample.py` | `stratified_sample("A1:D200", "tier", 50)` | Proportional stratified sample. See [docs/python/stratified_sample.md](python/stratified_sample.md). |
| `systematic_sample` | `source/python-in-excel/functions/systematic_sample.py` | `systematic_sample("A1:D200", 50)` | Systematic sample of rows at a regular interval. See [docs/python/systematic_sample.md](python/systematic_sample.md). |
| `two_stage_cluster_sample` | `source/python-in-excel/functions/two_stage_cluster_sample.py` | `two_stage_cluster_sample("A1:D200", "school", 5, 10)` | Two-stage cluster sample. See [docs/python/two_stage_cluster_sample.md](python/two_stage_cluster_sample.md). |
| `reservoir_sample` | `source/python-in-excel/functions/reservoir_sample.py` | `reservoir_sample("A1:D2000", 50)` | Algorithm R reservoir sample of rows. See [docs/python/reservoir_sample.md](python/reservoir_sample.md). |
