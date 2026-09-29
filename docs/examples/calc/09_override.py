"""Override: an analyst marks down an illiquid bond and downgrades it; only those cells change."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "extensions": {
        "whatif": {
            "steps": [
                {
                    "kind": "override",
                    "edits": [
                        {"key": {"security_id": 6}, "column": "price", "value": "80.00"},
                        {"key": {"security_id": 6}, "column": "rating", "value": "B"},
                    ],
                }
            ]
        }
    },
    "query": {
        "filter": "asset_class == 'Fixed Income' and quantity > 0",
        "select": ["security_id", "security", "rating", "price", "yield"],
        "sort": [{"by": "security_id"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
