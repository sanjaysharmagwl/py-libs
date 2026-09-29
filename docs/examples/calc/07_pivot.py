"""Pivot: currency exposure by asset class, as weights in the fund, with row totals."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "query": {
        "filter": "quantity > 0",
        "derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}],
        "group_by": ["asset_class"],
        "measures": [{"name": "mv", "fn": "sum", "of": "mv"}],
        "post": [{"name": "weight_pct", "expr": "round(100 * mv / total(mv), 2)"}],
        "pivot": {"on": ["currency"], "values": ["weight_pct"], "totals": True},
        "sort": [{"by": "asset_class"}],
    },
}

result = engine().run(REQUEST)
print(table(result))
print(f"Pivot columns: `{result.meta.pivot_fields}`")
