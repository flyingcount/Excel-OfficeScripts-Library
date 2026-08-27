# qq_norm

Normal Q-Q plot with **Shapiro-Wilk** and **Anderson-Darling** on the chart. The same statistics are attributes on the figure so other PY cells can read them.

Formula: `source/python-in-excel/functions/qq_norm.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste the whole `init/PaulPythonLibrary.py`.

Chart (leave as a **Python object**):

```python
qq_norm("A1:A10")
qq_norm([88, 92, 95, 85, 90, 89, 93, 87, 91, 86])
```

Table (PY cell output **Excel value**):

```python
qq_norm("A1:A10", plot=False)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, Series, list, or `xl()` result. |
| `plot` | No | `True` (default) returns the annotated Q-Q figure. `False` spills a metric/value table. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least 3 numeric values. Blanks are dropped. If `data` is a DataFrame, the first numeric column is used.

## Result (plot)

A matplotlib `Figure`. The Q-Q panel shows Shapiro-Wilk W and p, the note “(If p > 0.05, normal distribution in the data can be assumed)”, and Anderson-Darling A^2 against the 5% critical value.

If the chart is in `B2`, other PY cells can take the numbers (set those cells to **Excel value**):

```python
B2.shapiro_stat
B2.shapiro_pvalue
B2.anderson_stat
B2.anderson_critical_5
B2.results
```

`B2.results` is the same metric/value table as `plot=False`. Shapiro p > 0.05, and Anderson-Darling A^2 below the 5% critical value, both suggest the sample is consistent with a normal distribution.

## Result (table)

Two columns: `metric`, `value`.

| Metric | Meaning |
|--------|---------|
| `n` | Count after dropping blanks. |
| `shapiro_stat` | Shapiro-Wilk W. |
| `shapiro_pvalue` | Shapiro-Wilk p. Small p → not normal. |
| `anderson_stat` | Anderson-Darling A^2. |
| `anderson_critical_5` | Anderson-Darling 5% critical value. A^2 above this → not normal at 5%. |
