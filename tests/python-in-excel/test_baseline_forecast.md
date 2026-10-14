# Test: baseline_forecast

## Setup

1. Formulas → **Initialization** → paste `baseline_forecast` from `source/python-in-excel/functions/baseline_forecast.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Build a small table in `A1:B5` with headers `Date` and `Value`:

   | Date | Value |
   |------|-------|
   | 2020-01-01 | 10 |
   | 2020-02-01 | 20 |
   | 2020-03-01 | 30 |
   | 2020-04-01 | 40 |
   | 2020-05-01 | 50 |

3. Put `1, 2, 3, 4` in `C1:C4` for seasonal_naive tests without dates.

## Cases

In a PY cell, set output to **Excel value**.

### Shape and columns (table with dates)

| Python | Expected |
|--------|----------|
| `list(baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=3).columns)` | `['date', 'value', 'label']` |
| `baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=3).shape` | `(8, 3)` |
| `baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=12).shape` | `(17, 3)` |

5 actual rows + `h` forecast rows.

### Labels

| Python | Expected |
|--------|----------|
| `baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=2)["label"].iloc[0]` | `Actual` |
| `baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=2)["label"].iloc[4]` | `Actual` |
| `baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=2)["label"].iloc[5]` | `Forecast Naive` |
| `baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=2, method="drift")["label"].iloc[6]` | `Forecast Drift` |
| `baseline_forecast("C1:C4", h=2, method="seasonal_naive", period=4)["label"].iloc[4]` | `Forecast Seasonal Naive` |

### Naive values

Last value in table is 50.

| Python | Expected |
|--------|----------|
| `baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=3)["value"].iloc[-3:].tolist()` | `[50.0, 50.0, 50.0]` |
| `baseline_forecast([7], h=2)["value"].tolist()` | `[7.0, 7.0, 7.0]` |
| `baseline_forecast([7], h=2)["label"].tolist()` | `['Actual', 'Forecast Naive', 'Forecast Naive']` |

### Drift values

Slope = (50 − 10) / 4 = 10.

| Python | Expected |
|--------|----------|
| `baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=3, method="drift")["value"].iloc[-3:].tolist()` | `[60.0, 70.0, 80.0]` |

### Seasonal naive

| Python | Expected |
|--------|----------|
| `baseline_forecast("C1:C4", h=6, method="seasonal_naive", period=4)["value"].iloc[-6:].tolist()` | `[1.0, 2.0, 3.0, 4.0, 1.0, 2.0]` |

### Forecast dates (monthly table)

Last actual date 2020-05-01; step is one month.

| Python | Expected |
|--------|----------|
| `str(baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=2)["date"].iloc[5].date())` | `2020-06-01` |
| `str(baseline_forecast("A1:B5", date_col="Date", value_col="Value", h=2)["date"].iloc[6].date())` | `2020-07-01` |

### Edge cases

| Python | Expected |
|--------|----------|
| `baseline_forecast([1], h=1, method="drift")` | `#PYTHON!` — `Need at least 2 observations for drift.` |
| `baseline_forecast([1], h=3, method="seasonal_naive", period=4)` | `#PYTHON!` — `Need at least 4 observations for seasonal_naive` |
| `baseline_forecast([], h=1)` | `#PYTHON!` — `Need at least 1 observation.` |
| `baseline_forecast([1, 2, 3], method="foo")` | `#PYTHON!` — `method 'foo' not supported` |
| `baseline_forecast("A1:B5", date_col="Missing", value_col="Value")` | `#PYTHON!` — `Column 'Missing' not found` |
