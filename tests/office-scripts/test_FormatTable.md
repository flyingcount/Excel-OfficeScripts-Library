# Test: Format Table

## Setup

1. Excel on the web (or desktop Automate) → **Automate** → **New Script**.
2. Paste `source/office-scripts/scripts/FormatTable.ts`. Save as **Format Table**.
3. On a sheet, create an Excel table (Insert → Table) with a few columns. Leave another cell **outside** the table for the no-table case.

## Run

Select a cell **inside** the table. Run.

Select a cell **outside** any table. Run again.

## Expected

Inside a table:

- Sheet tab is green; gridlines are on.
- That table uses **TableStyleLight14**.
- Table cells are font size 10.
- Table columns are width 56. Other columns on the sheet are unchanged.

Outside a table:

- Sheet tab is still green; gridlines stay on.
- No table style or column-width change.
- Automate console: `Active cell is not within a table.`
