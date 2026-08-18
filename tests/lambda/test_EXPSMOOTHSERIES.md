# Test: EXPSMOOTHSERIES

## Setup

1. Formulas → Name Manager → New.
2. Name `EXPSMOOTHSERIES`. Paste the `=LAMBDA` line from `source/lambda/functions/EXPSMOOTHSERIES.lambda`.
3. Put `10`, `12`, `14` in `A1:A3`.

## Cases

Default alpha `0.2`. First output is the first observation. Then `s_t = alpha*x_t + (1-alpha)*s_{t-1}`.

| Formula | Expected |
|---------|----------|
| `=EXPSMOOTHSERIES(A1:A3)` | `{10; 10.4; 11.12}` |
| `=ROWS(EXPSMOOTHSERIES(A1:A3))` | `3` |
| `=EXPSMOOTHSERIES(A1:A3,0.2)` | same as omitted alpha |

Step check: `0.2*12 + 0.8*10 = 10.4`, then `0.2*14 + 0.8*10.4 = 11.12`.
