# Test: EXPSMOOTH

## Setup

1. Formulas → Name Manager → New. Add `EXPSMOOTH` (and `EXPSMOOTHSERIES` to cross-check).
2. Paste the `=LAMBDA` line from `source/lambda/functions/EXPSMOOTH.lambda`.
3. Put `10`, `12`, `14` in `A1:A3`.

## Cases

Default alpha `0.2`. Result is the last value of the smoothed series after the first observation (same as `TAKE(EXPSMOOTHSERIES(...),-1)` only if the series includes the seed — here it is the last SCAN value, `11.12`).

| Formula | Expected |
|---------|----------|
| `=EXPSMOOTH(A1:A3)` | `11.12` |
| `=EXPSMOOTH(A1:A3,0.2)` | `11.12` |
| `=EXPSMOOTH(A1:A3)=INDEX(EXPSMOOTHSERIES(A1:A3),3)` | `TRUE` |
