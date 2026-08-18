# Test: List worksheets

## Setup

1. Excel on the web (or desktop Automate) → **Automate** → **New Script**.
2. Paste `source/office-scripts/scripts/ListWorksheets.ts`.
3. Use a workbook with at least two worksheets, one of them hidden.

## Run

**Run** the script.

## Expected

- Sheet **Worksheets** exists (replaced if it already existed).
- Row 1 is bold: Name, Visibility, Used range, Row count, Column count.
- One data row per worksheet except **Worksheets**.
- Hidden sheet shows visibility **Hidden**.
- Empty sheet has a blank used range and 0 row/column counts.

Run a second time: still a single **Worksheets** sheet, not a duplicate.
