# Adding a Lambda

One named formula = one file under `source/lambda/functions/`.

## Checklist

1. Add `source/lambda/functions/NAME.lambda`. The file name (without extension) should match the Excel name.
2. Use this shape:

   ```
   Name: NAME
   Description: One line.
   Parameters: arg1, arg2
   =LAMBDA(arg1, arg2, /* body */)
   ```

3. The Excel name is the `Name:` line. The paste target is the `=LAMBDA(...)` line only.
4. Add a row to [LambdaMap.md](LambdaMap.md) and the README Lambda table.
5. Add a short note under **Added** in `CHANGELOG.md`.
6. Add `tests/lambda/test_NAME.md` with a grid of inputs and expected results.
7. If the function needs more than a one-line description, add `docs/lambda/NAME.md` and link it from [LambdaMap.md](LambdaMap.md).
8. Rebuild the git-synced workbook so the new row appears on **Lambda functions**:

   ```powershell
   powershell -ExecutionPolicy Bypass -File scripts/Build-LambdaWorkbook.ps1
   ```

## Install in Excel

Open `workbook/Paul Lambda function library.xlsx`. Select one or more table rows, then run Automate script **Activate Lambda functions** (paste `source/office-scripts/scripts/ActivateLambdaFunctions.ts` once if needed). That writes the names into Name Manager.

You can still add a name by hand: Formulas → **Name Manager** → New → paste the `=LAMBDA(...)` line.

## Naming

- Excel name: `UPPERCASE` or `UPPER.CASE` (`ROUND2`, `ISZERO2`). Avoid names that collide with built-in functions.
- File: `NAME.lambda` matching the Excel name.
- Recursion: if the `LAMBDA` calls itself, the defined name must already match.

## What not to add here

- Office Scripts (use `source/office-scripts/`)
- Python in Excel (use `source/python-in-excel/` and [AddingPython.md](AddingPython.md))
- VBA modules (use [Excel-VBA-Library](https://github.com/flyingcount/Excel-VBA-Library))
- Power Query M (use [PowerQuery-Library](https://github.com/flyingcount/PowerQuery-Library))
- Secrets or personal data. The catalog workbook `workbook/Paul Lambda function library.xlsx` is rebuilt, not edited by hand.
