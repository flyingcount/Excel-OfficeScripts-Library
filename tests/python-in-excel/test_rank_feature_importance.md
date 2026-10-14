# Test: rank_feature_importance

## Setup

1. Formulas → **Initialization** → paste `rank_feature_importance` from `source/python-in-excel/functions/rank_feature_importance.py` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.
2. Headers `id`, `amount`, `segment`, `noise`, `churn` in `A1:E1`.
3. Rows in `A2:E9`:

| id | amount | segment | noise | churn |
|----|--------|---------|-------|-------|
| 1 | 10 | A | 5 | 0 |
| 2 | 11 | A | 20 | 0 |
| 3 | 12 | A | 8 | 0 |
| 4 | 13 | A | 15 | 0 |
| 5 | 40 | B | 7 | 1 |
| 6 | 42 | B | 18 | 1 |
| 7 | 41 | B | 9 | 1 |
| 8 | 43 | B | 16 | 1 |

`id` is skipped (all unique). `segment` vs `churn` is a perfect 2×2, so Cramer's V = 1. `amount` is a near-step vs `churn` (point-biserial |r| close to 1). `noise` is weaker.

## Cases

In a PY cell, set output to **Excel value**.

```python
df = pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6, 7, 8],
    "amount": [10, 11, 12, 13, 40, 42, 41, 43],
    "segment": list("AAAABBBB"),
    "noise": [5, 20, 8, 15, 7, 18, 9, 16],
    "churn": [0, 0, 0, 0, 1, 1, 1, 1],
})
```

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(rank_feature_importance("A1:E9", "churn").columns)` | `['rank', 'feature', 'type', 'method', 'score', 'p_value', 'iv', 'strength']` |
| `set(rank_feature_importance("A1:E9", "churn", top=0)["feature"])` | `{'amount', 'segment', 'noise'}` |
| `rank_feature_importance("A1:E9", "churn", top=1).shape` | `(1, 8)` |
| `rank_feature_importance(df, "CHURN").shape[0]` | `3` |

### Binary target scores

Use `.set_index("feature")` after the call, or filter the spill in Excel.

| Python | Expected |
|--------|----------|
| `float(rank_feature_importance("A1:E9", "churn").set_index("feature").loc["segment", "score"])` | `1.0` |
| `rank_feature_importance("A1:E9", "churn").set_index("feature").loc["segment", "method"]` | `chi-square` |
| `rank_feature_importance("A1:E9", "churn").set_index("feature").loc["amount", "method"]` | `point-biserial` |
| `float(rank_feature_importance("A1:E9", "churn").set_index("feature").loc["amount", "score"]) > 0.95` | `True` |
| `float(rank_feature_importance("A1:E9", "churn").set_index("feature").loc["noise", "score"]) < float(rank_feature_importance("A1:E9", "churn").set_index("feature").loc["amount", "score"])` | `True` |
| `float(rank_feature_importance("A1:E9", "churn").set_index("feature").loc["segment", "iv"]) > 1` | `True` |
| `rank_feature_importance("A1:E9", "churn").set_index("feature").loc["segment", "strength"]` | `strong` |
| `rank_feature_importance("A1:E9", "churn").set_index("feature").loc["amount", "type"]` | `numeric` |
| `rank_feature_importance("A1:E9", "churn")["rank"].iloc[0]` | `1.0` |

### Continuous target and Series y

| Python | Expected |
|--------|----------|
| `rank_feature_importance(pd.DataFrame({"x": list(range(1, 15)), "y": [2 * i for i in range(1, 15)]}), "y")["method"].iloc[0]` | `pearson` |
| `round(float(rank_feature_importance(pd.DataFrame({"x": list(range(1, 15)), "y": [2 * i for i in range(1, 15)]}), "y")["score"].iloc[0]), 6)` | `1.0` |
| `pd.isna(rank_feature_importance(pd.DataFrame({"x": list(range(1, 15)), "y": [2 * i for i in range(1, 15)]}), "y")["iv"].iloc[0])` | `True` |
| `float(rank_feature_importance(df.drop(columns=["churn"]), df["churn"]).set_index("feature").loc["segment", "score"])` | `1.0` |

### Edge cases

| Python | Expected |
|--------|----------|
| `rank_feature_importance(pd.DataFrame({"x": [1, 2], "y": [0, 1]}), "y")` | `#PYTHON!` — `Need at least 3 rows with a target.` |
| `rank_feature_importance(pd.DataFrame({"id": ["a", "b", "c"], "y": [0, 0, 1]}), "y")` | `#PYTHON!` — `No scorable features.` |
