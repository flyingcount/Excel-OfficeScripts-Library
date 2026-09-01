# Test: resid_analysis

## Setup

1. Formulas → **Initialization** → paste `resid_analysis` from `source/python-in-excel/functions/resid_analysis.py` after the default imports → Save.
2. Put `1`, `2`, `3`, `4`, `5` in `A1:A5`.
3. Optional: 24 seasonal values in `B1:B24` for the `stl` cross-check.

## Cases

Table: set the PY cell to **Excel value**. Plot, and rows that read `.std_resid`: leave as a **Python object**.

| Python | Expected |
|--------|----------|
| `resid_analysis("A1:A5").set_index("metric").loc["n", "value"]` | `5` |
| `resid_analysis("A1:A5").set_index("metric").loc["sum", "value"]` | `15` |
| `resid_analysis("A1:A5").set_index("metric").loc["mean", "value"]` | `3` |
| `abs(resid_analysis("A1:A5").set_index("metric").loc["slope_vs_order", "value"] - 1) < 1e-12` | `True` |
| `abs(resid_analysis("A1:A5").set_index("metric").loc["intercept_vs_order", "value"]) < 1e-12` | `True` |
| `abs(resid_analysis("A1:A5").set_index("metric").loc["rsq_vs_order", "value"] - 1) < 1e-12` | `True` |
| `resid_analysis([0, 0, 0, 0]).set_index("metric").loc["n", "value"]` | `4` |
| `resid_analysis(stl([1, 2, 3, 4] * 6, 4)).set_index("metric").loc["n", "value"]` | `24` |
| `list(resid_analysis("A1:A5")["metric"])[:14]` | `n`, `mean`, `std`, `min`, `max`, `sum`, `slope_vs_order`, `intercept_vs_order`, `rsq_vs_order`, `ljung_box_lags`, `ljung_box_stat`, `ljung_box_pvalue`, `jarque_bera_stat`, `jarque_bera_pvalue` |
| `abs(resid_analysis("A1:A5").set_index("metric").loc["durbin_watson", "value"] - 4 / 55) < 1e-12` | `True` |
| `0 < resid_analysis("A1:A5").set_index("metric").loc["shapiro_stat", "value"] <= 1` | `True` |
| `0 <= resid_analysis("A1:A5").set_index("metric").loc["shapiro_pvalue", "value"] <= 1` | `True` |
| `abs(resid_analysis("A1:A5").set_index("metric").loc["std_resid_max_abs", "value"] - 2 ** 0.5) < 1e-12` | `True` |
| `resid_analysis("A1:A5").set_index("metric").loc["n_std_resid_gt_2", "value"]` | `0` |
| `len(resid_analysis("A1:A5").std_resid)` | `5` |
| `abs(resid_analysis("A1:A5").std_resid.iloc[0] + 2 ** 0.5) < 1e-12` | `True` |
| `pd.isna(resid_analysis([0, 0, 0, 0]).set_index("metric").loc["durbin_watson", "value"])` | `True` |
| `pd.isna(resid_analysis([0, 0, 0, 0]).set_index("metric").loc["std_resid_max_abs", "value"])` | `True` |
| `type(resid_analysis("A1:A5", plot=True)).__name__` | `Figure` |
| `len(resid_analysis("A1:A5", plot=True).axes)` | at least `4` |
| `len(resid_analysis("A1:A5", plot=True).std_resid)` | `5` |
| `list(resid_analysis("A1:A5").columns)` | `metric`, `value`, `guidance` |
| `resid_analysis("A1:A5")["guidance"].notna().all() and (resid_analysis("A1:A5")["guidance"].str.len() > 0).all()` | `True` |
| `"0.05" in resid_analysis("A1:A5").set_index("metric").loc["ljung_box_pvalue", "guidance"]` | `True` |
| `"Near 2" in resid_analysis("A1:A5").set_index("metric").loc["durbin_watson", "guidance"]` | `True` |
