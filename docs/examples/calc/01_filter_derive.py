"""Filter + derive: the EMEA positions and their notional."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "query": {
        "filter": "region == 'EMEA' and quantity != 0",
        "derive": [
            {"name": "notional", "expr": "price * quantity"},
            {"name": "side", "expr": "'long' if quantity > 0 else 'short'"},
        ],
        "select": ["position_id", "desk", "price", "quantity", "notional", "side"],
        "sort": [{"by": "position_id"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
