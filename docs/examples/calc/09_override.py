"""Override: a trader corrects two marks, and only those cells change."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "what_if": [
        {
            "kind": "override",
            "edits": [
                {"key": {"position_id": 4}, "column": "price", "value": "95.00"},
                {"key": {"position_id": 5}, "column": "rating", "value": "B"},
            ],
        }
    ],
    "query": {
        "filter": "desk == 'Credit'",
        "select": ["position_id", "instrument", "price", "rating"],
        "sort": [{"by": "position_id"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
