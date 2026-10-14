# check_collinearity

Flag **redundant numeric columns**: pairwise Pearson |r| above a cutoff, and **variance inflation factor** (VIF). Use this before ranking drivers (`rank_feature_importance`) so duplicate inputs do not inflate importance.

For a full correlation matrix with no VIF, use `corr`.

Formula: `source/python-in-excel/functions/check_collinearity.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
check_collinearity("A1:F100")
check_collinearity("Table1[#All]", threshold=0.8, vif_threshold=5)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Range, table, DataFrame, Series, or `xl()` result. |
| `threshold` | No | Flag a column when its strongest \|Pearson r\| is **greater than** this. Default `0.8`. |
| `vif_threshold` | No | Flag a column when VIF is **greater than** this. Default `5`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Need at least two non-constant numeric columns and three rows with no blanks in those columns. Excel 1×1 arrays for the cutoffs are unwrapped. `threshold` must be in `(0, 1]`; `vif_threshold` must be > 0.

## How columns are used

| Input | Treatment |
|-------|-----------|
| Numeric (int/float) | Used. Constants (population std 0) are dropped. |
| Bool | Converted to 0/1. |
| Text that is mostly numbers | Coerced to numeric (same 80% rule as `cluster_prep`). |
| Datetime, categories, IDs as text | Skipped. |

**max_r** uses pairwise Pearson (a pair can use rows the other columns do not). **VIF** uses listwise complete rows: each column is regressed on the others plus an intercept; VIF = 1 / (1 − R²). Perfect collinearity yields infinite VIF.

## Result

Set the PY cell to **Excel value**. One row per numeric feature, strongest flags first.

| Column | Notes |
|--------|-------|
| `feature` | Column name. |
| `vif` | Variance inflation factor. |
| `max_r` | Signed Pearson r with `with` (largest \|r\|). |
| `with` | Partner for `max_r`. |
| `n_high` | How many other columns have \|r\| > `threshold`. |
| `flag_corr` | `1` if \|max_r\| > `threshold`, else `0`. |
| `flag_vif` | `1` if VIF > `vif_threshold` (or infinite), else `0`. |
| `flag` | `1` if either flag is 1. |

Conventional VIF bands: ~1 none, > 5 worth a look, > 10 serious. \|r\| > 0.8 is a simple pairwise screen; VIF can still be high when several moderate correlations stack.

## Example

```python
check_collinearity(pd.DataFrame({
    "a": [1, 2, 3, 4, 5, 6, 7, 8],
    "b": [2, 4, 6, 8, 10, 12, 14, 16],
    "c": [0, 1, 0, 1, 0, 1, 0, 1],
}))
```

`a` and `b` are exact duplicates (`max_r` = 1, VIF infinite, `flag` = 1). `c` should not flag at the default cutoffs.
