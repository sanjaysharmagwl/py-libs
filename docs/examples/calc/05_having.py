"""Having: only the desks whose gross exposure is over their limit of 400,000."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "query": {
        "derive": [{"name": "gross", "expr": "abs(price * quantity)"}],
        "group_by": ["desk"],
        "measures": [{"name": "gross", "fn": "sum", "of": "gross"}],
        "having": "gross > 400000",
        "sort": [{"by": "gross", "desc": True}],
    },
}

result = engine().run(REQUEST)
print(table(result))
