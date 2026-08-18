# Test: DDL

## Setup

1. Formulas → Name Manager → New.
2. Name `DDL`. Paste the `=LAMBDA` line from `source/lambda/functions/DDL.lambda`.
3. Enter this block in `A1:C4` (no header):

| A | B | C |
|---|---|---|
| Fruit | Apple | Gala |
| Fruit | Apple | Fuji |
| Fruit | Orange | Navel |
| Veg | Carrot | Nantes |

## Cases

| Formula | Expected |
|---------|----------|
| `=DDL(A1:C4)` | `{Fruit; Fruit; Fruit; Veg}` |
| `=UNIQUE(DDL(A1:C4))` | `{Fruit; Veg}` |
| `=DDL(A1:C4,"Fruit")` | `{Apple; Apple; Orange}` |
| `=UNIQUE(DDL(A1:C4,"Fruit"))` | `{Apple; Orange}` |
| `=DDL(A1:C4,"Fruit","Apple")` | `{Gala; Fuji}` |
| `=DDL(A1:C4,"Veg","Carrot")` | `Nantes` |

Rows for the same parent path must stay together. If the two Apple rows are split by Orange, `DDL(...,"Fruit","Apple")` will not return both varieties.
