# reservoir_sample

**Algorithm R** reservoir sampling: a uniformly random sample of `k` rows from a table or stream, using memory proportional to `k` rather than the full length.

Formula: `source/python-in-excel/functions/reservoir_sample.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/Sampling.py` (sampling functions only) or the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
reservoir_sample("A1:D2000", 50)
reservoir_sample("Table1[#All]", 100, random_state=42)
reservoir_sample("B2:B5000", 20, headers=False)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Range, table, DataFrame, Series, list, or `xl()` result. Rows are the sampling units. |
| `k` | Yes | Desired sample size. Must be at least 1. |
| `random_state` | No | Seed for reproducibility. Default `42`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Empty rows are dropped. Excel 1×1 cells for `k` and `random_state` are unwrapped to scalars.

## How it works

1. Put the first `k` rows into the reservoir.
2. For each later row at position `i` (0-based), draw `j` uniformly from `0` through `i`. If `j < k`, that row replaces reservoir slot `j`. Replacement probability is `k / (i + 1)`, so every row seen so far is equally likely to be in the sample.

If the table has fewer than `k` rows, the result is the whole table in order. Unlike `systematic_sample`, `k` larger than `N` does not raise.

The original index is not kept. Set the PY cell to **Excel value** to spill.

## Example

Header `x` in `A1`. Values `1` through `10` in `A2:A11`. Three-row sample:

```python
reservoir_sample("A1:A11", 3)
```
