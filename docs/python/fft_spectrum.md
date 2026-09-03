# fft_spectrum

Real **FFT periodogram**: cycles, frequency, period, and power. Output is a **table** (`plot=False`) or a **two-panel chart** (`plot=True`).

Formula: `source/python-in-excel/functions/fft_spectrum.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/TimeSeries.py` or `init/PaulPythonLibrary.py`.

Table (PY cell output **Excel value**):

```python
fft_spectrum("A1:A48")
fft_spectrum("A1:A48", dt=1)
```

Chart (leave as a **Python object**):

```python
fft_spectrum("A1:A48", plot=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `data` | Yes | Value column, ref string, Series, or DataFrame (first numeric column). |
| `dt` | No | Time between observations. Default `1` (period is in observation units). Monthly data with `dt=1` gives period in months. |
| `plot` | No | `False` (default) spills a table. `True` returns power vs frequency (top) and power vs period (bottom). |
| `headers` | No | First row is headers when `data` is a ref string. Default `False`. |

Need at least 4 numeric values. The series is demeaned. The DC bin (k=0) is omitted.

## Result (table)

| Column | Notes |
|--------|-------|
| `cycles` | DFT bin *k*: number of cycles in the sample window. |
| `frequency` | Cycles per time unit: `k / (n × dt)`. |
| `period` | Time units per cycle: `1 / frequency`. |
| `power` | Periodogram `|FFT|² / n`. |
| `peak` | `1` on the strongest bin, else `0`. |

A 12-month cycle in 48 monthly points has `cycles=4`, `frequency=1/12`, `period=12`.

## Result (plot)

Stem plots of power vs frequency and power vs period. Leave the cell as a **Python object**, not Excel value.
