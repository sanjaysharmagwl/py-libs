---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/logical.py
---

# Filtered measures

!!! question "The business question"
    *"In each region, how much of the fund is in equities, how much in bonds and how much in
    cash?"*

Any measure can take a `where`, which narrows the rows **that measure** sees without changing which groups exist. It works like SQL's `SUM(x) FILTER (WHERE ...)`, and it saves you from running three queries and joining them.

## Try it

=== "Python"

    ```python
    --8<-- "03_filtered_measures.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("03_filtered_measures.py"))
    ```

## Result

```python exec="on"
--8<-- "03_filtered_measures.py"
```

## What to notice

- The fund holds no bonds in **Japan** (it is underweight the JGB), so `bonds` is **null** there (a sum over no rows), not 0. Only North America has cash.
- `equity + bonds + cash = fund` on every row, counting a null as nothing. The groups are the same for all four measures.
- A query-level `filter` would have removed rows for **every** measure. A measure's `where` removes them for that measure only. The same trick puts the fund and its benchmark side by side; see [Weights and active weights](weights.md).

## Gotchas

- `where` is evaluated per row **before** aggregation. To filter groups by an aggregated value, use [`having`](having.md).
