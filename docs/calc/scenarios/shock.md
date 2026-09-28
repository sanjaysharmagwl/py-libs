---
covers:
  - packages/calc_whatif/src/pylibs_calc_whatif/spec.py
  - packages/calc_whatif/src/pylibs_calc_whatif/polars.py
---

# Shock a column

!!! question "The business question"
    *"What happens to my bond book if Tech names rally 5% and yields rise 25 basis points
    across the board?"*

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

- ACME (97.25) and Initech (102.10) are the two Tech bonds. Their prices move by 5%: 97.25 × 1.05 = 102.1125, which rounds to **102.11**.
- 102.10 × 1.05 = 107.205, which rounds to **107.20**. The rounding is half-to-even, so an exact half rounds to the even digit (see [Numbers, types and nulls](../concepts/numbers-types-nulls.md)).
- Every yield is 25bp higher. Only the `price` and `yield` columns change, and no row is added or removed.

## The operations

| `op` | Effect | Example |
| --- | --- | --- |
| `add` | Adds `value` | `{"op": "add", "value": "0.0025"}`: +25bp on a yield |
| `mul` | Multiplies by `value` | `{"op": "mul", "value": "0.9"}`: −10% |
| `pct` | Moves by `value` percent | `{"op": "pct", "value": 5}`: ×1.05 |

`where` is any boolean formula. Rows where it is false **or null** are left alone.

## Gotchas

- **Decimal columns** are rounded half-to-even back to the column's scale after the shock, so a 2-decimal price stays 2-decimal.
- **Integer columns** (such as `quantity`) refuse a shock with a fractional result: `422 needs_rounding`. Add `"round": true` to round half-to-even instead. For example, −500 × 1.033 = −516.5 becomes −516.
- Shocks and overrides apply **in the order they are written**. A shock after an override moves the overridden value.
- Only **editable** columns can be shocked (`422 not_editable` otherwise).
