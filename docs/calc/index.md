# pylibs-calc

**An embeddable calculation engine for the portfolio grids that fund managers and research analysts slice, edit and aggregate, extensible with plugins such as what-if analysis.**

It is built for the investment teams of an active asset manager: **portfolio managers**, **equity and credit analysts**, and the investment risk, compliance and client reporting teams around them. You give it a table, such as a fund's holdings next to its benchmark. It answers questions like *"What happens to the fund's active weight in tech if tech stocks fall 10%?"*:

- with exact decimal arithmetic
- with results you can reproduce and audit
- fast enough to drive an interactive grid over millions of rows

It is a Python **library** built on [Polars](https://pola.rs). You embed it in your own service, and it comes with a ready-made [FastAPI router](integrations/fastapi.md) and an [AG Grid adapter](integrations/aggrid.md). The core engine does the calculations every analytics service needs; [plugins](concepts/plugins.md) add analyses on top, starting with the [what-if plugin](whatif/index.md).

<div class="grid cards" markdown>

-   :material-book-open-variant: **New to investing?**

    ---

    Holdings, NAV, weights, benchmarks, active weights, shocks and basis points, explained from scratch.

    [:octicons-arrow-right-24: Investment primer](getting-started/finance-primer.md)

-   :material-rocket-launch-outline: **New here?**

    ---

    Install it and run your first calculation in five minutes.

    [:octicons-arrow-right-24: Quick start](getting-started/quickstart.md)

-   :material-briefcase-outline: **PM, analyst or QA?**

    ---

    Click around a live grid, or send JSON with curl. No Python needed.

    [:octicons-arrow-right-24: Run the demo grid](getting-started/run-the-demo.md)

-   :material-school-outline: **Learning a feature?**

    ---

    Each feature has a page with a PM's or analyst's question, a runnable request and its real output.

    [:octicons-arrow-right-24: Scenarios by feature](scenarios/index.md)

-   :material-code-braces: **Integrating it?**

    ---

    Architecture, the API reference, deployment and error codes.

    [:octicons-arrow-right-24: Architecture](concepts/architecture.md)

</div>

## What it does

| Capability | In one line | Learn it |
| --- | --- | --- |
| Rows | Filters and derived columns | [Filter and derive](scenarios/filter-derive.md) |
| Aggregation | Group-by, filtered and weighted measures, ratios of sums, subtotals, pivots | [Measures](scenarios/measures.md), [Rollup](scenarios/rollup.md), [Pivot](scenarios/pivot.md) |
| Weights | Portfolio weights, benchmark weights and active weights with `total()`, correct at every subtotal | [Weights and active weights](scenarios/weights.md) |
| Comparison | The same query on two sides (base and scenario), with deltas and percentage changes, for the fund and its benchmark at once | [Compare](scenarios/compare.md) |
| Extensibility | Plugins add functions, aggregates, dataset transforms, operations and HTTP routes | [Plugins](concepts/plugins.md), [Write a plugin](extending/write-a-plugin.md) |
| What-if (plugin) | Cell overrides, bulk shocks (`price −10% where sector == 'Information Technology'`, the dollar +5%), formula columns | [Override](scenarios/override.md), [Shock](scenarios/shock.md) |
| Scenarios (plugin) | Saved, versioned, forkable what-ifs with an audit trail | [Saved scenarios](scenarios/saved-scenarios.md) |
| Exact numbers | Decimal arithmetic with explicit scales and half-to-even rounding | [Numbers, types and nulls](concepts/numbers-types-nulls.md) |
| Verifiability | A fingerprint on every result, `explain`, and an independent reference evaluator | [Audit a number](scenarios/audit.md) |
| Entitlements | Row filters and column visibility enforced for every request | [Access control](scenarios/access-control.md) |

## A request at a glance

```python exec="on" source="tabbed-left" tabs="Request|Result"
from book import engine, table

result = engine().run({
    "dataset": "holdings",
    "extensions": {"whatif": {"steps": [
        {"kind": "shock", "column": "price", "op": "pct", "value": -10,
         "where": "sector == 'Information Technology' and asset_class == 'Equity'"},
    ]}},
    "query": {
        "derive": [
            {"name": "fund", "expr": "round(price * quantity * fx_rate, 2)"},
            {"name": "bench", "expr": "round(price * bench_quantity * fx_rate, 2)"},
        ],
        "group_by": ["sector"],
        "measures": [
            {"name": "fund", "fn": "sum", "of": "fund"},
            {"name": "bench", "fn": "sum", "of": "bench"},
        ],
        "post": [
            {"name": "weight_pct", "expr": "round(100 * fund / total(fund), 2)"},
            {"name": "active_pct", "expr": "round(100 * (fund / total(fund) - bench / total(bench)), 2)"},
        ],
        "sort": [{"by": "active_pct"}],
    },
})
print(table(result))
```
