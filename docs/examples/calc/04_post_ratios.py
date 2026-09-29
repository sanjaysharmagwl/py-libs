"""Post-aggregation: upside to the analysts' targets per region, as a ratio of sums."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "query": {
        "filter": "asset_class == 'Equity' and quantity > 0",
        "derive": [
            {"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"},
            {"name": "target_mv", "expr": "round(target_price * quantity * fx_rate, 2)"},
            {"name": "upside_pct", "expr": "100 * (float(target_price) / float(price) - 1)"},
        ],
        "group_by": ["region"],
        "measures": [
            {"name": "mv", "fn": "sum", "of": "mv"},
            {"name": "target_mv", "fn": "sum", "of": "target_mv"},
            {"name": "avg_upside_pct", "fn": "mean", "of": "upside_pct"},
        ],
        "post": [{"name": "upside_pct", "expr": "round(100 * (target_mv / mv - 1), 2)"}],
        "sort": [{"by": "region"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
