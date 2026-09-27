"""Post-aggregation: average price as a ratio of sums, and gross leverage per region."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "query": {
        "filter": "desk in ('Rates', 'Credit')",
        "derive": [{"name": "notional", "expr": "price * quantity"}],
        "group_by": ["region"],
        "measures": [
            {"name": "notional", "fn": "sum", "of": "notional"},
            {"name": "gross", "fn": "sum", "of": "abs(notional)"},
            {"name": "quantity", "fn": "sum", "of": "quantity"},
        ],
        "post": [
            {"name": "avg_px", "expr": "notional / quantity"},
            {"name": "net_to_gross", "expr": "notional / gross"},
        ],
        "sort": [{"by": "region"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
