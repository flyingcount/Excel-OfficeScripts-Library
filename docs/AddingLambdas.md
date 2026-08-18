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

## Install in Excel

1. Formulas → **Name Manager** (desktop) or **Defined names** (Excel on the web) → New.
2. Name: exactly the `Name:` line (for example `ROUND2`).
3. Refers to: paste the `=LAMBDA(...)` line.
4. OK. On a sheet: `=ROUND2(A1)`.

Excel Labs **Advanced Formula Environment** can hold the same named formula if you prefer that editor.

## Naming

- Excel name: `UPPERCASE` or `UPPER.CASE` (`ROUND2`, `ISZERO2`). Avoid names that collide with built-in functions.
- File: `NAME.lambda` matching the Excel name.
- Recursion: if the `LAMBDA` calls itself, the defined name must already match.

## What not to add here

- Office Scripts (use `source/office-scripts/`)
- VBA modules (use [Excel-VBA-Library](https://github.com/flyingcount/Excel-VBA-Library))
- Power Query M (use [PowerQuery-Library](https://github.com/flyingcount/PowerQuery-Library))
- Workbook binaries, secrets, or personal data
