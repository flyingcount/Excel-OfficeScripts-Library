# u_chart

**u chart** for defects per unit. Sample size / area of opportunity may vary. Default result is a spill table. `plot=True` draws u with time-varying CL/UCL/LCL.

For a constant inspection unit (count of defects, not rate) use `c_chart`. For fraction defective use `p_chart` / `np_chart`.

Formula: `source/python-in-excel/functions/u_chart.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

Table (PY cell output **Excel value**):

```python
u_chart("B2:B50", "C2:C50")
u_chart(defects, units)
u_chart(defects, 50)
```

Chart (leave as a **Python object**):

```python
u_chart("B2:B50", "C2:C50", plot=True, title="Scratches per panel")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `defects` | Yes | Defect counts c. Ref string, DataFrame, Series, or list. |
| `units` | Yes | Opportunity n (area, items, hours). A column aligned with `defects`, or a **scalar** for constant n. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib figure. |
| `title` | No | Chart title when `plot=True`. Default `'u chart'`. |
| `headers` | No | First row is headers when a ref string is used. Default `False`. |

Need at least two complete pairs. Blanks are dropped. Counts must be ≥ 0; units must be > 0.

## Limits

u_i = c_i / n_i  
ū = Σc / Σn

| | |
|--|--|
| Center | ū |
| UCL_i | ū + 3 √(ū / n_i) |
| LCL_i | max(0, ū − 3 √(ū / n_i)) |

Limits widen when n_i is smaller. LCL is floored at 0.

## Result (table)

| Column | Notes |
|--------|-------|
| `t` | 1 … k. |
| `defects` | Counts c. |
| `units` | Opportunity n. |
| `u` | c / n. |
| `cl`, `ucl`, `lcl` | Center and 3σ limits (vary with n). |
| `is_outlier` | `1` if u is beyond UCL or LCL. |

## Example

```python
u_chart([10, 12, 8, 15], 50)
```

ū = 0.225. All four rates sit inside the limits.
