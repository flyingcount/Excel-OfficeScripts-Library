# nelson_rules

**Nelson's eight tests** on an individuals chart. Center is x̄; σ is MR̄ / 1.128 (same as `xmr`). Result is one row per point. A rule flags the point that **completes** the pattern. Each `rule_N` **header** includes a brief explanation (the data rows are only 0/1 flags).

For Shewhart 3σ plus an 8-point run only, use `xmr`. For CUSUM/EWMA flags use `process_shift_detection`.

Formula: `source/python-in-excel/functions/nelson_rules.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

PY cell output **Excel value**:

```python
nelson_rules("B2:B50")
nelson_rules(data)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, DataFrame, Series, or list. First numeric column is used. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least two numeric values. Blanks are dropped. Limits are not recomputed after a shift (unlike `xmr`).

## Rules (Nelson 1984)

Headers (and meaning):

| Header | Test |
|--------|------|
| `rule_1: One point beyond 3σ` | One point beyond 3σ. |
| `rule_2: Nine in a row on the same side of x̄` | Nine in a row on the same side of x̄ (flags from the 9th onward). |
| `rule_3: Six in a row steadily up or down` | Six in a row steadily increasing or decreasing (strict). |
| `rule_4: Fourteen alternating up and down` | Fourteen in a row alternating up and down. |
| `rule_5: Two of three beyond 2σ, same side` | Two of three consecutive points beyond 2σ, same side. |
| `rule_6: Four of five beyond 1σ, same side` | Four of five consecutive points beyond 1σ, same side. |
| `rule_7: Fifteen in a row within 1σ` | Fifteen in a row within 1σ (either side). |
| `rule_8: Eight in a row beyond 1σ` | Eight in a row beyond 1σ (either side). |

A constant series has σ = 0, so distance rules other than `rule_7` stay off. After 15 constants, `rule_7` turns on.

## Result

| Column | Notes |
|--------|-------|
| `t` | 1 … n. |
| `value` | Individuals. |
| `rule_1: …` … `rule_8: …` | `1` if that rule fires at this point. The explanation is in the header, not in the first data row. |
| `n_rules` | How many rules fire. |
| `is_signal` | `1` if any rule fires. |

## Example

```python
nelson_rules([10, 11, 10, 11, 10, 11, 10, 30])
```

The last point is beyond 3σ (`rule_1`). The first in-control rows stay 0 under every rule column.
