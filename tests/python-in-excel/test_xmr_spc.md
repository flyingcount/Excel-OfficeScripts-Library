# Test: xmr_spc

## Setup

1. Formulas → **Initialization** → paste `xmr_spc` from `source/python-in-excel/functions/xmr_spc.py` after the default imports → Save. Or paste `init/SPC.py`.
2. Put `10, 12, 11, 13, 12, 11, 10, 14` in `A1:A8`.
3. Put `10, 11, 9, 12, 10, 11, 10, 30` in `B1:B8`.
4. Put `10, 11, 10, 11, 10, 11, 10, 11, 12, 13, 12, 13, 12, 13, 12, 13` in `C1:C16`.
5. Put dates `2020-01-01` … `2020-01-08` in `D1:D8`.

`A1:A8`: n=8, x̄=11.625, MR̄=12/7≈1.7143, σ=MR̄/1.128, UCL≈16.1843, LCL≈7.0657, MR UCL≈5.6006. No X/MR outliers; no 8-point shift.

`B1:B8`: last value 30 is an X and MR outlier.

`C1:C16`: two runs of 8 on opposite sides of overall x̄=11.5. Limits recompute per half: first-8 CL=10.5, last-8 CL=12.5. All points inside local 3σ. `is_shift` is 1 on every row (runs vs overall x̄).

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(xmr_spc("A1:A8").columns)` | `['t', 'value', 'mr', 'cl', 'ucl', 'lcl', 'mr_cl', 'mr_ucl', 'mr_lcl', 'is_outlier', 'is_shift', 'is_mr_outlier']` |
| `xmr_spc("A1:A8").shape` | `(8, 12)` |
| `list(xmr_spc("A1:A8", dates="D1:D8").columns)[:3]` | `['t', 'date', 'value']` |
| `xmr_spc([10, 12, 11]).shape[0]` | `3` |

### Limits (A1:A8)

| Python | Expected |
|--------|----------|
| `round(float(xmr_spc("A1:A8")["cl"].iloc[0]), 4)` | `11.625` |
| `round(float(xmr_spc("A1:A8")["mr_cl"].iloc[0]), 4)` | `1.7143` |
| `round(float(xmr_spc("A1:A8")["ucl"].iloc[0]), 4)` | `16.1843` |
| `round(float(xmr_spc("A1:A8")["lcl"].iloc[0]), 4)` | `7.0657` |
| `round(float(xmr_spc("A1:A8")["mr_ucl"].iloc[0]), 4)` | `5.6006` |
| `float(xmr_spc("A1:A8")["mr_lcl"].iloc[0])` | `0.0` |
| `pd.isna(xmr_spc("A1:A8")["mr"].iloc[0])` | `True` |
| `float(xmr_spc("A1:A8")["mr"].iloc[1])` | `2.0` |
| `xmr_spc("A1:A8")["is_outlier"].sum()` | `0.0` |
| `xmr_spc("A1:A8")["is_shift"].sum()` | `0.0` |
| `xmr_spc("A1:A8")["is_mr_outlier"].sum()` | `0.0` |

### X and MR outliers (B1:B8)

| Python | Expected |
|--------|----------|
| `float(xmr_spc("B1:B8")["is_outlier"].iloc[7])` | `1.0` |
| `float(xmr_spc("B1:B8")["is_mr_outlier"].iloc[7])` | `1.0` |
| `xmr_spc("B1:B8")["is_outlier"].iloc[:7].sum()` | `0.0` |
| `xmr_spc("B1:B8")["is_shift"].sum()` | `0.0` |

### 8-point shift (C1:C16)

| Python | Expected |
|--------|----------|
| `xmr_spc("C1:C16")["is_outlier"].sum()` | `0.0` |
| `xmr_spc("C1:C16")["is_shift"].tolist()` | `[1.0] * 16` |
| `round(float(xmr_spc("C1:C16")["cl"].iloc[0]), 1)` | `10.5` |
| `round(float(xmr_spc("C1:C16")["cl"].iloc[7]), 1)` | `10.5` |
| `round(float(xmr_spc("C1:C16")["cl"].iloc[8]), 1)` | `12.5` |
| `round(float(xmr_spc("C1:C16")["cl"].iloc[15]), 1)` | `12.5` |
| `round(float(xmr_spc([10]*8 + [12, 9, 13, 8, 12])["cl"].iloc[0]), 1)` | `10.0` |
| `round(float(xmr_spc([10]*8 + [12, 9, 13, 8, 12])["cl"].iloc[8]), 1)` | `10.8` |

### Constant series and dates

| Python | Expected |
|--------|----------|
| `float(xmr_spc([5, 5, 5])["ucl"].iloc[0])` | `5.0` |
| `float(xmr_spc([5, 5, 5])["lcl"].iloc[0])` | `5.0` |
| `xmr_spc([5, 5, 5])["is_outlier"].sum()` | `0.0` |
| `xmr_spc("A1:A8", dates="D1:D8")["date"].iloc[0]` | first date in `D1` |
| `xmr_spc("A1:A8", dates="D1:D8")["t"].iloc[0]` | `1.0` |
| `float(xmr_spc(pd.Series([10, 12, 11, 13, 12, 11, 10, 14]), dates=pd.date_range("2020-01-01", periods=8))["value"].iloc[0])` | `10.0` |

### Plot

Leave as a **Python object**.

| Python | Expected |
|--------|----------|
| `type(xmr_spc("A1:A8", plot=True)).__name__` | `Figure` |
| `len(xmr_spc("A1:A8", plot=True).axes)` | `2` |
| `xmr_spc("A1:A8", plot=True, title="Test")._suptitle.get_text()` | `Test` |

### Edge cases

| Python | Expected |
|--------|----------|
| `xmr_spc([1])` | `#PYTHON!` — `Need at least 2 numeric values.` |
| `xmr_spc([1, None])` | `#PYTHON!` — `Need at least 2 numeric values.` |
