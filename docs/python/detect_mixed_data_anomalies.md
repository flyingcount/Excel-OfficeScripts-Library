# detect_mixed_data_anomalies

Flag anomalous **rows** in a mixed table (numeric + categorical). Combines **Mahalanobis distance**, **univariate |z| > 3**, **rare categories**, **within-group numeric extremes**, and **Isolation Forest**.

This is for cross-sectional tables. For an ordered series use `detect_anomalies`. For a single numeric column use `outlier_flag`.

Formula: `source/python-in-excel/functions/detect_mixed_data_anomalies.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
detect_mixed_data_anomalies("A1:G100")
detect_mixed_data_anomalies("Table1[#All]", contamination=0.05)
detect_mixed_data_anomalies("A1:G100", max_categories=10)
```

scipy and scikit-learn are in the Python in Excel runtime; they are imported inside the function.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Range, table, DataFrame, Series, or `xl()` result. |
| `contamination` | No | Expected anomaly share in `(0, 0.5]`. Default `0.05` (5%). Chi-square cutoff for Mahalanobis, Isolation Forest `contamination`, and the rare-category frequency cap. |
| `max_categories` | No | Skip text columns with more unique values than this (IDs / free text). Default `15`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Excel may pass a 1×1 array for a scalar; those values are unwrapped.

## How columns are used

| Input | Treatment |
|-------|-----------|
| Numeric (int/float) | Univariate z-score, Mahalanobis (if 2+ numeric columns), scaled for Isolation Forest. Blanks filled with the column median. |
| Text that is mostly numbers | Coerced to numeric (same 80% rule as `cluster_prep`). |
| Text with repeated values | One-hot encoded for Isolation Forest if unique count is between 2 and `max_categories`, and not all-unique (IDs). Blanks become `"Missing"`. Rare if that value’s share ≤ `contamination`. |
| Constant text, all-unique text, or high-cardinality text | Skipped. |

Mahalanobis runs only when there are **two or more** numeric columns. With fewer, `md_distance` is 0, `md_p_value` is 1, and `flag_md` is 0. Isolation Forest still runs on whatever numeric and categorical features remain.

Need at least two rows. `contamination` outside `(0, 0.5]` raises an error.

## Methods

### Extreme value (univariate)

Population |z-score| > 3 on any numeric column (`ddof=0`).

### Mahalanobis distance (multivariate numeric)

Distance of each row from the numeric mean, using the pseudoinverse of the covariance matrix. Squared distance is compared to the chi-square quantile at `1 - contamination` with degrees of freedom = number of numeric columns.

### Rare category

A categorical value whose share of rows is ≤ `contamination` (for example one `Z` among 20 rows at 5%).

### Inconsistent structural combo

A numeric value that is extreme **within its category** (|z| > 3, group size at least 4, group smaller than the whole table) but not a global extreme. Isolation Forest leftovers (flagged by IF only) use this label too.

### Isolation Forest (mixed)

`StandardScaler` on numeric columns and `OneHotEncoder` on valid categoricals, then sklearn `IsolationForest` (`random_state=42`). `if_score` is `decision_function`: **lower** (more negative) is more anomalous. `flag_if` is 1 when `predict` returns −1.

## Result

The input columns plus:

| Column | Notes |
|--------|-------|
| `md_distance` | Mahalanobis distance (0 when fewer than 2 numeric columns). |
| `md_p_value` | Chi-square tail probability of the squared distance (1 when MD is skipped). |
| `if_score` | Isolation Forest decision score. Lower = more anomalous. |
| `flag_md` | `1` if MD flags the row, else `0`. |
| `flag_if` | `1` if Isolation Forest flags the row, else `0`. |
| `flag_extreme` | `1` if any numeric |z| > 3, else `0`. |
| `flag_rare` | `1` if any used category is rare, else `0`. |
| `anomaly_class` | See below. First matching rule wins. |

| `anomaly_class` | When |
|-----------------|------|
| `Consensus Anomaly` | Numeric signal (extreme or MD) **and** categorical signal (rare or within-group combo). |
| `Extreme Value (Numeric)` | Global \|z\| > 3, no categorical signal. |
| `Multivariate Outlier (Numeric)` | Mahalanobis only (unusual numeric combination, no univariate extreme). |
| `Rare Category (Categorical)` | Rare label, no numeric signal. |
| `Inconsistent Structural Combo` | Within-group numeric extreme, or Isolation Forest only. |
| `Normal` | None of the above. |

Set the PY cell to **Excel value** to spill.

## Example

19 rows at `(x=10, y=20, grp=A)` and one row at `(x=100, y=200, grp=Z)`:

```python
detect_mixed_data_anomalies(pd.DataFrame({
    "x": [10] * 19 + [100],
    "y": [20] * 19 + [200],
    "grp": ["A"] * 19 + ["Z"],
}))
```

The last row is a **Consensus Anomaly** (extreme numbers and a rare category). Same numbers with `grp=A` on every row is **Extreme Value (Numeric)**.
