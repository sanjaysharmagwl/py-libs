"""Filtered measures: long and short notional side by side, like SQL FILTER (WHERE ...)."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "query": {
        "derive": [{"name": "notional", "expr": "price * quantity"}],
        "group_by": ["desk"],
        "measures": [
            {"name": "long", "fn": "sum", "of": "notional", "where": "quantity > 0"},
            {"name": "short", "fn": "sum", "of": "notional", "where": "quantity < 0"},
            {"name": "net", "fn": "sum", "of": "notional"},
        ],
        "sort": [{"by": "desk"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
