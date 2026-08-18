# Test: DoubleXLookup

## Setup

1. Formulas → Name Manager → New.
2. Name `DoubleXLookup`. Paste the `=LAMBDA` line from `source/lambda/functions/DoubleXLookup.lambda`.
3. Enter:

|   | A | B | C | D |
|---|---|---|---|---|
| 1 |   | Jan | Feb | Mar |
| 2 | North | 10 | 20 | 30 |
| 3 | South | 40 | 50 | 60 |

## Cases

| Formula | Expected |
|---------|----------|
| `=DoubleXLookup("South",A2:A3,"Feb",B1:D1,B2:D3)` | `50` |
| `=DoubleXLookup("North",A2:A3,"Mar",B1:D1,B2:D3)` | `30` |
| `=DoubleXLookup("East",A2:A3,"Feb",B1:D1,B2:D3,"missing")` | `missing` |
| `=DoubleXLookup("East",A2:A3,"Feb",B1:D1,B2:D3)` | `#N/A` |
| `=DoubleXLookup("South",A2:A3,"Apr",B1:D1,B2:D3,0)` | `0` |
