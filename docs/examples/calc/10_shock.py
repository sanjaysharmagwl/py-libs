"""Shocks: Tech prices +5%, and yields +25bp on every bond."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "extensions": {
        "whatif": {
            "steps": [
                {
                    "kind": "shock",
                    "column": "price",
                    "op": "pct",
                    "value": 5,
                    "where": "sector == 'Tech'",
                },
                {"kind": "shock", "column": "yield", "op": "add", "value": "0.0025"},
            ]
        }
    },
    "query": {
        "filter": "desk in ('Rates', 'Credit')",
        "select": ["position_id", "instrument", "sector", "price", "yield"],
        "sort": [{"by": "position_id"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
