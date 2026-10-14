# np_chart

**np chart** for the count of defective items (binomial). Constant n is the usual case. Default result is a spill table. `plot=True` draws np with CL/UCL/LCL.

When n varies, prefer `p_chart`. For defects (not defectives) use `c_chart` / `u_chart`.

Formula: `source/python-in-excel/functions/np_chart.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

Table (PY cell output **Excel value**):

```python
np_chart("B2:B50", 50)
np_chart(defectives, sample_size)
```

Chart (leave as a **Python object**):

```python
np_chart("B2:B50", 50, plot=True, title="Defective items")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `defectives` | Yes | Count of defective *items*. Ref string, DataFrame, Series, or list. |
| `sample_size` | Yes | n inspected. A **scalar** (usual) or a column. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib figure. |
| `title` | No | Chart title when `plot=True`. Default `'np chart'`. |
| `headers` | No | First row is headers when a ref string is used. Default `False`. |

Need at least two complete pairs. Blanks are dropped. Defectives must be ≥ 0 and ≤ n; n must be > 0.

## Limits

p̄ = Σd / Σn  
CL_i = n_i p̄

| | |
|--|--|
| Center | n_i p̄ |
| UCL_i | min(n_i, n_i p̄ + 3 √[n_i p̄(1−p̄)]) |
| LCL_i | max(0, n_i p̄ − 3 √[n_i p̄(1−p̄)]) |

With constant n, the center is np̄. If p̄ is 0 or 1, UCL = LCL = n p̄.

## Result (table)

| Column | Notes |
|--------|-------|
| `t` | 1 … k. |
| `defectives` | Counts d (plotted). |
| `sample_size` | n. |
| `cl`, `ucl`, `lcl` | Center and 3σ limits. |
| `is_outlier` | `1` if d is beyond UCL or LCL. |

## Example

```python
np_chart([5, 8, 3, 20], 50)
```

np̄ = 9. The last point (20) is above the UCL.
