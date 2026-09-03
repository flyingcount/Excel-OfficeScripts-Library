# Changelog

All notable changes to this library are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Changed
- `expsmooth` — spills actuals plus an `h`-step SES forecast (default 12) with `lower`/`upper` prediction intervals (`level=0.95`). `plot=True` returns a chart. Future steps are flat at the last level (same as LAMBDA `EXPSMOOTH`). Docs: `docs/python/expsmooth.md`.
- `ets_forecast` — same interval columns and `plot=True` chart as `expsmooth`. Interval uses Hyndman additive-error `v_h` around the Holt-Winters point forecast. Docs: `docs/python/ets_forecast.md`.

### Fixed
- `ets_forecast` — `trend="mul"` / `seasonal="mul"` no longer fail with “endog must be strictly positive” when the series has zeros or blank-as-zero Excel cells. Those points are linearly interpolated for the fit. Docs: `docs/python/ets_forecast.md`.
- `init/PaulPythonLibrary.py` is now the **general** init only. Time series and sampling functions were removed from it (they live only in `init/TimeSeries.py` and `init/Sampling.py`). Init pastes no longer duplicate functions. Cursor rules updated: put each new public `def` in exactly one init file; when creating a new collection init, move matching functions out of Paul.

### Added
- `forecast_plot` — chart of actuals, point forecast, and optional lower/upper interval. Docs: `docs/python/forecast_plot.md`.
- `fourier_features` — sine/cosine Fourier terms for a seasonal period. Docs: `docs/python/fourier_features.md`.
- `difference` — regular or seasonal differencing. Docs: `docs/python/difference.md`.
- `impute` — fill blanks (linear, ffill, bfill, mean, median, seasonal). Docs: `docs/python/impute.md`.
- `seasonal_indices` / `seasonally_adjust` — seasonal index table and seasonally adjusted series. Docs: `docs/python/seasonal_indices.md`, `docs/python/seasonally_adjust.md`.
- `kpss_test` — KPSS stationarity test. Docs: `docs/python/kpss_test.md`.
- `ets_forecast`, `arima_forecast`, `sarima_forecast` — Holt-Winters / ARIMA / SARIMA forecasts with actual + forecast rows. Docs under `docs/python/`.
- `rolling_cv` — walk-forward CV metrics for naive / seasonal naive / drift. Docs: `docs/python/rolling_cv.md`.
- `detect_anomalies` — flag anomalies via STL residual z-score, IQR, or z-score. Docs: `docs/python/detect_anomalies.md`.
- Cursor rule `.cursor/rules/python-in-excel-init-contents.mdc` — hard rule: every library init file must have `contents()`; update `contents()` in the same change whenever a public function is added; Paul is general-only; `DefaultInitialization.py` stays defaults-only (no `contents()`).
- `contents()` in `init/PaulPythonLibrary.py`, `init/Sampling.py`, and `init/TimeSeries.py` — spill a table of public function names, a brief explanation, and the call signature (same as the quoted line after each `def`).
- Repository scaffold for an Excel Office Scripts library (`source/scripts`, shared helpers, script map).
- `ListWorksheets` — write a **Worksheets** sheet with name, visibility, and used range for each worksheet.
- `PaulsFormat` (**Paul's format**) — apply a named custom number format to the selected range.
- `FormatTable` (**Format Table**) — green sheet tab, gridlines, and TableStyleLight14 on the table at the active cell.
- `TableOfContents` (**Table of contents**) — first-tab sheet with numbered hyperlinks to A1 of every other worksheet.
- `HighlightDifferences` (**Highlight Differences**) — conditional formatting on the selection: green `#97FFC6` if `ROUND(cell,2)=0`, else red `#FFBDBD` when `ROUND` of the top-row cell in that column is not 0.
- Lambda library under `source/lambda/functions/`: `ROUND2`, `ISZERO2`, `IFERROR0`.
- Exponential smoothing Lambdas: `EXPSMOOTHWEIGHTS`, `ESMOOTHWEIGHTEDVALUES`, `EXPSMOOTHSERIES`, `EXPSMOOTH` (optional alpha, default 0.2).
- `DDL` — dependent drop-down list from a hierarchy table (up to 10 parent lookups). Docs: `docs/lambda/DDL.md`.
- `DDLSorter` (**DDL Sorter**) — sort a hierarchy table by every column so `DDL` parent paths are contiguous. Docs: `docs/lambda/DDLSorter.md`.
- `DoubleXLookup` — two-way `XMATCH`/`INDEX` lookup with optional `if_not_found` and match/search modes. Docs: `docs/lambda/DoubleXLookup.md`.
- `SuperXLookup` — `XLOOKUP` that returns a whole row (one-column lookup value) or whole column. Docs: `docs/lambda/SuperXLookup.md`.
- `workbook/Paul Lambda function library.xlsx` — git-synced catalog of every `LAMBDA` (sheet **Lambda functions**). Rebuild with `scripts/Build-LambdaWorkbook.ps1`.
- `ActivateLambdaFunctions` (**Activate Lambda functions**) — write selected catalog rows into Name Manager.
- Python in Excel library under `source/python-in-excel/functions/`: `xl_df`, `describe`, `corr`, `expsmooth`. Paste `init/PaulPythonLibrary.py` into **Formulas → Initialization**.
- `stl` — STL seasonal-trend-residual decomposition via statsmodels. Docs: `docs/python/stl.md`.
- `stl_plot` — same STL fit as a four-panel matplotlib chart (`DecomposeResult.plot`). Docs: `docs/python/stl_plot.md`.
- `resid_analysis` — residual diagnostics (VBA Residuals analysis stats plus Ljung-Box, Durbin–Watson, Jarque-Bera, and Shapiro–Wilk; z-scored residual summaries; `plot=True` for vs-order / hist / QQ / ACF). Docs: `docs/python/resid_analysis.md`.
- `arima_order` — AIC grid search for ARIMA(p, d, q). Docs: `docs/python/arima_order.md`.
- `zscore_replace` — replace time-series points outside a z-score cutoff using interpolation. Docs: `docs/python/zscore_replace.md`.
- `date_features` — expand a date column into calendar parts, cyclical sine/cosine encodings (month, day, dayofweek, dayofyear), and a public-holiday flag (`country_holiday='UK'` default, or `'US'`; `None` to disable). Holidays are computed algorithmically — no external package needed. Docs: `docs/python/date_features.md`.
- `outlier_flag` — flag outlier rows using IQR (Tukey fence), MAD, or z-score methods. Returns value, is_outlier, score, lower_bound, upper_bound. Docs: `docs/python/outlier_flag.md`.
- `cluster_prep` — scale numeric columns and one-hot encode categoricals so mixed tables are ready for clustering. Docs: `docs/python/cluster_prep.md`.
- `stratified_sample` — proportional stratified sample from a table by a stratum column. Docs: `docs/python/stratified_sample.md`.
- `systematic_sample` — systematic sample of rows at a regular interval from a random start. Docs: `docs/python/systematic_sample.md`.
- `two_stage_cluster_sample` — two-stage cluster sample (select clusters, then rows within each). Docs: `docs/python/two_stage_cluster_sample.md`.
- `reservoir_sample` — Algorithm R reservoir sample of rows from a table or stream. Docs: `docs/python/reservoir_sample.md`.
- `normality_check` — one pasteable module: Shapiro-Wilk (`shapiro`), Anderson-Darling (`anderson`), and a normal Q-Q plot (`normality_check` / `qq_norm`). Docs: `docs/python/normality_check.md`.
- `init/Sampling.py` — Initialization paste with Excel defaults plus sampling functions only (`stratified_sample`, `systematic_sample`, `two_stage_cluster_sample`, `reservoir_sample`).
- Cursor rule `.cursor/rules/python-in-excel-sampling.mdc` — sampling functions go in `init/Sampling.py` only (not Paul).
- `lag_features` — lag columns, rolling-window statistics (mean, std, min, max, median, sum), and EMA from a value series; rolling and EMA use past values only. Docs: `docs/python/lag_features.md`.
- `forecast_metrics` — MAE, RMSE, MAPE, MASE, and related accuracy scores from user-named actual and forecast columns. Docs: `docs/python/forecast_metrics.md`.
- `fft_spectrum` — real FFT periodogram (cycles, frequency, period, power) as a table or two-panel chart. Docs: `docs/python/fft_spectrum.md`.
- `adf_test` — Augmented Dickey–Fuller unit-root test for stationarity (p-value, critical values, `stationary` flag). Docs: `docs/python/adf_test.md`.
- `acf_pacf` — sample ACF and PACF as a table (`plot=False`) or a two-panel chart (`plot=True`). Docs: `docs/python/acf_pacf.md`.
- `acf_ljungbox` — sample ACF and Ljung-Box Q at each lag (default 20), with Bartlett bands and significance flags. Docs: `docs/python/acf_ljungbox.md`.
- `baseline_forecast` — naive, seasonal naive, or drift baseline forecast with configurable horizon. Docs: `docs/python/baseline_forecast.md`.
- `arima_estimate` — estimate ARIMA(p,d,q) using ADF-based differencing and AIC/BIC grid search. Returns p, d, q, aic, bic, adf_pvalue; `full=True` spills the entire grid. Docs: `docs/python/arima_estimate.md`.
- `init/TimeSeries.py` — Initialization paste with Excel defaults plus time series functions only (`expsmooth`, `stl`, `stl_plot`, `resid_analysis`, `acf_ljungbox`, `acf_pacf`, `adf_test`, `fft_spectrum`, `arima_order`, `arima_estimate`, `baseline_forecast`, `forecast_metrics`, `zscore_replace`, `date_features`, `lag_features`, `fourier_features`, `difference`, `impute`, `seasonal_indices`, `seasonally_adjust`, `kpss_test`, `ets_forecast`, `arima_forecast`, `sarima_forecast`, `rolling_cv`, `detect_anomalies`, `forecast_plot`).
- Cursor rule `.cursor/rules/python-in-excel-timeseries.mdc` — time series functions go in `init/TimeSeries.py` only (not Paul).
- Cursor rule `.cursor/rules/python-in-excel.mdc` — pattern for adding Python in Excel PY-cell functions.
- Cursor rule `.cursor/rules/python-in-excel-limits.mdc` — Excel formula/cell limits (8,192 formula characters, 255 arguments, 64 nest levels, 32,767 characters per cell) for `source/python-in-excel/**/*.py`.
- Excel default Python Initialization snapshot (`init/DefaultInitialization.py`). Library init pastes include those imports so a full paste restores defaults and that collection.

### Changed
- `baseline_forecast` — reads `date_col` and `value_col` from a table, spills actual rows then forecast rows with `date`, `value`, and `label` (`Actual`, `Forecast Naive`, `Forecast Seasonal Naive`, `Forecast Drift`). Forecast dates extend from the last observed date.
- `resid_analysis` — Durbin–Watson, Shapiro–Wilk, and z-scored residual summaries (`std_resid_max_abs`, `n_std_resid_gt_2`; `.std_resid` on the table and figure). Existing metric rows keep their names and order.
- `resid_analysis` — metric table spills a third `guidance` column with how to interpret each row. `metric` and `value` are unchanged.
- `normality_check` / `shapiro` / `anderson` spilled tables include an `interpretation` column. `metric` and `value` are unchanged.
- Compacted `normality_check.py` and `resid_analysis.py` so each file stays under the 8192-character Python in Excel formula limit.
- `anderson` interpretation text says whether the data is normal from A^2 vs the critical value, instead of "reject normality".
- Highlight Differences rules are now `=ROUND(Q11,2)=0` (green) and `=ROUND(Q$11,2)<>0` (red), where Q11 is the top-left of the selection.
- Split source into `source/office-scripts/` and `source/lambda/`. Office Script tests moved to `tests/office-scripts/`.
- Python in Excel function files end with a quoted call so a pasted PY cell displays the signature for reuse.
