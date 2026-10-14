# seasonally_adjust

Remove a seasonal index from a series (same kind as `seasonal_indices`).

Formula: `source/python-in-excel/functions/seasonally_adjust.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
seasonally_adjust("A1:A48", period=12)
seasonally_adjust("A1:A48", period=12, kind="additive")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `period` | No | Season length. Default `12`. |
| `kind` | No | `multiplicative` (default) or `additive`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Columns: `value`, `season`, `index`, `adjusted`.
