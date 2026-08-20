# Adding a Python in Excel function

One reusable function = one file under `source/python-in-excel/functions/`.

## Checklist

1. Add `source/python-in-excel/functions/name.py`. The file name (without extension) should match the Python function name.
2. Use this shape:

   ```python
   # Name: name
   # Description: One line.
   # Parameters: arg1, arg2=default

   def name(arg1, arg2=default):
       """One line."""
       ...

   "name(arg1, arg2=default)"
   ```

   The last line is a quoted call. When the file is pasted into a PY cell, Excel displays that signature so it can be copied into another cell.

3. The paste target is the `def` (and any helpers it needs). Do not wrap it in `=PY(...)`.
4. Append the same `def` and quoted call to `source/python-in-excel/init/PaulPythonLibrary.py`.
5. Add a row to [PythonMap.md](PythonMap.md) and the README Python in Excel table.
6. Add a short note under **Added** in `CHANGELOG.md`.
7. Add `tests/python-in-excel/test_name.md` with a grid of PY-cell inputs and expected results.
8. If the function needs more than a one-line description, add `docs/python/name.md` and link it from [PythonMap.md](PythonMap.md).
9. Copy any new helper into `source/python-in-excel/shared/` and into the function file (no `import` from this repo).

## Install in Excel

Python in Excel is Microsoft 365 only.

**Workbook-wide (preferred):** Formulas → **Initialization** → replace the editor with `source/python-in-excel/init/PaulPythonLibrary.py` → Save. That file includes the Excel default imports and the library functions. Then in a PY cell: `describe("Table1[#All]")`.

**One function:** paste that file’s `def` into Initialization after the default imports, or into a Python cell above and to the left of the cells that call it.

**One-shot:** in a PY cell, paste a call such as `describe(xl("A1:D20", headers=True))` without installing the library.

Switch the cell to **Excel value** if the result should spill into the grid.

## Restore default Initialization

Excel’s default Initialization is stored at `source/python-in-excel/init/DefaultInitialization.py` (`numpy`, `pandas`, `matplotlib`, `seaborn`, `statsmodels`, `excel`, `warnings`, and the `xl` scalar/array conversion settings).

If those imports were deleted or edited:

1. Formulas → **Initialization**.
2. Select all in the editor and paste `DefaultInitialization.py`.
3. Save.

To restore defaults **and** the library functions in one step, paste `PaulPythonLibrary.py` instead. Do not wrap either file in `=PY(...)`.

## Naming

- Python name: `snake_case` (`xl_df`, `expsmooth`). Avoid names that collide with pandas/numpy (`pd`, `np`, `xl`).
- File: `name.py` matching the function name.
- These are Python callables in PY cells, not Excel worksheet names like `ROUND2`.

## What not to add here

- Office Scripts (use `source/office-scripts/` and [AddingScripts.md](AddingScripts.md))
- Named `LAMBDA` formulas (use `source/lambda/` and [AddingLambdas.md](AddingLambdas.md))
- VBA modules (use [Excel-VBA-Library](https://github.com/flyingcount/Excel-VBA-Library))
- Power Query M (use [PowerQuery-Library](https://github.com/flyingcount/PowerQuery-Library))
- xlwings, PyXLL, or local CPython packages
- Secrets or personal data
