# Excel Office Scripts Library

Reusable **Excel Office Scripts** (TypeScript) for Excel on the web and desktop Automate.

Each file under `source/scripts/` is one script you paste into **Automate → New Script**. Grow the library one script at a time; do not mix these with the VBA add-in.

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
│   ├── AddingScripts.md   ← how to add the next script
│   └── ScriptMap.md       ← inventory of scripts
├── source/
│   ├── scripts/           ← one TypeScript file per Automate script
│   └── shared/            ← helpers to copy into a script (single-file runtime)
├── tests/
└── types/                 ← ExcelScript typings for the editor
```

## Quick start

Office Scripts in Excel are **one file each**. The Automate editor cannot import other files from this repo.

1. Excel on the web (or desktop with Automate) → **Automate** → **New Script**.
2. Paste the contents of a file from `source/scripts/`.
3. **Save** → **Run**.

Example: `source/scripts/ListWorksheets.ts` writes a **Worksheets** inventory sheet.

## Scripts

| Script | File | What it does |
|--------|------|----------------|
| List worksheets | `source/scripts/ListWorksheets.ts` | Sheet name, visibility, used range |
| Paul's format | `source/scripts/PaulsFormat.ts` | Number format on the selection (0dp / 2dp / colour / k / m / dates) |
| Format Table | `source/scripts/FormatTable.ts` | Green tab, gridlines, TableStyleLight14 on the table at the active cell |
| Table of contents | `source/scripts/TableOfContents.ts` | First-tab sheet with hyperlinks to every other worksheet |
| Highlight Differences | `source/scripts/HighlightDifferences.ts` | Green/red fill on the selection when values match to 2 decimal places |

See [docs/ScriptMap.md](docs/ScriptMap.md) for the full list as it grows.

## Adding a script

Follow [docs/AddingScripts.md](docs/AddingScripts.md): one `.ts` file, a `main(workbook)` entry point, a changelog line, a test note, and a ScriptMap row.

Shared helpers live in `source/shared/`. Copy the function into the script file; do not `import` it (Automate will not resolve that).

## License

MIT — see [LICENSE](LICENSE).
