---
covers:
  - packages/calc/src/pylibs_calc/spec/scenario.py
  - packages/calc/src/pylibs_calc/compile/mutations.py
---

# Override a cell

!!! question "The business question"
    *"The mark on ACME is stale: it should be 95.00. And Globex was just downgraded to B. What
    does my Credit book look like now?"*

An **override** sets individual cells, found by the row's key. It is how a trader's manual edit in a grid gets into the calculation.

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

- **Only the two edited cells change.** Initech is untouched.
- The edit is part of `what_if`, so it applies to **this request only**. To keep it and share it, put it in a [saved scenario](saved-scenarios.md).
- `value` is given as the **string** `"95.00"`, so it stays an exact decimal. A JSON number would work too, but strings avoid any float rounding on the way in.
- `key` needs a value for every key column of the dataset (here only `position_id`).

## Gotchas

- An edit whose key matches no row is an error, `422 unmatched_edits`, so a typo can't silently do nothing. Set `"options": {"strict_edits": false}` to allow it; the unmatched keys are then listed in `meta.unmatched_edits`.
- Within one override step, the last edit of the same cell wins.
- Overrides and shocks may only change columns the dataset registered as **editable** (default: every non-key column). Key columns can never be changed. Anything else is a `422 not_editable`. See [Datasets and the catalog](../concepts/datasets.md).
