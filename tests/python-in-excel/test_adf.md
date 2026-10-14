# Test: adf

## Setup

1. Formulas → **Initialization** → paste `adf` from `source/python-in-excel/functions/adf.py` after the default imports → Save.
2. Put `1, -1` repeated 20 times in `A1:A40` (oscillating, mean-reverting).
3. Put this random-walk path in `B1:B40`: `1, 0, 2, 3, 1, 1, 2, 1, 4, 2, 3, 3, 2, 4, 3, 4, 1, 3, 3, 4, 5, 4, 6, 7, 5, 5, 6, 5, 8, 6, 7, 7, 6, 8, 7, 8, 5, 7, 7, 8`.

Set the PY cell to **Excel value**. H0 is a unit root. Small p-value → `stationary` is True.

## Cases

| Python | Expected |
|--------|----------|
| `list(adf("A1:A40").columns)` | `['metric', 'value']` |
| `list(adf("A1:A40")["metric"])` | `['n', 'adf_stat', 'pvalue', 'lags', 'nobs', 'crit_1pct', 'crit_5pct', 'crit_10pct', 'icbest', 'alpha', 'stationary']` |
| `adf("A1:A40").set_index("metric").loc["n", "value"]` | `40` |
| `adf("A1:A40").set_index("metric").loc["alpha", "value"]` | `0.05` |
| `bool(adf("A1:A40").set_index("metric").loc["stationary", "value"])` | `True` |
| `adf("A1:A40").set_index("metric").loc["pvalue", "value"] < 0.05` | `True` |
| `bool(adf("B1:B40").set_index("metric").loc["stationary", "value"])` | `False` |
| `bool(adf([1, 0, 2, 3, 1, 1, 2, 1, 4, 2, 3, 3, 2, 4, 3, 4, 1, 3, 3, 4, 5, 4, 6, 7, 5, 5, 6, 5, 8, 6, 7, 7, 6, 8, 7, 8, 5, 7, 7, 8]).set_index("metric").loc["stationary", "value"])` | `False` |
| `adf([1, -1] * 20).set_index("metric").loc["n", "value"]` | `40` |
| `adf([1, -1] * 20, alpha=0.01).set_index("metric").loc["alpha", "value"]` | `0.01` |
