# Test: contents

## Setup (full library)

1. Formulas → **Initialization** → paste `source/python-in-excel/init/PaulPythonLibrary.py` → Save.

## Cases (full library)

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(contents().columns)` | `['function', 'description', 'call']` |
| `"xl_df" in set(contents()["function"])` | `True` |
| `"stratified_sample" in set(contents()["function"])` | `True` |
| `"qq_norm" in set(contents()["function"])` | `True` |
| `"contents" in set(contents()["function"])` | `True` |
| `"lag_features" in set(contents()["function"])` | `True` |
| `"outlier_flag" in set(contents()["function"])` | `True` |
| `"stl_fit" in set(contents()["function"])` | `False` |
| `"_norm_values" in set(contents()["function"])` | `False` |
| `contents().loc[contents()["function"] == "stratified_sample", "description"].iloc[0]` | `Stratified sample` |
| `contents().loc[contents()["function"] == "describe", "call"].iloc[0]` | `describe(data, headers=True)` |
| `contents().loc[contents()["function"] == "lag_features", "call"].iloc[0]` | `lag_features(data, value_col=None, date_col=None, lags=1, windows=7, stats='mean', ema=0, headers=True)` |
| `contents().loc[contents()["function"] == "contents", "call"].iloc[0]` | `contents()` |
| `len(contents())` | `29` |

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
