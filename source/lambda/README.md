# Lambda functions

Each file under `functions/` is one named Excel `LAMBDA`. The Excel name is the `Name:` line; the formula is the `=LAMBDA(...)` line.

Excel cannot import this folder. Copy the formula into **Formulas → Name Manager → New** (desktop) or **Formulas → Defined names** (Excel on the web), using the same name.

Excel Labs **Advanced Formula Environment** can also store these as named formulas.

`shared/` is for reusable fragments you copy into a `LAMBDA`, not for `LET` modules Excel will load on its own.
