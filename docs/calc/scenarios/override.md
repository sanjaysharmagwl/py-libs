---
covers:
  - packages/calc_whatif/src/pylibs_calc_whatif/spec.py
  - packages/calc_whatif/src/pylibs_calc_whatif/polars.py
---

# Override a cell

!!! question "The business question"
    *"Globex's bond hasn't traded for weeks and the quoted price of 88.40 is stale. Our credit
    analyst thinks 80.00 is fair, and the issuer was just downgraded to B. What do the fund's bonds
    look like now?"*

!!! info "What-if plugin"
    This feature comes from the [what-if plugin](../whatif/index.md) (`pylibs-calc-whatif`). Its
    steps go in a request's `extensions.whatif` block.

An **override** sets individual cells, found by the row's key. It is how an analyst's or a PM's manual edit in a grid gets into the calculation: a price for an illiquid bond, a new rating, or a trade the PM is considering (a new `quantity`).

## Try it

=== "Python"

    ```python
    --8<-- "09_override.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("09_override.py"))
    ```

## Result

```python exec="on"
--8<-- "09_override.py"
```

## What to notice

- **Only the two edited cells change.** ACME and the government bonds are untouched.
- Everything computed from the price follows: Globex's market value, its weight, the fund's NAV and every other holding's weight. Run a [compare](compare.md) with the same `extensions` to see the change next to the base.
- The edit is in the request's `extensions.whatif.steps`, so it applies to **this request only**. To keep it and share it, put it in a [saved scenario](saved-scenarios.md).
- `value` is given as the **string** `"80.00"`, so it stays an exact decimal. A JSON number would work too, but strings avoid any float rounding on the way in.
- `key` needs a value for every key column of the dataset (here only `security_id`).

## Gotchas

- An edit whose key matches no row is an error, `422 unmatched_edits`, so a typo can't silently do nothing. Set `"strict_edits": false` in the `whatif` block to allow it; the unmatched keys are then listed in `meta.extensions.whatif.unmatched_edits`.
- Within one override step, the last edit of the same cell wins.
- Overrides and shocks may only change columns the dataset registered as **editable** (default: every non-key column). Key columns can never be changed. Anything else is a `422 not_editable`. See [Datasets and the catalog](../concepts/datasets.md).
