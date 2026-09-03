# Test: arima_estimate

## Setup

1. Formulas → **Initialization** → paste `arima_estimate` from `source/python-in-excel/functions/arima_estimate.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put a trending series of at least 20 values in `A1:A24` (for example `1, 3, 2, 4, 3, 5, 4, 6, 5, 7, 6, 8, 7, 9, 8, 10, 9, 11, 10, 12, 11, 13, 12, 14`).
3. Put a stationary series (e.g. `np.random.seed(42); list(np.random.randn(30))`) in `B1:B30`, or use `0.5, -0.1, 0.3, -0.4, 0.2, ...` (30 mean-zero values).

The search can take several seconds. Set the PY cell to **Excel value**.

## Cases

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(arima_estimate("A1:A24").columns)` | `['p', 'd', 'q', 'aic', 'bic', 'adf_pvalue', 'adf_d']` |
| `arima_estimate("A1:A24").shape` | `(1, 7)` |
| `arima_estimate("A1:A24", full=True).shape[1]` | `7` |
| `arima_estimate("A1:A24", full=True).shape[0] > 1` | `True` |

### ADF determines d

The trending series in A1:A24 should not be stationary at d=0, so ADF should set d ≥ 1.

| Python | Expected |
|--------|----------|
| `int(arima_estimate("A1:A24")["d"].iloc[0]) >= 1` | `True` |
| `int(arima_estimate("A1:A24")["adf_d"].iloc[0]) >= 1` | `True` |
| `arima_estimate("A1:A24")["adf_pvalue"].iloc[0] < 1.0` | `True` |

### p and q within bounds

| Python | Expected |
|--------|----------|
| `int(arima_estimate("A1:A24")["p"].iloc[0]) in range(4)` | `True` |
| `int(arima_estimate("A1:A24")["q"].iloc[0]) in range(4)` | `True` |
| `int(arima_estimate("A1:A24", p_max=1, q_max=1)["p"].iloc[0]) in range(2)` | `True` |
| `int(arima_estimate("A1:A24", p_max=1, q_max=1)["q"].iloc[0]) in range(2)` | `True` |

### AIC and BIC columns are finite

| Python | Expected |
|--------|----------|
| `np.isfinite(arima_estimate("A1:A24")["aic"].iloc[0])` | `True` |
| `np.isfinite(arima_estimate("A1:A24")["bic"].iloc[0])` | `True` |

### BIC criterion may differ from AIC

| Python | Expected |
|--------|----------|
| `arima_estimate("A1:A24", criterion="bic")["bic"].iloc[0] <= arima_estimate("A1:A24", criterion="bic", full=True)["bic"].iloc[-1]` | `True` |

### full=True grid is sorted by criterion

| Python | Expected |
|--------|----------|
| `arima_estimate("A1:A24", full=True)["aic"].is_monotonic_increasing` | `True` |
| `arima_estimate("A1:A24", criterion="bic", full=True)["bic"].is_monotonic_increasing` | `True` |

### d_max=0 forces d=0

| Python | Expected |
|--------|----------|
| `int(arima_estimate("A1:A24", d_max=0)["d"].iloc[0])` | `0` |

### Edge cases

| Python | Expected |
|--------|----------|
| `arima_estimate([1, 2, 3])` | `#PYTHON!` — `Need at least 4 observations.` |
| `arima_estimate([1, 2, 3, 4], criterion="foo")` | `#PYTHON!` — `criterion must be 'aic' or 'bic'` |
| `arima_estimate([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], p_max=0, q_max=0).shape` | `(1, 7)` |
