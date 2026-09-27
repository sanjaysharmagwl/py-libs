---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/logical.py
---

# Ratios after aggregation

!!! question "The business question"
    *"What is the average price of my Rates and Credit bonds in each region, and how net is each
    region (net notional over gross)?"*

`post` computes values from the **measures** after aggregation. Use it for ratios, spreads and percentages.

## Try it

=== "Python"

    ```python
    --8<-- "04_post_ratios.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("04_post_ratios.py"))
    ```

## Result

```python exec="on"
--8<-- "04_post_ratios.py"
```

## What to notice

- `avg_px = notional / quantity` is a **ratio of sums**: total notional over total quantity. It is not the mean of the prices. In AMER, 145,670 / 1,500 = 97.113…
- `net_to_gross` is 1 in APAC because the only position there is long.
- A `post` expression can refer to measures, to group columns and to earlier `post` values.

!!! info "Why a ratio of sums matters"
    With [subtotals](rollup.md), a `post` expression is recomputed **at every level** from that level's sums. The book-level average price is total notional over total quantity, never an average of the regional averages. `wavg` works the same way.

## Gotchas

- Division by zero gives **null**, not an error or infinity.
- Divisions are exact decimals at `NumericConfig.division_scale` places (10 by default).
