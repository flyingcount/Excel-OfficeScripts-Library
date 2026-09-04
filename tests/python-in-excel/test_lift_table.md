# Test: lift_table

## Setup

1. Formulas → **Initialization** → paste `lift_table` from `source/python-in-excel/functions/lift_table.py` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.
2. Headers `churn`, `proba` in `A1:B1`.
3. Rows in `A2:B11`: actual `1,1,0,1,0,0,1,0,0,0` and scores `0.95,0.90,0.80,0.70,0.60,0.50,0.40,0.30,0.20,0.10`.

n=10, positives=4, base rate=0.4. Default `bins=10`. With `bins=5`, bin 1 is the top 20%: 2 positives, `cum_gain` 0.5, `cum_lift` 2.5.

## Cases

In a PY cell, set output to **Excel value** for the table. Leave `plot=True` as a **Python object**.

```python
df = pd.DataFrame({
    "churn": [1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
    "proba": [0.95, 0.90, 0.80, 0.70, 0.60, 0.50, 0.40, 0.30, 0.20, 0.10],
})
```

| Python | Expected |
|--------|----------|
| `list(lift_table("A1:B11").columns)` | `['bin', 'n', 'positives', 'response_rate', 'lift', 'cum_n', 'cum_positives', 'cum_pct', 'cum_gain', 'cum_lift', 'min_proba', 'max_proba']` |
| `lift_table("A1:B11").shape` | `(10, 12)` |
| `float(lift_table("A1:B11")["bin"].iloc[0])` | `1.0` |
| `float(lift_table("A1:B11").set_index("bin").loc[2, "cum_pct"])` | `0.2` |
| `float(lift_table("A1:B11").set_index("bin").loc[2, "cum_gain"])` | `0.5` |
| `float(lift_table("A1:B11").set_index("bin").loc[2, "cum_lift"])` | `2.5` |
| `float(lift_table(df, "churn", "proba", bins=5).shape[0])` | `5.0` |
| `float(lift_table(df, bins=5).set_index("bin").loc[1, "n"])` | `2.0` |
| `float(lift_table(df, bins=5).set_index("bin").loc[1, "positives"])` | `2.0` |
| `float(lift_table(df, bins=5).set_index("bin").loc[1, "response_rate"])` | `1.0` |
| `float(lift_table(df, bins=5).set_index("bin").loc[1, "lift"])` | `2.5` |
| `float(lift_table(df, bins=5).set_index("bin").loc[1, "cum_gain"])` | `0.5` |
| `float(lift_table(df, bins=5).set_index("bin").loc[1, "min_proba"])` | `0.9` |
| `float(lift_table(df, bins=5).set_index("bin").loc[5, "cum_gain"])` | `1.0` |
| `float(lift_table(df, bins=5).set_index("bin").loc[5, "cum_lift"])` | `1.0` |
| `lift_table(df, bins=1)` | `#PYTHON!` — `bins must be >= 2.` |
| `lift_table(df, bins=20)` | `#PYTHON!` — `Need at least as many rows as bins.` |
| `lift_table(pd.DataFrame({"a": [0, 0, 0], "b": [0.9, 0.5, 0.1]}))` | `#PYTHON!` — `Need at least 1 positive case.` |

### Plot (`plot=True`, leave as **Python object**)

| Python | Expected |
|--------|----------|
| `type(lift_table(df, plot=True)).__name__` | `Figure` |
| `len(lift_table(df, plot=True).axes)` | `2` |
| `lift_table(df, plot=True).axes[0].get_title()` | `Cumulative gain and lift` |
