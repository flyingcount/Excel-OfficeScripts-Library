# Excel Office Scripts, Lambda, and Python Library

Reusable **Excel Office Scripts** (TypeScript), named **LAMBDA** functions, and **Python in Excel** snippets for Excel on the web and Microsoft 365.

Office Scripts live under `source/office-scripts/`. Named formulas live under `source/lambda/`. Python in Excel functions live under `source/python-in-excel/`. Grow each library one file at a time. Do not mix these with the VBA add-in.

Related:

- [Excel-VBA-Library](https://github.com/flyingcount/Excel-VBA-Library) (desktop VBA add-in)
- [PowerQuery-Library](https://github.com/flyingcount/PowerQuery-Library) (Power Query M functions)

## Layout

```text
.
├── README.md
├── CHANGELOG.md
├── LICENSE
├── docs/
│   ├── AddingScripts.md   ← next Automate script
│   ├── AddingLambdas.md   ← next named LAMBDA
│   ├── AddingPython.md    ← next Python in Excel function
│   ├── ScriptMap.md
│   ├── LambdaMap.md
│   └── PythonMap.md
├── source/
│   ├── office-scripts/
│   │   ├── scripts/       ← one TypeScript file per Automate script
│   │   └── shared/        ← helpers to copy into a script
│   ├── lambda/
│   │   ├── functions/     ← one named LAMBDA per file
│   │   └── shared/        ← fragments to copy into a LAMBDA
│   └── python-in-excel/
│       ├── functions/     ← one Python function per file
│       ├── init/          ← PaulPythonLibrary.py, Sampling.py, TimeSeries.py, or DefaultInitialization.py → Formulas → Initialization
│       └── shared/        ← fragments to copy into a function
├── tests/
│   ├── office-scripts/
│   ├── lambda/
│   └── python-in-excel/
├── examples/              ← reference workbooks (not the library)
├── workbook/                ← Paul Lambda function library.xlsx
├── scripts/
│   └── Build-LambdaWorkbook.ps1
└── types/                 ← ExcelScript typings for the editor
```

## Quick start: Office Scripts

Office Scripts in Excel are **one file each**. The Automate editor cannot import other files from this repo.

1. Excel on the web (or desktop with Automate) → **Automate** → **New Script**.
2. Paste the contents of a file from `source/office-scripts/scripts/`.
3. **Save** → **Run**.

Example: `source/office-scripts/scripts/ListWorksheets.ts` writes a **Worksheets** inventory sheet.

## Quick start: Lambda functions

Open `workbook/Paul Lambda function library.xlsx`. Sheet **Lambda functions** lists every named formula.

1. First time: **Automate → New Script** → paste `source/office-scripts/scripts/ActivateLambdaFunctions.ts` (or the **Activate script** sheet) → Save as **Activate Lambda functions**.
2. Select one or more rows in the table (Name / Lambda code / Note).
3. Run **Activate Lambda functions**. Those names appear in Name Manager.
4. On a sheet: `=ROUND2(A1)`.

After you add a `.lambda` file, rebuild the workbook:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/Build-LambdaWorkbook.ps1
```

You can still paste a single `=LAMBDA(...)` into Name Manager by hand. Excel Labs **Advanced Formula Environment** can also store named formulas.

## Quick start: Python in Excel

Microsoft 365 with Python in Excel enabled.

1. Formulas → **Initialization** → paste the init for your work: `init/PaulPythonLibrary.py` (general), `init/Sampling.py` (sampling), or `init/TimeSeries.py` (time series) → Save. These pastes do not overlap — series and sampling functions are not in Paul.
2. Insert a Python cell (**Formulas → Insert Python**, or `=PY`).
3. Call a function from that paste, for example `describe("Table1[#All]")` (Paul) or `stl_plot("A1:A24", 12)` (TimeSeries). Call `contents()` for names, descriptions, and call signatures in that Initialization.
4. Set the cell output to **Excel value** if a table should spill into the grid. Leave a **Python object** for charts such as `stl_plot`.

If the default imports were deleted or edited, paste `source/python-in-excel/init/DefaultInitialization.py` into **Initialization** and Save. Then paste the library init you need (or paste only from the first `def` onward if the defaults are already there).

You can paste a single file from `source/python-in-excel/functions/` instead of the whole init module.

## Scripts

| Script | File | What it does |
|--------|------|----------------|
| List worksheets | `source/office-scripts/scripts/ListWorksheets.ts` | Sheet name, visibility, used range |
| Paul's format | `source/office-scripts/scripts/PaulsFormat.ts` | Number format on the selection (0dp / 2dp / colour / k / m / dates) |
| Format Table | `source/office-scripts/scripts/FormatTable.ts` | Green tab, gridlines, TableStyleLight14 on the table at the active cell |
| Table of contents | `source/office-scripts/scripts/TableOfContents.ts` | First-tab sheet with hyperlinks to every other worksheet |
| Highlight Differences | `source/office-scripts/scripts/HighlightDifferences.ts` | Green/red fill on the selection: ROUND to 2 d.p. equal to zero vs not |
| Activate Lambda functions | `source/office-scripts/scripts/ActivateLambdaFunctions.ts` | Write selected rows from **Lambda functions** into Name Manager |

See [docs/ScriptMap.md](docs/ScriptMap.md). Add scripts with [docs/AddingScripts.md](docs/AddingScripts.md).

## Lambda functions

| Name | File | What it does |
|------|------|----------------|
| `ROUND2` | `source/lambda/functions/ROUND2.lambda` | Round to two decimal places |
| `ISZERO2` | `source/lambda/functions/ISZERO2.lambda` | TRUE if the value rounds to 0 at 2 d.p. |
| `IFERROR0` | `source/lambda/functions/IFERROR0.lambda` | Value, or 0 on error |
| `EXPSMOOTHWEIGHTS` | `source/lambda/functions/EXPSMOOTHWEIGHTS.lambda` | Exponential-smoothing weights (default α 0.2) |
| `ESMOOTHWEIGHTEDVALUES` | `source/lambda/functions/ESMOOTHWEIGHTEDVALUES.lambda` | Values times SES weights |
| `EXPSMOOTHSERIES` | `source/lambda/functions/EXPSMOOTHSERIES.lambda` | Full simple exponential smoothing series |
| `EXPSMOOTH` | `source/lambda/functions/EXPSMOOTH.lambda` | Last SES smoothed value |
| `DDL` | `source/lambda/functions/DDL.lambda` | Dependent drop-down list from a hierarchy table |
| `DDLSorter` | `source/lambda/functions/DDLSorter.lambda` | Sort a hierarchy table by every column (DDL Sorter) |
| `DoubleXLookup` | `source/lambda/functions/DoubleXLookup.lambda` | Two-way XMATCH/INDEX lookup |
| `SuperXLookup` | `source/lambda/functions/SuperXLookup.lambda` | XLOOKUP that returns a whole row or column |

See [docs/LambdaMap.md](docs/LambdaMap.md). Add functions with [docs/AddingLambdas.md](docs/AddingLambdas.md).

## Python in Excel

| Name | File | What it does |
|------|------|----------------|
| `xl_df` | `source/python-in-excel/functions/xl_df.py` | Load a range, table, or name as a DataFrame |
| `describe` | `source/python-in-excel/functions/describe.py` | pandas summary statistics |
| `corr` | `source/python-in-excel/functions/corr.py` | Numeric correlation matrix |
| `expsmooth` | `source/python-in-excel/functions/expsmooth.py` | SES forecast with prediction interval, or `plot=True` for a chart |
| `stl` | `source/python-in-excel/functions/stl.py` | STL seasonal-trend-residual decomposition |
| `stl_plot` | `source/python-in-excel/functions/stl_plot.py` | STL four-panel chart (`DecomposeResult.plot`) |
| `resid_analysis` | `source/python-in-excel/functions/resid_analysis.py` | Residual diagnostics (table, or `plot=True` for charts) |
| `acf_ljungbox` | `source/python-in-excel/functions/acf_ljungbox.py` | ACF and Ljung-Box Q at each lag (default 20) |
| `acf_pacf` | `source/python-in-excel/functions/acf_pacf.py` | ACF and PACF table, or `plot=True` for charts |
| `adf_test` | `source/python-in-excel/functions/adf_test.py` | Augmented Dickey–Fuller test for stationarity |
| `fft_spectrum` | `source/python-in-excel/functions/fft_spectrum.py` | FFT periodogram (cycles, frequency, period, power; or plot) |
| `normality_check` | `source/python-in-excel/functions/normality_check.py` | Q-Q plot plus Shapiro-Wilk and Anderson-Darling (one paste) |
| `arima_order` | `source/python-in-excel/functions/arima_order.py` | AIC grid search for ARIMA(p, d, q) |
| `arima_estimate` | `source/python-in-excel/functions/arima_estimate.py` | ADF + AIC/BIC grid search for ARIMA(p, d, q) |
| `baseline_forecast` | `source/python-in-excel/functions/baseline_forecast.py` | Actuals plus appended forecast with date/value labels |
| `forecast_metrics` | `source/python-in-excel/functions/forecast_metrics.py` | MAE, RMSE, MAPE, MASE from actual and forecast columns |
| `zscore_replace` | `source/python-in-excel/functions/zscore_replace.py` | Replace points outside a z-score cutoff by interpolation |
| `date_features` | `source/python-in-excel/functions/date_features.py` | Calendar parts, cyclical sine/cosine encodings, and public-holiday flag |
| `lag_features` | `source/python-in-excel/functions/lag_features.py` | Lag columns, rolling-window statistics, and EMA from a value series |
| `lead_features` | `source/python-in-excel/functions/lead_features.py` | Lead columns from a value series |
| `fourier_features` | `source/python-in-excel/functions/fourier_features.py` | Sine/cosine Fourier terms for a seasonal period |
| `difference` | `source/python-in-excel/functions/difference.py` | Regular or seasonal differencing |
| `impute` | `source/python-in-excel/functions/impute.py` | Fill blanks in a series |
| `seasonal_indices` | `source/python-in-excel/functions/seasonal_indices.py` | Seasonal index per slot |
| `seasonally_adjust` | `source/python-in-excel/functions/seasonally_adjust.py` | Remove seasonal index from a series |
| `kpss_test` | `source/python-in-excel/functions/kpss_test.py` | KPSS stationarity test |
| `ets_forecast` | `source/python-in-excel/functions/ets_forecast.py` | Holt-Winters ETS forecast with prediction interval, or `plot=True` for a chart |
| `arima_forecast` | `source/python-in-excel/functions/arima_forecast.py` | ARIMA(p,d,q) forecast |
| `sarima_forecast` | `source/python-in-excel/functions/sarima_forecast.py` | Seasonal ARIMA forecast with prediction interval, or `plot=True` for a chart |
| `rolling_cv` | `source/python-in-excel/functions/rolling_cv.py` | Walk-forward CV for baseline methods |
| `detect_anomalies` | `source/python-in-excel/functions/detect_anomalies.py` | Flag series anomalies (STL, IQR, z-score) |
| `breakpoints` | `source/python-in-excel/functions/breakpoints.py` | Chow, CUSUM, or Bai-Perron structural breaks, or `plot=True` for a chart |
| `forecast_plot` | `source/python-in-excel/functions/forecast_plot.py` | Chart of actuals, forecast, and optional interval |
| `cluster_prep` | `source/python-in-excel/functions/cluster_prep.py` | Scale numbers and one-hot encode categories for clustering |
| `outlier_flag` | `source/python-in-excel/functions/outlier_flag.py` | Flag outliers by IQR, MAD, z-score, STL residuals, or Isolation Forest |
| `stratified_sample` | `source/python-in-excel/functions/stratified_sample.py` | Proportional stratified sample from a table |
| `systematic_sample` | `source/python-in-excel/functions/systematic_sample.py` | Systematic sample of rows at a regular interval |
| `two_stage_cluster_sample` | `source/python-in-excel/functions/two_stage_cluster_sample.py` | Two-stage cluster sample: pick clusters, then rows |
| `reservoir_sample` | `source/python-in-excel/functions/reservoir_sample.py` | Algorithm R reservoir sample of rows |

See [docs/PythonMap.md](docs/PythonMap.md). Add functions with [docs/AddingPython.md](docs/AddingPython.md).

## License

MIT — see [LICENSE](LICENSE).
