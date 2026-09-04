# confusion_matrix

True positives, false positives, false negatives, and true negatives with **business wording** in the `meaning` column (for example Actual Churn and Predicted Churn). Default result is a spill table. `plot=True` draws a **2×2 heatmap**.

Use hard class labels, not probabilities. For scores, first pick a cutoff with `find_optimal_threshold`. Pair with `classification_metrics` for accuracy, F1, MCC, and related scores.

Formula: `source/python-in-excel/functions/confusion_matrix.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

Table (PY cell output **Excel value**):

```python
confusion_matrix("A1:B100")
confusion_matrix(data, "churn", "pred", pos_name="Churn", neg_name="Not Churn")
confusion_matrix(data, "churn", "pred", positive="Yes", pos_name="Churn", neg_name="Stay")
```

Chart (leave as a **Python object**):

```python
confusion_matrix("A1:B100", plot=True)
confusion_matrix(data, "churn", "pred", pos_name="Churn", neg_name="Not Churn", plot=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Table/range with actual and predicted, or a label column if `predicted` is a Series/range. |
| `actual` | No | Actual-label column name, range, or Series. Default: first column of `data`. |
| `predicted` | No | Predicted-label column name, range, or Series. Default: second column of `data`. |
| `positive` | No | Value that means the positive class. Default `1`. |
| `pos_name` | No | Word for the positive class in `meaning` and on the heatmap. Default `'Positive'`. |
| `neg_name` | No | Word for the negative class. Default `'Negative'`. |
| `plot` | No | `False` (default) spills a table. `True` returns a heatmap. |
| `headers` | No | First row is headers when a ref string is used. Default `True`. |

Rows with a blank in either column are dropped. Need at least one remaining pair. Excel 1×1 arrays for scalars are unwrapped. Column names are case-insensitive.

## Result (table)

| Column | Notes |
|--------|-------|
| `metric` | `true_positive`, `false_positive`, `false_negative`, `true_negative`. |
| `count` | Number of rows in that cell. |
| `meaning` | `Actual {pos/neg} and Predicted {pos/neg}`. |

## Result (plot)

A square heatmap. Rows are actual (`pos_name`, then `neg_name`); columns are predicted (same order). Cells are TP / FN on the first row and FP / TN on the second. Leave the cell as a **Python object**.

## Example

```python
confusion_matrix(pd.DataFrame({
    "churn": [1, 1, 1, 1, 0, 0, 0, 0],
    "pred": [1, 1, 0, 1, 0, 0, 1, 0],
}), "churn", "pred", pos_name="Churn", neg_name="Not Churn")
```

Counts: TP 3, FP 1, FN 1, TN 3. The TP meaning is `Actual Churn and Predicted Churn`.
