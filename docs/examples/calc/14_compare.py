"""Compare: the P&L impact of a rates sell-off, by desk, against the base book."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "what_if": [
        {"kind": "shock", "column": "price", "op": "pct", "value": -2, "where": "desk == 'Rates'"},
        {"kind": "shock", "column": "price", "op": "pct", "value": -1, "where": "desk == 'Credit'"},
    ],
    "query": {
        "derive": [{"name": "mv", "expr": "price * quantity"}],
        "group_by": ["desk"],
        "measures": [{"name": "mv", "fn": "sum", "of": "mv"}],
        "sort": [{"by": "mv__delta"}],
    },
}

result = engine().compare(REQUEST)
print(table(result))
