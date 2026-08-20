# Test: describe

## Setup

1. Formulas → **Initialization** → paste `describe` from `source/python-in-excel/functions/describe.py` after the default imports → Save.
2. Put `10`, `12`, `14` in `A2:A4` with header `Value` in `A1`.

## Cases

In a PY cell, set output to **Excel value**.

| Python | Expected |
|--------|----------|
| `describe("A1:A4").loc["count", "Value"]` | `3` |
| `describe("A1:A4").loc["mean", "Value"]` | `12` |
| `describe("A1:A4").loc["min", "Value"]` | `10` |
| `describe("A1:A4").loc["max", "Value"]` | `14` |
