# pylibs-calc

**An embeddable what-if calculation engine for the grids that finance teams slice, edit and aggregate.**

You give it a table, such as positions, trades or exposures. It answers questions like *"What is each desk's exposure if Tech rallies 5%?"*:

- with exact decimal arithmetic
- with results you can reproduce and audit
- fast enough to drive an interactive grid over millions of rows

It is a Python **library** built on [Polars](https://pola.rs). You embed it in your own service, and it comes with a ready-made [FastAPI router](integrations/fastapi.md) and an [AG Grid adapter](integrations/aggrid.md).

<div class="grid cards" markdown>

-   :material-book-open-variant: **New to finance?**

    ---

    Positions, desks, notional, shocks, basis points and P&L impact, explained from scratch.

    [:octicons-arrow-right-24: Finance primer](getting-started/finance-primer.md)

-   :material-rocket-launch-outline: **New here?**

    ---

    Install it and run your first calculation in five minutes.

    [:octicons-arrow-right-24: Quick start](getting-started/quickstart.md)

-   :material-briefcase-outline: **Business user or QA?**

    ---

    Click around a live grid, or send JSON with curl. No Python needed.

    [:octicons-arrow-right-24: Run the demo grid](getting-started/run-the-demo.md)

-   :material-school-outline: **Learning a feature?**

    ---

    Each feature has a page with a finance scenario, a runnable request and its real output.

    [:octicons-arrow-right-24: Scenarios by feature](scenarios/index.md)

-   :material-code-braces: **Integrating it?**

    ---

    Architecture, the API reference, deployment and error codes.

    [:octicons-arrow-right-24: Architecture](concepts/architecture.md)

</div>

## What it does

| Capability | In one line | Learn it |
| --- | --- | --- |
| Row changes | Filters, derived columns, cell overrides, and bulk shocks (`price +5% where sector == 'Tech'`) | [Override](scenarios/override.md), [Shock](scenarios/shock.md) |
| Aggregation | Group-by, filtered and weighted measures, ratios of sums, subtotals, pivots | [Measures](scenarios/measures.md), [Rollup](scenarios/rollup.md), [Pivot](scenarios/pivot.md) |
| Scenarios | Saved, versioned, forkable what-ifs with an audit trail | [Saved scenarios](scenarios/saved-scenarios.md) |
| Comparison | The same query on two sides, with deltas and percentage changes | [Compare](scenarios/compare.md) |
| Exact numbers | Decimal arithmetic with explicit scales and half-to-even rounding | [Numbers, types and nulls](concepts/numbers-types-nulls.md) |
| Verifiability | A fingerprint on every result, `explain`, and an independent reference evaluator | [Audit a number](scenarios/audit.md) |
| Entitlements | Row filters and column visibility enforced for every request | [Access control](scenarios/access-control.md) |

## A request at a glance

```python exec="on" source="tabbed-left" tabs="Request|Result"
from book import engine, table

result = engine().run({
    "dataset": "positions",
    "what_if": [{"kind": "shock", "column": "price", "op": "pct", "value": 5, "where": "sector == 'Tech'"}],
    "query": {
        "group_by": ["desk"],
        "measures": [
            {"name": "notional", "fn": "sum", "of": "price * quantity"},
            {"name": "yield", "fn": "wavg", "of": "yield", "weight": "abs(float(price * quantity))"},
        ],
        "sort": [{"by": "desk"}],
    },
})
print(table(result))
```
