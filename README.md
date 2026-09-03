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

1. Formulas → **Initialization** → replace the editor with `source/python-in-excel/init/PaulPythonLibrary.py` → Save. That file includes Excel’s default imports and the library functions. For **sampling functions only**, paste `init/Sampling.py` instead. For **time series functions only**, paste `init/TimeSeries.py` instead.
2. Insert a Python cell (**Formulas → Insert Python**, or `=PY`).
3. Call a function, for example `describe("Table1[#All]")` or `stl_plot("A1:A24", 12)`.
4. Set the cell output to **Excel value** if a table should spill into the grid. Leave a **Python object** for charts such as `stl_plot`.

If the default imports were deleted or edited, paste `source/python-in-excel/init/DefaultInitialization.py` into **Initialization** and Save. Then paste `PaulPythonLibrary.py` (or paste only from the first `def` onward if the defaults are already there).

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
| `expsmooth` | `source/python-in-excel/functions/expsmooth.py` | Last simple-exponential-smoothing value (default α 0.2) |
| `stl` | `source/python-in-excel/functions/stl.py` | STL seasonal-trend-residual decomposition |
| `stl_plot` | `source/python-in-excel/functions/stl_plot.py` | STL four-panel chart (`DecomposeResult.plot`) |
| `resid_analysis` | `source/python-in-excel/functions/resid_analysis.py` | Residual diagnostics (table, or `plot=True` for charts) |
| `normality_check` | `source/python-in-excel/functions/normality_check.py` | Q-Q plot plus Shapiro-Wilk and Anderson-Darling (one paste) |
| `arima_order` | `source/python-in-excel/functions/arima_order.py` | AIC grid search for ARIMA(p, d, q) |
| `zscore_replace` | `source/python-in-excel/functions/zscore_replace.py` | Replace points outside a z-score cutoff by interpolation |
| `date_features` | `source/python-in-excel/functions/date_features.py` | Calendar parts, cyclical sine/cosine encodings, and public-holiday flag |
| `cluster_prep` | `source/python-in-excel/functions/cluster_prep.py` | Scale numbers and one-hot encode categories for clustering |
| `outlier_flag` | `source/python-in-excel/functions/outlier_flag.py` | Flag outliers by IQR, MAD, or z-score |
| `stratified_sample` | `source/python-in-excel/functions/stratified_sample.py` | Proportional stratified sample from a table |
| `systematic_sample` | `source/python-in-excel/functions/systematic_sample.py` | Systematic sample of rows at a regular interval |
| `two_stage_cluster_sample` | `source/python-in-excel/functions/two_stage_cluster_sample.py` | Two-stage cluster sample: pick clusters, then rows |
| `reservoir_sample` | `source/python-in-excel/functions/reservoir_sample.py` | Algorithm R reservoir sample of rows |

See [docs/PythonMap.md](docs/PythonMap.md). Add functions with [docs/AddingPython.md](docs/AddingPython.md).

## License

MIT — see [LICENSE](LICENSE).
