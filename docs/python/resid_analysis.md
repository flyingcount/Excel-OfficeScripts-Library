# resid_analysis

Residual diagnostics for a numeric series. Python counterpart of VBA **Residuals analysis**, plus Ljung-Box and Durbin–Watson (serial correlation), Jarque-Bera and Shapiro–Wilk (normality), and z-scored residual summaries.

Formula: `source/python-in-excel/functions/resid_analysis.py`

Works on a residual column or on `stl()` output (uses the `resid` column).

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste the whole `init/PaulPythonLibrary.py`.

Table (PY cell output **Excel value**):

```python
resid_analysis("C2:C25")
resid_analysis(stl("B2:B25", 12))
```

Chart (leave as a **Python object**):

```python
resid_analysis("C2:C25", plot=True)
resid_analysis(stl("B2:B25", 12), plot=True)
```

The z-scored residual series is `result.std_resid` on the table or the figure. Leave that cell as a **Python object** to read it from another PY cell (for example `B2.std_resid`).

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Residual column, `stl()` DataFrame, Series, or `xl()` result. |
| `lags` | No | Ljung-Box / ACF lags. Default `min(10, n-2)`. |
| `plot` | No | `True` returns a four-panel figure instead of the table. Default `False`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least 3 numeric values. Blanks are dropped. If `data` is a DataFrame, the column named `resid` / `residual` / `residuals` is used when present; otherwise the first numeric column.

## Result (table)

Two columns: `metric`, `value`. Existing rows stay in the same order; new diagnostics are appended.

| Metric | Meaning |
|--------|---------|
| `n` | Count after dropping blanks. |
| `mean`, `std`, `min`, `max`, `sum` | Sample stats (`std` uses n−1). |
| `slope_vs_order`, `intercept_vs_order`, `rsq_vs_order` | Linear fit of residuals on 1…n (VBA Slope / Intercept / R²). |
| `ljung_box_lags`, `ljung_box_stat`, `ljung_box_pvalue` | Ljung-Box at the chosen lag. Small p → leftover autocorrelation. |
| `jarque_bera_stat`, `jarque_bera_pvalue` | Jarque-Bera normality. Small p → not normal. |
| `durbin_watson` | Durbin–Watson. Near 2 → little lag-1 autocorrelation; toward 0 → positive; toward 4 → negative. |
| `shapiro_stat`, `shapiro_pvalue` | Shapiro–Wilk normality. Small p → not normal. |
| `std_resid_max_abs` | Largest absolute z-score (population sd, ddof=0). Blank when the series is constant. |
| `n_std_resid_gt_2` | Count of points with \|z-score\| > 2. |

## Result (plot)

Four panels: residuals vs order (with trend line), histogram, normal QQ, ACF. The figure also has `.std_resid`.
