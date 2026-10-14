# two_stage_cluster_sample

**Two-stage cluster sampling:** first pick a random set of clusters, then randomly sample rows inside each chosen cluster.

Formula: `source/python-in-excel/functions/two_stage_cluster_sample.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/Sampling.py` (sampling functions only) or the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
two_stage_cluster_sample("A1:D200", "school", 5, 10)
two_stage_cluster_sample("Table1[#All]", "region", 3, 20, random_state=42)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Range, table, DataFrame, Series, or `xl()` result. |
| `cluster_col` | Yes | Column that identifies cluster membership. Case-insensitive if the exact header is not found. |
| `n_clusters` | Yes | How many clusters to select in stage 1. Must be between 1 and the number of distinct clusters. |
| `sample_per_cluster` | Yes | How many rows to sample from each selected cluster in stage 2. |
| `random_state` | No | Seed for reproducibility. Default `42`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Empty rows are dropped. Rows with a blank cluster value are dropped. Excel 1×1 cells for `cluster_col`, `n_clusters`, `sample_per_cluster`, and `random_state` are unwrapped to scalars.

## How it works

1. **Stage 1.** Choose `n_clusters` clusters at random without replacement from the unique values in `cluster_col`.
2. **Stage 2.** Inside each selected cluster, draw `sample_per_cluster` rows at random. If a cluster has fewer rows than `sample_per_cluster`, take the whole cluster.

`n_clusters` larger than the number of clusters raises `ValueError`. The original index is not kept. Set the PY cell to **Excel value** to spill.

## Example

Header `cluster` in `A1`, `value` in `B1`. Three clusters `A`, `B`, `C` with three rows each in `A2:B10`. Select 2 clusters and 2 rows from each (up to 4 rows):

```python
two_stage_cluster_sample("A1:B10", "cluster", 2, 2)
```
