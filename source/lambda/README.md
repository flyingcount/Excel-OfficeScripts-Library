# Lambda functions

Each file under `functions/` is one named Excel `LAMBDA`. The Excel name is the `Name:` line; the formula is the `=LAMBDA(...)` line.

Excel cannot import this folder by itself. The git-synced workbook `workbook/Paul Lambda function library.xlsx` lists every function. Select rows and run **Activate Lambda functions** to write them into Name Manager. Rebuild that workbook after you add a `.lambda` file (`scripts/Build-LambdaWorkbook.ps1`).

`shared/` is for reusable fragments you copy into a `LAMBDA`, not for `LET` modules Excel will load on its own.
