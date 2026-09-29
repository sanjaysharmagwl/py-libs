---
covers:
  - packages/calc_whatif/src/pylibs_calc_whatif/spec.py
  - packages/calc_whatif/src/pylibs_calc_whatif/polars.py
---

# Shock a column

!!! question "The business question"
    *"What if tech stocks fall 10% and bond yields rise 25 basis points? And separately, what if
    the dollar strengthens 5%: how much is the fund's foreign money worth then?"*

!!! info "What-if plugin"
    This feature comes from the [what-if plugin](../whatif/index.md) (`pylibs-calc-whatif`). Its
    steps go in a request's `extensions.whatif` block.

A **shock** changes a whole column at once, optionally only on the rows where a condition
holds. It is the building block of stress tests and sensitivities.

## Try it

=== "Python"

    ```python
    --8<-- "10_shock.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("10_shock.py"))
    ```

## Result

```python exec="on"
--8<-- "10_shock.py"
```

## What to notice

- **The first table** shows the two tech stocks 10% lower: Cyberdyne Systems 185.40 → **166.86**, and Initech 64.30 × 0.9 = 57.87. The `where` also names the asset class, so ACME, a tech company's *bond*, keeps its price.
- Every bond's yield is 25bp higher. Only the `price` and `yield` columns change, and no row is added or removed.
- Decimal results are rounded half-to-even back to 2 places: 98.50 × 1.05 would be 103.425, which becomes **103.42** (see [Numbers, types and nulls](../concepts/numbers-types-nulls.md)).
- **The second table** is a currency shock, run as a [compare](compare.md). A stronger dollar means each unit of a foreign currency buys fewer dollars, so the shock lowers `fx_rate` by 5% on every non-USD row. The fund loses 5% on its euro, sterling and yen holdings and nothing on its dollar holdings.

## The operations

| `op` | Effect | Example |
| --- | --- | --- |
| `add` | Adds `value` | `{"op": "add", "value": "0.0025"}`: +25bp on a yield |
| `mul` | Multiplies by `value` | `{"op": "mul", "value": "0.9"}`: −10% |
| `pct` | Moves by `value` percent | `{"op": "pct", "value": 5}`: ×1.05 |

`where` is any boolean formula. Rows where it is false **or null** are left alone.

## Gotchas

- **Decimal columns** are rounded half-to-even back to the column's scale after the shock, so a 2-decimal price stays 2-decimal.
- **Integer columns** (such as `quantity`) refuse a shock with a fractional result: `422 needs_rounding`. Add `"round": true` to round half-to-even instead. For example, 2,500 × 1.033 = 2,582.5 becomes 2,582.
- Shocks and overrides apply **in the order they are written**. A shock after an override moves the overridden value.
- Only **editable** columns can be shocked (`422 not_editable` otherwise).
