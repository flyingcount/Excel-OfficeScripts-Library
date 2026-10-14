# rank_feature_importance

Rank table columns as **drivers of a target** without fitting a machine-learning model. Uses **point-biserial correlation** (numeric vs binary), **chi-square / Cramer's V** (categorical), and **Information Value** when the target is binary.

This is a cross-sectional table tool. For pairwise numeric correlation only, use `corr`. For mixed-table row flags, use `detect_mixed_data_anomalies`.

Formula: `source/python-in-excel/functions/rank_feature_importance.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
rank_feature_importance("A1:E100", "churn")
rank_feature_importance("Table1[#All]", "churn", top=5)
rank_feature_importance(data, data["churn"])
```

scipy is in the Python in Excel runtime; it is imported inside the function.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Range, table, DataFrame, Series, or `xl()` result. |
| `target` | Yes | Target column name (case-insensitive), a range such as `"E2:E100"`, or a Series/column of y. |
| `top` | No | How many rows to return. Default `10`. `0` returns every scored feature. |
| `headers` | No | First row is headers when `data` or `target` is a ref string. Default `True`. |

Need at least three rows with a non-blank target. Excel 1×1 arrays for `target` and `top` are unwrapped.

## How columns are scored

The target is **binary** when it has exactly two distinct values (for example `0`/`1` or `Yes`/`No`). A numeric target with more than 12 distinct values is treated as continuous. Other targets are multi-class.

| Feature | Binary target | Continuous target | Multi-class target |
|---------|---------------|-------------------|--------------------|
| Numeric | \|point-biserial r\|; IV from up to 10 quantile bins | \|Pearson r\| | eta (correlation ratio) |
| Categorical | Cramer's V from χ² (no Yates correction); IV from the categories | eta of y within categories | Cramer's V from χ² |

`score` is the association in that table (0–1 for |r|, V, and eta; IV is typically 0–about 3 and is stored in `iv`, not used as `score`). Rows are sorted by `score` descending, then feature name.

Text that is mostly numbers is coerced to numeric (same 80% rule as `cluster_prep`). Constant columns, datetime columns, and all-unique text (IDs) are skipped. Integer codes that stand for categories stay numeric unless you store them as text.

## Strength

From `score` (|r|, Cramer's V, or eta):

| `strength` | `score` |
|------------|---------|
| weak | < 0.1 |
| modest | 0.1 – < 0.3 |
| moderate | 0.3 – < 0.5 |
| strong | ≥ 0.5 |

Information Value (`iv`, binary target only, 0.5 Laplace smoothing) is a credit-risk style extra. Rough Siddiqi bands: < 0.02 not useful, 0.02–0.1 weak, 0.1–0.3 medium, 0.3–0.5 strong, > 0.5 suspiciously strong (possible leakage).

## Result

Set the PY cell to **Excel value**.

| Column | Notes |
|--------|-------|
| `rank` | 1 … `top` after sorting by `score`. |
| `feature` | Column name. |
| `type` | `numeric` or `categorical`. |
| `method` | `point-biserial`, `chi-square`, `pearson`, or `eta`. |
| `score` | Association strength used for ranking. |
| `p_value` | Two-sided p from the method’s test. |
| `iv` | Information Value when the target is binary; blank otherwise. |
| `strength` | Label from `score` (table above). |

## Example

```python
rank_feature_importance(pd.DataFrame({
    "id": [1, 2, 3, 4, 5, 6, 7, 8],
    "amount": [10, 11, 12, 13, 40, 42, 41, 43],
    "segment": list("AAAABBBB"),
    "noise": [5, 20, 8, 15, 7, 18, 9, 16],
    "churn": [0, 0, 0, 0, 1, 1, 1, 1],
}), "churn")
```

`id` is skipped (all unique). `amount` and `segment` score as strong; `noise` ranks lower. `segment` has Cramer's V = 1.
