# Test: contents

## Setup (full library)

1. Formulas → **Initialization** → paste `source/python-in-excel/init/PaulPythonLibrary.py` → Save.

## Cases (full library)

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(contents().columns)` | `['function', 'description']` |
| `"xl_df" in set(contents()["function"])` | `True` |
| `"stratified_sample" in set(contents()["function"])` | `True` |
| `"qq_norm" in set(contents()["function"])` | `True` |
| `"contents" in set(contents()["function"])` | `True` |
| `"lag_features" in set(contents()["function"])` | `True` |
| `"outlier_flag" in set(contents()["function"])` | `True` |
| `"stl_fit" in set(contents()["function"])` | `False` |
| `"_norm_values" in set(contents()["function"])` | `False` |
| `contents().loc[contents()["function"] == "stratified_sample", "description"].iloc[0]` | `Stratified sample` |
| `len(contents())` | `29` |

## Setup (sampling only)

1. Formulas → **Initialization** → paste `source/python-in-excel/init/Sampling.py` → Save.

## Cases (sampling only)

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `list(contents().columns)` | `['function', 'description']` |
| `list(contents()["function"])` | `['contents', 'stratified_sample', 'systematic_sample', 'two_stage_cluster_sample', 'reservoir_sample']` |
| `"xl_df" in set(contents()["function"])` | `False` |
| `contents().loc[contents()["function"] == "reservoir_sample", "description"].iloc[0]` | `Reservoir sample` |
| `len(contents())` | `5` |
