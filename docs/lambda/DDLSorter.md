# DDL Sorter

Sorts a hierarchy table by **every column from left to right**, so identical parent paths sit in one block. `DDL` needs that for first-to-last `XLOOKUP`.

The Excel defined name is **`DDLSorter`** (no space). Display name: DDL Sorter.

Formula: `source/lambda/functions/DDLSorter.lambda`

## Install

1. Formulas → **Name Manager** → New.
2. Name: `DDLSorter`.
3. Refers to: paste the `=LAMBDA(...)` line from that file.
4. On a sheet: `=DDLSorter(A2:C20)` or `=DDL(DDLSorter(A2:C20),"Fruit")`.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `Range` | Yes | Hierarchy block (same shape `DDL` expects). |
| `SortOrder` | No | Passed through to `SORT`. `1` (or omitted, Excel default) is ascending; `-1` is descending. An array of `1`/`-1` can set the order per column. |

## Behaviour

`SORT(Range, SEQUENCE(, COLUMNS(Range)), SortOrder)` uses columns `1, 2, …, n` as sort keys, so it sorts by column 1, then 2, then 3, and so on.

The result spills. Feed that spill into `DDL`, or store it as the source table.

## Example

Unsorted:

| Category | Item | Variety |
|----------|------|---------|
| Fruit | Orange | Navel |
| Veg | Carrot | Nantes |
| Fruit | Apple | Fuji |
| Fruit | Apple | Gala |

`=DDLSorter(A2:C5)`:

| Category | Item | Variety |
|----------|------|---------|
| Fruit | Apple | Fuji |
| Fruit | Apple | Gala |
| Fruit | Orange | Navel |
| Veg | Carrot | Nantes |

Then `=DDL(DDLSorter(A2:C5),"Fruit","Apple")` returns Fuji, Gala.

Descending: `=DDLSorter(A2:C5,-1)`.

## See also

- [DDL](DDL.md)
