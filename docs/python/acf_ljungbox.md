# acf_ljungbox

Sample **ACF** and **Ljung-Box** Q statistic at each lag from 1 through `lags` (default 20). Use this on a series or on residuals (`stl()` output uses the `resid` column).

Formula: `source/python-in-excel/functions/acf_ljungbox.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` or `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
acf_ljungbox("A1:A100")
acf_ljungbox("A1:A100", lags=12)
acf_ljungbox(stl("B2:B25", 12))
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, residual column, `stl()` table, Series, DataFrame, or ref string. First numeric column, or `resid` / `residual` / `residuals` when present. |
| `lags` | No | Maximum lag. Default `20`. Capped at `n-2`. |
| `alpha` | No | Significance for `lb_sig`. Default `0.05`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least 3 numeric values. Blanks are dropped.

## Result

One row per lag. Set the PY cell to **Excel value** to spill.

| Column | Notes |
|--------|-------|
| `lag` | 1 through the chosen lag count. |
| `acf` | Sample autocorrelation at that lag (statsmodels `acf`, lag 0 omitted). |
| `acf_se` | White-noise standard error `1 / sqrt(n)`. |
| `acf_sig` | `1` if \|acf\| > 1.96 × `acf_se`, else `0`. |
| `lb_stat` | Ljung-Box Q up to that lag. |
| `lb_pvalue` | p-value for Q. p < `alpha` suggests leftover autocorrelation. |
| `lb_sig` | `1` if `lb_pvalue` < `alpha`, else `0`. |

`resid_analysis` reports Ljung-Box at a single lag. This function reports ACF and Ljung-Box **at every lag**.
