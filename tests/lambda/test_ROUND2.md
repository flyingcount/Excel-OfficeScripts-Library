# Test: ROUND2

## Setup

1. Formulas → Name Manager → New.
2. Name `ROUND2`. Paste the `=LAMBDA` line from `source/lambda/functions/ROUND2.lambda`.

## Cases

| Formula | Expected |
|---------|----------|
| `=ROUND2(1.234)` | `1.23` |
| `=ROUND2(1.235)` | `1.24` |
| `=ROUND2(-1.235)` | `-1.24` |
| `=ROUND2(0.004)` | `0` |
| `=ROUND2(0.006)` | `0.01` |
