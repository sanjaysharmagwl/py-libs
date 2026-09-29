"""Quick start: the fund's market value and weight by asset class."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "query": {
        "filter": "quantity > 0",
        "derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}],
        "group_by": ["asset_class"],
        "measures": [
            {"name": "mv", "fn": "sum", "of": "mv"},
            {"name": "holdings", "fn": "count_rows"},
        ],
        "post": [{"name": "weight_pct", "expr": "round(100 * mv / total(mv), 2)"}],
        "sort": [{"by": "weight_pct", "desc": True}],
    },
}

result = engine().run(REQUEST)
print(table(result))
