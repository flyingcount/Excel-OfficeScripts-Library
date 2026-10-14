# ewma

**EWMA** (exponentially weighted moving average) control chart for individuals. Sensitive to small sustained shifts. Default result is a spill table. `plot=True` draws the EWMA with time-varying limits.

For large shifts use `xmr`. For an accumulating sum use `cusum`. For a unified shift-flag table use `process_shift_detection`.

Formula: `source/python-in-excel/functions/ewma.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

Table (PY cell output **Excel value**):

```python
ewma("B2:B50")
ewma(data, lambda_=0.1, l=2.7)
```

Chart (leave as a **Python object**):

```python
ewma("B2:B50", plot=True, title="Wait time")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, DataFrame, Series, or list. First numeric column is used. |
| `lambda_` | No | Weight on the newest point, in (0, 1]. Default `0.2`. Smaller values catch smaller shifts. |
| `l` | No | Limit width in sigma units. Default `3`. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib figure. |
| `title` | No | Chart title when `plot=True`. Default `'EWMA chart'`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least two numeric values. Blanks are dropped. Sigma is MR̄ / 1.128 (same as `xmr`). The EWMA starts at x̄.

## Limits

z_t = λ x_t + (1−λ) z_{t−1}

| | |
|--|--|
| Center | x̄ |
| UCL_t | x̄ + L σ √[λ/(2−λ) × (1−(1−λ)^{2t})] |
| LCL_t | x̄ − L σ √[λ/(2−λ) × (1−(1−λ)^{2t})] |

Limits widen toward the steady-state value. LCL is not floored at 0. A constant series has σ = 0, so UCL = LCL = x̄.

## Result (table)

| Column | Notes |
|--------|-------|
| `t` | 1 … n. |
| `value` | Individuals. |
| `ewma` | z_t. |
| `cl`, `ucl`, `lcl` | Center and time-varying limits. |
| `is_outlier` | `1` if the EWMA is beyond UCL or LCL. |

## Example

```python
ewma([10, 12, 11, 13, 12])
```

x̄ = 11.6, λ = 0.2. First EWMA is 11.28.
