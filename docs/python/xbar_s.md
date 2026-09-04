# xbar_s

**X-bar and S** statistical process control for rational subgroups of size 2–25. Default result is a spill table (one row per subgroup). `plot=True` draws a **two-panel chart** (X-bar on top, S below). Prefer this when n > 10; for n = 2 to 10 `xbar_r` is the usual choice.

For one-at-a-time measurements use `xmr`.

Formula: `source/python-in-excel/functions/xbar_s.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

In a PY cell, set output to **Excel value** for the table. Leave a **Python object** for the chart:

```python
xbar_s("A1:A80", 10)
xbar_s("A1:J20", 10, headers=True)
xbar_s(data, 12, plot=True, title="Fill weight")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value stream or subgroup table. Ref string, DataFrame, Series, or list. |
| `subgroup_size` | Yes | n = 2 to 25. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib figure. |
| `title` | No | Chart title when `plot=True`. Default `'X-bar S chart'`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

If there are at least `subgroup_size` numeric columns, each **row** is a subgroup (first n numeric columns; incomplete rows dropped). Otherwise the **first numeric column** is split in time order into groups of n (a leftover incomplete group is dropped). Need at least two complete subgroups. S is the sample standard deviation (n−1).

## Limits

Shewhart A3, B3, B4 from c4. X̄̄ is the mean of subgroup means; s̄ is the mean of subgroup standard deviations.

| Chart | Center | UCL | LCL |
|-------|--------|-----|-----|
| X-bar | X̄̄ | X̄̄ + A3 × s̄ | X̄̄ − A3 × s̄ |
| S | s̄ | B4 × s̄ | B3 × s̄ |

X-bar LCL is **not** floored at 0. For small n, B3 = 0 so S LCL is 0. A constant process (s̄ = 0) has UCL = LCL = X̄̄.

## Result (table)

Set the PY cell to **Excel value**.

| Column | Notes |
|--------|-------|
| `subgroup` | 1 … k. |
| `n` | Subgroup size. |
| `xbar` | Subgroup mean. |
| `s` | Subgroup sample standard deviation. |
| `cl`, `ucl`, `lcl` | X-bar center line and limits. |
| `s_cl`, `s_ucl`, `s_lcl` | S center line and limits. |
| `is_outlier` | `1` if X-bar is beyond UCL or LCL. |
| `is_s_outlier` | `1` if S is beyond UCL or LCL. |

## Result (chart)

`plot=True` returns a matplotlib `Figure`: X-bar and S with CL/UCL/LCL; red markers beyond limits. Leave the cell as a **Python object**.

## Example

```python
xbar_s([
    10, 12, 11, 13, 10,
    11, 11, 12, 10, 11,
    12, 13, 12, 14, 13,
    10, 11, 10, 12, 11,
], 5)
```

Four subgroups of n=5. X̄̄ = 11.45. Subgroup 3 (X-bar 12.8) is above the X-bar UCL.
