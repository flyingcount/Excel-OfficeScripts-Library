# Python in Excel map

Inventory of reusable Python functions. Add a row when you add a file under `source/python-in-excel/functions/`. After pasting `init/PaulPythonLibrary.py` or `init/Sampling.py`, call `contents()` in a PY cell to spill the public names, a brief explanation, and the call signature for that Initialization. New public functions in those init files must get a `contents()` row (see `.cursor/rules/python-in-excel-init-contents.mdc`).

| Name | File | Call | Notes |
|------|------|------|--------|
| `xl_df` | `source/python-in-excel/functions/xl_df.py` | `xl_df("Table1[#All]")` | DataFrame from a range, table, or name. Drops all-empty rows. |
| `describe` | `source/python-in-excel/functions/describe.py` | `describe("A1:D20")` | pandas `describe()`. Accepts a ref string or a DataFrame. |
| `corr` | `source/python-in-excel/functions/corr.py` | `corr("A1:D20")` | Numeric correlation matrix. `method` pearson / kendall / spearman. |
| `expsmooth` | `source/python-in-excel/functions/expsmooth.py` | `expsmooth("A1:A3")` | Last SES value, default α 0.2. Matches LAMBDA `EXPSMOOTH`. |
| `stl` | `source/python-in-excel/functions/stl.py` | `stl("A1:A24", 12)` | STL trend / seasonal / resid table. See [docs/python/stl.md](python/stl.md). |
| `stl_plot` | `source/python-in-excel/functions/stl_plot.py` | `stl_plot("A1:A24", 12)` | Same fit as `stl`, as `DecomposeResult.plot()`. See [docs/python/stl_plot.md](python/stl_plot.md). |
| `resid_analysis` | `source/python-in-excel/functions/resid_analysis.py` | `resid_analysis("C2:C25")` | Residual diagnostics table (Ljung-Box, Durbin–Watson, Jarque-Bera, Shapiro–Wilk, z-scored residuals), or `plot=True` for vs-order / hist / QQ / ACF. See [docs/python/resid_analysis.md](python/resid_analysis.md). |
| `acf_ljungbox` | `source/python-in-excel/functions/acf_ljungbox.py` | `acf_ljungbox("A1:A100")` | ACF and Ljung-Box Q at each lag (default 20). See [docs/python/acf_ljungbox.md](python/acf_ljungbox.md). |
| `acf_pacf` | `source/python-in-excel/functions/acf_pacf.py` | `acf_pacf("A1:A100")` | ACF and PACF table, or `plot=True` for a two-panel chart. See [docs/python/acf_pacf.md](python/acf_pacf.md). |
| `adf_test` | `source/python-in-excel/functions/adf_test.py` | `adf_test("A1:A50")` | Augmented Dickey–Fuller stationarity test (p-value, critical values, stationary flag). See [docs/python/adf_test.md](python/adf_test.md). |
| `fft_spectrum` | `source/python-in-excel/functions/fft_spectrum.py` | `fft_spectrum("A1:A48")` | FFT periodogram: cycles, frequency, period, power; `plot=True` for charts. See [docs/python/fft_spectrum.md](python/fft_spectrum.md). |
| `normality_check` | `source/python-in-excel/functions/normality_check.py` | `normality_check("A1:A10")` | One paste: Q-Q plot (`normality_check` / `qq_norm`), `shapiro("A1:A10", "pvalue")`, `anderson("A1:A10", "stat")`. See [docs/python/normality_check.md](python/normality_check.md). |
| `arima_order` | `source/python-in-excel/functions/arima_order.py` | `arima_order("A1:A50")` | AIC grid search for ARIMA(p, d, q). See [docs/python/arima_order.md](python/arima_order.md). |
| `arima_estimate` | `source/python-in-excel/functions/arima_estimate.py` | `arima_estimate("A1:A50")` | ADF-based differencing + AIC/BIC grid search for ARIMA(p,d,q). `full=True` spills the whole grid. See [docs/python/arima_estimate.md](python/arima_estimate.md). |
| `baseline_forecast` | `source/python-in-excel/functions/baseline_forecast.py` | `baseline_forecast("A1:B100", date_col="Date", value_col="Sales")` | Actuals plus appended forecast rows with date, value, and label (`Actual`, `Forecast Naive`, etc.). See [docs/python/baseline_forecast.md](python/baseline_forecast.md). |
| `forecast_metrics` | `source/python-in-excel/functions/forecast_metrics.py` | `forecast_metrics("A1:B50", "Actual", "Forecast")` | MAE, RMSE, MAPE, MASE, and related scores from actual and forecast columns. See [docs/python/forecast_metrics.md](python/forecast_metrics.md). |
| `zscore_replace` | `source/python-in-excel/functions/zscore_replace.py` | `zscore_replace("A1:A9", z=2)` | Replace points outside a z-score cutoff by interpolation. See [docs/python/zscore_replace.md](python/zscore_replace.md). |
| `date_features` | `source/python-in-excel/functions/date_features.py` | `date_features("A2:A400")` | Calendar parts, cyclical sine/cosine encodings, and a public-holiday flag (UK default, or US) from a date column. See [docs/python/date_features.md](python/date_features.md). |
| `lag_features` | `source/python-in-excel/functions/lag_features.py` | `lag_features("A1:B50", value_col="Sales")` | Lag columns, rolling-window statistics, and EMA from a value series. See [docs/python/lag_features.md](python/lag_features.md). |
| `cluster_prep` | `source/python-in-excel/functions/cluster_prep.py` | `cluster_prep("A1:D20")` | Scale numeric columns and one-hot encode categoricals for clustering. See [docs/python/cluster_prep.md](python/cluster_prep.md). |
| `outlier_flag` | `source/python-in-excel/functions/outlier_flag.py` | `outlier_flag("B2:B100")` | Flag outliers by IQR, MAD, or z-score with value, flag, score, and bounds. See [docs/python/outlier_flag.md](python/outlier_flag.md). |
| `stratified_sample` | `source/python-in-excel/functions/stratified_sample.py` | `stratified_sample("A1:D200", "tier", 50)` | Proportional stratified sample. See [docs/python/stratified_sample.md](python/stratified_sample.md). |
| `systematic_sample` | `source/python-in-excel/functions/systematic_sample.py` | `systematic_sample("A1:D200", 50)` | Systematic sample of rows at a regular interval. See [docs/python/systematic_sample.md](python/systematic_sample.md). |
| `two_stage_cluster_sample` | `source/python-in-excel/functions/two_stage_cluster_sample.py` | `two_stage_cluster_sample("A1:D200", "school", 5, 10)` | Two-stage cluster sample. See [docs/python/two_stage_cluster_sample.md](python/two_stage_cluster_sample.md). |
| `reservoir_sample` | `source/python-in-excel/functions/reservoir_sample.py` | `reservoir_sample("A1:D2000", 50)` | Algorithm R reservoir sample of rows. See [docs/python/reservoir_sample.md](python/reservoir_sample.md). |
