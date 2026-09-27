---
covers:
  - packages/calc/src/pylibs_calc/compile/compare.py
  - packages/calc/src/pylibs_calc/engine.py
  - packages/calc/src/pylibs_calc/spec/query.py
---

# Compare two sides

!!! question "The business question"
    *"If Rates sells off 2% and Credit 1%, what is the market-value impact per desk, largest loss
    first?"*

`compare` runs **the same query on two sides** and joins the results, adding a base value, a delta and a percentage change for every measure.

## Try it

=== "Python"

    ```python
    --8<-- "14_compare.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("14_compare.py", route="/calc/compare"))
    ```

## Result

```python exec="on"
--8<-- "14_compare.py"
```

## What to notice

- For each measure `m`, you get:
    - `m`: the scenario side
    - `m__base`: the base side
    - `m__delta`: scenario − base
    - `m__pct`: the change in percent
- You can sort by any of them. Here `mv__delta` ascending puts the biggest loss first.
- Desks the shocks don't touch show a delta of 0.

## Choosing the two sides

| Scenario side | Base side | Compares |
| --- | --- | --- |
| `what_if` | — | One-off changes vs the unmodified data (this example) |
| `scenario` | — | A saved scenario vs the unmodified data |
| `scenario` | `base` | Two saved scenarios, e.g. "hedged" vs "unhedged" |
| `scenario` | `base` + `base_what_if` | A scenario vs another with extra changes |

- Aggregated queries are joined on the group columns.
- Row views are joined on the dataset's key columns, so you see the change per position.

## Gotchas

- `m__pct` is **null when the base is 0**.
- Compare doesn't support `pivot`, or more than two sides, yet.
