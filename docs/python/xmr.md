# xmr

Individuals and moving-range (**XmR**) statistical process control. Default result is a spill table of values, limits, and signals. `plot=True` draws a **two-panel chart** (X on top, MR below).

Formula: `source/python-in-excel/functions/xmr.py`

This is an SPC function. For rational subgroups of size 2–10 use `xbar_r`; for n up to 25 use `xbar_s`. For small sustained shifts use `ewma` or `cusum`. For Cp/Cpk/Pp/Ppk use `capability_report`. For an ordered forecast series use TimeSeries tools such as `detect_anomalies`. For a single-column outlier flag without control limits use `outlier_flag`.

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

In a PY cell, set output to **Excel value** for the table. Leave a **Python object** for the chart:

```python
xmr("B2:B50")
xmr("B2:B50", dates="A2:A50")
xmr(data["Monthly_Expenses"], dates=data["Date"])
xmr("B2:B50", plot=True, title="Expense claims")
```

matplotlib is in the default Initialization (`plt`); it is not re-imported.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, DataFrame, Series, or `xl()` result. First numeric column is used. |
| `dates` | No | Optional x-axis labels: a range (`"A2:A50"`), Series, or list. Pass `data["Date"]`, not the string `"Date"`. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib figure. |
| `title` | No | Chart title when `plot=True`. Default `'XmR chart'`. |
| `headers` | No | First row is headers when `data` or `dates` is a ref string. Default `False`. |

Need at least two numeric values. Blanks are dropped (paired with `dates` when supplied). Excel 1×1 arrays for `plot` and `title` are unwrapped.

## Limits

Natural process limits from the **average moving range** (|x_t − x_{t−1}|), Shewhart constants for n=2:

| Chart | Center | UCL | LCL |
|-------|--------|-----|-----|
| Individuals (X) | x̄ | x̄ + 3 × (MR̄ / 1.128) | x̄ − 3 × (MR̄ / 1.128) |
| Moving range (MR) | MR̄ | 3.267 × MR̄ | 0 |

LCL on X is **not** floored at 0 (the process may be negative). A constant series has MR̄ = 0, so UCL = LCL = x̄.

Runs of 8 or more on one side of the **overall** x̄ are a shift. At each shift start or end, CL/UCL/LCL and MR limits are recomputed from that segment (MR̄ from consecutive differences **inside** the segment). A 1-point fragment inherits the previous segment’s limits. Outlier flags use the **local** limits. A large spike can still pull overall x̄ so that a long run of in-control points is scored as a shift.

## Signals

| Flag | Rule |
|------|------|
| `is_outlier` | X beyond the **local** UCL or LCL (3-sigma). |
| `is_mr_outlier` | MR beyond the **local** MR UCL. The first MR is blank. |
| `is_shift` | 8 or more consecutive X points on the same side of **overall** x̄ (points on the mean break the run). The whole run is flagged. |

## Result (table)

Set the PY cell to **Excel value**.

| Column | Notes |
|--------|-------|
| `t` | 1 … n after dropping blanks. |
| `date` | Present when `dates` was supplied. |
| `value` | Individuals. |
| `mr` | Moving range (blank on the first row). |
| `cl`, `ucl`, `lcl` | X center line and 3-sigma limits (step when the regime changes). |
| `mr_cl`, `mr_ucl`, `mr_lcl` | MR center line and limits (step with the same regimes). |
| `is_outlier` | `1` if X is beyond 3σ, else `0`. |
| `is_shift` | `1` if the point is in an 8+ run, else `0`. |
| `is_mr_outlier` | `1` if MR is beyond UCL, else `0`. |

## Result (chart)

`plot=True` returns a matplotlib `Figure`: individuals (stepped mean/UCL/LCL; red = X beyond 3σ, orange = 8-point shift) and moving range (stepped MR̄/UCL/LCL=0; red = MR beyond UCL). A/B/C zone fills are drawn only when there is a single regime. Leave the cell as a **Python object**.

## Example

```python
xmr([10, 11, 9, 12, 10, 11, 10, 30])
```

x̄ = 12.875, MR̄ = 30/7 ≈ 4.286. The last point (30) is beyond the X UCL and its moving range is beyond the MR UCL.

Two opposite 8-point runs recompute limits on each half:

```python
xmr([10, 11, 10, 11, 10, 11, 10, 11, 12, 13, 12, 13, 12, 13, 12, 13])
```

Overall x̄ = 11.5, so `is_shift` is 1 on every row. CL is 10.5 on the first eight rows and 12.5 on the last eight.
