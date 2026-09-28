"""Formula steps: notional is recomputed after every value change, even a later override."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "extensions": {
        "whatif": {
            "steps": [
                {"kind": "formula", "name": "notional", "expr": "price * quantity"},
                {
                    "kind": "override",
                    "edits": [{"key": {"position_id": 8}, "column": "price", "value": "300.00"}],
                },
            ]
        }
    },
    "query": {
        "filter": "desk == 'Equities'",
        "select": ["position_id", "instrument", "price", "quantity", "notional"],
        "sort": [{"by": "position_id"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
