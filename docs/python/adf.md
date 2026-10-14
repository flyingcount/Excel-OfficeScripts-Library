# adf

Augmented Dickey-Fuller (ADF) test for a **unit root**. Use it to check whether a series looks stationary (mean-reverting) before you treat it as a trading spread or oscillator.

Formula: `source/python-in-excel/functions/adf.py`

Null hypothesis **H0**: the series has a unit root (non-stationary). A small p-value rejects H0: the series looks stationary, which is consistent with mean-reversion.

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
adf("B2:B50")
adf("B2:B50", regression="ct")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric column). |
| `regression` | No | `"c"` constant (default), `"ct"` constant + trend, `"ctt"` constant + trend + trend², `"n"` none. |
| `alpha` | No | P-value cutoff for the `stationary` flag. Default `0.05`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least 8 numeric values. Blanks are dropped. Lag length is chosen by AIC (`statsmodels.tsa.stattools.adfuller`).

## Result

Two columns: `metric`, `value`.

| Metric | Meaning |
|--------|---------|
| `n` | Count after dropping blanks. |
| `adf_stat` | ADF test statistic. More negative → more evidence against a unit root. |
| `pvalue` | MacKinnon p-value. Small → reject H0 (stationary). |
| `lags` | AIC-chosen lag count. |
| `nobs` | Observations used in the regression. |
| `crit_1pct`, `crit_5pct`, `crit_10pct` | Critical values for the statistic. |
| `icbest` | Best information criterion from the lag search. |
| `alpha` | Cutoff you passed. |
| `stationary` | `True` when `pvalue < alpha`. |

Failing to reject H0 does **not** prove a random walk. It means you do not have evidence of stationarity at that alpha, so do not assume mean-reversion.

## Example

Oscillating values in `A1:A40` (`1, -1, 1, -1`, …):

```python
adf("A1:A40")
```

`stationary` should be `True`. A stochastic trend (random walk) typically stays `False`. A deterministic line such as `1…40` is not a unit-root process, so do not use it as the non-stationary check.
