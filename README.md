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
└── types/                 ← ExcelScript typings for the editor
```

## Quick start: Office Scripts

Office Scripts in Excel are **one file each**. The Automate editor cannot import other files from this repo.

1. Excel on the web (or desktop with Automate) → **Automate** → **New Script**.
2. Paste the contents of a file from `source/office-scripts/scripts/`.
3. **Save** → **Run**.

Example: `source/office-scripts/scripts/ListWorksheets.ts` writes a **Worksheets** inventory sheet.

## Quick start: Lambda functions

Excel named formulas are **one `LAMBDA` each**. Excel cannot import the folder; you paste into Name Manager.

1. Formulas → **Name Manager** (desktop) or **Defined names** (Excel on the web) → New.
2. Name: the `Name:` line in the file (for example `ROUND2`).
3. Refers to: paste the `=LAMBDA(...)` line from `source/lambda/functions/`.
4. On a sheet: `=ROUND2(A1)`.

Excel Labs **Advanced Formula Environment** can store the same named formulas.

## Scripts

| Script | File | What it does |
|--------|------|----------------|
| List worksheets | `source/office-scripts/scripts/ListWorksheets.ts` | Sheet name, visibility, used range |
| Paul's format | `source/office-scripts/scripts/PaulsFormat.ts` | Number format on the selection (0dp / 2dp / colour / k / m / dates) |
| Format Table | `source/office-scripts/scripts/FormatTable.ts` | Green tab, gridlines, TableStyleLight14 on the table at the active cell |
| Table of contents | `source/office-scripts/scripts/TableOfContents.ts` | First-tab sheet with hyperlinks to every other worksheet |
| Highlight Differences | `source/office-scripts/scripts/HighlightDifferences.ts` | Green/red fill on the selection: ROUND to 2 d.p. equal to zero vs not |

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

See [docs/LambdaMap.md](docs/LambdaMap.md). Add functions with [docs/AddingLambdas.md](docs/AddingLambdas.md).

## License

MIT — see [LICENSE](LICENSE).
