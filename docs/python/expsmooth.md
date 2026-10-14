# expsmooth

Simple exponential smoothing (SES) forecast with a prediction interval. Spills actuals plus appended forecast rows, or `plot=True` for a chart.

Formula: `source/python-in-excel/functions/expsmooth.py`

The level is `St = alpha * xt + (1 - alpha) * S(t-1)`, seeded with the first observation. SES has no trend or seasonality, so every future step equals the last level. That last level matches LAMBDA `EXPSMOOTH`.

The interval is `value ± z * sigma * sqrt(1 + alpha^2 * (h-1))`, where `sigma` is the RMSE of one-step in-sample errors and `z` is the normal quantile for `level` (default 0.95). The band widens with the horizon.

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

Table (PY cell output **Excel value**):

```python
expsmooth("A1:A24")
expsmooth("A1:A24", alpha=0.2, h=12)
expsmooth(df, h=6, level=0.8)
```

Chart (leave as a **Python object**):

```python
expsmooth("A1:A24", plot=True)
expsmooth(df, h=6, level=0.8, plot=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric col). |
| `alpha` | No | Smoothing constant. Default `0.2`. |
| `h` | No | Forecast horizon. Default `12`. |
| `level` | No | Prediction interval coverage between 0 and 1. Default `0.95`. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib chart. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Keep `alpha` as the second argument so `expsmooth(data, 0.2)` still sets α, not the horizon. Pass `h`, `level`, and `plot` by name, or `h` as the third argument (`expsmooth(data, 0.2, 6)`).

## Result (table)

Columns: `t`, `value`, `lower`, `upper`, `label` (`Actual` / `Forecast SES`). Set the PY cell to **Excel value** to spill. Actual rows leave `lower` / `upper` blank. Forecast rows are flat at the last SES level; the interval widens with `h`.

For `10, 12, 14` with `alpha=0.2` and `h=3`, the last level is `11.12` and the three forecast `value` cells are all `11.12`.

## Result (plot)

Actuals, point forecast, and a shaded interval. Leave the cell as a **Python object**, not Excel value.
