# Test: outlier_flag

## Setup

1. Formulas → **Initialization** → paste `outlier_flag` from `source/python-in-excel/functions/outlier_flag.py` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.
2. Put `1, 2, 3, 4, 100` in `A1:A5`.
3. Put `5, 5, 5, 5, 50, 5, 5, 5, 5` in `B1:B9`.

Reference values for `A1:A5`: Q1=2, Q3=4, IQR=2. Mean=22, std(ddof=0)≈39.19. Median=3, MAD=1, MAD×1.4826=1.4826.

## Cases

In a PY cell, set output to **Excel value**.

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(outlier_flag("A1:A5").columns)` | `['value', 'is_outlier', 'score', 'lower_bound', 'upper_bound']` |
| `outlier_flag("A1:A5").shape` | `(5, 5)` |
| `outlier_flag([1, 2, 3]).shape` | `(3, 5)` |

### IQR (default)

`[1, 2, 3, 4, 100]`: Q1=2, Q3=4, IQR=2, lower=−1, upper=7. Only 100 is an outlier.

| Python | Expected |
|--------|----------|
| `outlier_flag("A1:A5")["is_outlier"].tolist()` | `[0.0, 0.0, 0.0, 0.0, 1.0]` |
| `outlier_flag("A1:A5")["lower_bound"].iloc[0]` | `-1.0` |
| `outlier_flag("A1:A5")["upper_bound"].iloc[0]` | `7.0` |
| `outlier_flag("A1:A5")["value"].iloc[4]` | `100.0` |
| `outlier_flag([1, 2, 3, 4, 5])["is_outlier"].sum()` | `0.0` |
| `outlier_flag([1, 2, 3, 4, 100], threshold=3)["is_outlier"].iloc[4]` | `1.0` |

IQR far outlier threshold: lower = 2 − 3×2 = −4, upper = 4 + 3×2 = 10. 100 is still an outlier.

### MAD

`[1, 2, 3, 4, 100]`: median=3, MAD=1, scaled=1.4826. Score of 100 = 97/1.4826 ≈ 65.4.

| Python | Expected |
|--------|----------|
| `outlier_flag("A1:A5", method="mad")["is_outlier"].tolist()` | `[0.0, 0.0, 0.0, 0.0, 1.0]` |
| `round(outlier_flag("A1:A5", method="mad")["score"].iloc[4], 1)` | `65.4` |
| `round(outlier_flag("A1:A5", method="mad")["lower_bound"].iloc[0], 4)` | `0.7761` |
| `round(outlier_flag("A1:A5", method="mad")["upper_bound"].iloc[0], 4)` | `5.2239` |

### Z-score

`[5, 5, 5, 5, 50, 5, 5, 5, 5]`: mean=10, std(ddof=0)=√200≈14.1421. |z| of 50 = 40/14.1421 ≈ 2.8284.

| Python | Expected |
|--------|----------|
| `outlier_flag("B1:B9", method="zscore", threshold=2)["is_outlier"].iloc[4]` | `1.0` |
| `outlier_flag("B1:B9", method="zscore", threshold=3)["is_outlier"].iloc[4]` | `0.0` |
| `round(outlier_flag("B1:B9", method="zscore", threshold=2)["score"].iloc[4], 4)` | `2.8284` |
| `round(outlier_flag("B1:B9", method="zscore", threshold=2)["lower_bound"].iloc[0], 4)` | `-18.2843` |
| `round(outlier_flag("B1:B9", method="zscore", threshold=2)["upper_bound"].iloc[0], 4)` | `38.2843` |

### Edge cases

| Python | Expected |
|--------|----------|
| `outlier_flag([5, 5, 5])["is_outlier"].sum()` | `0.0` |
| `outlier_flag([5, 5, 5], method="mad")["is_outlier"].sum()` | `0.0` |
| `outlier_flag([5, 5, 5], method="zscore", threshold=2)["is_outlier"].sum()` | `0.0` |
| `outlier_flag([1, None, 3])["is_outlier"].iloc[1]` | blank (`NaN`) |
| `outlier_flag([1, None, 3])["value"].iloc[1]` | blank (`NaN`) |
| `outlier_flag([1, 2, 3], method="foo")` | `#PYTHON!` — `method 'foo' not supported` |
