---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/logical.py
---

# Filtered measures

!!! question "The business question"
    *"Per desk, how much of my notional is long, how much is short, and what is the net?"*

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

- **Commodities** has no short positions, so `short` is **null** there (a sum over no rows), not 0.
- `long + short = net` on every row where both exist. The groups are the same for all three measures.
- A query-level `filter` would have removed rows for **every** measure. A measure's `where` removes them for that measure only.

## Gotchas

- `where` is evaluated per row **before** aggregation. To filter groups by an aggregated value, use [`having`](having.md).
