# Test: Paul's format

## Setup

1. Excel on the web (or desktop Automate) → **Automate** → **New Script**.
2. Paste `source/office-scripts/scripts/PaulsFormat.ts`. Save as **Paul's format**.
3. Put sample values in a block, e.g. `A1:A4`:
   - `1234.56`
   - `-1234.56`
   - `0`
   - `44927` (a date serial)

## Run

Select `A1:A3`. Run with style **0dp**.

Repeat on the same cells for **2dp**, **0dp Colour**, **2dp Colour**, **0dp k**, **1dp m**.

Select `A4`. Run with **Date dd-mm-yyyy**, then **Date dd-mmm-yyyy**.

## Expected

| Style | Positive | Negative | Zero |
|-------|----------|----------|------|
| 0dp | `1,235` | `(1,235)` | ` -` |
| 2dp | `1,234.56` | `(1,234.56)` | ` -` |
| 0dp Colour | same as 0dp | red `(1,235)` | ` -` |
| 2dp Colour | same as 2dp | red `(1,234.56)` | ` -` |
| 0dp k | `1 k` | scaled thousands with a `k` suffix | |
| 1dp m | `0.0 m` for 1234.56 | scaled millions with a `m` suffix | |
| Date dd-mm-yyyy | `01-01-2023` style day-month-year | | |
| Date dd-mmm-yyyy | `01-Jan-2023` style | | |

Default (no style picked) is **0dp**. Only the selected range changes; other cells keep their formats.
