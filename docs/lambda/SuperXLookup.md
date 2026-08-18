# SuperXLookup

`XLOOKUP` that returns a **whole row** or a **whole column** from `return_array`.

- If `lookup_value` has **one column** (a cell or a column): `XMATCH` in `lookup_array` and return that **row**.
- If `lookup_value` has **more than one column** (a row): `XMATCH` in `lookup_array` and return that **column**.

A single cell is one column, so it is a row lookup. For a column lookup, pass a horizontal `lookup_value` (width > 1).

Formula: `source/lambda/functions/SuperXLookup.lambda`

## Install

1. Formulas → **Name Manager** → New.
2. Name: `SuperXLookup`.
3. Refers to: paste the `=LAMBDA(...)` line from that file.
4. On a sheet: `=SuperXLookup(G2,A2:A5,B2:D5)`.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `lookup_value` | Yes | Value to find. One column → return a row; two or more columns → return a column. |
| `lookup_array` | Yes | Labels to search (row headers for a row lookup, column headers for a column lookup). |
| `return_array` | Yes | Body whose matching row or column is returned. |
| `if_not_found` | No | Value if there is no match. Omitted → `#N/A`. |
| `match_mode` | No | Passed to `XMATCH` (default exact, `0`). |
| `search_mode` | No | Passed to `XMATCH` (default first-to-last, `1`). |

## Behaviour

Row lookup (`COLUMNS(lookup_value)=1`):

```
INDEX(return_array, XMATCH(...), SEQUENCE(1, COLUMNS(return_array)))
```

Column lookup:

```
INDEX(return_array, SEQUENCE(ROWS(return_array)), XMATCH(...))
```

If that errors, the formula returns `if_not_found`, or `NA()` when that argument is omitted.

## Example

|    | Jan | Feb | Mar |
|----|-----|-----|-----|
| North | 10 | 20 | 30 |
| South | 40 | 50 | 60 |

Row labels `A2:A3`, column labels `B1:D1`, body `B2:D3`.

| Formula | Result |
|---------|--------|
| `=SuperXLookup("South",A2:A3,B2:D3)` | `{40,50,60}` (South row) |
| `=SuperXLookup("East",A2:A3,B2:D3,"missing")` | `missing` |
| `=SuperXLookup("East",A2:A3,B2:D3)` | `#N/A` |

Column lookup: `lookup_value` must be wider than one column (for example a 1×2 range whose first cell is `Feb`). `lookup_array` is then `B1:D1`.

For a single cell at the intersection of a row and a column, use [DoubleXLookup](DoubleXLookup.md).

Needs Microsoft 365 (`XMATCH`).
