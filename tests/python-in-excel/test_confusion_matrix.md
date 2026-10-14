# Test: confusion_matrix

## Setup

1. Formulas → **Initialization** → paste `confusion_matrix` from `source/python-in-excel/functions/confusion_matrix.py` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.
2. Headers `churn`, `pred` in `A1:B1`.
3. Rows in `A2:B9`: actual `1,1,1,1,0,0,0,0` and predicted `1,1,0,1,0,0,1,0`.

TP=3, FP=1, FN=1, TN=3.

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

```python
df = pd.DataFrame({
    "churn": [1, 1, 1, 1, 0, 0, 0, 0],
    "pred": [1, 1, 0, 1, 0, 0, 1, 0],
})
```

| Python | Expected |
|--------|----------|
| `list(confusion_matrix("A1:B9").columns)` | `['metric', 'count', 'meaning']` |
| `list(confusion_matrix("A1:B9")["metric"])` | `['true_positive', 'false_positive', 'false_negative', 'true_negative']` |
| `float(confusion_matrix("A1:B9").set_index("metric").loc["true_positive", "count"])` | `3.0` |
| `float(confusion_matrix("A1:B9").set_index("metric").loc["false_positive", "count"])` | `1.0` |
| `float(confusion_matrix("A1:B9").set_index("metric").loc["false_negative", "count"])` | `1.0` |
| `float(confusion_matrix("A1:B9").set_index("metric").loc["true_negative", "count"])` | `3.0` |
| `confusion_matrix(df, "churn", "pred", pos_name="Churn", neg_name="Not Churn").set_index("metric").loc["true_positive", "meaning"]` | `Actual Churn and Predicted Churn` |
| `confusion_matrix(df, "CHURN", "PRED").shape` | `(4, 3)` |
| `confusion_matrix(pd.DataFrame({"a": [None], "b": [1]}))` | `#PYTHON!` — `Need at least 1 row with actual and predicted.` |

### Plot (`plot=True`, leave as **Python object**)

| Python | Expected |
|--------|----------|
| `type(confusion_matrix(df, plot=True)).__name__` | `Figure` |
| `len(confusion_matrix(df, plot=True).axes)` | `1` |
| `confusion_matrix(df, plot=True).axes[0].get_title()` | `Confusion matrix` |
| `confusion_matrix(df, plot=True).axes[0].get_xlabel()` | `Predicted` |
| `confusion_matrix(df, plot=True).axes[0].get_ylabel()` | `Actual` |
