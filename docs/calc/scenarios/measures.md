---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/logical.py
  - packages/calc/src/pylibs_calc/compile/query.py
---

# Measures

!!! question "The business question"
    *"For each desk: what is the net notional, how many positions are there, and what is the
    exposure-weighted yield?"*

`group_by` splits the rows into groups, and each **measure** aggregates one value per group.

## Try it

=== "Python"

    ```python
    --8<-- "02_measures.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("02_measures.py"))
    ```

## Result

```python exec="on"
--8<-- "02_measures.py"
```

## The measure functions

| `fn` | Meaning | Needs |
| --- | --- | --- |
| `sum` | Sum of non-null values. **Null when there is nothing to sum**, as in SQL | `of` |
| `mean` | `sum / count` of non-null values | `of` |
| `min`, `max` | Smallest and largest. Also work for strings and dates | `of` |
| `count` | Non-null values | `of` |
| `count_rows` | Rows in the group, whatever their values | — |
| `count_distinct` | Distinct non-null values | `of` |
| `wavg` | `sum(of × weight) / sum(weight)` over rows where both are present | `of`, `weight` |

`of` and `weight` are formulas, not just column names. `{"fn": "sum", "of": "price * quantity"}` works without a separate `derive`.

Plugins can add more `fn`s, such as a median or a VaR quantile (see [`AggregateDef`](../concepts/plugins.md#functions-and-aggregates)). They take `of`, and are recomputed from the rows at every subtotal level, like the built-ins.

## What to notice

- **Equities, FX and Commodities** have no yields, so `with_yield` is 0 and `wavg_yield` is null. There is no fake zero.
- **`wavg_yield`** for Credit weights each bond's yield by the absolute size of its position. `float(notional)` converts the exact decimal to a float, because `yield` is a float (see [Numbers, types and nulls](../concepts/numbers-types-nulls.md)).
- **`avg_price`** is a decimal at the division scale (10 places by default).
- **Without `group_by`**, measures give one row for the whole book.

## Gotchas

- `sum` over only nulls is **null**, not 0. Wrap it, `coalesce(...)`, in a `post` expression if you want a 0.
- An average of averages is wrong. For ratios such as the average price, use [Ratios after aggregation](post-ratios.md), which are always computed from sums.
