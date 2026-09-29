# Scenarios by feature

Every feature of `pylibs-calc` has a page here that follows the same five-part pattern, so you can learn one feature in a few minutes and try it yourself:

1. **The business question** is what a portfolio manager, research analyst or someone on the investment risk team actually wants to know.
2. **Try it** shows the request, in Python and as the JSON you would send to the HTTP API.
3. **Result** is the real output. The docs site runs every example when it is built, so the tables can't drift from what the engine does.
4. **What to notice** points out the details that matter.
5. **Gotchas** covers what most often surprises people.

## The example fund

All examples run against the same fictional multi-asset **Global Income Fund** (base currency USD) and its 60/40 equity and government bond benchmark, held as one table of fourteen securities. It is defined in [`docs/examples/calc/book.py`](https://github.com/sanjaysharmagwl/py-libs/blob/master/docs/examples/calc/book.py) and registered as the dataset `holdings`, with `security_id` as the key:

```python exec="on"
from book import holdings, table

print(table(holdings()))
```

- **`quantity`** is what the fund holds, and **`bench_quantity`** what the benchmark holds. A `0` in one of them is a security only the other one owns: an underweight, or an off-benchmark holding.
- **`price`** is in the security's own currency, as an exact decimal with 2 places. **`fx_rate`** converts that currency to US dollars, so `price * quantity * fx_rate` is the market value in USD.
- **`yield`** and **`duration`** are floats, null except for bonds. **`target_price`** is the equity analyst's target, null except for equities.
- The columns match the demo service, so every **JSON (curl)** tab also works against [the demo](../getting-started/run-the-demo.md). The numbers will differ, because the demo generates 200,000 holdings.

New to these terms? The [Investment primer](../getting-started/finance-primer.md) explains every column.

!!! tip "Run any example yourself"
    ```bash
    make install
    uv run python docs/examples/calc/10_shock.py
    ```

## Pages

### Core engine

| Feature | Business question |
| --- | --- |
| [Filter and derive](filter-derive.md) | What are my foreign holdings worth in dollars, and what upside do the analysts see? |
| [Measures](measures.md) | What is each asset class worth, and at what weighted yield? |
| [Filtered measures](filtered-measures.md) | What is the asset mix in each region? |
| [Ratios after aggregation](post-ratios.md) | What upside to target does each region have, done right? |
| [Weights and active weights](weights.md) | Where is the fund overweight and underweight its benchmark? |
| [Having](having.md) | Which holdings break the concentration limit? |
| [Subtotals (rollup)](rollup.md) | Fund, asset class and sector weights in one grid |
| [Pivot](pivot.md) | An asset class × currency exposure matrix |
| [Sort and page](sort-page.md) | The top ten holdings, a page at a time |
| [Compare two sides](compare.md) | How do the fund and its benchmark come through a bond sell-off? |
| [Access control](access-control.md) | An analyst sees only their coverage |
| [Audit a number](audit.md) | Prove where an active weight came from |
| [Errors and limits](errors-limits.md) | What the engine refuses, and why |

### What-if plugin

These need the [what-if plugin](../whatif/index.md) (`pylibs-calc-whatif`), which the example fund's engine installs.

| Feature | Business question |
| --- | --- |
| [Override a cell](override.md) | An analyst marks down an illiquid bond |
| [Shock a column](shock.md) | Tech −10%, yields +25bp, the dollar +5% |
| [Formula columns](formula.md) | Keep market values correct after edits |
| [Disable a step](disable.md) | Undo part of a scenario without losing history |
| [Saved scenarios and forks](saved-scenarios.md) | Save a what-if, share it, branch it |
