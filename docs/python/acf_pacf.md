# acf_pacf

Autocorrelation (ACF) and partial autocorrelation (PACF) of a series. Use the plot to see lag effects and momentum: slow ACF decay suggests persistence; a PACF spike at lag *k* points to an AR(*k*)-style lag.

Formula: `source/python-in-excel/functions/acf_pacf.py`

`resid_analysis(..., plot=True)` already includes an ACF panel for residuals. Use `acf_pacf` on the raw series (prices, returns, or a spread).

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste the whole `init/PaulPythonLibrary.py`.

Chart (leave as a **Python object**):

```python
acf_pacf("B2:B50")
acf_pacf("B2:B50", lags=20)
```

Table (PY cell output **Excel value**):

```python
acf_pacf("B2:B50", plot=False)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric column). |
| `lags` | No | Number of lags. Default `min(10, n//2 - 1)`. |
| `plot` | No | `True` (default) returns a two-panel figure. `False` spills `lag`, `acf`, `pacf`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least 4 numeric values. Blanks are dropped.

## Result (plot)

Two panels: **ACF** and **PACF**, with statsmodels confidence bands. Keep the PY cell as a Python object so Excel draws the figure.

## Result (table)

| Column | Meaning |
|--------|---------|
| `lag` | 0 … `lags`. Lag 0 is 1 for both ACF and PACF. |
| `acf` | Correlation with the series lagged by that many steps. |
| `pacf` | Partial autocorrelation at that lag. |

Large ACF at short lags is momentum (or leftover trend). ACF that flips sign can show mean-reversion. Read PACF for the lag that remains after earlier lags are removed.
