---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/exprs.py
  - packages/calc/src/pylibs_calc/compile/query.py
---

# Filter and derive

!!! question "The business question"
    *"Show me every EMEA position, with its notional and whether it is long or short."*

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

- `notional = price * quantity` is an **exact decimal**: 2 decimal places from `price`, times an integer, gives 2 places.
- `'long' if quantity > 0 else 'short'` is the formula language's conditional. The whole language is described in [Formula language](../concepts/formula-language.md).
- Derived columns can use earlier derived columns, and can be used by `select`, `sort`, measures and `having`.
- `filter` always runs first, whatever order you write the fields in. See [Order of evaluation](../concepts/evaluation-order.md).

## Gotchas

- A `filter` whose condition is **null** for a row (for example `yield > 0.03` where `yield` is null) drops that row, as SQL does.
- A derive can take `where` and `otherwise`: `{"name": "hedge", "expr": "quantity", "where": "desk == 'Rates'", "otherwise": "0"}`.
- Without `page`, a row view may return at most `Limits.max_unpaged_rows` rows (100,000 by default). Past that it is a `413 limit_exceeded`. See [Sort and page](sort-page.md).
