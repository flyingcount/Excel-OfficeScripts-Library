# Test: arima_order

## Setup

1. Formulas → **Initialization** → paste `arima_order` from `source/python-in-excel/functions/arima_order.py` after the default imports → Save.
2. Put a numeric series of at least 20 values in `A1:A24` (for example two copies of `1` … `12`).

The search can take several seconds. Set the PY cell to **Excel value**.

## Cases

| Python | Expected |
|--------|----------|
| `list(arima_order("A1:A24").columns)` | `['p', 'd', 'q']` |
| `arima_order("A1:A24").shape` | `(1, 3)` |
| `arima_order("A1:A24")["p"].iloc[0] in range(4)` | `True` |
| `arima_order("A1:A24")["d"].iloc[0] in range(3)` | `True` |
| `arima_order("A1:A24")["q"].iloc[0] in range(4)` | `True` |
| `arima_order("A1:A24", p_max=1, d_max=0, q_max=0).shape` | `(1, 3)` |
| `int(arima_order("A1:A24", p_max=0, d_max=0, q_max=0)["p"].iloc[0])` | `0` |
| `int(arima_order("A1:A24", p_max=0, d_max=0, q_max=0)["d"].iloc[0])` | `0` |
| `int(arima_order("A1:A24", p_max=0, d_max=0, q_max=0)["q"].iloc[0])` | `0` |
