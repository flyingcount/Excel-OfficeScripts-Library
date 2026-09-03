# baseline_forecast

Generate a baseline forecast using **naive**, **seasonal naive**, or **drift** methods. Spills **actual rows** followed by **forecast rows** with a `label` column (`Actual`, `Forecast Naive`, etc.).

Formula: `source/python-in-excel/functions/baseline_forecast.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` (time series functions only) or the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
baseline_forecast("Table1[#All]", date_col="Date", value_col="Sales")
baseline_forecast("A1:B100", date_col="Date", value_col="Value", h=6, method="drift")
baseline_forecast("A1:B100", date_col="Date", value_col="Value", h=24,
                  method="seasonal_naive", period=12)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Table/range with date and value columns, DataFrame, or value Series/list. |
| `date_col` | No | Header of the date column (e.g. `"Date"`). Auto-detected if omitted. |
| `value_col` | No | Header of the value column (e.g. `"Sales"`). Auto-detected if omitted. |
| `h` | No | Forecast horizon — number of future steps. Default `12`. |
| `method` | No | `'naive'` (default), `'seasonal_naive'` (or `'snaive'`), or `'drift'`. |
| `period` | No | Seasonal period for `seasonal_naive`. Default `1`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Pass `date_col` and `value_col` to match your table headers. If omitted, the first parseable date column and first numeric column are used.

Forecast dates extend from the last actual date using the median step between observed dates (daily if irregular). Value-only input (no dates) uses integer steps `1..n` for actuals and `n+1..n+h` for forecasts.

## Methods

### Naive (default)

Repeat the last observed value for every future step.

### Seasonal naive

Cycle the last `period` values. Label: `Forecast Seasonal Naive`.

### Drift

Extend a line from the first to the last observation. Label: `Forecast Drift`.

## Result

One table: actual rows first, forecast rows appended. Set the PY cell to **Excel value** to spill it.

| Column | Notes |
|--------|-------|
| `date` | Observed dates, then projected forecast dates. |
| `value` | Observed values, then forecast values. |
| `label` | `Actual` for history; `Forecast Naive`, `Forecast Seasonal Naive`, or `Forecast Drift` for future rows. |

## Example

```python
df = pd.DataFrame({
    "Date": pd.date_range("2020-01-01", periods=5, freq="MS"),
    "Sales": [10, 20, 30, 40, 50],
})
baseline_forecast(df, date_col="Date", value_col="Sales", h=3, method="drift")
```

| date | value | label |
|------|-------|-------|
| 2020-01-01 | 10 | Actual |
| … | … | Actual |
| 2020-05-01 | 50 | Actual |
| 2020-06-01 | 60 | Forecast Drift |
| 2020-07-01 | 70 | Forecast Drift |
| 2020-08-01 | 80 | Forecast Drift |

Naive with `h=3` on the same data: forecast rows are all `50` with label `Forecast Naive`.
