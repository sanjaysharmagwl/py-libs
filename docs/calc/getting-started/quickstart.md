---
covers:
  - packages/calc/src/pylibs_calc/engine.py
  - packages/calc/src/pylibs_calc/catalog.py
---

# Quick start

This page takes five minutes. You will register a dataset, run a query, try a what-if, and read the result's metadata.

## 1. Register data and create an engine

```python
import polars as pl
from pylibs_calc import CalcEngine, Catalog, InMemoryScenarioStore

catalog = Catalog()
catalog.register_frame("positions", df, key_columns=["position_id"], version="2026-09-30")
engine = CalcEngine(catalog, InMemoryScenarioStore())
```

`df` is any Polars DataFrame. These docs use a [twelve-position example book](../scenarios/index.md#the-example-book), and `book.engine()` does exactly the three lines above.

## 2. Ask a question

A request is plain JSON: the same dictionary works from Python and over HTTP.

```python exec="on" source="above"
--8<-- "00_quickstart.py"
```

## 3. Ask "what if?"

Add `what_if` steps to change the data for this request only. Here, Equities fall 10%:

```python exec="on" source="above"
from book import engine, table

result = engine().compare(
    {
        "dataset": "positions",
        "what_if": [
            {
                "kind": "shock",
                "column": "price",
                "op": "pct",
                "value": -10,
                "where": "desk == 'Equities'",
            }
        ],
        "query": {
            "group_by": ["desk"],
            "measures": [{"name": "mv", "fn": "sum", "of": "price * quantity"}],
            "sort": [{"by": "desk"}],
        },
    }
)
print(table(result))
```

`compare` runs the query with and without the change, and adds the base value, the delta and the percentage change.

## 4. Read the metadata

```python exec="on" source="above"
from book import engine

result = engine().run(
    {
        "dataset": "positions",
        "query": {"group_by": ["desk"], "measures": [{"name": "n", "fn": "count_rows"}]},
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
