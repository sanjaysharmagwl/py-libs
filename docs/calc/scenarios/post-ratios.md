---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/logical.py
---

# Ratios after aggregation

!!! question "The business question"
    *"How much upside do our analysts see in the fund's equities in each region, if every stock
    reached its target price?"*

`post` computes values from the **measures** after aggregation. Use it for ratios, spreads, percentages and [weights](weights.md).

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

- `upside_pct = target_mv / mv − 1` is a **ratio of sums**: the value at target prices over today's value. Each stock counts in proportion to how much the fund holds, which is the upside a PM would actually capture.
- `avg_upside_pct` is the plain mean of each stock's upside, and it is different wherever a region has more than one stock. In North America it is about 12.01% against 12.18%, because Stark Industries (a larger holding) has less upside than Umbrella Health.
- The UK's upside is negative: the fund's one UK stock, Wayne Financial, trades above its target.
- A `post` expression can refer to measures, to group columns and to earlier `post` values.

!!! info "Why a ratio of sums matters"
    With [subtotals](rollup.md), a `post` expression is recomputed **at every level** from that level's sums. The fund-level upside is total target value over total value, never an average of the regional upsides. `wavg` works the same way.

## Gotchas

- Division by zero gives **null**, not an error or infinity.
- `post` sees one group at a time. To divide by the whole fund, for a weight, use [`total()`](weights.md).
- Divisions are exact decimals at `NumericConfig.division_scale` places (10 by default).
