---
covers:
  - packages/calc/src/pylibs_calc/compile/compare.py
  - packages/calc/src/pylibs_calc/engine.py
  - packages/calc/src/pylibs_calc/spec/query.py
---

# Compare two sides

!!! question "The business question"
    *"If government bonds sell off 4% and corporate bonds 2%, how much does the fund lose in each
    asset class, and how does that compare with the benchmark?"*

`compare` runs **the same query on two sides** and joins the results, adding a base value, a delta and a percentage change for every measure. It is part of the core engine: a side is the dataset (at a version) with its own plugin `extensions`, so you can compare what-if scenarios, two versions of the data, or anything a plugin transform produces.

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
- The query has two measures, `fund` and `bench`, so **one compare gives the fund and the benchmark side by side**. The script keeps only those columns for display.
- **Read the relative result, not only the loss.** Within bonds, the fund loses less than the benchmark (about −3.5% against −4.0%): part of its bond money is in corporate bonds, which were shocked less. But the fund holds more bonds than the benchmark (46% against 40%), so on the whole fund the loss is slightly larger (about −1.63% against −1.60%).
- The `rollup` adds the fund-level row (`__level` 0). Compare works with subtotals, and so do `post` values such as [weights](weights.md): each side gets its own `total()`.
- Asset classes the shocks don't touch show a delta of 0. The benchmark holds no cash, so its `bench__pct` for cash is null.
- You can sort by any of the columns, for example `fund__delta` ascending to put the biggest loss first.

## Choosing the two sides

The target side is the request's `dataset` and `extensions`; the base side is `base`, which has its own `extensions` and an optional dataset `version`. By default the base is the unmodified dataset.

| Target side | Base side (`base`) | Compares |
| --- | --- | --- |
| `extensions.whatif.steps` | — | One-off changes vs the unmodified data (this example) |
| `extensions.whatif.scenario` | — | A saved scenario vs the unmodified data |
| `extensions.whatif.scenario` | `{"extensions": {"whatif": {"scenario": ...}}}` | Two saved scenarios, e.g. "buy Initech" vs "as is" |
| `extensions.whatif.scenario` | `{"extensions": {"whatif": {"scenario": ..., "steps": [...]}}}` | A scenario vs another with extra changes |
| `dataset.version` = today | `{"version": "yesterday"}` | Two versions of the data, no plugin needed |

- Aggregated queries are joined on the group columns.
- Row views are joined on the dataset's key columns, so you see the change per holding.

## Gotchas

- `m__pct` is **null when the base is 0**.
- Compare doesn't support `pivot`, or more than two sides, yet.
