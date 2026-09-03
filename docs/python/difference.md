# difference

Regular or seasonal differencing. Applied `order` times at the given `lag`. Leading rows that cannot be differenced are blank.

Formula: `source/python-in-excel/functions/difference.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
difference("A1:A50", lag=1, order=1)
difference("A1:A48", lag=12, order=1)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `lag` | No | Difference step. Default `1`. |
| `order` | No | How many times to difference. Default `1`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Columns: `value`, `diff`.
