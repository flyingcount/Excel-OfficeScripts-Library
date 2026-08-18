# Test: DDLSorter

## Setup

1. Formulas → Name Manager → New.
2. Name `DDLSorter`. Paste the `=LAMBDA` line from `source/lambda/functions/DDLSorter.lambda`.
3. Enter this unsorted block in `A1:C4`:

| A | B | C |
|---|---|---|
| Fruit | Orange | Navel |
| Veg | Carrot | Nantes |
| Fruit | Apple | Fuji |
| Fruit | Apple | Gala |

## Cases

| Formula | Expected |
|---------|----------|
| `=DDLSorter(A1:C4)` | Fruit/Apple/Fuji, Fruit/Apple/Gala, Fruit/Orange/Navel, Veg/Carrot/Nantes |
| `=INDEX(DDLSorter(A1:C4),1,2)` | `Apple` |
| `=INDEX(DDLSorter(A1:C4),4,1)` | `Veg` |
| `=DDLSorter(A1:C4,1)` | same as omitted `SortOrder` (ascending) |
| `=INDEX(DDLSorter(A1:C4,-1),1,1)` | `Veg` |

If `DDL` is installed: `=DDL(DDLSorter(A1:C4),"Fruit","Apple")` returns `{Fuji; Gala}`.
