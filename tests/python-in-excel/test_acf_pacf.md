# Test: acf_pacf

## Setup

1. Formulas → **Initialization** → paste `acf_pacf` from `source/python-in-excel/functions/acf_pacf.py` after the default imports → Save.
2. Put `1` … `24` in `A1:A24`.

Plot: leave the PY cell as a **Python object**. Table: set output to **Excel value**.

## Cases

| Python | Expected |
|--------|----------|
| `type(acf_pacf("A1:A24")).__name__` | `Figure` |
| `len(acf_pacf("A1:A24").axes)` | `2` |
| `acf_pacf("A1:A24").axes[0].get_title()` | `ACF` |
| `acf_pacf("A1:A24").axes[1].get_title()` | `PACF` |
| `list(acf_pacf("A1:A24", plot=False).columns)` | `['lag', 'acf', 'pacf']` |
| `acf_pacf([1, 2, 3, 4] * 6, lags=4, plot=False).shape` | `(5, 3)` |
| `acf_pacf([1, 2, 3, 4] * 6, lags=4, plot=False)["acf"].iloc[0]` | `1` |
| `acf_pacf([1, 2, 3, 4] * 6, lags=4, plot=False)["pacf"].iloc[0]` | `1` |
| `int(acf_pacf([1, 2, 3, 4] * 6, lags=4, plot=False)["lag"].iloc[-1])` | `4` |
| `type(acf_pacf([1, 2, 3, 4] * 6)).__name__` | `Figure` |
