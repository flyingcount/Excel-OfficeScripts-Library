# acf_pacf

Sample **ACF** and **PACF** at lags 1 through `lags` (default 20). Output is a **table** (`plot=False`) or a **two-panel chart** (`plot=True`). Used to identify AR/MA orders; `acf_ljungbox` adds Ljung-Box Q instead of PACF.

Formula: `source/python-in-excel/functions/acf_pacf.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` or `init/PaulPythonLibrary.py`.

Table (PY cell output **Excel value**):

```python
acf_pacf("A1:A100")
acf_pacf("A1:A100", lags=12)
acf_pacf(stl("B2:B25", 12))
```

Chart (leave as a **Python object**):

```python
acf_pacf("A1:A100", plot=True)
acf_pacf("A1:A100", lags=24, plot=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, residual column, `stl()` table, Series, DataFrame, or ref string. Uses `resid` / `residual` / `residuals` when present; otherwise the first numeric column. |
| `lags` | No | Maximum lag. Default `20`. Capped at `min(n-2, n//2 - 1)` so PACF is defined. |
| `plot` | No | `False` (default) spills a table. `True` returns ACF (top) and PACF (bottom) charts. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least 4 numeric values. Blanks are dropped. PACF uses the Yule–Walker (`ywm`) method.

## Result (table)

| Column | Notes |
|--------|-------|
| `lag` | 1 through the chosen lag count. |
| `acf` | Sample autocorrelation. |
| `pacf` | Sample partial autocorrelation. |
| `se` | White-noise standard error `1 / sqrt(n)`. |
| `acf_sig` | `1` if \|acf\| > 1.96 × `se`. |
| `pacf_sig` | `1` if \|pacf\| > 1.96 × `se`. |

## Result (plot)

Two panels from `plot_acf` and `plot_pacf`. Leave the cell as a **Python object**, not Excel value.
