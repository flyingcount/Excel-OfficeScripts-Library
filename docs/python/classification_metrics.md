# classification_metrics

Binary classification scores from actual vs predicted **hard labels**: accuracy, error rate, TPR/FPR/TNR/FNR, precision, prevalence, likelihood ratios, diagnostic odds ratio, F1, F-beta, MCC, informedness, markedness, and threat score.

For a labeled confusion matrix use `confusion_matrix`. For probability cutoffs use `find_optimal_threshold`. For ranking leads by score (gain/lift) use `lift_table`.

Formula: `source/python-in-excel/functions/classification_metrics.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
classification_metrics("A1:B100")
classification_metrics(data, "churn", "pred")
classification_metrics(data, "churn", "pred", positive="Yes", beta=2)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Table/range, or actual labels if `predicted` is a Series/range. |
| `actual` | No | Actual-label column name, range, or Series. Default: first column. |
| `predicted` | No | Predicted-label column name, range, or Series. Default: second column. |
| `positive` | No | Value that means the positive class. Default `1`. |
| `beta` | No | Recall weight in F-beta. Default `1` (same as F1). Must be > 0. |
| `headers` | No | First row is headers when a ref string is used. Default `True`. |

Use **class labels**, not probabilities. Rows with a blank in either column are dropped. Need at least one remaining pair. Rates with a zero denominator are 0. Likelihood ratios, diagnostic odds ratio, MCC, and threat score are blank (NaN) when undefined.

## Result

| `metric` | Meaning |
|----------|---------|
| `n` | Pairs after dropping blanks. |
| `accuracy` | (TP + TN) / n. |
| `misclassification_rate` | (FP + FN) / n. |
| `true_positive_rate` | TP / (TP + FN). Recall / sensitivity. |
| `false_positive_rate` | FP / (FP + TN). |
| `true_negative_rate` | TN / (TN + FP). Specificity. |
| `false_negative_rate` | FN / (TP + FN). |
| `precision` | TP / (TP + FP). |
| `prevalence` | (TP + FN) / n. |
| `lr_positive` | TPR / FPR (LR+). |
| `lr_negative` | FNR / TNR (LR−). |
| `diagnostic_odds_ratio` | LR+ / LR−. |
| `f1` | Harmonic mean of precision and TPR. |
| `beta` | The `beta` argument. |
| `f_beta` | (1+β²)·precision·TPR / (β²·precision + TPR). |
| `mcc` | Matthews correlation coefficient. |
| `informedness` | TPR + TNR − 1 (Bookmaker informedness). |
| `markedness` | Precision + NPV − 1. |
| `threat_score` | TP / (TP + FP + FN) (critical success index). |

## Example

```python
classification_metrics(pd.DataFrame({
    "churn": [1, 1, 1, 1, 0, 0, 0, 0],
    "pred": [1, 1, 0, 1, 0, 0, 1, 0],
}), "churn", "pred")
```

TP=3, FP=1, FN=1, TN=3. Accuracy = precision = TPR = 0.75, MCC = 0.5, threat score = 0.6, LR+ = 3, DOR = 9.
