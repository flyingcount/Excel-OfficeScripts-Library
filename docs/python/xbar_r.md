# xbar_r

**X-bar and R** statistical process control for rational subgroups of size 2–10. Default result is a spill table (one row per subgroup). `plot=True` draws a **two-panel chart** (X-bar on top, R below).

For one-at-a-time measurements use `xmr`. For n > 10 use `xbar_s`.

Formula: `source/python-in-excel/functions/xbar_r.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

In a PY cell, set output to **Excel value** for the table. Leave a **Python object** for the chart:

```python
xbar_r("A1:A40", 5)
xbar_r("A1:E20", 5, headers=True)
xbar_r(data, 4, plot=True, title="Fill weight")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value stream or subgroup table. Ref string, DataFrame, Series, or list. |
| `subgroup_size` | Yes | n = 2 to 10. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib figure. |
| `title` | No | Chart title when `plot=True`. Default `'X-bar R chart'`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

If there are at least `subgroup_size` numeric columns, each **row** is a subgroup (first n numeric columns; incomplete rows dropped). Otherwise the **first numeric column** is split in time order into groups of n (a leftover incomplete group is dropped). Need at least two complete subgroups.

## Limits

Shewhart constants A2, D3, D4 for the chosen n. X̄̄ is the mean of subgroup means; R̄ is the mean of subgroup ranges (max − min).

| Chart | Center | UCL | LCL |
|-------|--------|-----|-----|
| X-bar | X̄̄ | X̄̄ + A2 × R̄ | X̄̄ − A2 × R̄ |
| R | R̄ | D4 × R̄ | D3 × R̄ |

X-bar LCL is **not** floored at 0. For n ≤ 6, D3 = 0 so R LCL is 0. A constant process (R̄ = 0) has UCL = LCL = X̄̄.

## Result (table)

Set the PY cell to **Excel value**.

| Column | Notes |
|--------|-------|
| `subgroup` | 1 … k. |
| `n` | Subgroup size. |
| `xbar` | Subgroup mean. |
| `r` | Subgroup range. |
| `cl`, `ucl`, `lcl` | X-bar center line and limits. |
| `r_cl`, `r_ucl`, `r_lcl` | R center line and limits. |
| `is_outlier` | `1` if X-bar is beyond UCL or LCL. |
| `is_r_outlier` | `1` if R is beyond UCL or LCL. |

## Result (chart)

`plot=True` returns a matplotlib `Figure`: X-bar and R with CL/UCL/LCL; red markers beyond limits. Leave the cell as a **Python object**.

## Example

```python
xbar_r([
    10, 12, 11, 13, 10,
    11, 11, 12, 10, 11,
    12, 13, 12, 14, 13,
    10, 11, 10, 12, 11,
], 5)
```

Four subgroups of n=5. X̄̄ = 11.45, R̄ = 2.25, A2 = 0.577. Subgroup 3 (X-bar 12.8) is above the X-bar UCL.
