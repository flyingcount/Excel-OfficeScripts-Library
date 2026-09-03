# Test: acf_ljungbox

## Setup

1. Formulas → **Initialization** → paste `acf_ljungbox` from `source/python-in-excel/functions/acf_ljungbox.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put `1, 2, 3, 4, 5, 6, 7, 8, 9, 10` in `A1:A10` (strong lag-1 autocorrelation).
3. Put ten copies of `0` except one spike, or use `np.random.seed(1); list(np.random.randn(40))` in `B1:B40` for a longer series.

Need at least 3 values. Default `lags=20` is capped at `n-2`, so `A1:A10` yields 8 rows.

## Cases

In a PY cell, set output to **Excel value**.

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(acf_ljungbox("A1:A10").columns)` | `['lag', 'acf', 'acf_se', 'acf_sig', 'lb_stat', 'lb_pvalue', 'lb_sig']` |
| `acf_ljungbox("A1:A10").shape` | `(8, 7)` |
| `acf_ljungbox("A1:A10", lags=3).shape` | `(3, 7)` |
| `int(acf_ljungbox("A1:A10", lags=3)["lag"].iloc[0])` | `1` |
| `int(acf_ljungbox("A1:A10", lags=3)["lag"].iloc[2])` | `3` |

### ACF and Ljung-Box

A linear trend has large lag-1 ACF. `acf_se` for n=10 is `1/sqrt(10)` ≈ 0.3162.

| Python | Expected |
|--------|----------|
| `round(float(acf_ljungbox("A1:A10", lags=1)["acf_se"].iloc[0]), 4)` | `0.3162` |
| `acf_ljungbox("A1:A10", lags=1)["acf"].iloc[0] > 0.5` | `True` |
| `int(acf_ljungbox("A1:A10", lags=1)["acf_sig"].iloc[0])` | `1` |
| `np.isfinite(acf_ljungbox("A1:A10", lags=3)["lb_stat"].iloc[0])` | `True` |
| `acf_ljungbox("A1:A10", lags=3)["lb_pvalue"].iloc[0] < 0.05` | `True` |
| `int(acf_ljungbox("A1:A10", lags=3)["lb_sig"].iloc[0])` | `1` |
| `acf_ljungbox([0, 0, 0, 0, 0, 1, 0, 0, 0, 0], lags=2)["acf"].iloc[0] < 0.5` | `True` |

### Edge cases

| Python | Expected |
|--------|----------|
| `acf_ljungbox([1, 2])` | `#PYTHON!` — `Need at least 3 numeric values.` |
| `acf_ljungbox(pd.DataFrame({"resid": [1, 2, 3, 4, 5, 6, 7, 8]}), lags=2).shape` | `(2, 7)` |
