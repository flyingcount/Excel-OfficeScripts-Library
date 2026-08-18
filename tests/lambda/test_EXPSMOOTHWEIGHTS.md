# Test: EXPSMOOTHWEIGHTS

## Setup

1. Formulas → Name Manager → New.
2. Name `EXPSMOOTHWEIGHTS`. Paste the `=LAMBDA` line from `source/lambda/functions/EXPSMOOTHWEIGHTS.lambda`.
3. Put `10`, `12`, `14` in `A1:A3`.

## Cases

Default alpha `0.2`. Weights are `a*(1-a)^(n-i)`, then residual `1-SUM(w)` is added to the first weight.

| Formula | Expected |
|---------|----------|
| `=EXPSMOOTHWEIGHTS(A1:A3)` | `{0.64; 0.16; 0.2}` |
| `=SUM(EXPSMOOTHWEIGHTS(A1:A3))` | `1` |
| `=EXPSMOOTHWEIGHTS(A1:A3,0.2)` | same as omitted alpha |

With alpha `0.5` on the same three rows: `w = {0.125; 0.25; 0.5}`, residual `0.125`, first weight `0.25`, result `{0.25; 0.25; 0.5}`.
