# c_chart

**c chart** for the count of defects per inspection unit when the area of opportunity is constant (Poisson). Default result is a spill table. `plot=True` draws c with CL/UCL/LCL.

For defects **per unit** with possibly varying n, use `u_chart`. For fraction defective (items) use `p_chart` / `np_chart`. For variable data use `xmr` or `xbar_r`.

Formula: `source/python-in-excel/functions/c_chart.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

Table (PY cell output **Excel value**):

```python
c_chart("B2:B50")
c_chart(defects)
```

Chart (leave as a **Python object**):

```python
c_chart("B2:B50", plot=True, title="Paint defects")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `defects` | Yes | Defect counts. Ref string, DataFrame, Series, or list. First numeric column is used. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib figure. |
| `title` | No | Chart title when `plot=True`. Default `'c chart'`. |
| `headers` | No | First row is headers when `defects` is a ref string. Default `False`. |

Need at least two numeric values. Blanks are dropped. Counts must be ≥ 0.

## Limits

c̄ is the mean of the defect counts.

| | |
|--|--|
| Center | c̄ |
| UCL | c̄ + 3 √c̄ |
| LCL | max(0, c̄ − 3 √c̄) |

LCL is floored at 0 (counts cannot be negative). If every count is 0, UCL = LCL = 0.

## Result (table)

| Column | Notes |
|--------|-------|
| `t` | 1 … k. |
| `defects` | Counts c. |
| `cl`, `ucl`, `lcl` | Center and 3σ limits. |
| `is_outlier` | `1` if c is beyond UCL or LCL. |

## Example

```python
c_chart([10, 12, 8, 15, 9, 30])
```

c̄ = 14. The last point (30) is above the UCL.
