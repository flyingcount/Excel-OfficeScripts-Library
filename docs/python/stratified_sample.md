# stratified_sample

Draw a **proportional stratified sample**: each group in a stratum column gets a share of `total_n` equal to its share of the population, then rows are sampled independently inside that group.

Formula: `source/python-in-excel/functions/stratified_sample.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/Sampling.py` (sampling functions only) or the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
stratified_sample("A1:D200", "tier", 50)
stratified_sample("Table1[#All]", "region", 100, random_state=42)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Range, table, DataFrame, Series, or `xl()` result. |
| `strata_col` | Yes | Column name that defines the strata. Case-insensitive if the exact header is not found. |
| `total_n` | Yes | Target sample size across all strata. |
| `random_state` | No | Seed for reproducibility. Default `42`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Empty rows are dropped. Rows with a blank stratum value are dropped. Excel 1×1 cells for `strata_col`, `total_n`, and `random_state` are unwrapped to scalars.

## Allocation

For a stratum of size `n_h` in a population of size `N`:

`n_h_sample = min(n_h, max(1, round(total_n * n_h / N)))`

Each non-empty stratum gets at least one row (capped at the stratum size), so the returned row count can differ from `total_n` when rounding or when there are many small groups. If `total_n` is larger than the population, the result is the full table (every stratum taken in full).

The original index is not kept. Set the PY cell to **Excel value** to spill.

## Example

Headers `tier`, `value` in `A1:B1`. Four `A` rows and two `B` rows in `A2:B7`. Target `n=3` allocates 2 from `A` and 1 from `B`:

```python
stratified_sample("A1:B7", "tier", 3)
```
