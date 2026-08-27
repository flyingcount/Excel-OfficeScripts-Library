# Test: qq_norm

## Setup

1. Formulas → **Initialization** → paste `qq_norm` from `source/python-in-excel/functions/qq_norm.py` after the default imports → Save.
2. Put `88`, `92`, `95`, `85`, `90`, `89`, `93`, `87`, `91`, `86` in `A1:A10`.

Table: set the PY cell to **Excel value**. Plot: leave as a **Python object**.

## Cases

| Python | Expected |
|--------|----------|
| `qq_norm("A1:A10", plot=False).set_index("metric").loc["n", "value"]` | `10` |
| `qq_norm([88, 92, 95, 85, 90, 89, 93, 87, 91, 86], plot=False).set_index("metric").loc["n", "value"]` | `10` |
| `qq_norm("A1:A10", plot=False).set_index("metric").loc["shapiro_pvalue", "value"] > 0.05` | `True` |
| `qq_norm("A1:A10", plot=False).set_index("metric").loc["anderson_stat", "value"] < qq_norm("A1:A10", plot=False).set_index("metric").loc["anderson_critical_5", "value"]` | `True` |
| `type(qq_norm("A1:A10")).__name__` | `Figure` |
| `qq_norm("A1:A10").shapiro_pvalue > 0.05` | `True` |
| `qq_norm("A1:A10").results.set_index("metric").loc["n", "value"]` | `10` |
| `any("Shapiro" in t.get_text() for t in qq_norm("A1:A10").axes[0].texts)` | `True` |
| `any("p > 0.05" in t.get_text() for t in qq_norm("A1:A10").axes[0].texts)` | `True` |
| `any("Anderson" in t.get_text() for t in qq_norm("A1:A10").axes[0].texts)` | `True` |
