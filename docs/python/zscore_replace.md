# zscore_replace

Replace time-series values whose **absolute z-score** is above a cutoff. Replacement values come from interpolation of the remaining points.

Formula: `source/python-in-excel/functions/zscore_replace.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
zscore_replace("B2:B25")
zscore_replace("B2:B25", z=2)
zscore_replace("B2:B25", z=2, dates="A2:A25")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, or a date+value range/table. Ref string, DataFrame, Series, or list. |
| `z` | No | Absolute z-score cutoff. Points with \|z-score\| > `z` are replaced. Default `3`. |
| `dates` | No | Date column when dates are not in `data`. Used for time-based interpolation. |
| `headers` | No | First row is headers when `data` or `dates` is a ref string. Default `False`. |

Z-scores use the series mean and population standard deviation (`ddof=0`). A constant series (std = 0) is returned unchanged. Original blanks stay blank; they are not treated as outliers.

## Interpolation

- Interior outliers: linear interpolation between neighboring kept points. With a monotonic unique datetime index, interpolation is by time rather than by row number.
- Leading or trailing outliers: nearest remaining value (`bfill` / `ffill`).

## Result

A Series named `value`, same length as the input values. Set the PY cell to **Excel value** to spill the cleaned column.

## Example

Values in `B2:B10` with one spike. Cutoff `2` replaces the spike with the interpolated neighbors:

```python
zscore_replace([5, 5, 5, 5, 50, 5, 5, 5, 5], z=2)
```

Result: `5, 5, 5, 5, 5, 5, 5, 5, 5`. The same call with default `z=3` keeps `50` (its z-score is about 2.83).
