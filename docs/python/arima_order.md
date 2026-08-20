# arima_order

AIC grid search for a non-seasonal **ARIMA(p, d, q)** order. Uses `statsmodels.tsa.arima.model.ARIMA`.

Formula: `source/python-in-excel/functions/arima_order.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
arima_order("A1:A50")
arima_order("A1:A50", p_max=2, d_max=1, q_max=2)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric column). |
| `p_max` | No | Search `p` from 0 through this value. Default `3`. |
| `d_max` | No | Search `d` from 0 through this value. Default `2`. |
| `q_max` | No | Search `q` from 0 through this value. Default `3`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Fits that error are skipped. Warnings from statsmodels are suppressed only for the search.

The default grid is 4 × 3 × 4 = 48 models and can take several seconds in Python in Excel.

## Result

One-row spill: `p`, `d`, `q` for the lowest finite AIC. Empty (headers only) if no model fitted.
