# Test: expsmooth

## Setup

1. Formulas → **Initialization** → paste `expsmooth` from `source/python-in-excel/functions/expsmooth.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put `10`, `12`, `14` in `A1:A3`.
3. Optional: add LAMBDA `EXPSMOOTH` to cross-check the last SES level (`11.12`).

## Cases (table)

In a PY cell, set output to **Excel value**. Default `alpha=0.2`, `h=12`, `level=0.95`. SES forecasts are flat at the last level; `lower` / `upper` are blank on actual rows and widen with the horizon.

| Python | Expected |
|--------|----------|
| `list(expsmooth([10, 12, 14]).columns)` | `['t', 'value', 'lower', 'upper', 'label']` |
| `expsmooth([10, 12, 14]).shape` | `(15, 5)` |
| `str(expsmooth([10, 12, 14]).iloc[0]["label"])` | `Actual` |
| `str(expsmooth([10, 12, 14]).iloc[-1]["label"])` | `Forecast SES` |
| `int((expsmooth([10, 12, 14])["label"] == "Forecast SES").sum())` | `12` |
| `round(float(expsmooth([10, 12, 14], 0.2, 3).iloc[-1]["value"]), 2)` | `11.12` |
| `bool(pd.isna(expsmooth([10, 12, 14], h=1).iloc[0]["lower"]))` | `True` |
| `float(expsmooth([10, 12, 14], 0.2, 1).iloc[-1]["lower"]) < 11.12` | `True` |
| `float(expsmooth([10, 12, 14], 0.2, 1).iloc[-1]["upper"]) > 11.12` | `True` |
| `float(expsmooth([10, 12, 14], 0.2, 3).iloc[-1]["lower"]) < float(expsmooth([10, 12, 14], 0.2, 3).iloc[3]["lower"])` | `True` |
| `float(expsmooth([10, 12, 14], 0.2, 1, 0.99).iloc[-1]["upper"]) > float(expsmooth([10, 12, 14], 0.2, 1, 0.95).iloc[-1]["upper"])` | `True` |
| `expsmooth("A1:A3", 0.2, 3).shape` | `(6, 5)` |
| `round(float(expsmooth("A1:A3", h=3).iloc[-1]["value"]), 2)` | `11.12` |
| `float(expsmooth([10, 12, 14], 1, 2).iloc[-1]["value"])` | `14` |

## Cases (plot)

Leave the PY cell as a **Python object**.

| Python | Expected |
|--------|----------|
| `type(expsmooth([10, 12, 14], plot=True)).__name__` | `Figure` |
| `len(expsmooth([10, 12, 14], h=3, plot=True).axes)` | `1` |
| `expsmooth([10, 12, 14], plot=True).axes[0].get_title()` | `SES forecast` |
| `len(expsmooth([10, 12, 14], h=3, plot=True).axes[0].collections) >= 1` | `True` |
