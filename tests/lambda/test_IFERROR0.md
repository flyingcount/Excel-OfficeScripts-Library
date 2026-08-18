# Test: IFERROR0

## Setup

1. Formulas → Name Manager → New.
2. Name `IFERROR0`. Paste the `=LAMBDA` line from `source/lambda/functions/IFERROR0.lambda`.

## Cases

| Formula | Expected |
|---------|----------|
| `=IFERROR0(10)` | `10` |
| `=IFERROR0(1/0)` | `0` |
| `=IFERROR0(VALUE("x"))` | `0` |
| `=IFERROR0(0)` | `0` |
