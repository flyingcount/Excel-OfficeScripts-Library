# outlier_flag

Flag outlier rows using **IQR**, **MAD**, or **z-score** methods. Returns the original values alongside an outlier flag, the detection score, and the lower/upper bounds so you can filter, chart, or feed the flag into a model.

Formula: `source/python-in-excel/functions/outlier_flag.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
outlier_flag("B2:B100")
outlier_flag("B2:B100", method="mad", threshold=2)
outlier_flag("B2:B100", method="zscore", threshold=3)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, DataFrame, Series, or list. First numeric column is used. |
| `method` | No | `'iqr'` (default), `'mad'`, or `'zscore'`. |
| `threshold` | No | Sensitivity. Meaning depends on method (see below). Default `1.5`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

## Methods

### IQR (default)

Interquartile range. A point is an outlier when it falls below Q1 − t × IQR or above Q3 + t × IQR.

- `threshold=1.5` flags "mild" outliers (the Tukey fence used in box plots).
- `threshold=3` flags "far" or "extreme" outliers.
- `score` column is the raw value (compare it to the bounds).

### MAD

Median absolute deviation. A point is an outlier when |value − median| / MAD\_scaled > t.

MAD\_scaled = MAD × 1.4826, which approximates the standard deviation for normally distributed data. The bounds are median ± t × MAD\_scaled.

- `threshold=1.5` is moderate; `threshold=2` is a common choice.
- `score` column is |value − median| / MAD\_scaled.

### Z-score

Population z-score (mean and std with ddof=0, same convention as `zscore_replace`). A point is an outlier when |z| > t. The bounds are mean ± t × std.

- `threshold=3` is the classic three-sigma rule.
- `score` column is |z|.

## Constant data

When the spread (IQR, MAD, or std) is zero, no points are flagged.

## Result

A DataFrame with one row per input value. Set the PY cell to **Excel value** to spill it.

| Column | Notes |
|--------|-------|
| `value` | The original numeric values (coerced, same length as input). |
| `is_outlier` | `1` if outlier, `0` otherwise. Blank rows stay blank. |
| `score` | IQR: raw value. MAD: scaled deviation. Z-score: |z|. |
| `lower_bound` | Lower fence (same for every row). |
| `upper_bound` | Upper fence (same for every row). |

## Example

```python
outlier_flag([1, 2, 3, 4, 100])
```

With IQR and threshold 1.5: Q1 = 2, Q3 = 4, IQR = 2, lower = −1, upper = 7. Row 4 (value 100) is flagged.

```python
outlier_flag([1, 2, 3, 4, 100], method="zscore", threshold=2)
```

Mean ≈ 22, std ≈ 39.2. |z| of 100 ≈ 1.99 — borderline, just under 2.
