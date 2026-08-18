# Test: ESMOOTHWEIGHTEDVALUES

## Setup

1. Formulas → Name Manager → New. Add `ESMOOTHWEIGHTEDVALUES` (and `EXPSMOOTHWEIGHTS` if you want to cross-check).
2. Paste the `=LAMBDA` line from `source/lambda/functions/ESMOOTHWEIGHTEDVALUES.lambda`.
3. Put `10`, `12`, `14` in `A1:A3`.

## Cases

Default alpha `0.2`. This is `values * EXPSMOOTHWEIGHTS(values)`.

| Formula | Expected |
|---------|----------|
| `=ESMOOTHWEIGHTEDVALUES(A1:A3)` | `{6.4; 1.92; 2.8}` |
| `=SUM(ESMOOTHWEIGHTEDVALUES(A1:A3))` | `11.12` |
| `=ESMOOTHWEIGHTEDVALUES(A1:A3,0.2)` | same as omitted alpha |
