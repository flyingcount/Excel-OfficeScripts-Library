# cluster_prep

Prepare a mixed table for clustering: **standard-scale** numeric columns and **one-hot encode** categoricals so Euclidean methods (k-means, hierarchical, DBSCAN) can run. Follows the [Statology mixed-encoding pipeline](https://www.statology.org/encoding-mixed-datasets-for-clustering/) (`StandardScaler` + `OneHotEncoder` via `ColumnTransformer`), with automatic column typing so any range or DataFrame works.

Formula: `source/python-in-excel/functions/cluster_prep.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
cluster_prep("A1:D20")
cluster_prep("Table1[#All]")
cluster_prep(xl_df("Table1[#All]"))
```

scikit-learn is in the Python in Excel runtime; it is imported inside the function.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Range, table, DataFrame, Series, or `xl()` result. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

## Type detection

Empty rows and columns are dropped first. Remaining columns are classified as:

| Input | Treatment |
|-------|-----------|
| Numeric (int/float) | `StandardScaler` (mean 0, population std 1) |
| Bool | Converted to 0/1, then scaled |
| Datetime / timedelta, or text that is mostly dates | Converted to numeric days, then scaled |
| Object/text that is mostly numbers | Coerced to numeric, then scaled |
| Other text with repeated values | One-hot encoded (binary 0/1 columns) |
| Constant text, or all-unique text (IDs) | Skipped |

Rows with any remaining blank in the kept columns are dropped, matching the article’s `dropna()` before encoding.

Integer codes that represent categories (for example 1/2/3 for region) stay numeric. Store those as text in Excel if they should be one-hot encoded.

## Result

A dense DataFrame: scaled numeric columns first, then one-hot columns named `column_category` (sorted categories). Rows that had blanks are omitted, so the result can be shorter than the input. Set the PY cell to **Excel value** to spill.

Feed the result to clustering, for example:

```python
from sklearn.cluster import KMeans
encoded = cluster_prep("A1:D20")
KMeans(n_clusters=3, random_state=42, n_init="auto").fit_predict(encoded)
```

## Example

Headers `bill`, `mass`, `sex` in `A1:C1`. Rows: `(39.1, 3750, Male)`, `(39.5, 3800, Female)`, `(40.3, 3250, Female)` in `A2:C4`.

```python
cluster_prep("A1:C4")
```

`bill` and `mass` are z-scored. `sex` becomes `sex_Female` and `sex_Male`.
