# p_chart

**p chart** for the fraction of defective items (binomial). Sample size may vary. Default result is a spill table. `plot=True` draws p with CL/UCL/LCL.

For the **count** of defectives with constant n, `np_chart` is the usual chart. For defects (not defectives) use `c_chart` / `u_chart`.

Formula: `source/python-in-excel/functions/p_chart.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

Table (PY cell output **Excel value**):

```python
p_chart("B2:B50", "C2:C50")
p_chart(defectives, sample_size)
p_chart(defectives, 50)
```

Chart (leave as a **Python object**):

```python
p_chart("B2:B50", 50, plot=True, title="Fraction defective")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `defectives` | Yes | Count of defective *items* (not defects on an item). Ref string, DataFrame, Series, or list. |
| `sample_size` | Yes | n inspected. A column aligned with `defectives`, or a **scalar** for constant n. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib figure. |
| `title` | No | Chart title when `plot=True`. Default `'p chart'`. |
| `headers` | No | First row is headers when a ref string is used. Default `False`. |

Need at least two complete pairs. Blanks are dropped. Defectives must be ≥ 0 and ≤ n; n must be > 0.

## Limits

p_i = d_i / n_i  
p̄ = Σd / Σn

| | |
|--|--|
| Center | p̄ |
| UCL_i | min(1, p̄ + 3 √[p̄(1−p̄)/n_i]) |
| LCL_i | max(0, p̄ − 3 √[p̄(1−p̄)/n_i]) |

Limits widen when n_i is smaller. If p̄ is 0 or 1, UCL = LCL = p̄.

## Result (table)

| Column | Notes |
|--------|-------|
| `t` | 1 … k. |
| `defectives` | Counts d. |
| `sample_size` | n. |
| `p` | d / n. |
| `cl`, `ucl`, `lcl` | Center and 3σ limits (vary with n). |
| `is_outlier` | `1` if p is beyond UCL or LCL. |

## Example

```python
p_chart([5, 8, 3, 20], 50)
```

p̄ = 0.18. The last point (20/50) is above the UCL.
