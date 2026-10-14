# match_transactions

Match **transaction rows** between two tables on **description** and **value**. Each row from `df1` and `df2` is used at most once (1:1). Extra columns are ignored. Date is shown on the result but is not used to pair rows.

Formula: `source/python-in-excel/functions/match_transactions.py`

## Install

Formulas → **Initialization** → paste the `def` after the default imports → Save. Or paste `init/PaulPythonLibrary.py`.

In a PY cell (output **Excel value**):

```python
match_transactions("Table1[#All]", "Table2[#All]")
match_transactions(df1, df2, date_col="TranDate", description_col="Narrative", value_col="Amount")
match_transactions(df1, df2, summary=True)
```

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `df1` | Yes | First table/range, DataFrame, or `xl()` result. |
| `df2` | Yes | Second table/range, DataFrame, or `xl()` result. |
| `date_col` | No | Date column header. Default `'Date'`. |
| `description_col` | No | Description column header. Default `'Description'`. |
| `value_col` | No | Value column header. Default `'Value'`. |
| `value_tol` | No | Max \|df1_value − df2_value\| for an approximate value match. Default `0.01`. |
| `desc_tol` | No | Minimum `difflib` ratio (0 to 1) for an approximate description match. Default `0.8`. |
| `summary` | No | `False` (default) spills one row per transaction. `True` spills grouped totals. |
| `headers` | No | First row is headers when a ref string is used. Default `True`. |

Column names are **case-insensitive** (`Date` finds `DATE` / `date`). Same header names are used on both tables. Other columns are ignored. Blank values become `0`. Excel 1×1 arrays for the options are unwrapped.

Set `desc_tol=0` to pair on value only. Raise `value_tol` to pair on description when amounts differ more.

## How rows are paired

Greedy 1:1, best remaining partner first:

1. **Exact match** — normalized description equal and \|value diff\| ≤ 1e-9. Descriptions are compared after `casefold` and collapsing whitespace (`Rent` = `rent`).
2. **Approximate match (description)** — similar description (ratio ≥ `desc_tol`) and exact value.
3. **Approximate match (value)** — exact description and \|value diff\| ≤ `value_tol`.
4. **Approximate match (value and description)** — similar description and close value.
5. Leftovers from **both** tables: **Exists only in df1** and **Exists only in df2**.

## Result (detail)

Set the PY cell to **Excel value**. One row per `df1` row plus unmatched `df2` rows.

| Column | Notes |
|--------|-------|
| `df1_date`, `df2_date` | Parsed dates. Missing dates are Python `None` (blank in Excel), not `#NUM!`. |
| `df1_description`, `df2_description` | Original text. `None` on the empty side. |
| `df1_value`, `df2_value` | Numeric; blanks filled with `0`. |
| `Difference` | `df1_value - df2_value` on every row (unmatched df2 rows are `0 - df2_value`). |
| `match_details` | Exact / unmatched labels, or approximate plus `desc` similarity (`tol` is `desc_tol`). Amount gap is in `Difference`. |
| `match_group` | `Matched` or `Unmatched`. |

## Result (summary)

Approximate `match_details` include the description ratio, for example `Approximate match (value); desc 1 (tol 0.8)`. The amount gap is in `Difference`. `summary=True` still groups by the match type (the text before the first `;`).

## Example

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
})
match_transactions(df1, df2)
```

`Rent`/`rent` is an exact match. `Amazon UK` vs `Amazon UK Ltd` is an approximate description match. `Coffee` 5.00 vs 5.01 is an approximate value match. `Only df1` / `Only df2` exist on one side. The Coffee row’s missing `df1` date is `None`.
