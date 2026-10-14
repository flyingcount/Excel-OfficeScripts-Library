# lag_features

Lag columns, **rolling-window statistics**, and **EMA** from a value series. Rolling stats and EMA use only **past** values, so the current row is not in the window.

Formula: `source/python-in-excel/functions/lag_features.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` or `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
lag_features("A1:A20")
lag_features("A1:B50", value_col="Sales", date_col="Date")
lag_features("A1:A20", lags=3, windows=7)
lag_features("A1:A20", lags="1,7,12", windows="7,28", stats="mean,std")
lag_features("A1:A20", lags=1, windows=0, ema=12)
lag_features("A1:A20", lags=0, windows=0, ema="12,26")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, or a table with dates and values. Ref string, DataFrame, Series, or list. |
| `value_col` | No | Header of the value column. First numeric column if omitted. |
| `date_col` | No | Header of the date column. Auto-detected from datetime (or text dates) if omitted. Excel serials need this argument. |
| `lags` | No | `3` gives `lag_1` … `lag_3`. A list or `"1,7,12"` gives those lags only. `0` or `None` skips lags. Default `1`. |
| `windows` | No | Window length, or a list / `"7,28"`. `0` or `None` skips rolling stats. Default `7`. |
| `stats` | No | Rolling aggregations: `mean`, `std`, `min`, `max`, `median`, `sum`. Comma-separated or list. Default `'mean'`. |
| `ema` | No | EMA span, or a list / `"12,26"`. Recursive EMA with α = 2/(span+1), then shifted by 1. `0` or `None` skips. Default `0`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Need at least one lag, window, or EMA span. Rows are sorted by date when a date column is present.

## Result

One row per input. Set the PY cell to **Excel value**.

| Column | Notes |
|--------|-------|
| `date` | Present when a date column is found or named. |
| value | Original series, named from `value_col` (or `value`). |
| `lag_k` | Value from `k` rows earlier. |
| `roll_mean_w`, `roll_std_w`, … | Statistic over the previous `w` values (`y.shift(1).rolling(w)`). Sample std (`ddof=1`). |
| `ema_s` | Recursive EMA of span `s` (`α = 2/(s+1)`), then shifted by 1 so row `t` is the EMA through `t-1`. |

Early rows are blank until each lag or window has enough history. Drop those rows before fitting a model that cannot take blanks.

Default `lag_features("A1:A20")` spills the value, `lag_1`, and `roll_mean_7`.
