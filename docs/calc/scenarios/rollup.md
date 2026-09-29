---
covers:
  - packages/calc/src/pylibs_calc/compile/query.py
  - packages/calc/src/pylibs_calc/compile/logical.py
---

# Subtotals (rollup)

!!! question "The business question"
    *"Give me the fund's weight in each asset class, and in each sector within it, with the fund
    total, in one grid."*

`"rollup": true` adds a subtotal row for every prefix of `group_by`, plus a grand total. It is the result a grouped grid or a factsheet breakdown needs.

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

- **`__level`** says which row is which: `0` is the whole fund, `1` an asset class subtotal, and `2` an asset-class-and-sector detail row. The columns grouped away at a level are null.
- **Subtotal rows sort right after their details**, so the result reads top to bottom like an indented report.
- **Every level is computed from the base rows**, not by adding up the rows above it. Counts, `mean`, `count_distinct`, `wavg` and [`post` ratios](post-ratios.md) are therefore correct at every level.
- **Weights work at every level.** `total(mv)` is always the whole fund, so each subtotal's `weight_pct` is its share of the fund: equities are 50.73% of it, and the grand total is 100%.
- Information Technology appears twice: as an equity (Cyberdyne Systems) and as a corporate bond (ACME Corp). Group by `sector` alone to see the fund's total tech exposure.

## Gotchas

- `rollup` needs `group_by`.
- A group whose own value is null (for example a holding with no sector) also shows null in that column. Use `__level`, not the nulls, to tell subtotals apart from details.
- Sorting a rollup by a measure is not supported yet. Sort by the group columns.
