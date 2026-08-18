# Test: Highlight Differences

## Setup

1. Excel on the web (or desktop Automate) → **Automate** → **New Script**.
2. Paste `source/scripts/HighlightDifferences.ts`. Save as **Highlight Differences**.
3. Enter a two-column block, e.g. `A1:B4`:

| A | B |
|---|---|
| 1.234 | 1.231 |
| 1.234 | 1.239 |
| 10 | 10.004 |
| 10 | 10.006 |

## Run

Select `A1:B4`. Run.

Run a second time on the same range (conditional formats should not stack extra rules).

Optional: select two rows, or one column, and run.

## Expected

Two-column selection, match if `ROUND(value, 2)` is equal:

- Row 1 (`1.23` vs `1.23`): both cells **#97FFC6**
- Row 2 (`1.23` vs `1.24`): both cells **#FFBDBD**
- Row 3 (`10.00` vs `10.00`): green
- Row 4 (`10.00` vs `10.01`): red

A blank or text in either cell of the pair is red.

A second run still has two conditional format rules (green equal, red not), not four.
