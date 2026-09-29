"""Filter + derive: the fund's non-USD holdings, in USD, with the analyst's upside to target."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "query": {
        "filter": "currency != 'USD' and quantity > 0",
        "derive": [
            {"name": "mv_usd", "expr": "round(price * quantity * fx_rate, 2)"},
            {
                "name": "upside_pct",
                "expr": "round(100 * (target_price / price - 1), 1)",
                "where": "target_price is not None",
            },
        ],
        "select": ["security", "currency", "price", "quantity", "mv_usd", "upside_pct"],
        "sort": [{"by": "mv_usd", "desc": True}],
    },
}

result = engine().run(REQUEST)
print(table(result))
