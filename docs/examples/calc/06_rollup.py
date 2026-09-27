"""Rollup: book -> region -> desk subtotals in one result."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "query": {
        "derive": [{"name": "notional", "expr": "price * quantity"}],
        "group_by": ["region", "desk"],
        "rollup": True,
        "measures": [
            {"name": "notional", "fn": "sum", "of": "notional"},
            {"name": "positions", "fn": "count_rows"},
        ],
        "sort": [{"by": "region"}, {"by": "desk"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
