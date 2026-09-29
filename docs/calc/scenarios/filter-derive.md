---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/exprs.py
  - packages/calc/src/pylibs_calc/compile/query.py
---

# Filter and derive

!!! question "The business question"
    *"Show me every holding the fund has outside US dollars, with its value in dollars and the
    upside our analysts see to their target price."*

`filter` keeps only the rows where a condition is true. `derive` adds columns computed from other columns, for this query only. A query with no `group_by` and no measures returns rows (a *row view*), and `select` picks which columns to return.

## Try it

=== "Python"

    ```python
    --8<-- "01_filter_derive.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("01_filter_derive.py"))
    ```

## Result

```python exec="on"
--8<-- "01_filter_derive.py"
```

## What to notice

- `mv_usd = round(price * quantity * fx_rate, 2)` is an **exact decimal**. `price` has 2 places and `fx_rate` 6, so the product has 8; `round(…, 2)` brings it back to cents.
- `upside_pct` has a `where`: it is computed only for rows with a target price (the equities), and is null for the bonds. Wayne Financial trades above its target, so its upside is negative.
- The whole formula language, including `x if cond else y`, is described in [Formula language](../concepts/formula-language.md).
- Derived columns can use earlier derived columns, and can be used by `select`, `sort`, measures and `having`.
- `filter` always runs first, whatever order you write the fields in. See [Order of evaluation](../concepts/evaluation-order.md).

## Gotchas

- A `filter` whose condition is **null** for a row (for example `yield > 0.03` where `yield` is null) drops that row, as SQL does.
- A derive with `where` can also take `otherwise`, the value for the other rows: `{"name": "bond_mv", "expr": "price * quantity", "where": "asset_class == 'Fixed Income'", "otherwise": "0"}`.
- `quantity > 0` keeps what the fund actually holds. Without it you would also get the securities that only the benchmark holds.
- Without `page`, a row view may return at most `Limits.max_unpaged_rows` rows (100,000 by default). Past that it is a `413 limit_exceeded`. See [Sort and page](sort-page.md).
