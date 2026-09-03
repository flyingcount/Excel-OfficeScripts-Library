# impute

Fill missing values in a series. Spills the original value, the filled series, and a missing flag.

Formula: `source/python-in-excel/functions/impute.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
impute("A1:A50", method="linear")
impute("A1:A48", method="seasonal", period=12)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `method` | No | `linear`, `ffill`, `bfill`, `mean`, `median`, or `seasonal`. Default `linear`. |
| `period` | No | Season length for `seasonal`. Default `12`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Columns: `value`, `imputed`, `was_missing` (1/0).
