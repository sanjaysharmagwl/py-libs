---
covers:
  - packages/calc/src/pylibs_calc/compile/query.py
  - packages/calc/src/pylibs_calc/compile/logical.py
---

# Subtotals (rollup)

!!! question "The business question"
    *"Give me the book total, a subtotal per region, and each desk within each region, in one
    grid."*

`"rollup": true` adds a subtotal row for every prefix of `group_by`, plus a grand total. It is the result a grouped grid or a P&L explain needs.

## Try it

=== "Python"

    ```python
    --8<-- "06_rollup.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("06_rollup.py"))
    ```

## Result

```python exec="on"
--8<-- "06_rollup.py"
```

## What to notice

- **`__level`** says which row is which: `0` is the grand total, `1` a region subtotal, and `2` a region-and-desk detail row. The columns grouped away at a level are null.
- **Subtotal rows sort right after their details**, so the result reads top to bottom like an indented report.
- **Every level is computed from the base rows**, not by adding up the rows above it. Counts, `mean`, `count_distinct`, `wavg` and [`post` ratios](post-ratios.md) are therefore correct at every level.
- The grand total, **−6,685,077.50**, is dominated by the short USD/JPY forward in APAC.

## Gotchas

- `rollup` needs `group_by`.
- A group whose own value is null (for example a position with no desk) also shows null in that column. Use `__level`, not the nulls, to tell subtotals apart from details.
- Sorting a rollup by a measure is not supported yet. Sort by the group columns.
