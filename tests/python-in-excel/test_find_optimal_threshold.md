# Test: find_optimal_threshold

## Setup

1. Formulas → **Initialization** → paste `find_optimal_threshold` from `source/python-in-excel/functions/find_optimal_threshold.py` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.
2. Headers `churn`, `proba` in `A1:B1`.
3. Rows in `A2:B9`: actual `1,1,1,1,0,0,0,0` and scores `0.9,0.8,0.4,0.7,0.2,0.1,0.6,0.3`.

Default sweep is 0.1, 0.2, …, 0.9. F1 is highest at 0.7 (precision 1, recall 0.75, F1 ≈ 0.8571).

## Cases

In a PY cell, set output to **Excel value**.

```python
df = pd.DataFrame({
    "churn": [1, 1, 1, 1, 0, 0, 0, 0],
    "proba": [0.9, 0.8, 0.4, 0.7, 0.2, 0.1, 0.6, 0.3],
})
```

| Python | Expected |
|--------|----------|
| `list(find_optimal_threshold("A1:B9").columns)` | `['threshold', 'accuracy', 'precision', 'recall', 'f1', 'is_best']` |
| `find_optimal_threshold("A1:B9").shape[0]` | `9` |
| `float(find_optimal_threshold("A1:B9")["is_best"].sum())` | `1.0` |
| `round(float(find_optimal_threshold("A1:B9").set_index("is_best").loc[1.0, "threshold"]), 1)` | `0.7` |
| `round(float(find_optimal_threshold("A1:B9").set_index("is_best").loc[1.0, "f1"]), 4)` | `0.8571` |
| `round(float(find_optimal_threshold(df, "churn", "proba").set_index("is_best").loc[1.0, "precision"]), 2)` | `1.0` |
| `find_optimal_threshold(df, metric="pr")` | `#PYTHON!` — `metric must be 'f1' or 'balanced'.` |
| `find_optimal_threshold(df, step=0)` | `#PYTHON!` — `Need low <= high and step > 0.` |
| `find_optimal_threshold(pd.DataFrame({"a": [None], "b": [0.5]}))` | `#PYTHON!` — `Need at least 1 row with actual and probability.` |
