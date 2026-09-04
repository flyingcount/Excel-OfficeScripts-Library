# Test: nelson_rules

## Setup

1. Formulas → **Initialization** → paste `nelson_rules` from `source/python-in-excel/functions/nelson_rules.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put `10, 11, 9, 12, 10, 11, 10, 30` in `A1:A8`.

σ from MR̄/1.128. The 30 is beyond 3σ (`rule_1` at t=8). Rule text is in the **headers**, not the first data row. Other constructed lists below isolate later rules.

## Cases

In a PY cell, set output to **Excel value**.

```python
r1 = "rule_1: One point beyond 3σ"
r2c = "rule_2: Nine in a row on the same side of x̄"
r3c = "rule_3: Six in a row steadily up or down"
r4c = "rule_4: Fourteen alternating up and down"
r7c = "rule_7: Fifteen in a row within 1σ"
r2 = [12, 13, 12, 13, 12, 13, 12, 13, 12, 10, 11, 10, 11, 10, 11, 10]
r3 = [1, 2, 3, 4, 5, 6, 5]
r4 = [1, 2] * 7
r7 = [10, 11] * 7 + [10]
```

| Python | Expected |
|--------|----------|
| `list(nelson_rules("A1:A8").columns)[:4]` | `['t', 'value', 'rule_1: One point beyond 3σ', 'rule_2: Nine in a row on the same side of x̄']` |
| `list(nelson_rules("A1:A8").columns)[-2:]` | `['n_rules', 'is_signal']` |
| `nelson_rules("A1:A8").shape` | `(8, 12)` |
| `float(nelson_rules("A1:A8")[r1].iloc[0])` | `0.0` |
| `float(nelson_rules("A1:A8")[r1].iloc[7])` | `1.0` |
| `nelson_rules("A1:A8")[r1].iloc[:7].sum()` | `0.0` |
| `float(nelson_rules("A1:A8")["is_signal"].iloc[7])` | `1.0` |
| `float(nelson_rules(r2)[r2c].iloc[7])` | `0.0` |
| `float(nelson_rules(r2)[r2c].iloc[8])` | `1.0` |
| `float(nelson_rules(r3)[r3c].iloc[4])` | `0.0` |
| `float(nelson_rules(r3)[r3c].iloc[5])` | `1.0` |
| `float(nelson_rules(r4)[r4c].iloc[12])` | `0.0` |
| `float(nelson_rules(r4)[r4c].iloc[13])` | `1.0` |
| `float(nelson_rules(r7)[r7c].iloc[13])` | `0.0` |
| `float(nelson_rules(r7)[r7c].iloc[14])` | `1.0` |
| `nelson_rules([5, 5, 5])["is_signal"].sum()` | `0.0` |
| `float(nelson_rules([5] * 15)[r7c].iloc[14])` | `1.0` |
| `nelson_rules([1])` | `#PYTHON!` — `Need at least 2 numeric values.` |
