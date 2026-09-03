# breakpoints

Structural-break tests: **CUSUM**, **Chow**, or **Bai-Perron**. Table by default; `plot=True` for a chart.

Formula: `source/python-in-excel/functions/breakpoints.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py`.

Table (PY cell output **Excel value**):

```python
breakpoints("A1:A80")
breakpoints("A1:A80", method="chow", at=40)
breakpoints("A1:A80", method="baiperron")
breakpoints("A1:A80", method="baiperron", nbreaks=2)
```

Chart (leave as a **Python object**):

```python
breakpoints("A1:A80", plot=True)
breakpoints("A1:A80", method="baiperron", plot=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, table, Series, or ref string (first numeric col). |
| `method` | No | `cusum` (default), `chow`, or `baiperron` (`bp` / `bai-perron`). |
| `alpha` | No | Significance level. Default `0.05`. |
| `at` | No | Chow only: 1-based last t of regime 1, or a fraction in (0, 1). Omitted: sup-F over a 15% trimmed interior. |
| `nbreaks` | No | Bai-Perron only. Omitted: choose m by BIC (max 5). An integer fixes m. |
| `plot` | No | `False` (default) spills a table. `True` returns a matplotlib chart. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Need at least 10 numeric values.

### CUSUM

Ploberger–Kramer CUSUM on residuals from an intercept + trend OLS fit. `is_break` is 1 when p < `alpha`.

### Chow

F test that intercept and slope differ across a split. With `at` omitted, reports the split with the largest F (Quandt / sup-F).

### Bai-Perron

Mean-shift dates that minimise SSR, with a 10% minimum segment. `break_i` is the 1-based last t of regime `i` (same split as Chow `at`).

## Result (table)

Columns: `metric`, `value`, `guidance`. Set the PY cell to **Excel value**.

## Result (plot)

Series with dashed lines at Chow / Bai-Perron dates. CUSUM adds a second panel of the CUSUM path and ±5% bands. Leave the cell as a **Python object**.
