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
| `DDL` | `source/lambda/functions/DDL.lambda` | `=LAMBDA(range,[lookup1],…,[lookup10],…)` | Dependent drop-down from a hierarchy table. See [docs/lambda/DDL.md](lambda/DDL.md). |
| `DDLSorter` | `source/lambda/functions/DDLSorter.lambda` | `=LAMBDA(Range,[SortOrder],SORT(Range, SEQUENCE(, COLUMNS(Range)), SortOrder))` | DDL Sorter. See [docs/lambda/DDLSorter.md](lambda/DDLSorter.md). |
| `DoubleXLookup` | `source/lambda/functions/DoubleXLookup.lambda` | `=LAMBDA(vlookup_value,vlookup_array,hlookup_value,hlookup_array,return_array,[if_not_found],…)` | Two-way lookup. See [docs/lambda/DoubleXLookup.md](lambda/DoubleXLookup.md). |
| `SuperXLookup` | `source/lambda/functions/SuperXLookup.lambda` | `=LAMBDA(lookup_value,lookup_array,return_array,[if_not_found],…)` | Whole row or column. See [docs/lambda/SuperXLookup.md](lambda/SuperXLookup.md). |
