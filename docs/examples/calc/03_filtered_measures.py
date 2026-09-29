"""Filtered measures: the fund's asset mix per region, side by side, like SQL FILTER (WHERE ...)."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "query": {
        "filter": "quantity > 0",
        "derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}],
        "group_by": ["region"],
        "measures": [
            {"name": "equity", "fn": "sum", "of": "mv", "where": "asset_class == 'Equity'"},
            {"name": "bonds", "fn": "sum", "of": "mv", "where": "asset_class == 'Fixed Income'"},
            {"name": "cash", "fn": "sum", "of": "mv", "where": "asset_class == 'Cash'"},
            {"name": "fund", "fn": "sum", "of": "mv"},
        ],
        "sort": [{"by": "region"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
