# stl

STL (Seasonal-Trend decomposition using LOESS) splits a series into **trend**, **seasonal**, and **residual**. Uses `statsmodels.tsa.seasonal.STL`, which is in the Python in Excel runtime.

Formula: `source/python-in-excel/functions/stl.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` (time series functions only) or the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
stl("B2:B49", 12)
stl("A1:B49", 12, headers=True)
stl("B2:B49", 12, dates="A2:A49")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, or a date+value range/table. Ref string, DataFrame, Series, or `xl()` result. |
| `period` | Yes | Observations per season. `12` monthly, `7` weekly, `4` quarterly. |
| `dates` | No | Date column when dates are not in `data`. |
| `robust` | No | `True` down-weights outliers. Default `False`. |
| `headers` | No | First row is headers when `data` or `dates` is a ref string. Default `False`. |

Need at least two full seasons (`2 * period` points). Missing values are dropped; remaining points are treated as equally spaced.

## Result

| Column | Meaning |
|--------|---------|
| `date` | Present when dates were supplied or detected in `data`. |
| `observed` | Input values after dropping blanks. |
| `trend` | Slow-moving level. |
| `seasonal` | Repeating seasonal component. |
| `resid` | Remainder. |

Additive identity: `observed = trend + seasonal + resid`.

## Example

Monthly values in `B2:B25`, period 12:

```python
stl("B2:B25", 12)
```

For the four-panel chart, use [stl_plot](stl_plot.md) instead of spilling this table.

To diagnose the `resid` column, use [resid_analysis](resid_analysis.md):

```python
resid_analysis(stl("B2:B25", 12))
resid_analysis(stl("B2:B25", 12), plot=True)
```


