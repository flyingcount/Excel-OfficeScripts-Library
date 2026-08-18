# Excel Office Scripts and Lambda Library

Reusable **Excel Office Scripts** (TypeScript) and named **LAMBDA** functions for Excel on the web and Microsoft 365.

Office Scripts live under `source/office-scripts/`. Named formulas live under `source/lambda/`. Grow each library one file at a time. Do not mix these with the VBA add-in.

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
│   ├── ScriptMap.md
│   └── LambdaMap.md
├── source/
│   ├── office-scripts/
│   │   ├── scripts/       ← one TypeScript file per Automate script
│   │   └── shared/        ← helpers to copy into a script
│   └── lambda/
│       ├── functions/     ← one named LAMBDA per file
│       └── shared/        ← fragments to copy into a LAMBDA
├── tests/
│   ├── office-scripts/
│   └── lambda/
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

## License

MIT — see [LICENSE](LICENSE).
