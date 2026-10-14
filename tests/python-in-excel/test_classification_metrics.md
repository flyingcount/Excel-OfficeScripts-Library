# Test: classification_metrics

## Setup

1. Formulas → **Initialization** → paste `classification_metrics` from `source/python-in-excel/functions/classification_metrics.py` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.
2. Headers `churn`, `pred` in `A1:B1`.
3. Rows in `A2:B9`: actual `1,1,1,1,0,0,0,0` and predicted `1,1,0,1,0,0,1,0`.

TP=3, FP=1, FN=1, TN=3, n=8. Accuracy = TPR = precision = 0.75. MCC = 0.5. Threat score = 0.6. LR+ = 3. DOR = 9.

## Cases

In a PY cell, set output to **Excel value**.

```python
df = pd.DataFrame({
    "churn": [1, 1, 1, 1, 0, 0, 0, 0],
    "pred": [1, 1, 0, 1, 0, 0, 1, 0],
})
```

| Python | Expected |
|--------|----------|
| `list(classification_metrics("A1:B9")["metric"])` | `['n', 'accuracy', 'misclassification_rate', 'true_positive_rate', 'false_positive_rate', 'true_negative_rate', 'false_negative_rate', 'precision', 'prevalence', 'lr_positive', 'lr_negative', 'diagnostic_odds_ratio', 'f1', 'beta', 'f_beta', 'mcc', 'informedness', 'markedness', 'threat_score']` |
| `classification_metrics("A1:B9").shape` | `(19, 2)` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["n", "value"])` | `8.0` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["accuracy", "value"])` | `0.75` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["misclassification_rate", "value"])` | `0.25` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["true_positive_rate", "value"])` | `0.75` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["false_positive_rate", "value"])` | `0.25` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["true_negative_rate", "value"])` | `0.75` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["false_negative_rate", "value"])` | `0.25` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["precision", "value"])` | `0.75` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["prevalence", "value"])` | `0.5` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["lr_positive", "value"])` | `3.0` |
| `round(float(classification_metrics("A1:B9").set_index("metric").loc["lr_negative", "value"]), 4)` | `0.3333` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["diagnostic_odds_ratio", "value"])` | `9.0` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["f1", "value"])` | `0.75` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["beta", "value"])` | `1.0` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["f_beta", "value"])` | `0.75` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["mcc", "value"])` | `0.5` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["informedness", "value"])` | `0.5` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["markedness", "value"])` | `0.5` |
| `float(classification_metrics("A1:B9").set_index("metric").loc["threat_score", "value"])` | `0.6` |
| `float(classification_metrics(df, "churn", "pred", beta=1).set_index("metric").loc["f1", "value"])` | `0.75` |
| `classification_metrics(df, beta=0)` | `#PYTHON!` — `beta must be > 0.` |
| `classification_metrics(pd.DataFrame({"a": [None], "b": [1]}))` | `#PYTHON!` — `Need at least 1 row with actual and predicted.` |
