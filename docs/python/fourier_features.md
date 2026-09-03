# fourier_features

Sine and cosine Fourier terms for seasonal regression. For harmonic `k = 1..order`, angle = `2 * pi * k * t / period` with `t = 0` at the first row.

Formula: `source/python-in-excel/functions/fourier_features.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

```python
fourier_features("A1:A365", period=365, order=3)
fourier_features([1, 2, 3, 4], period=4, order=1)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `period` | No | Seasonal length in rows. Default `365`. |
| `order` | No | Number of harmonics. Default `3`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Result

Columns: `value`, `sin_1`…`sin_order`, `cos_1`…`cos_order`.
