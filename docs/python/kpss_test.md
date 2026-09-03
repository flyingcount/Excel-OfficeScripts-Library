# kpss_test

KPSS stationarity test. Null hypothesis is stationarity (opposite of ADF). Spills statistic, p-value, critical values, and a `stationary` flag (`1` when p ≥ alpha).

Formula: `source/python-in-excel/functions/kpss_test.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
kpss_test("A1:A50")
kpss_test("A1:A50", alpha=0.05, regression="ct")
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `alpha` | No | Significance level. Default `0.05`. |
| `regression` | No | `c` (constant, default) or `ct` (constant + trend). |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Metric table with `stationary` = 1 if you fail to reject H0 (treat as stationary).
