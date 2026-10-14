# adf_test

**Augmented Dickey–Fuller** unit-root test for stationarity (`statsmodels.tsa.stattools.adfuller`). Spills a metric table with the statistic, p-value, critical values, and a stationary flag.

Formula: `source/python-in-excel/functions/adf_test.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` or `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
adf_test("A1:A50")
adf_test("A1:A50", alpha=0.01)
adf_test("A1:A50", regression="ct")
```

## Hypothesis

H0: the series has a unit root (non-stationary).  
H1: the series is stationary.

Reject H0 when `pvalue` < `alpha` (default 0.05). That is also when `stationary` is `1`.

`arima_estimate` uses the same ADF test to choose the differencing order `d`. Use `adf_test` when you only need the stationarity result.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric column). |
| `alpha` | No | Significance level for `stationary`. Default `0.05`. |
| `regression` | No | `'c'` constant (default), `'ct'` constant and trend, `'n'` no constant, `'ctt'` constant, trend, and quadratic. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least 4 numeric values. Blanks are dropped. ADF lag length is chosen by AIC.

## Result

| Metric | Notes |
|--------|-------|
| `n` | Count after dropping blanks. |
| `adf_stat` | Test statistic. More negative than a critical value supports stationarity. |
| `pvalue` | MacKinnon p-value. p < alpha → stationary. |
| `usedlag` | Lag length chosen by AIC. |
| `nobs` | Observations used after lags. |
| `crit_1`, `crit_5`, `crit_10` | Critical values at 1%, 5%, 10%. |
| `alpha` | Level used for the flag. |
| `regression` | Spec that was fitted. |
| `stationary` | `1` if p-value < alpha, else `0`. |
| `interpretation` | One-line conclusion. |
