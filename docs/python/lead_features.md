# lead_features

Lead columns from a value series (`y.shift(-k)`). Pair with `lag_features` for past values.

Formula: `source/python-in-excel/functions/lead_features.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
lead_features("A1:A20")
lead_features("A1:A20", leads=3)
lead_features("A1:A20", leads="1,7,12")
lead_features("A1:B50", leads=1, value_col="Sales", date_col="Date")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, or a table with dates and values. |
| `leads` | No | `3` gives `lead_1` … `lead_3`. A list or `"1,7,12"` gives those leads only. Default `1`. |
| `value_col` | No | Header of the value column. First numeric if omitted. |
| `date_col` | No | Header of the date column. Auto-detected if omitted. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Rows are sorted by date when a date column is present. Trailing rows are blank until each lead has a future value.

## Result

| Column | Notes |
|--------|-------|
| `date` | Present when a date column is found or named. |
| value | Original series, named from `value_col` (or `value`). |
| `lead_k` | Value from `k` rows later. |
