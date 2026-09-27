"""Quick start: total exposure per desk."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "query": {
        "derive": [{"name": "notional", "expr": "price * quantity"}],
        "group_by": ["desk"],
        "measures": [
            {"name": "notional", "fn": "sum", "of": "notional"},
            {"name": "positions", "fn": "count_rows"},
        ],
        "sort": [{"by": "desk"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
