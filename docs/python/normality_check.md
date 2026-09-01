# normality_check

Shapiro-Wilk, Anderson-Darling, and a normal Q-Q plot in **one file**. Paste this module once, then call any of the three tests.

Formula: `source/python-in-excel/functions/normality_check.py`

Functions in the file: `shapiro`, `anderson`, `normality_check` (Q-Q chart; `qq_norm` is the same function).

## Install

Formulas → **Initialization** → paste the whole file after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

If you paste the file into a PY cell instead, that cell shows:

```text
normality_check(data, plot=True, headers=False)
qq_norm(data, plot=True, headers=False)
shapiro(data)
anderson(data)
```

Copy a line from there into another PY cell to run a test. Functions are available workbook-wide only after they are in Initialization.

## Shapiro-Wilk (Excel value)

P-value in that cell:

```python
shapiro("A1:A10", "pvalue")
```

Statistic: `shapiro("A1:A10", "stat")`. Both values as a table: `shapiro("A1:A10")` (columns `metric`, `value`, `interpretation`).

If p > 0.05, a normal distribution in the data can be assumed.

## Anderson-Darling (Excel value)

A^2 in that cell:

```python
anderson("A1:A10", "stat")
```

5% critical value: `anderson("A1:A10", "critical_5")`. Full table: `anderson("A1:A10")` (includes `interpretation`).

A^2 above the 5% critical value suggests the data are not normal at 5%.

## Q-Q plot (Python object)

```python
normality_check("A1:A10")
qq_norm("A1:A10")
```

Leave as a **Python object**. Combined table: `normality_check("A1:A10", plot=False)` as **Excel value** (`metric`, `value`, `interpretation`).

If the chart is in `B2`, other PY cells (Excel value):

```python
B2.shapiro_pvalue
B2.anderson_stat
B2.results
```

## Arguments

Shared: `data` is a value column, Series, list, or `xl()` result. `headers` is True when the first row of a ref string is headers. Need at least 3 numeric values. Blanks are dropped. DataFrames use the first numeric column.

| Function | Extra arguments |
|----------|-----------------|
| `shapiro` | `metric`: `"pvalue"` or `"stat"` for a float; omit to spill the table. |
| `anderson` | `metric`: `"stat"` or `"critical_5"` (also `critical_15`, `critical_10`, `critical_2_5`, `critical_1`); omit to spill the table. |
| `normality_check` / `qq_norm` | `plot`: `True` (default) is the chart; `False` spills n, Shapiro, Anderson, and an interpretation column. |
