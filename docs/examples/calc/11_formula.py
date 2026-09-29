"""Formula steps: market value is recomputed after every value change, even a later override."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "extensions": {
        "whatif": {
            "steps": [
                {"kind": "formula", "name": "mv", "expr": "round(price * quantity * fx_rate, 2)"},
                {
                    "kind": "override",
                    "edits": [{"key": {"security_id": 8}, "column": "price", "value": "300.00"}],
                },
            ]
        }
    },
    "query": {
        "filter": "asset_class == 'Equity' and currency == 'USD' and quantity > 0",
        "select": ["security_id", "security", "price", "quantity", "mv"],
        "sort": [{"by": "security_id"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
