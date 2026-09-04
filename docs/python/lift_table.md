# lift_table

Rank rows by predicted **probability** (highest first) and split into equal-count **bins** (default 10 = deciles). Each row is a slice of the campaign: response rate, lift vs the base rate, and **cumulative gain** (share of all conversions captured so far). That is the “top 20% of predicted leads yield 65% of all conversions” table used in marketing, sales, and risk.

Use scores, not hard labels. For a cutoff use `find_optimal_threshold`. For label metrics use `classification_metrics`.

Formula: `source/python-in-excel/functions/lift_table.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

Table (PY cell output **Excel value**):

```python
lift_table("A1:B100")
lift_table(data, "churn", "proba")
lift_table(data, "churn", "proba", bins=5)
```

Chart (leave as a **Python object**):

```python
lift_table("A1:B100", plot=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Table/range, or actual labels if `proba` is a Series/range. |
| `actual` | No | Actual-label column name, range, or Series. Default: first column. |
| `proba` | No | Predicted-score column name, range, or Series. Default: second column. |
| `bins` | No | Equal-count groups. Default `10` (deciles). Must be ≥ 2. |
| `positive` | No | Value that means the positive class. Default `1`. |
| `plot` | No | `False` (default) spills a table. `True` returns a two-panel chart. |
| `headers` | No | First row is headers when a ref string is used. Default `True`. |

Rows with a blank actual or score are dropped. Need at least `bins` remaining rows and at least one positive. Ties keep original order (stable sort, highest score first). `bin` 1 is the best scores.

## Result (table)

| Column | Notes |
|--------|-------|
| `bin` | 1 = highest scores. |
| `n` | Rows in the bin. |
| `positives` | Positives in the bin. |
| `response_rate` | `positives / n`. |
| `lift` | `response_rate / overall rate`. |
| `cum_n`, `cum_positives` | Running totals from bin 1. |
| `cum_pct` | `cum_n / N` (population captured). |
| `cum_gain` | `cum_positives / all positives` (conversions captured). |
| `cum_lift` | `cum_gain / cum_pct`. |
| `min_proba`, `max_proba` | Score range in the bin (`min_proba` is the cutoff for this slice and better). |

## Result (plot)

Cumulative gain (with a random diagonal) above cumulative lift (hline at 1). Leave the cell as a **Python object**.

## Example

```python
lift_table(pd.DataFrame({
    "churn": [1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    "proba": [0.95, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10],
}), "churn", "proba", bins=5)
```

Four conversions in ten rows. Top 20% (`bin` 1, `cum_pct` 0.2) captures 50% of conversions (`cum_gain` 0.5), so `cum_lift` is 2.5.
