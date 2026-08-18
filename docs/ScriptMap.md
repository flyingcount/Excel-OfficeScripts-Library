# Script map

Inventory of Automate scripts in this library. Add a row when you add a file under `source/office-scripts/scripts/`.

| Script | File | Output | Notes |
|--------|------|--------|--------|
| List worksheets | `source/office-scripts/scripts/ListWorksheets.ts` | Sheet **Worksheets** | Replaces the output sheet each run. Skips that sheet in the list. |
| Paul's format | `source/office-scripts/scripts/PaulsFormat.ts` | Selected range number format | Dropdown: 0dp, 2dp, colour variants, k/m scale, two date formats. Default **0dp**. |
| Format Table | `source/office-scripts/scripts/FormatTable.ts` | Active sheet tab/gridlines; table at active cell | TableStyleLight14, font 10, column width 56 on the table only. |
| Table of contents | `source/office-scripts/scripts/TableOfContents.ts` | Sheet **Table of Contents** at position 0 | Hyperlinks to A1 of each other sheet. Replaces an existing TOC sheet. |
| Highlight Differences | `source/office-scripts/scripts/HighlightDifferences.ts` | Conditional fill on the selection | Green `=ROUND(Q11,2)=0` `#97FFC6`; red `=ROUND(Q$11,2)<>0` `#FFBDBD` (Q11 = top-left of the selection). |
| Activate Lambda functions | `source/office-scripts/scripts/ActivateLambdaFunctions.ts` | Name Manager in the open workbook | Select rows on **Lambda functions** in `workbook/Paul Lambda function library.xlsx`. |
