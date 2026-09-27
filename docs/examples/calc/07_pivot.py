"""Pivot: a desk x region exposure matrix, with row totals."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "query": {
        "derive": [{"name": "notional", "expr": "price * quantity"}],
        "group_by": ["desk"],
        "measures": [{"name": "notional", "fn": "sum", "of": "notional"}],
        "pivot": {"on": ["region"], "totals": True},
        "sort": [{"by": "desk"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
print(f"Pivot columns: `{result.meta.pivot_fields}`")
