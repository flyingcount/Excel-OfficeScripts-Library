# Lambda map

Inventory of named `LAMBDA` formulas. Add a row when you add a file under `source/lambda/functions/`.

| Name | File | Formula | Notes |
|------|------|---------|--------|
| `ROUND2` | `source/lambda/functions/ROUND2.lambda` | `=LAMBDA(value, ROUND(value, 2))` | Two decimal places. |
| `ISZERO2` | `source/lambda/functions/ISZERO2.lambda` | `=LAMBDA(value, ROUND(value, 2)=0)` | Matches Highlight Differences green rule. |
| `IFERROR0` | `source/lambda/functions/IFERROR0.lambda` | `=LAMBDA(value, IFERROR(value, 0))` | Errors become 0. |
