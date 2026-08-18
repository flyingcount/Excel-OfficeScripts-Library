# Script map

Inventory of Automate scripts in this library. Add a row when you add a file under `source/scripts/`.

| Script | File | Output | Notes |
|--------|------|--------|--------|
| List worksheets | `source/scripts/ListWorksheets.ts` | Sheet **Worksheets** | Replaces the output sheet each run. Skips that sheet in the list. |
| Paul's format | `source/scripts/PaulsFormat.ts` | Selected range number format | Dropdown: 0dp, 2dp, colour variants, k/m scale, two date formats. Default **0dp**. |
| Format Table | `source/scripts/FormatTable.ts` | Active sheet tab/gridlines; table at active cell | TableStyleLight14, font 10, column width 56 on the table only. |
| Table of contents | `source/scripts/TableOfContents.ts` | Sheet **Table of Contents** at position 0 | Hyperlinks to A1 of each other sheet. Replaces an existing TOC sheet. |
| Highlight Differences | `source/scripts/HighlightDifferences.ts` | Conditional fill on the selection | Green `#97FFC6` if equal to 2 d.p., else red `#FFBDBD`. Two columns: left vs right. |
