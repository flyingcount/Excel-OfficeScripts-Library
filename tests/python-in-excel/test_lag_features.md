# Test: lag_features

## Setup

1. Formulas → **Initialization** → paste `lag_features` from `source/python-in-excel/functions/lag_features.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put `10, 20, 30, 40, 50` in `A1:A5`.
3. Optional table in `C1:D6`:

   | Date | Sales |
   |------|-------|
   | 2020-01-05 | 50 |
   | 2020-01-01 | 10 |
   | 2020-01-02 | 20 |
   | 2020-01-03 | 30 |
   | 2020-01-04 | 40 |

Lags are `y.shift(k)`. Rolling stats are `y.shift(1).rolling(w)` — the current row is not in the window. EMA is recursive (`α = 2/(span+1)`), then shifted by 1.

For `10, 20, 30, 40, 50` with `lags=2` and `windows=3`: `lag_1` is blank, 10, 20, 30, 40; `roll_mean_3` is blank until row 4, then 20 and 30.

## Cases

In a PY cell, set output to **Excel value**.

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(lag_features([10, 20, 30, 40, 50], lags=2, windows=3).columns)` | `['value', 'lag_1', 'lag_2', 'roll_mean_3']` |
| `lag_features([10, 20, 30, 40, 50], lags=2, windows=3).shape` | `(5, 4)` |
| `list(lag_features([10, 20, 30, 40], lags=1, windows=0).columns)` | `['value', 'lag_1']` |
| `list(lag_features([10, 20, 30, 40], lags=0, windows=2, stats="mean,std").columns)` | `['value', 'roll_mean_2', 'roll_std_2']` |
| `list(lag_features([10, 20, 30, 40], lags="1,3", windows=0).columns)` | `['value', 'lag_1', 'lag_3']` |
| `list(lag_features([10, 20, 30, 40], lags=0, windows=0, ema=2).columns)` | `['value', 'ema_2']` |
| `list(lag_features([10, 20, 30, 40], lags=0, windows=0, ema="2,3").columns)` | `['value', 'ema_2', 'ema_3']` |

### Values

| Python | Expected |
|--------|----------|
| `float(lag_features([10, 20, 30, 40, 50], lags=2, windows=3).loc[1, "lag_1"])` | `10.0` |
| `float(lag_features([10, 20, 30, 40, 50], lags=2, windows=3).loc[2, "lag_2"])` | `10.0` |
| `pd.isna(lag_features([10, 20, 30, 40, 50], lags=2, windows=3).loc[0, "lag_1"])` | `True` |
| `float(lag_features([10, 20, 30, 40, 50], lags=2, windows=3).loc[3, "roll_mean_3"])` | `20.0` |
| `float(lag_features([10, 20, 30, 40, 50], lags=2, windows=3).loc[4, "roll_mean_3"])` | `30.0` |
| `pd.isna(lag_features([10, 20, 30, 40, 50], lags=2, windows=3).loc[2, "roll_mean_3"])` | `True` |
| `round(float(lag_features([10, 20, 30, 40], lags=0, windows=2, stats="std").loc[2, "roll_std_2"]), 4)` | `7.0711` |
| `round(float(lag_features([10, 20, 30, 40], lags=0, windows=0, ema=2).loc[2, "ema_2"]), 4)` | `16.6667` |
| `round(float(lag_features([10, 20, 30, 40], lags=0, windows=0, ema=2).loc[3, "ema_2"]), 4)` | `25.5556` |
| `pd.isna(lag_features([10, 20, 30, 40], lags=0, windows=0, ema=2).loc[1, "ema_2"])` | `True` |

`roll_mean_3` at row 4 (0-based index 3) is the mean of 10, 20, 30 — the three values **before** 40.

### Table with dates (sorts by date)

| Python | Expected |
|--------|----------|
| `list(lag_features("C1:D6", value_col="Sales", date_col="Date", lags=1, windows=0)["Sales"])` | `[10, 20, 30, 40, 50]` |
| `float(lag_features("C1:D6", value_col="Sales", date_col="Date", lags=1, windows=0).loc[1, "lag_1"])` | `10.0` |

### Edge cases

| Python | Expected |
|--------|----------|
| `lag_features([10, 20], lags=0, windows=0)` | `#PYTHON!` — `Provide at least one lag, window, or ema span.` |
| `lag_features([10, 20], lags=1, windows=2, stats="foo")` | `#PYTHON!` — `stats must be mean, std, min, max, median, or sum.` |
| `lag_features(pd.DataFrame({"Sales": [10, 20]}), value_col="Missing")` | `#PYTHON!` — `Column 'Missing' not found` |
