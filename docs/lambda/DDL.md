# DDL

Dependent drop-down list. `DDL` reads a hierarchy table (one level per column) and returns the values for the **next** column given the parent selections. Use it as the source of a data-validation list.

Formula: `source/lambda/functions/DDL.lambda`

## Install

1. Formulas → **Name Manager** → New.
2. Name: `DDL`.
3. Refers to: paste the `=LAMBDA(...)` line from that file.
4. On a sheet: `=DDL(Table1)` or `=DDL($A$1:$C$100, $E$1)`.

## Arguments

| Argument | Required | Meaning |
|----------|----------|---------|
| `range` | Yes | Block or table of cascading categories. Column 1 is the top level, column 2 the next, and so on (up to 10 levels plus the return column). |
| `lookup1` … `lookup10` | No | Selected parent values, left to right. Omit all of them to return column 1 (the first drop-down). |

Do not put the delimiter `%^&&@` inside category text; that token joins keys internally.

## Behaviour

1. Parent lookups are concatenated with `%^&&@`. Empty omitted lookups are ignored when counting levels.
2. `levelIndex` is one past the last supplied parent, so that is the column to return.
3. If `lookup1` is omitted, `DDL` returns the whole of column 1 (top-level list). Duplicate top-level names are **not** uniqued; wrap with `UNIQUE` if the drop-down should show each value once.
4. Otherwise each row’s parent columns are joined the same way, and `XLOOKUP` takes the **first** matching row through the **last** matching row in the return column. Sort the table so identical parent paths are contiguous (`=DDLSorter(range)`).
5. The result spills. Point data validation at the spill (`#`) or wrap `UNIQUE(DDL(...))`.

## Example

| Category | Item | Variety |
|----------|------|---------|
| Fruit | Apple | Gala |
| Fruit | Apple | Fuji |
| Fruit | Orange | Navel |
| Veg | Carrot | Nantes |

Range `A2:C5`.

| Formula | Result |
|---------|--------|
| `=DDL(A2:C5)` | Fruit, Fruit, Fruit, Veg |
| `=UNIQUE(DDL(A2:C5))` | Fruit, Veg |
| `=DDL(A2:C5,"Fruit")` | Apple, Apple, Orange |
| `=DDL(A2:C5,"Fruit","Apple")` | Gala, Fuji |
| `=DDL(A2:C5,"Veg","Carrot")` | Nantes |

Data validation on `E2` (category): `=UNIQUE(DDL($A$2:$C$5))`.  
On `F2` (item): `=UNIQUE(DDL($A$2:$C$5,$E$2))`.  
On `G2` (variety): `=DDL($A$2:$C$5,$E$2,$F$2)`.

## Limits

- Up to 10 parent lookups (11 columns in `range` if you return the last column).
- Matching parents must be in a contiguous block (first-to-last `XLOOKUP`).
- Needs Microsoft 365 (`TEXTSPLIT`, `BYROW`, `EXPAND`, `CHOOSECOLS`, `XLOOKUP` search mode `-1`).
