# find_optimal_threshold

Sweep predicted **probabilities** from `low` to `high` and pick a cutoff. Default `metric='f1'` maximises F1. `metric='balanced'` minimises |precision − recall| (F1 breaks ties). A default 0.5 cutoff is often a poor fit for imbalanced business data.

Use the chosen `threshold` to turn scores into labels, then call `classification_metrics` / `confusion_matrix`.

Formula: `source/python-in-excel/functions/find_optimal_threshold.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
find_optimal_threshold("A1:B100")
find_optimal_threshold(data, "churn", "proba")
find_optimal_threshold(data, "churn", "proba", metric="balanced", step=0.05)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Table/range, or actual labels if `proba` is a Series/range. |
| `actual` | No | Actual-label column name, range, or Series. Default: first column. |
| `proba` | No | Predicted-score column name, range, or Series. Default: second column. |
| `metric` | No | `'f1'` (default) or `'balanced'`. |
| `low` | No | First cutoff. Default `0.1`. |
| `high` | No | Last cutoff. Default `0.9`. |
| `step` | No | Increment. Default `0.1`. |
| `positive` | No | Value that means the positive class. Default `1`. |
| `headers` | No | First row is headers when a ref string is used. Default `True`. |

A row is predicted positive when `proba >= threshold`. Need `low <= high` and `step > 0`. `metric` other than `f1` / `balanced` raises an error. Rows with a blank actual or score are dropped.

## Result

One row per cutoff:

| Column | Notes |
|--------|-------|
| `threshold` | Cutoff tested. |
| `accuracy`, `precision`, `recall`, `f1` | Same definitions as `classification_metrics` (recall is `true_positive_rate`). |
| `is_best` | `1` on the winning row, else `0`. |

## Example

```python
find_optimal_threshold(pd.DataFrame({
    "churn": [1, 1, 1, 1, 0, 0, 0, 0],
    "proba": [0.9, 0.8, 0.4, 0.7, 0.2, 0.1, 0.6, 0.3],
}), "churn", "proba")
```

F1 is highest at threshold 0.7 (precision 1, recall 0.75).
