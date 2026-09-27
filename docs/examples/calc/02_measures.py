"""Measures: exposure, counts and weighted yield per desk."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "query": {
        "derive": [{"name": "notional", "expr": "price * quantity"}],
        "group_by": ["desk"],
        "measures": [
            {"name": "notional", "fn": "sum", "of": "notional"},
            {"name": "avg_price", "fn": "mean", "of": "price"},
            {"name": "max_price", "fn": "max", "of": "price"},
            {"name": "positions", "fn": "count_rows"},
            {"name": "with_yield", "fn": "count", "of": "yield"},
            {"name": "sectors", "fn": "count_distinct", "of": "sector"},
            {
                "name": "wavg_yield",
                "fn": "wavg",
                "of": "yield",
                "weight": "abs(float(notional))",
            },
        ],
        "sort": [{"by": "desk"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
