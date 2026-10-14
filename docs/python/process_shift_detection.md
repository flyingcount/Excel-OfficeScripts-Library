# process_shift_detection

Flag **mean shifts** on individuals. Default method is tabular CUSUM (same rules as `cusum`). Result is one row per point.

For the full CUSUM/EWMA/XmR chart or statistic columns use `cusum`, `ewma`, or `xmr`. For Nelson's eight tests use `nelson_rules`. For structural-break dates on a series, use TimeSeries `breakpoints`.

Formula: `source/python-in-excel/functions/process_shift_detection.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

PY cell output **Excel value**:

```python
process_shift_detection("B2:B50")
process_shift_detection(data, method="ewma")
process_shift_detection(data, method="xmr")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, DataFrame, Series, or list. First numeric column is used. |
| `method` | No | `'cusum'` (default), `'ewma'`, or `'xmr'` (`'shewhart'` is an alias for `'xmr'`). |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least two numeric values. Blanks are dropped. Sigma is MR̄ / 1.128. Chart tuning (k, h, λ, L) stays on `cusum` / `ewma` / `xmr`; this detector uses those functions’ defaults.

## Methods

| `method` | Shift when |
|----------|------------|
| `cusum` | S⁺ or S⁻ exceeds 5σ (slack 0.5σ), same as `cusum`. |
| `ewma` | EWMA beyond time-varying 3σ limits (λ = 0.2), same as `ewma`. |
| `xmr` | Individual beyond 3σ, or an 8-point run on one side of x̄. |

## Result

| Column | Notes |
|--------|-------|
| `t` | 1 … n. |
| `value` | Individuals. |
| `method` | Method used. |
| `is_shift` | `1` if high or low. |
| `is_high` | `1` if an upward shift. |
| `is_low` | `1` if a downward shift. |

## Example

```python
process_shift_detection([10, 10, 10, 10, 10, 10, 10, 10, 20, 20, 20, 20])
```

Default CUSUM: `is_low` turns on at t=2; `is_high` turns on at the jump to 20.
