# arima_estimate

Estimate a non-seasonal **ARIMA(p, d, q)** order in two stages: an **ADF test** determines the differencing order `d`, then a **grid search** over `p` and `q` minimises AIC or BIC. Uses `statsmodels.tsa.arima.model.ARIMA` and `statsmodels.tsa.stattools.adfuller`.

Formula: `source/python-in-excel/functions/arima_estimate.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` (time series functions only) or the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
arima_estimate("A1:A100")
arima_estimate("A1:A100", criterion="bic")
arima_estimate("A1:A100", full=True)
```

## How it works

### Step 1 — ADF differencing

Starting with `d = 0`, run the Augmented Dickey–Fuller test on the series:

- If the ADF p-value < `alpha` (default 0.05), the series is stationary at that `d` — stop.
- Otherwise increment `d`, difference the series, and test again.
- Stop when `d` reaches `d_max` or fewer than 4 observations remain.

### Step 2 — grid search

For the chosen `d`, fit ARIMA(p, d, q) for every `p` in 0..`p_max` and `q` in 0..`q_max`. Models that fail to converge are skipped. The model with the lowest AIC (default) or BIC wins.

## Comparison with arima_order

| | `arima_order` | `arima_estimate` |
|-|---------------|------------------|
| Differencing | Brute-force: searches every `d` in 0..`d_max` | ADF test pins `d` first |
| Criterion | AIC only | AIC or BIC (`criterion`) |
| Grid size | `(p_max+1) × (d_max+1) × (q_max+1)` | `(p_max+1) × (q_max+1)` (smaller, faster) |
| Result | p, d, q only | p, d, q, aic, bic, adf_pvalue, adf_d |
| Full grid | No | `full=True` spills every fitted model |

Use `arima_order` for a quick, simple order pick. Use `arima_estimate` when you want the ADF test to determine stationarity, want to compare AIC vs BIC, or want to inspect the full grid.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric column). |
| `p_max` | No | Maximum AR order. Default `3`. |
| `q_max` | No | Maximum MA order. Default `3`. |
| `d_max` | No | Maximum differencing order for the ADF loop. Default `2`. |
| `criterion` | No | `'aic'` (default) or `'bic'`. |
| `alpha` | No | ADF significance level. Default `0.05`. |
| `full` | No | `False` (default) returns one row. `True` returns the full grid sorted by criterion. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

One-row spill (or full grid when `full=True`):

| Column | Notes |
|--------|-------|
| `p` | AR order. |
| `d` | Differencing order (set by ADF). |
| `q` | MA order. |
| `aic` | Akaike information criterion of the fitted model. |
| `bic` | Bayesian information criterion of the fitted model. |
| `adf_pvalue` | ADF test p-value at the chosen `d`. |
| `adf_d` | Same as `d` (confirms the ADF-selected differencing). |

Empty (headers only) if no model fitted.

## Example

```python
arima_estimate([1,3,2,4,3,5,4,6,5,7,6,8,7,9,8,10,9,11,10,12])
```

The ADF test likely finds the series non-stationary at `d=0`, stationary at `d=1`, then the grid search picks the best `(p, q)` pair.

```python
arima_estimate("A1:A100", criterion="bic", full=True)
```

Spills the full grid of fitted models sorted by BIC, so you can compare alternatives.
