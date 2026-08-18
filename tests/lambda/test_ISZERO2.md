# Test: ISZERO2

## Setup

1. Formulas → Name Manager → New.
2. Name `ISZERO2`. Paste the `=LAMBDA` line from `source/lambda/functions/ISZERO2.lambda`.

## Cases

| Formula | Expected |
|---------|----------|
| `=ISZERO2(0)` | `TRUE` |
| `=ISZERO2(0.004)` | `TRUE` |
| `=ISZERO2(0.006)` | `FALSE` |
| `=ISZERO2(-0.002)` | `TRUE` |
| `=ISZERO2(1)` | `FALSE` |
