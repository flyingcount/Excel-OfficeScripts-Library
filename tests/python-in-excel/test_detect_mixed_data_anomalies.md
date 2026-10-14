# Test: detect_mixed_data_anomalies

## Setup

1. Formulas → **Initialization** → paste `detect_mixed_data_anomalies` from `source/python-in-excel/functions/detect_mixed_data_anomalies.py` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.
2. Headers `x`, `y`, `grp` in `A1:C1`. Put `10`, `20`, `A` in `A2:C20`. Put `100`, `200`, `Z` in `A21:C21` (19 inliers + 1 mixed outlier).
3. Header `v` in `E1`. Put `1, 2, 3, 4, 5, 6, 7, 8, 9, 100` in `E2:E11`. Header `grp` in `F1`. Put `A` in `F2:F10` and `B` in `F11`.

Reference values for `A1:C21` at `contamination=0.05`: mean `(14.5, 29)`, collinear covariance (pseudoinverse). Inlier MD ≈ 0.2236 (`md²=0.05`). Outlier MD ≈ 4.2485 (`md²=18.05`). Chi-square cutoff `χ²_{0.95, df=2}` ≈ 5.991 on **squared** distance. Univariate |z| of 100 ≈ 4.36. Isolation Forest `random_state=42`.

Helpers (paste in a PY cell if needed):

```python
df_mixed = pd.DataFrame({"x": [10]*19+[100], "y": [20]*19+[200], "grp": ["A"]*19+["Z"]})
df_ext = pd.DataFrame({"x": [10]*19+[100], "y": [20]*19+[200], "grp": ["A"]*20})
df_rare = pd.DataFrame({"x": [10+0.01*i for i in range(20)], "y": [20+0.01*i for i in range(20)], "grp": ["A"]*19+["Z"]})
df_mv = pd.DataFrame({"x": list(range(30)), "y": list(range(29))+[0], "grp": ["A"]*30})
df_combo = pd.DataFrame({"spend": [100]*12+[10]*12+[0], "tier": ["Gold"]*12+["Bronze"]*12+["Gold"]})
```

## Cases

In a PY cell, set output to **Excel value**.

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(detect_mixed_data_anomalies("A1:C21").columns)` | `['x', 'y', 'grp', 'md_distance', 'md_p_value', 'if_score', 'flag_md', 'flag_if', 'flag_extreme', 'flag_rare', 'anomaly_class']` |
| `detect_mixed_data_anomalies("A1:C21").shape` | `(20, 11)` |
| `detect_mixed_data_anomalies(df_mixed).shape` | `(20, 11)` |

### Consensus Anomaly (extreme numeric + rare category)

Last row is far in both `x`/`y` and has a rare `grp`. Inliers are identical.

| Python | Expected |
|--------|----------|
| `detect_mixed_data_anomalies("A1:C21")["flag_md"].iloc[19]` | `1.0` |
| `detect_mixed_data_anomalies("A1:C21")["flag_extreme"].iloc[19]` | `1.0` |
| `detect_mixed_data_anomalies("A1:C21")["flag_rare"].iloc[19]` | `1.0` |
| `detect_mixed_data_anomalies("A1:C21")["flag_md"].iloc[0]` | `0.0` |
| `detect_mixed_data_anomalies("A1:C21")["anomaly_class"].iloc[19]` | `Consensus Anomaly` |
| `detect_mixed_data_anomalies("A1:C21")["anomaly_class"].iloc[0]` | `Normal` |
| `round(float(detect_mixed_data_anomalies("A1:C21")["md_distance"].iloc[0]), 4)` | `0.2236` |
| `round(float(detect_mixed_data_anomalies("A1:C21")["md_distance"].iloc[19]), 4)` | `4.2485` |
| `detect_mixed_data_anomalies("A1:C21")["md_p_value"].iloc[19] < 0.001` | `True` |
| `round(float(detect_mixed_data_anomalies("A1:C21")["md_p_value"].iloc[0]), 4)` | `0.9753` |
| `int(detect_mixed_data_anomalies("A1:C21")["if_score"].idxmin())` | `19` |

### Extreme Value (Numeric)

Same spike, but every row is `grp=A` (no rare category).

| Python | Expected |
|--------|----------|
| `detect_mixed_data_anomalies(df_ext)["flag_extreme"].iloc[19]` | `1.0` |
| `detect_mixed_data_anomalies(df_ext)["flag_rare"].iloc[19]` | `0.0` |
| `detect_mixed_data_anomalies(df_ext)["anomaly_class"].iloc[19]` | `Extreme Value (Numeric)` |
| `detect_mixed_data_anomalies(df_ext)["anomaly_class"].iloc[0]` | `Normal` |

### Rare Category (Categorical)

Tight numeric jitter; last row is `Z`.

| Python | Expected |
|--------|----------|
| `detect_mixed_data_anomalies(df_rare)["flag_rare"].iloc[19]` | `1.0` |
| `detect_mixed_data_anomalies(df_rare)["flag_extreme"].iloc[19]` | `0.0` |
| `detect_mixed_data_anomalies(df_rare)["anomaly_class"].iloc[19]` | `Rare Category (Categorical)` |
| `detect_mixed_data_anomalies(df_rare)["anomaly_class"].iloc[0]` | `Normal` |

### Multivariate Outlier (Numeric)

`y ≈ x` for 0–28; last point is `(29, 0)`. Individual |z| < 3; Mahalanobis flags the off-diagonal.

| Python | Expected |
|--------|----------|
| `detect_mixed_data_anomalies(df_mv)["flag_extreme"].iloc[29]` | `0.0` |
| `detect_mixed_data_anomalies(df_mv)["flag_md"].iloc[29]` | `1.0` |
| `detect_mixed_data_anomalies(df_mv)["anomaly_class"].iloc[29]` | `Multivariate Outlier (Numeric)` |
| `detect_mixed_data_anomalies(df_mv)["anomaly_class"].iloc[0]` | `Normal` |

### Inconsistent Structural Combo

Gold spend clustered at 100, Bronze at 10; last row is Gold with spend 0 (extreme within Gold, not globally).

| Python | Expected |
|--------|----------|
| `detect_mixed_data_anomalies(df_combo)["flag_extreme"].iloc[24]` | `0.0` |
| `detect_mixed_data_anomalies(df_combo)["flag_rare"].iloc[24]` | `0.0` |
| `detect_mixed_data_anomalies(df_combo)["anomaly_class"].iloc[24]` | `Inconsistent Structural Combo` |
| `detect_mixed_data_anomalies(df_combo)["anomaly_class"].iloc[0]` | `Normal` |

### One numeric column (Mahalanobis skipped)

`E1:F11` has one number column plus a category. Last row is both an extreme value (`100`) and a rare `B` → Consensus Anomaly. MD columns are the fallback (distance 0, p=1, flag 0).

| Python | Expected |
|--------|----------|
| `detect_mixed_data_anomalies("E1:F11", contamination=0.1)["md_distance"].tolist()` | `[0.0] * 10` |
| `detect_mixed_data_anomalies("E1:F11", contamination=0.1)["md_p_value"].tolist()` | `[1.0] * 10` |
| `detect_mixed_data_anomalies("E1:F11", contamination=0.1)["flag_md"].sum()` | `0.0` |
| `float(detect_mixed_data_anomalies("E1:F11", contamination=0.1)["flag_extreme"].iloc[9])` | `1.0` |
| `float(detect_mixed_data_anomalies("E1:F11", contamination=0.1)["flag_rare"].iloc[9])` | `1.0` |
| `detect_mixed_data_anomalies("E1:F11", contamination=0.1)["anomaly_class"].iloc[9]` | `Consensus Anomaly` |

### IDs skipped; numeric-as-text coerced

| Python | Expected |
|--------|----------|
| `detect_mixed_data_anomalies(pd.DataFrame({"id": list("abcdefghij"), "x": [1,2,3,4,5,6,7,8,9,100], "y": [1,2,3,4,5,6,7,8,9,100]}), contamination=0.1)["flag_md"].iloc[9]` | `1.0` |
| `'id' in list(detect_mixed_data_anomalies(pd.DataFrame({"id": list("abcdefghij"), "x": [1,2,3,4,5,6,7,8,9,100], "y": [1,2,3,4,5,6,7,8,9,100]}), contamination=0.1).columns)` | `True` |
| `float(detect_mixed_data_anomalies(pd.DataFrame({"x": ["1","2","3","4","5","6","7","8","9","100"], "y": ["1","2","3","4","5","6","7","8","9","100"]}), contamination=0.1)["flag_md"].iloc[9])` | `1.0` |

### Edge cases

| Python | Expected |
|--------|----------|
| `detect_mixed_data_anomalies(pd.DataFrame({"id": ["a", "b", "c"]}))` | `#PYTHON!` — `No numeric or categorical columns to process.` |
| `detect_mixed_data_anomalies(pd.DataFrame({"x": [1], "y": [2]}))` | `#PYTHON!` — `Need at least 2 rows for Isolation Forest.` |
| `detect_mixed_data_anomalies(df_mixed, contamination=0.8)` | `#PYTHON!` — `contamination must be in (0, 0.5].` |
| `detect_mixed_data_anomalies(pd.Series([1, 2, 3, 4, 5, 100]), contamination=0.15).shape[0]` | `6` |
