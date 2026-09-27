---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/query.py
---

# Having

!!! question "The business question"
    *"Which desks have a gross exposure over their limit of 400,000?"*

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
    ```

## Result

```python exec="on"
--8<-- "05_having.py"
```

## What to notice

- The derived column `gross` and the measure `gross` have the same name. In `having`, `gross` means **the measure**.
- The sort puts the biggest breach first.

## Gotchas

- `having` can't be combined with `pivot` yet.
- With `rollup`, `having` is checked on every row, subtotals included. The subtotals are still computed from **all** the rows beneath them, not only from the groups that pass `having`.
