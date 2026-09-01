# Test: two_stage_cluster_sample

## Setup

1. Formulas → **Initialization** → paste `two_stage_cluster_sample` from `source/python-in-excel/functions/two_stage_cluster_sample.py` after the default imports → Save. Or paste `init/Sampling.py`.
2. Headers `cluster`, `value` in `A1:B1`. Three rows each of `A`, `B`, and `C` in `A2:A10` with values `1` through `9` in `B2:B10`.

Nine rows, three clusters of size 3. `n_clusters=2` and `sample_per_cluster=2` returns 4 rows from 2 clusters. If `sample_per_cluster` exceeds a cluster’s size, that cluster is taken in full.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `len(two_stage_cluster_sample("A1:B10", "cluster", 2, 2))` | `4` |
| `int(two_stage_cluster_sample("A1:B10", "cluster", 2, 2)["cluster"].nunique())` | `2` |
| `int(two_stage_cluster_sample("A1:B10", "cluster", 2, 2)["cluster"].value_counts().max())` | `2` |
| `int(two_stage_cluster_sample("A1:B10", "cluster", 2, 2)["cluster"].value_counts().min())` | `2` |
| `list(two_stage_cluster_sample("A1:B10", "cluster", 2, 2).columns)` | `['cluster', 'value']` |
| `len(two_stage_cluster_sample("A1:B10", "cluster", 1, 10))` | `3` |
| `len(two_stage_cluster_sample("A1:B10", "cluster", 3, 3))` | `9` |
| `len(two_stage_cluster_sample("A1:B10", "Cluster", 2, 2))` | `4` |
| `two_stage_cluster_sample("A1:B10", "cluster", 2, 2).equals(two_stage_cluster_sample("A1:B10", "cluster", 2, 2, 42))` | `True` |
| `len(two_stage_cluster_sample(pd.DataFrame({"cluster": ["A", "A", "A", "B", "B", "B", "C", "C", "C"], "value": list(range(1, 10))}), "cluster", 2, 2))` | `4` |
