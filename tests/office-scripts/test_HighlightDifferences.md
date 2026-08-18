# Test: Highlight Differences

## Setup

1. Excel on the web (or desktop Automate) → **Automate** → **New Script**.
2. Paste `source/office-scripts/scripts/HighlightDifferences.ts`. Save as **Highlight Differences**.
3. Enter values in `Q11:Q14`:

| Cell | Value |
|------|-------|
| Q11 | `0.004` |
| Q12 | `0.001` |
| Q13 | `0.006` |
| Q14 | `-0.002` |

## Run

Select `Q11:Q14`. Run.

Open conditional formatting for the range and confirm the formulas.

Run a second time (rules should not stack).

## Expected

Rules on the selection (top-left Q11):

- Green: `=ROUND(Q11,2)=0` fill `#97FFC6`
- Red: `=ROUND(Q$11,2)<>0` fill `#FFBDBD`
- Green has **Stop if true**

With the sample:

- Q11 `0.004` → ROUND 0.00 → **green**
- Q12 `0.001` → ROUND 0.00 → **green**
- Q13 `0.006` → ROUND 0.01 → **red**
- Q14 `-0.002` → ROUND 0.00 → **green**

If Q11 is `0.006` (ROUND 0.01), Q11 is red, and Q12:Q14 are also red because the red formula locks row 11.

A second run still has two rules, not four.
