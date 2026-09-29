---
covers:
  - packages/calc/src/pylibs_calc/engine.py
  - packages/calc/src/pylibs_calc/catalog.py
---

# Quick start

This page takes five minutes. You will register a dataset, run a query, try a what-if with the what-if plugin, and read the result's metadata.

!!! tip "New to holdings, weights and benchmarks?"
    Read the [Investment primer](finance-primer.md) first. It explains every investment term these examples use.

## 1. Register data and create an engine

```python
import polars as pl
from pylibs_calc import CalcEngine, Catalog
from pylibs_calc_whatif import InMemoryScenarioStore, WhatIfPlugin

catalog = Catalog()
catalog.register_frame("holdings", df, key_columns=["security_id"], version="2026-09-30")
engine = CalcEngine(catalog, plugins=[WhatIfPlugin(store=InMemoryScenarioStore())])
```

`df` is any Polars DataFrame. These docs use an [example fund of fourteen securities, next to its benchmark](../scenarios/index.md#the-example-fund), and `book.engine()` does exactly the three lines above.

The core engine (`pylibs-calc`) filters, derives, aggregates, pivots and compares. Everything else is a [plugin](../concepts/plugins.md); `WhatIfPlugin` (`pip install pylibs-calc-whatif`) adds overrides, shocks, formula columns and saved scenarios. Without plugins, `CalcEngine(catalog)` is all you need.

## 2. Ask a question

A request is plain JSON: the same dictionary works from Python and over HTTP. Here, the fund's market value and weight in each asset class (`total(mv)` is the whole fund, so `mv / total(mv)` is a weight):

```python exec="on" source="above"
--8<-- "00_quickstart.py"
```

## 3. Ask "what if?"

Add what-if steps under `extensions.whatif` to change the data for this request only. Here, equities fall 10%, and the query shows the fund next to its benchmark:

```python exec="on" source="above"
from book import engine, table

result = engine().compare(
    {
        "dataset": "holdings",
        "extensions": {
            "whatif": {
                "steps": [
                    {
                        "kind": "shock",
                        "column": "price",
                        "op": "pct",
                        "value": -10,
                        "where": "asset_class == 'Equity'",
                    }
                ]
            }
        },
        "query": {
            "derive": [
                {"name": "fund", "expr": "round(price * quantity * fx_rate, 2)"},
                {"name": "bench", "expr": "round(price * bench_quantity * fx_rate, 2)"},
            ],
            "group_by": ["asset_class"],
            "measures": [
                {"name": "fund", "fn": "sum", "of": "fund"},
                {"name": "bench", "fn": "sum", "of": "bench"},
            ],
            "sort": [{"by": "asset_class"}],
        },
    }
)
print(table(result))
```

`compare` runs the query with and without the change, and adds the base value, the delta and the percentage change. The fund holds less in equities than its benchmark, so it loses less.

## 4. Read the metadata

```python exec="on" source="above"
from book import engine

result = engine().run(
    {
        "dataset": "holdings",
        "query": {"group_by": ["asset_class"], "measures": [{"name": "n", "fn": "count_rows"}]},
    }
)
print(
    f"- `result.meta.fingerprint`: `{result.meta.fingerprint[:16]}…`, the identity of this exact calculation"
)
print(f"- `result.meta.total_rows`: {result.meta.total_rows}, the rows before paging")
print(f"- `result.meta.columns`: {[(c.name, c.type) for c in result.meta.columns]}")
print(f"- `result.meta.timings_ms`: {sorted(result.meta.timings_ms)}")
```

`result.meta` is a `ResultMeta`, and each entry of `meta.columns` is a `ColumnInfo` (name, type and scale). `result.frame` is a Polars DataFrame. `result.to_dict()` gives JSON-safe rows plus the metadata, which is what the HTTP API returns.

## Next steps

- **Learn each feature** from [Scenarios by feature](../scenarios/index.md).
- **Put it behind HTTP** with the [FastAPI router](../integrations/fastapi.md).
- **Click around a live grid** in [Run the demo grid](run-the-demo.md).
