# Test: forecast_plot

## Setup

1. Formulas → **Initialization** → paste `forecast_plot` from `source/python-in-excel/functions/forecast_plot.py` after the default imports → Save. Or paste `init/TimeSeries.py`.

Keep the PY cell as a **Python object** (not Excel value).

## Cases

| Python | Expected |
|--------|----------|
| `type(forecast_plot([10, 12, 11, 13], [14, 15])).__name__` | `Figure` |
| `len(forecast_plot([10, 12, 11, 13], [14, 15]).axes)` | `1` |
| `forecast_plot([10, 12, 11, 13], [14, 15]).axes[0].get_title()` | `Forecast` |
| `len(forecast_plot([10, 12], [14], lower=[13], upper=[15]).axes[0].collections) >= 1` | `True` |
| `forecast_plot([], [1])` | `#PYTHON!` — `actual needs at least 1 numeric value.` |
| `forecast_plot([10, 12], [14, 15], lower=[13])` | figure (lower alone; no fill) |
| `forecast_plot([10, 12], [14], lower=[1, 2], upper=[3])` | `#PYTHON!` — `lower length must match forecast.` |
