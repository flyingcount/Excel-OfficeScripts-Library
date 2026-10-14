# Test: zscore_replace

## Setup

1. Formulas → **Initialization** → paste `zscore_replace` from `source/python-in-excel/functions/zscore_replace.py` after the default imports → Save. Or paste `init/TimeSeries.py`.
2. Put `5, 5, 5, 5, 50, 5, 5, 5, 5` in `A1:A9`.
3. Optional dates in `B1:B3`: `2020-01-01`, `2020-01-02`, `2020-01-11` with values `0, 100, 10` in `C1:C3`.

Z-scores use mean and population std (`ddof=0`). For `A1:A9` the spike `50` has |z| ≈ 2.83.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `zscore_replace("A1:A9", z=2).tolist()` | `[5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0]` |
| `zscore_replace("A1:A9").tolist()` | `[5.0, 5.0, 5.0, 5.0, 50.0, 5.0, 5.0, 5.0, 5.0]` |
| `zscore_replace([5, 5, 5, 5, 50, 5, 5, 5, 5], z=2).iloc[4]` | `5` |
| `zscore_replace([5, 5, 5, 5, 50, 5, 5, 5, 5]).iloc[4]` | `50` |
| `zscore_replace([50, 5, 5, 5, 5, 5, 5, 5, 5], z=2).iloc[0]` | `5` |
| `zscore_replace([5, 5, 5]).tolist()` | `[5.0, 5.0, 5.0]` |
| `zscore_replace([0, 100, 10], z=1, dates=["2020-01-01", "2020-01-02", "2020-01-11"]).iloc[1]` | `1` |
| `zscore_replace("A1:A9", 2).name` | `value` |
