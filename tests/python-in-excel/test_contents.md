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
| `"contents" in set(contents()["function"])` | `True` |
| `"expsmooth" in set(contents()["function"])` | `False` |
| `"lag_features" in set(contents()["function"])` | `False` |
| `"stratified_sample" in set(contents()["function"])` | `False` |
| `"stl_fit" in set(contents()["function"])` | `False` |
| `"_norm_values" in set(contents()["function"])` | `False` |
| `contents().loc[contents()["function"] == "describe", "call"].iloc[0]` | `describe(data, headers=True)` |
| `contents().loc[contents()["function"] == "contents", "call"].iloc[0]` | `contents()` |
| `len(contents())` | `10` |

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
| `"fourier_features" in set(contents()["function"])` | `True` |
| `"detect_anomalies" in set(contents()["function"])` | `True` |
| `"expsmooth" in set(contents()["function"])` | `True` |
| `"stratified_sample" in set(contents()["function"])` | `False` |
| `"describe" in set(contents()["function"])` | `False` |
| `"stl_fit" in set(contents()["function"])` | `False` |
| `contents().loc[contents()["function"] == "stl", "call"].iloc[0]` | `stl(data, period, dates=None, robust=False, headers=False)` |
| `len(contents())` | `27` |
