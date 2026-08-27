# Changelog

All notable changes to this library are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
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
- `resid_analysis` — residual diagnostics (VBA Residuals analysis stats plus Ljung-Box and Jarque-Bera; `plot=True` for vs-order / hist / QQ / ACF). Docs: `docs/python/resid_analysis.md`.
- `arima_order` — AIC grid search for ARIMA(p, d, q). Docs: `docs/python/arima_order.md`.
- `zscore_replace` — replace time-series points outside a z-score cutoff using interpolation. Docs: `docs/python/zscore_replace.md`.
- `normality_check` — one pasteable module: Shapiro-Wilk (`shapiro`), Anderson-Darling (`anderson`), and a normal Q-Q plot (`normality_check` / `qq_norm`). Docs: `docs/python/normality_check.md`.
- Cursor rule `.cursor/rules/python-in-excel.mdc` — pattern for adding Python in Excel PY-cell functions.
- Excel default Python Initialization snapshot (`init/DefaultInitialization.py`). `PaulPythonLibrary.py` includes those imports so a full paste restores defaults and the library.

### Changed
- Highlight Differences rules are now `=ROUND(Q11,2)=0` (green) and `=ROUND(Q$11,2)<>0` (red), where Q11 is the top-left of the selection.
- Split source into `source/office-scripts/` and `source/lambda/`. Office Script tests moved to `tests/office-scripts/`.
- Python in Excel function files end with a quoted call so a pasted PY cell displays the signature for reuse.
