# Test: match_transactions

## Setup

1. Formulas → **Initialization** → paste `match_transactions` from `source/python-in-excel/functions/match_transactions.py` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.
2. Optional grid: headers `Date`, `Description`, `Value` in `A1:C1` and `E1:G1` for two tables.

## Cases

In a PY cell, set output to **Excel value**.

```python
df1 = pd.DataFrame({
    "Date": [pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-02"), None, pd.Timestamp("2024-01-04")],
    "Description": ["Rent", "Amazon UK", "Coffee", "Only df1"],
    "Value": [100.0, 25.0, 5.0, 40.0],
    "Extra": [1, 2, 3, 4],
})
df2 = pd.DataFrame({
    "DATE": [pd.Timestamp("2024-01-01"), pd.Timestamp("2024-01-02"), pd.Timestamp("2024-01-03"), pd.Timestamp("2024-01-05")],
    "description": ["rent", "Amazon UK Ltd", "Coffee", "Only df2"],
    "VALUE": [100.0, 25.0, 5.01, 99.0],
    "Notes": ["a", "b", "c", "d"],
})
out = match_transactions(df1, df2)
sm = match_transactions(df1, df2, summary=True)
```

### Shape, columns, and pairing

| Python | Expected |
|--------|----------|
| `list(out.columns)` | `['df1_date', 'df1_description', 'df1_value', 'df2_date', 'df2_description', 'df2_value', 'Difference', 'match_details', 'match_group']` |
| `out.shape` | `(5, 9)` |
| `list([s.split(";")[0] for s in out["match_details"]])` | `['Exact match', 'Approximate match (description)', 'Approximate match (value)', 'Exists only in df1', 'Exists only in df2']` |
| `list(out["match_group"])` | `['Matched', 'Matched', 'Matched', 'Unmatched', 'Unmatched']` |
| `out.loc[out["df1_description"]=="Rent", "df2_description"].iloc[0]` | `rent` |
| `float(out.loc[out["df1_description"]=="Rent", "Difference"].iloc[0])` | `0.0` |
| `out.loc[out["df1_description"]=="Amazon UK", "match_details"].iloc[0].startswith("Approximate match (description);")` | `True` |
| `"(tol 0.8)" in out.loc[out["df1_description"]=="Amazon UK", "match_details"].iloc[0]` | `True` |
| `out.loc[out["df1_description"]=="Coffee", "match_details"].iloc[0]` | `Approximate match (value); desc 1 (tol 0.8)` |
| `round(float(out.loc[out["df1_description"]=="Coffee", "Difference"].iloc[0]), 4)` | `-0.01` |
| `out.loc[out["df1_description"]=="Only df1", "match_details"].iloc[0]` | `Exists only in df1` |
| `float(out.loc[out["df1_description"]=="Only df1", "df2_value"].iloc[0])` | `0.0` |
| `float(out.loc[out["df1_description"]=="Only df1", "Difference"].iloc[0])` | `40.0` |
| `out.loc[out["df2_description"]=="Only df2", "match_details"].iloc[0]` | `Exists only in df2` |
| `float(out.loc[out["df2_description"]=="Only df2", "df1_value"].iloc[0])` | `0.0` |
| `float(out.loc[out["df2_description"]=="Only df2", "Difference"].iloc[0])` | `-99.0` |

### Missing dates, missing values, and Difference

| Python | Expected |
|--------|----------|
| `out.loc[out["df1_description"]=="Coffee", "df1_date"].iloc[0] is None` | `True` |
| `any(v is pd.NaT for v in out["df1_date"])` | `False` |
| `float(match_transactions(pd.DataFrame({"date": ["2024-01-01"], "description": ["X"], "value": [None]}), pd.DataFrame({"date": ["2024-01-02"], "description": ["Y"], "value": [10]}))["df1_value"].iloc[0])` | `0.0` |
| `float(match_transactions(pd.DataFrame({"Date": ["2024-01-01"], "Description": ["Fee"], "Value": [10]}), pd.DataFrame({"Date": ["2024-01-01"], "Description": ["Fee"], "Value": [0]}), value_tol=10)["Difference"].iloc[0])` | `10.0` |
| `match_transactions(pd.DataFrame({"Date": ["2024-01-01"], "Description": ["Fee"], "Value": [10]}), pd.DataFrame({"Date": ["2024-01-01"], "Description": ["Fee"], "Value": [0]}), value_tol=10)["match_details"].iloc[0]` | `Approximate match (value); desc 1 (tol 0.8)` |

### Summary totals

| Python | Expected |
|--------|----------|
| `list(sm.columns)` | `['match_group', 'match_details', 'count', 'df1_value', 'df2_value', 'Difference']` |
| `list(sm["match_details"])` | `['Exact match', 'Approximate match (description)', 'Approximate match (value)', 'Total', 'Exists only in df1', 'Exists only in df2', 'Total']` |
| `float(sm.loc[(sm["match_group"]=="Matched") & (sm["match_details"]=="Total"), "count"].iloc[0])` | `3.0` |
| `float(sm.loc[(sm["match_group"]=="Matched") & (sm["match_details"]=="Total"), "df1_value"].iloc[0])` | `130.0` |
| `round(float(sm.loc[(sm["match_group"]=="Matched") & (sm["match_details"]=="Total"), "df2_value"].iloc[0]), 4)` | `130.01` |
| `round(float(sm.loc[(sm["match_group"]=="Matched") & (sm["match_details"]=="Total"), "Difference"].iloc[0]), 4)` | `-0.01` |
| `float(sm.loc[(sm["match_group"]=="Unmatched") & (sm["match_details"]=="Total"), "count"].iloc[0])` | `2.0` |
| `float(sm.loc[(sm["match_group"]=="Unmatched") & (sm["match_details"]=="Total"), "df1_value"].iloc[0])` | `40.0` |
| `float(sm.loc[(sm["match_group"]=="Unmatched") & (sm["match_details"]=="Total"), "df2_value"].iloc[0])` | `99.0` |
| `float(sm.loc[(sm["match_group"]=="Unmatched") & (sm["match_details"]=="Total"), "Difference"].iloc[0])` | `-59.0` |

### Approximate both and errors

| Python | Expected |
|--------|----------|
| `match_transactions(pd.DataFrame({"date": ["2024-01-01"], "description": ["Amazon UK"], "value": [10.0]}), pd.DataFrame({"date": ["2024-01-01"], "description": ["Amazon UK Ltd"], "value": [10.01]}))["match_details"].iloc[0].startswith("Approximate match (value and description);")` | `True` |
| `match_transactions(pd.DataFrame({"a": [1], "b": [2], "c": [3]}), df2)` | `#PYTHON!` — `Column 'Date' not found.` |
| `match_transactions(pd.DataFrame({"TranDate": ["2024-01-01"], "Narrative": ["Rent"], "Amount": [100.0]}), pd.DataFrame({"TranDate": ["2024-01-01"], "Narrative": ["rent"], "Amount": [100.0]}), date_col="TranDate", description_col="Narrative", value_col="Amount")["match_details"].iloc[0]` | `Exact match` |
| `match_transactions(df1, df2, value_tol=-1)` | `#PYTHON!` — `value_tol must be >= 0.` |
| `match_transactions(df1, df2, desc_tol=1.5)` | `#PYTHON!` — `desc_tol must be in [0, 1].` |
