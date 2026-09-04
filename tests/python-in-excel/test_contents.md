# Test: contents

## Setup (general library)

1. Formulas → **Initialization** → paste `source/python-in-excel/init/PaulPythonLibrary.py` → Save.

## Cases (general library)

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(contents().columns)` | `['function', 'description', 'call']` |
| `"xl_df" in set(contents()["function"])` | `True` |
| `"describe" in set(contents()["function"])` | `True` |
| `"qq_norm" in set(contents()["function"])` | `True` |
| `"outlier_flag" in set(contents()["function"])` | `True` |
| `"cluster_prep" in set(contents()["function"])` | `True` |
| `"detect_mixed_data_anomalies" in set(contents()["function"])` | `True` |
| `"rank_feature_importance" in set(contents()["function"])` | `True` |
| `"check_collinearity" in set(contents()["function"])` | `True` |
| `"confusion_matrix" in set(contents()["function"])` | `True` |
| `"classification_metrics" in set(contents()["function"])` | `True` |
| `"find_optimal_threshold" in set(contents()["function"])` | `True` |
| `"lift_table" in set(contents()["function"])` | `True` |
| `"contents" in set(contents()["function"])` | `True` |
| `"expsmooth" in set(contents()["function"])` | `False` |
| `"xmr_spc" in set(contents()["function"])` | `False` |
| `"lag_features" in set(contents()["function"])` | `False` |
| `"lead_features" in set(contents()["function"])` | `False` |
| `"breakpoints" in set(contents()["function"])` | `False` |
| `"stratified_sample" in set(contents()["function"])` | `False` |
| `"stl_fit" in set(contents()["function"])` | `False` |
| `"_norm_values" in set(contents()["function"])` | `False` |
| `contents().loc[contents()["function"] == "describe", "call"].iloc[0]` | `describe(data, headers=True)` |
| `contents().loc[contents()["function"] == "rank_feature_importance", "call"].iloc[0]` | `rank_feature_importance(data, target, top=10, headers=True)` |
| `contents().loc[contents()["function"] == "check_collinearity", "call"].iloc[0]` | `check_collinearity(data, threshold=0.8, vif_threshold=5, headers=True)` |
| `contents().loc[contents()["function"] == "classification_metrics", "call"].iloc[0]` | `classification_metrics(data, actual=None, predicted=None, positive=1, beta=1, headers=True)` |
| `contents().loc[contents()["function"] == "confusion_matrix", "call"].iloc[0]` | `confusion_matrix(data, actual=None, predicted=None, positive=1, pos_name='Positive', neg_name='Negative', plot=False, headers=True)` |
| `contents().loc[contents()["function"] == "lift_table", "call"].iloc[0]` | `lift_table(data, actual=None, proba=None, bins=10, positive=1, plot=False, headers=True)` |
| `contents().loc[contents()["function"] == "outlier_flag", "call"].iloc[0]` | `outlier_flag(data, method='iqr', threshold=1.5, headers=False, period=12)` |
| `contents().loc[contents()["function"] == "contents", "call"].iloc[0]` | `contents()` |
| `len(contents())` | `17` |

## Setup (sampling only)

1. Formulas → **Initialization** → paste `source/python-in-excel/init/Sampling.py` → Save.

## Cases (sampling only)

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(contents().columns)` | `['function', 'description', 'call']` |
| `list(contents()["function"])` | `['contents', 'stratified_sample', 'systematic_sample', 'two_stage_cluster_sample', 'reservoir_sample']` |
| `"xl_df" in set(contents()["function"])` | `False` |
| `contents().loc[contents()["function"] == "reservoir_sample", "description"].iloc[0]` | `Reservoir sample` |
| `contents().loc[contents()["function"] == "reservoir_sample", "call"].iloc[0]` | `reservoir_sample(data, k, random_state=42, headers=True)` |
| `len(contents())` | `5` |

## Setup (time series only)

1. Formulas → **Initialization** → paste `source/python-in-excel/init/TimeSeries.py` → Save.

## Cases (time series only)

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(contents().columns)` | `['function', 'description', 'call']` |
| `"lag_features" in set(contents()["function"])` | `True` |
| `"lead_features" in set(contents()["function"])` | `True` |
| `"fourier_features" in set(contents()["function"])` | `True` |
| `"detect_anomalies" in set(contents()["function"])` | `True` |
| `"breakpoints" in set(contents()["function"])` | `True` |
| `"forecast_plot" in set(contents()["function"])` | `True` |
| `"expsmooth" in set(contents()["function"])` | `True` |
| `"stratified_sample" in set(contents()["function"])` | `False` |
| `"xmr_spc" in set(contents()["function"])` | `False` |
| `"rank_feature_importance" in set(contents()["function"])` | `False` |
| `"check_collinearity" in set(contents()["function"])` | `False` |
| `"classification_metrics" in set(contents()["function"])` | `False` |
| `"confusion_matrix" in set(contents()["function"])` | `False` |
| `"lift_table" in set(contents()["function"])` | `False` |
| `"describe" in set(contents()["function"])` | `False` |
| `"stl_fit" in set(contents()["function"])` | `False` |
| `contents().loc[contents()["function"] == "expsmooth", "call"].iloc[0]` | `expsmooth(data, alpha=0.2, h=12, level=0.95, plot=False, headers=False)` |
| `contents().loc[contents()["function"] == "ets_forecast", "call"].iloc[0]` | `ets_forecast(data, h=12, trend='add', seasonal='add', period=12, level=0.95, plot=False, headers=False)` |
| `contents().loc[contents()["function"] == "sarima_forecast", "call"].iloc[0]` | `sarima_forecast(data, h=12, p=1, d=1, q=1, P=1, D=1, Q=1, s=12, level=0.95, plot=False, headers=False)` |
| `contents().loc[contents()["function"] == "lead_features", "call"].iloc[0]` | `lead_features(data, leads=1, value_col=None, date_col=None, headers=True)` |
| `contents().loc[contents()["function"] == "breakpoints", "call"].iloc[0]` | `breakpoints(data, method='cusum', alpha=0.05, at=None, nbreaks=None, plot=False, headers=True, date_col=None)` |
| `contents().loc[contents()["function"] == "stl", "call"].iloc[0]` | `stl(data, period, dates=None, robust=False, headers=False)` |
| `len(contents())` | `30` |

## Setup (SPC only)

1. Formulas → **Initialization** → paste `source/python-in-excel/init/SPC.py` → Save.

## Cases (SPC only)

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(contents().columns)` | `['function', 'description', 'call']` |
| `list(contents()["function"])` | `['contents', 'xmr_spc']` |
| `"describe" in set(contents()["function"])` | `False` |
| `"expsmooth" in set(contents()["function"])` | `False` |
| `"stratified_sample" in set(contents()["function"])` | `False` |
| `"rank_feature_importance" in set(contents()["function"])` | `False` |
| `"check_collinearity" in set(contents()["function"])` | `False` |
| `"classification_metrics" in set(contents()["function"])` | `False` |
| `"confusion_matrix" in set(contents()["function"])` | `False` |
| `"lift_table" in set(contents()["function"])` | `False` |
| `contents().loc[contents()["function"] == "xmr_spc", "call"].iloc[0]` | `xmr_spc(data, dates=None, plot=False, title='XmR chart', headers=False)` |
| `len(contents())` | `2` |
