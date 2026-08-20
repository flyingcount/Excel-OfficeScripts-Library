# Adding a script

One Automate script = one file under `source/office-scripts/scripts/`.

## Checklist

1. Add `source/office-scripts/scripts/YourScriptName.ts` with a `main(workbook: ExcelScript.Workbook)` entry point.
2. Paste any helpers from `source/office-scripts/shared/` **into that file** (no `import`).
3. Add a row to [ScriptMap.md](ScriptMap.md) and the README scripts table.
4. Add a short note under **Added** in `CHANGELOG.md`.
5. Add `tests/office-scripts/test_YourScriptName.md` with setup, run steps, and expected sheets/values.
6. Keep the script self-contained: cancel-safe where you prompt, restore the workbook if the user stops, do not leave orphan output sheets from a failed run if you can delete them.

## Naming

- File: `PascalCase.ts` matching the Automate script name (`ListWorksheets.ts`).
- Output sheets: title case, specific (`Worksheets`, not `Sheet1`).
- Prefer replacing a named output sheet over appending forever.

## What not to add here

- Named `LAMBDA` formulas (use `source/lambda/` and [AddingLambdas.md](AddingLambdas.md))
- Python in Excel (use `source/python-in-excel/` and [AddingPython.md](AddingPython.md))
- VBA modules (use [Excel-VBA-Library](https://github.com/flyingcount/Excel-VBA-Library))
- Power Query M (use [PowerQuery-Library](https://github.com/flyingcount/PowerQuery-Library))
- Secrets, workbook data, or downloaded `.xlsx` samples with personal content
