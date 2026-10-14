# capability_report

Process **capability** for individuals: within (Cp, Cpk) and overall (Pp, Ppk), plus expected overall PPM. Result is a **one-row spill table** whose columns are `mean`, `stdev_within`, `stdev_overall`, `cp`, `cpk`, `pp`, `ppk`, `ppm`.

For control-chart limits use `xmr`. For rational subgroups use `xbar_r` or `xbar_s`.

Formula: `source/python-in-excel/functions/capability_report.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/SPC.py`.

PY cell output **Excel value**:

```python
capability_report("B2:B50", 16, 8)
capability_report(data, usl, lsl)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, DataFrame, Series, or list. First numeric column is used. |
| `usl` | Yes | Upper specification limit. Must be > `lsl`. |
| `lsl` | Yes | Lower specification limit. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least two numeric values. Blanks are dropped.

## Formulas

σ_within is MR̄ / 1.128 (same as `xmr`). σ_overall is the sample standard deviation (n−1). Center is x̄.

| Index | Formula |
|-------|---------|
| Cp | (USL − LSL) / (6 σ_within) |
| Cpk | min( (USL − x̄) / (3 σ_within), (x̄ − LSL) / (3 σ_within) ) |
| Pp | (USL − LSL) / (6 σ_overall) |
| Ppk | min( (USL − x̄) / (3 σ_overall), (x̄ − LSL) / (3 σ_overall) ) |
| ppm | 10⁶ × [Φ((LSL − x̄)/σ_overall) + 1 − Φ((USL − x̄)/σ_overall)] |

`ppm` is **expected overall** nonconforming parts per million under a normal model, not the observed fraction out of spec. A constant series has both sigmas = 0: Cp/Cpk/Pp/Ppk are blank (`NaN`); `ppm` is 0 if x̄ is inside the specs, otherwise 1,000,000.

## Result

One row. Set the PY cell to **Excel value**.

| Column | Notes |
|--------|-------|
| `mean` | x̄ |
| `stdev_within` | MR̄ / 1.128 |
| `stdev_overall` | Sample s |
| `cp`, `cpk` | Potential capability (within) |
| `pp`, `ppk` | Overall capability |
| `ppm` | Expected overall PPM |

## Example

```python
capability_report([10, 12, 11, 13, 12], 16, 8)
```

x̄ = 11.6, σ_within ≈ 1.33, σ_overall ≈ 1.14.
