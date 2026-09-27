# Scenarios by feature

Every feature of `pylibs-calc` has a page here that follows the same five-part pattern, so you can learn one feature in a few minutes and try it yourself:

1. **The business question** is what a trader, risk manager or analyst actually wants to know.
2. **Try it** shows the request, in Python and as the JSON you would send to the HTTP API.
3. **Result** is the real output. The docs site runs every example when it is built, so the tables can't drift from what the engine does.
4. **What to notice** points out the details that matter.
5. **Gotchas** covers what most often surprises people.

## The example book

All examples run against the same twelve positions. They are defined in [`docs/examples/calc/book.py`](https://github.com/sanjaysharmagwl/py-libs/blob/master/docs/examples/calc/book.py) and registered as the dataset `positions`, with `position_id` as the key:

```python exec="on"
from book import positions, table

print(table(positions()))
```

- **Negative quantities** are short positions.
- **`price`** is an exact decimal with 2 places, as a mark in a risk system would be.
- **`yield`** is a float, and it is null where it doesn't apply (equities, FX and commodities).
- The columns match the demo service, so every **JSON (curl)** tab also works against [the demo](../getting-started/run-the-demo.md). The numbers will differ, because the demo generates 200,000 positions.

!!! tip "Run any example yourself"
    ```bash
    make install
    uv run python docs/examples/calc/10_shock.py
    ```

## Pages

| Feature | Business question |
| --- | --- |
| [Filter and derive](filter-derive.md) | What is my EMEA book, with notionals? |
| [Measures](measures.md) | What is each desk's exposure and weighted yield? |
| [Filtered measures](filtered-measures.md) | How much is long and how much short, per desk? |
| [Ratios after aggregation](post-ratios.md) | What is the average price per region, done right? |
| [Having](having.md) | Which desks are over their limit? |
| [Subtotals (rollup)](rollup.md) | Book, region and desk totals in one grid |
| [Pivot](pivot.md) | A desk × region exposure matrix |
| [Sort and page](sort-page.md) | The biggest positions, a page at a time |
| [Override a cell](override.md) | A trader corrects a mark |
| [Shock a column](shock.md) | Tech +5%, yields +25bp |
| [Formula columns](formula.md) | Keep notional correct after edits |
| [Disable a step](disable.md) | Undo part of a scenario without losing history |
| [Saved scenarios and forks](saved-scenarios.md) | Save a what-if, share it, branch it |
| [Compare two sides](compare.md) | What is the P&L impact of a sell-off? |
| [Access control](access-control.md) | A desk sees only its own positions |
| [Audit a number](audit.md) | Prove where a figure came from |
| [Errors and limits](errors-limits.md) | What the engine refuses, and why |
