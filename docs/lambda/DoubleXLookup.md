# DoubleXLookup

Two-way lookup. Finds the **row** with `XMATCH` on a vertical array, the **column** with `XMATCH` on a horizontal array, then `INDEX` into the body.

Formula: `source/lambda/functions/DoubleXLookup.lambda`

## Install

1. Formulas → **Name Manager** → New.
2. Name: `DoubleXLookup`.
3. Refers to: paste the `=LAMBDA(...)` line from that file.
4. On a sheet: `=DoubleXLookup(G2,A2:A5,H2,B1:D1,B2:D5)`.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `vlookup_value` | Yes | Value to find in the row headers. |
| `vlookup_array` | Yes | Vertical (row-header) range. One column, same height as `return_array`. |
| `hlookup_value` | Yes | Value to find in the column headers. |
| `hlookup_array` | Yes | Horizontal (column-header) range. One row, same width as `return_array`. |
| `return_array` | Yes | Body to return a cell from. |
| `if_not_found` | No | Value if either match fails. Omitted → `#N/A`. |
| `vmatch_mode` | No | Passed to row `XMATCH` (default exact, `0`). |
| `vsearch_mode` | No | Passed to row `XMATCH` (default first-to-last, `1`). |
| `hmatch_mode` | No | Passed to column `XMATCH`. |
| `hsearch_mode` | No | Passed to column `XMATCH`. |

## Behaviour

```
INDEX(
  return_array,
  XMATCH(vlookup_value, vlookup_array, vmatch_mode, vsearch_mode),
  XMATCH(hlookup_value, hlookup_array, hmatch_mode, hsearch_mode)
)
```

If that errors, the formula returns `if_not_found`, or `NA()` when that argument is omitted.

## Example

|    | Jan | Feb | Mar |
|----|-----|-----|-----|
| North | 10 | 20 | 30 |
| South | 40 | 50 | 60 |

Row headers `A2:A3`, column headers `B1:D1`, body `B2:D3`.

| Formula | Result |
|---------|--------|
| `=DoubleXLookup("South",A2:A3,"Feb",B1:D1,B2:D3)` | `50` |
| `=DoubleXLookup("East",A2:A3,"Feb",B1:D1,B2:D3,"missing")` | `missing` |
| `=DoubleXLookup("East",A2:A3,"Feb",B1:D1,B2:D3)` | `#N/A` |

For a whole matching row or column, use [SuperXLookup](SuperXLookup.md).

Needs Microsoft 365 (`XMATCH`).
