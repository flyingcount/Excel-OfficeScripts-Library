# cusum

Two-sided **tabular CUSUM** for individuals. Accumulates deviations from the mean (beyond a slack kσ) until a decision interval hσ is crossed. Default result is a spill table. `plot=True` draws S+ and −S− with ±hσ.

For one-point Shewhart limits use `xmr`. For a weighted average use `ewma`. For a unified shift-flag table use `process_shift_detection`. For structural-break dates on a series, use TimeSeries `breakpoints`.

Formula: `source/python-in-excel/functions/cusum.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

Table (PY cell output **Excel value**):

```python
cusum("B2:B50")
cusum(data, k=0.5, h=4)
```

Chart (leave as a **Python object**):

```python
cusum("B2:B50", plot=True, title="Wait time")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, DataFrame, Series, or list. First numeric column is used. |
| `k` | No | Slack (allowance) in **sigma units**. Default `0.5`. |
| `h` | No | Decision interval in **sigma units**. Default `5`. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib figure. |
| `title` | No | Chart title when `plot=True`. Default `'CUSUM chart'`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least two numeric values. Blanks are dropped. Sigma is MR̄ / 1.128 (same as `xmr`). Target is x̄. `k` and `h` must be > 0.

## Limits

S⁺_t = max(0, x_t − x̄ − kσ + S⁺_{t−1})  
S⁻_t = max(0, x̄ − kσ − x_t + S⁻_{t−1})

A high (low) signal when S⁺ (S⁻) exceeds hσ. A constant series has σ = 0, so both CUSUMs stay at 0.

## Result (table)

| Column | Notes |
|--------|-------|
| `t` | 1 … n. |
| `value` | Individuals. |
| `s_high` | Upper CUSUM S⁺. |
| `s_low` | Lower CUSUM S⁻. |
| `h_limit` | hσ. |
| `is_high` | `1` if S⁺ > hσ. |
| `is_low` | `1` if S⁻ > hσ. |

## Result (chart)

S⁺ above zero and S⁻ drawn downward; dashed lines at ±hσ. Leave the cell as a **Python object**.

## Example

```python
cusum([10, 10, 10, 10, 10, 10, 10, 10, 20, 20, 20, 20])
```

The first eight points sit below x̄, so `is_low` turns on; after the jump to 20, `is_high` turns on.
