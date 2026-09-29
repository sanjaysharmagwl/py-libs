"""Rollup: fund -> asset class -> sector, with each subtotal's weight in the fund."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "query": {
        "filter": "quantity > 0",
        "derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}],
        "group_by": ["asset_class", "sector"],
        "rollup": True,
        "measures": [
            {"name": "mv", "fn": "sum", "of": "mv"},
            {"name": "holdings", "fn": "count_rows"},
        ],
        "post": [{"name": "weight_pct", "expr": "round(100 * mv / total(mv), 2)"}],
        "sort": [{"by": "asset_class"}, {"by": "sector"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
