# Lambda map

Inventory of named `LAMBDA` formulas. Add a row when you add a file under `source/lambda/functions/`.

| Name | File | Formula | Notes |
|------|------|---------|--------|
| `ROUND2` | `source/lambda/functions/ROUND2.lambda` | `=LAMBDA(value, ROUND(value, 2))` | Two decimal places. |
| `ISZERO2` | `source/lambda/functions/ISZERO2.lambda` | `=LAMBDA(value, ROUND(value, 2)=0)` | Matches Highlight Differences green rule. |
| `IFERROR0` | `source/lambda/functions/IFERROR0.lambda` | `=LAMBDA(value, IFERROR(value, 0))` | Errors become 0. |
| `EXPSMOOTHWEIGHTS` | `source/lambda/functions/EXPSMOOTHWEIGHTS.lambda` | `=LAMBDA(values,[alpha],…)` | SES weights, default α 0.2; residual on first weight. |
| `ESMOOTHWEIGHTEDVALUES` | `source/lambda/functions/ESMOOTHWEIGHTEDVALUES.lambda` | `=LAMBDA(values,[alpha],…)` | Values times those weights. |
| `EXPSMOOTHSERIES` | `source/lambda/functions/EXPSMOOTHSERIES.lambda` | `=LAMBDA(data,[alpha],…)` | Full SES series, first obs then SCAN. |
| `EXPSMOOTH` | `source/lambda/functions/EXPSMOOTH.lambda` | `=LAMBDA(data,[alpha],…)` | Last SES value only. |
