# Test: cluster_prep

## Setup

1. Formulas → **Initialization** → paste `cluster_prep` from `source/python-in-excel/functions/cluster_prep.py` after the default imports → Save.
2. Headers `bill`, `mass`, `sex` in `A1:C1`. Rows: `(39.1, 3750, Male)`, `(39.5, 3800, Female)`, `(40.3, 3250, Female)` in `A2:C4`.
3. Numeric-only header `x` in `E1`. Rows: `1`, `2`, `3` in `E2:E4`.
4. Category-only header `grp` in `G1`. Rows: `A`, `B`, `A` in `G2:G4`.

`StandardScaler` uses population std (`ddof=0`). One-hot categories are sorted, so `sex_Female` then `sex_Male`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(cluster_prep("A1:C4").columns)` | `['bill', 'mass', 'sex_Female', 'sex_Male']` |
| `round(float(cluster_prep("A1:C4")["bill"].mean()), 10)` | `0` |
| `round(float(cluster_prep("A1:C4")["bill"].std(ddof=0)), 10)` | `1` |
| `round(float(cluster_prep("A1:C4")["mass"].std(ddof=0)), 10)` | `1` |
| `cluster_prep("A1:C4")["sex_Female"].tolist()` | `[0.0, 1.0, 1.0]` |
| `cluster_prep("A1:C4")["sex_Male"].tolist()` | `[1.0, 0.0, 0.0]` |
| `round(float(cluster_prep("E1:E4")["x"].iloc[1]), 10)` | `0` |
| `list(cluster_prep("G1:G4").columns)` | `['grp_A', 'grp_B']` |
| `cluster_prep("G1:G4")["grp_A"].tolist()` | `[1.0, 0.0, 1.0]` |
| `list(cluster_prep(pd.DataFrame({"id": ["a", "b", "c"], "x": [1, 2, 3]})).columns)` | `['x']` |
| `round(float(cluster_prep(pd.DataFrame({"a": ["1", "2", "3"]}))["a"].iloc[1]), 10)` | `0` |
