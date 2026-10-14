# Test: acf_pacf

## Setup

1. Formulas → **Initialization** → paste `acf_pacf` from `source/python-in-excel/functions/acf_pacf.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put `1, 2, 3, 4, 5, 6, 7, 8, 9, 10` in `A1:A10`.
3. For plots, use a PY cell left as a **Python object**.

For n=10, max lag is `min(8, 4) = 4`, so default `lags=20` yields 4 rows.

## Cases

### Table (`plot=False`, output **Excel value**)

| Python | Expected |
|--------|----------|
| `list(acf_pacf("A1:A10").columns)` | `['lag', 'acf', 'pacf', 'se', 'acf_sig', 'pacf_sig']` |
| `acf_pacf("A1:A10").shape` | `(4, 6)` |
| `acf_pacf("A1:A10", lags=2).shape` | `(2, 6)` |
| `int(acf_pacf("A1:A10", lags=2)["lag"].iloc[0])` | `1` |
| `round(float(acf_pacf("A1:A10", lags=1)["se"].iloc[0]), 4)` | `0.3162` |
| `acf_pacf("A1:A10", lags=1)["acf"].iloc[0] > 0.5` | `True` |
| `np.isfinite(acf_pacf("A1:A10", lags=2)["pacf"].iloc[0])` | `True` |
| `int(acf_pacf("A1:A10", lags=1)["acf_sig"].iloc[0])` | `1` |

### Plot (`plot=True`, leave as **Python object**)

| Python | Expected |
|--------|----------|
| `type(acf_pacf("A1:A10", plot=True)).__name__` | `Figure` |
| `len(acf_pacf("A1:A10", plot=True).axes)` | `2` |

### Edge cases

| Python | Expected |
|--------|----------|
| `acf_pacf([1, 2, 3])` | `#PYTHON!` — `Need at least 4 numeric values.` |
| `acf_pacf(pd.DataFrame({"resid": [1, 2, 3, 4, 5, 6, 7, 8]}), lags=2).shape` | `(2, 6)` |
