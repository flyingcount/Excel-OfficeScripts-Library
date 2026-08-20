# Python in Excel map

Inventory of reusable Python functions. Add a row when you add a file under `source/python-in-excel/functions/`.

| Name | File | Call | Notes |
|------|------|------|--------|
| `xl_df` | `source/python-in-excel/functions/xl_df.py` | `xl_df("Table1[#All]")` | DataFrame from a range, table, or name. Drops all-empty rows. |
| `describe` | `source/python-in-excel/functions/describe.py` | `describe("A1:D20")` | pandas `describe()`. Accepts a ref string or a DataFrame. |
| `corr` | `source/python-in-excel/functions/corr.py` | `corr("A1:D20")` | Numeric correlation matrix. `method` pearson / kendall / spearman. |
| `expsmooth` | `source/python-in-excel/functions/expsmooth.py` | `expsmooth("A1:A3")` | Last SES value, default α 0.2. Matches LAMBDA `EXPSMOOTH`. |
| `stl` | `source/python-in-excel/functions/stl.py` | `stl("A1:A24", 12)` | STL trend / seasonal / resid table. See [docs/python/stl.md](python/stl.md). |
| `stl_plot` | `source/python-in-excel/functions/stl_plot.py` | `stl_plot("A1:A24", 12)` | Same fit as `stl`, as `DecomposeResult.plot()`. See [docs/python/stl_plot.md](python/stl_plot.md). |
| `resid_analysis` | `source/python-in-excel/functions/resid_analysis.py` | `resid_analysis("C2:C25")` | Residual diagnostics table, or `plot=True` for vs-order / hist / QQ / ACF. See [docs/python/resid_analysis.md](python/resid_analysis.md). |
| `arima_order` | `source/python-in-excel/functions/arima_order.py` | `arima_order("A1:A50")` | AIC grid search for ARIMA(p, d, q). See [docs/python/arima_order.md](python/arima_order.md). |
