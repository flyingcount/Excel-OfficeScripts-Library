# detect_anomalies

Flag unusual points in an ordered series.

Formula: `source/python-in-excel/functions/detect_anomalies.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
detect_anomalies("A1:A48", method="stl", period=12)
detect_anomalies("A1:A50", method="iqr", z=1.5)
detect_anomalies("A1:A50", method="zscore", z=3)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `method` | No | `stl` (default), `iqr`, or `zscore`. |
| `period` | No | STL seasonal length. Default `12`. |
| `z` | No | Cutoff. STL/zscore: \|z\| > z (default `3`). IQR: fence multiplier (pass `1.5` for Tukey). |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Columns: `t`, `value`, `residual`, `score`, `is_anomaly` (1/0).
