# Test: fft_spectrum

## Setup

1. Formulas → **Initialization** → paste `fft_spectrum` from `source/python-in-excel/functions/fft_spectrum.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put a 12-period sine in `A1:A48`: `=SIN(2*PI()*(ROW()-1)/12)` copied down 48 rows.

Peak should be at 4 cycles in the window (`48/12`), frequency `1/12`, period `12`.

## Cases

In a PY cell, set output to **Excel value** for the table.

### Shape and columns

| Python | Expected |
|--------|----------|
| `list(fft_spectrum("A1:A48").columns)` | `['cycles', 'frequency', 'period', 'power', 'peak']` |
| `fft_spectrum("A1:A48").shape[1]` | `5` |
| `int(fft_spectrum("A1:A48")["peak"].sum())` | `1` |

### Sine with period 12 (48 points)

| Python | Expected |
|--------|----------|
| `int(fft_spectrum([np.sin(2*np.pi*t/12) for t in range(48)]).query("peak==1")["cycles"].iloc[0])` | `4` |
| `round(float(fft_spectrum([np.sin(2*np.pi*t/12) for t in range(48)]).query("peak==1")["period"].iloc[0]), 6)` | `12.0` |
| `round(float(fft_spectrum([np.sin(2*np.pi*t/12) for t in range(48)]).query("peak==1")["frequency"].iloc[0]), 6)` | `0.083333` |

### dt scaling

With `dt=2`, frequency halves and period doubles.

| Python | Expected |
|--------|----------|
| `round(float(fft_spectrum([np.sin(2*np.pi*t/12) for t in range(48)], dt=2).query("peak==1")["period"].iloc[0]), 6)` | `24.0` |

### Plot

Leave as a **Python object**.

| Python | Expected |
|--------|----------|
| `type(fft_spectrum([1, 2, 3, 4, 5, 6, 7, 8], plot=True)).__name__` | `Figure` |
| `len(fft_spectrum([1, 2, 3, 4, 5, 6, 7, 8], plot=True).axes)` | `2` |

### Edge cases

| Python | Expected |
|--------|----------|
| `fft_spectrum([1, 2, 3])` | `#PYTHON!` — `Need at least 4 numeric values.` |
| `fft_spectrum([1, 2, 3, 4], dt=0)` | `#PYTHON!` — `dt must be positive.` |
