# Test: Activate Lambda functions

## Setup

1. Rebuild or open `workbook/Paul Lambda function library.xlsx`.
2. Excel → **Automate** → **New Script**. Paste `source/office-scripts/scripts/ActivateLambdaFunctions.ts`. Save as **Activate Lambda functions**.
3. Sheet **Lambda functions** should list every named function (Name, Lambda code, Note).

## Run

Select the `ROUND2` data row (not the header). Run **Activate Lambda functions**.

Select two or more data rows (for example `DDL` and `ISZERO2`). Run again.

## Expected

- Console: `Activated 1 named function(s)` then `Activated 2 named function(s)`.
- Formulas → Name Manager shows those names. `Refers to` is the Lambda code. Comment is the Note.
- On any sheet: `=ROUND2(1.234)` returns `1.23`.
- Running again on the same row replaces the name (no duplicate, no error).
- Selecting only the instruction rows or the header throws: no function rows selected.
- Selection on another sheet throws: select rows on **Lambda functions**.
