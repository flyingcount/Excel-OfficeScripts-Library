# seasonal_indices

Seasonal index for each slot in the cycle (multiplicative or additive).

Formula: `source/python-in-excel/functions/seasonal_indices.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
seasonal_indices("A1:A48", period=12)
seasonal_indices("A1:A48", period=12, kind="additive")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `period` | No | Season length. Default `12`. |
| `kind` | No | `multiplicative` (default) or `additive`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Columns: `season`, `index`, `kind`. One row per season slot.
