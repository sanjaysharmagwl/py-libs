---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/query.py
---

# Having

!!! question "The business question"
    *"Which holdings are above our 10% concentration limit? And which sectors are more than 5
    points away from the benchmark?"*

`having` filters **groups** after aggregation, using the measures and `post` values, as SQL's `HAVING` does.

## Try it

=== "Python"

    ```python
    --8<-- "05_having.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("05_having.py"))
    print(curl("05_having.py", name="ACTIVE_REQUEST"))
    ```

## Result

```python exec="on"
--8<-- "05_having.py"
```

## What to notice

- The first table is a **concentration check**. Rules such as "no single holding above 10% of the fund" are common in fund regulation and in investment guidelines. Two holdings breach it here.
- The second table is an **active-weight check**: the sectors where the fund is more than 5 points over- or underweight its benchmark. Information Technology is 15 points underweight.
- `having` can use `post` values such as `weight_pct`, and `total()` directly: `"having": "mv > total(mv) / 10"` is the same concentration check.
- **The denominator doesn't shrink.** `total()` is computed before `having` removes groups, so a weight is always a share of the whole fund, not of the groups that pass.
- The derived column `mv` and the measure `mv` have the same name. In `having`, `mv` means **the measure**.

## Gotchas

- `having` can't be combined with `pivot` yet.
- With `rollup`, `having` is checked on every row, subtotals included. The subtotals are still computed from **all** the rows beneath them, not only from the groups that pass `having`.
