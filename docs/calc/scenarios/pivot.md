---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/compile/query.py
---

# Pivot

!!! question "The business question"
    *"Show desks down the side, regions across the top, and net notional in the cells, with a
    total per desk."*

`pivot` spreads the measures across one column per value (or combination of values) of the `on` columns.

## Try it

=== "Python"

    ```python
    --8<-- "07_pivot.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("07_pivot.py"))
    ```

## Result

```python exec="on"
--8<-- "07_pivot.py"
```

## What to notice

- **Column names** are `{value}{separator}{measure}`: `EMEA_notional`. `separator` defaults to `_`.
- **`totals: true`** adds each measure across all pivot columns under its plain name (`notional`).
- **Empty cells are null**, not 0. For example, there are no Commodities positions in AMER.
- `result.meta.pivot_fields` lists the pivot columns, in order. A grid uses it to build its column headers.

## Options

| Field | Meaning |
| --- | --- |
| `on` | One or more columns whose values become columns |
| `values` | Which measures to pivot (default: all) |
| `domain` | A fixed list of value combinations, in order, e.g. `[["AMER"], ["EMEA"], ["APAC"]]`. Without it, the sorted distinct values of the filtered rows are used |
| `totals` | Add the across-columns totals |
| `separator` | Between the parts of a column name |
| `null_label` | The label for a null pivot value (default `(blank)`) |

## Gotchas

- Pass a `domain` when the columns must stay stable across requests, for example while a user drills down in a grid.
- `Limits.max_pivot_columns` (2,000 by default) caps the number of generated columns.
- A pivot can't be combined with `having`, or used in [compare](compare.md), yet.
