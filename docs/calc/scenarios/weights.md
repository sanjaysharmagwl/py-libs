---
covers:
  - packages/calc/src/pylibs_calc/compile/validate.py
  - packages/calc/src/pylibs_calc/compile/logical.py
---

# Weights and active weights

!!! question "The business question"
    *"What share of the fund is in each sector, what share of the benchmark, and where are we
    overweight or underweight?"*

A **weight** is a group's share of the whole: its market value divided by the fund's NAV. A `post`
expression sees one group at a time, so it needs a way to reach the whole. That is **`total(m)`**:
the measure `m` computed over **every row the query sees**, available in `post` and `having`.

- **Weight:** `mv / total(mv)`.
- **Active weight:** the fund's weight minus the benchmark's weight. The fund and the benchmark
  are two measures over the same rows, each divided by its own total.

## Try it

=== "Python"

    ```python
    --8<-- "19_weights.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("19_weights.py"))
    ```

## Result

```python exec="on"
--8<-- "19_weights.py"
```

## What to notice

- **Each column adds up to 100%.** `total(fund)` is the fund's NAV and `total(bench)` is the
  benchmark's, so `fund_pct` and `bench_pct` are each a complete breakdown, and `active_pct` adds
  up to 0.
- **The fund's big bets are easy to read.** It is overweight Energy and Financials, holds cash that
  the benchmark doesn't, and is 15 points **underweight Information Technology**: it owns no
  Initech and less Cyberdyne than the index.
- **`round(100 * mv / total(mv), 2)`** gives a percentage with 2 decimals. Both sides are exact
  decimals, so the division is exact to `NumericConfig.division_scale` places before rounding.
  Leave out the `100 *` and the `round` if you want a fraction.
- `active_pct` uses the earlier `post` values `fund_pct` and `bench_pct`. A `post` expression can
  use any earlier one.

## What "every row the query sees" means

| Stage | Does it change `total()`? |
| --- | --- |
| `filter`, and the plugin transforms (what-if [shocks](shock.md) and [overrides](override.md)) | **Yes.** The total is over the rows that remain, with their changed values. Use `"filter": "quantity > 0"` for weights in the fund alone, or a measure's `where` to split the rows without removing them. |
| [Access control](access-control.md) `row_filter` | **Yes.** A caller who sees only part of the fund gets weights within that part. |
| `group_by`, [`rollup`](rollup.md) | **No.** Every level divides by the same grand total, so a subtotal's weight is its share of the fund. |
| [`having`](having.md) | **No.** Groups that `having` removes still count in the total. |
| [`pivot`](pivot.md) | **No.** Every cell divides by the same grand total, across all the pivot columns. |
| `sort`, [`page`](sort-page.md) | **No.** The second page's weights are still shares of the whole fund. |
| [Compare](compare.md) | Each side has **its own** total, so a scenario that moves prices also moves weights. |

## Gotchas

- `total()` takes the **name of a measure**: `total(mv)`. It can't take an expression or a `post`
  name, and it is refused outside `post` and `having` (`422 invalid_total`), because it has no
  meaning before aggregation.
- A total of zero, or of nothing at all, makes the weight **null**, as any division by zero does.
- `total()` is always the grand total. A share *within* a parent (a stock's weight inside its
  sector) needs two queries for now; see [Assumptions and limitations](../limitations.md).
- To put the fund and the benchmark in one table, the example fund holds both quantities on each
  row (`quantity` and `bench_quantity`). If your benchmark comes as weights instead, sum the weight
  column directly: `{"name": "bench_w", "fn": "sum", "of": "bench_weight"}`.
