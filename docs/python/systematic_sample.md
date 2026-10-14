# systematic_sample

Draw a **systematic sample** of rows: pick a random start in the first interval, then take every *k*th row. Same method as sampling an ordered list with interval `k = N // sample_size`.

Formula: `source/python-in-excel/functions/systematic_sample.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/Sampling.py` (sampling functions only) or the whole `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
systematic_sample("A1:D200", 50)
systematic_sample("Table1[#All]", 100, random_state=42)
systematic_sample("B2:B100", 20, headers=False)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Range, table, DataFrame, Series, list, or `xl()` result. Rows are the sampling units. |
| `sample_size` | Yes | Number of rows to return. Must be between 1 and the population size. |
| `random_state` | No | Seed for the random start. Default `42`. |
| `headers` | No | First row is headers when `data` is a ref string. Default `True`. |

Empty rows are dropped before `N` is counted. Excel 1×1 cells for `sample_size` and `random_state` are unwrapped to scalars.

## How it works

1. `k = N // sample_size` (step between selected rows).
2. Start is a random integer from `0` through `k - 1` (the first interval). That is what randomizes the sample; without it the same positions would always be chosen.
3. Rows at `start`, `start+k`, `start+2k`, … are kept, then trimmed to `sample_size` if integer division produced one extra row.

`sample_size` larger than `N` raises `ValueError`. If `sample_size` equals `N`, `k` is 1 and the result is the full table in order.

The original index is not kept. Set the PY cell to **Excel value** to spill.

## Example

Header `x` in `A1`. Values `1` through `10` in `A2:A11`. Five rows, interval `k=2`, so the sample is either the odd or the even values depending on the start:

```python
systematic_sample("A1:A11", 5)
```
