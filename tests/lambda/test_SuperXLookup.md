# Test: SuperXLookup

## Setup

1. Formulas → Name Manager → New.
2. Name `SuperXLookup`. Paste the `=LAMBDA` line from `source/lambda/functions/SuperXLookup.lambda`.
3. Enter:

|   | A | B | C | D |
|---|---|---|---|---|
| 1 |   | Jan | Feb | Mar |
| 2 | North | 10 | 20 | 30 |
| 3 | South | 40 | 50 | 60 |

## Cases

Row lookup (`COLUMNS(lookup_value)=1`):

| Formula | Expected |
|---------|----------|
| `=SuperXLookup("South",A2:A3,B2:D3)` | `{40,50,60}` |
| `=SuperXLookup("North",A2:A3,B2:D3)` | `{10,20,30}` |
| `=INDEX(SuperXLookup("South",A2:A3,B2:D3),1,2)` | `50` |
| `=SuperXLookup("East",A2:A3,B2:D3,"missing")` | `missing` |
| `=SuperXLookup("East",A2:A3,B2:D3)` | `#N/A` |

Column lookup (`COLUMNS(lookup_value)>1`). Put `Feb` in `F1` and any dummy in `G1`, then:

| Formula | Expected |
|---------|----------|
| `=SuperXLookup(F1:G1,B1:D1,B2:D3)` | `{20;50}` (Feb column), if `XMATCH` resolves `F1:G1` to Feb |
