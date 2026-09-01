# Test: normality_check

## Setup

1. Formulas → **Initialization** → paste `source/python-in-excel/functions/normality_check.py` after the default imports → Save.
2. Put `88`, `92`, `95`, `85`, `90`, `89`, `93`, `87`, `91`, `86` in `A1:A10`.

Table / scalar: set the PY cell to **Excel value**. Plot: leave as a **Python object**.

## Cases

| Python | Expected |
|--------|----------|
| `shapiro("A1:A10", "pvalue") > 0.05` | `True` |
| `shapiro([88, 92, 95, 85, 90, 89, 93, 87, 91, 86], "pvalue") > 0.05` | `True` |
| `shapiro("A1:A10", "pvalue") == shapiro("A1:A10", "shapiro_pvalue")` | `True` |
| `0 < shapiro("A1:A10", "stat") <= 1` | `True` |
| `shapiro("A1:A10").set_index("metric").loc["shapiro_pvalue", "value"] > 0.05` | `True` |
| `list(shapiro("A1:A10")["metric"])` | `shapiro_stat`, `shapiro_pvalue` |
| `list(shapiro("A1:A10").columns)` | `metric`, `value`, `interpretation` |
| `"p > 0.05" in shapiro("A1:A10").set_index("metric").loc["shapiro_pvalue", "interpretation"]` | `True` |
| `anderson("A1:A10", "stat") < anderson("A1:A10", "critical_5")` | `True` |
| `anderson("A1:A10", "stat") == anderson("A1:A10", "anderson_stat")` | `True` |
| `anderson("A1:A10", "critical_5") == anderson("A1:A10", "anderson_critical_5")` | `True` |
| `"anderson_critical_5" in list(anderson("A1:A10")["metric"])` | `True` |
| `normality_check("A1:A10", plot=False).set_index("metric").loc["n", "value"]` | `10` |
| `list(normality_check("A1:A10", plot=False).columns)` | `metric`, `value`, `interpretation` |
| `"p > 0.05" in normality_check("A1:A10", plot=False).set_index("metric").loc["shapiro_pvalue", "interpretation"]` | `True` |
| `normality_check("A1:A10", plot=False).set_index("metric").loc["shapiro_pvalue", "value"] > 0.05` | `True` |
| `type(normality_check("A1:A10")).__name__` | `Figure` |
| `qq_norm is normality_check` | `True` |
| `normality_check("A1:A10").shapiro_pvalue > 0.05` | `True` |
| `any("Shapiro" in t.get_text() for t in normality_check("A1:A10").axes[0].texts)` | `True` |
| `any("p > 0.05" in t.get_text() for t in normality_check("A1:A10").axes[0].texts)` | `True` |
| `any("Anderson" in t.get_text() for t in normality_check("A1:A10").axes[0].texts)` | `True` |
