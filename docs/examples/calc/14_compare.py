"""Compare: a bond sell-off, fund against benchmark, by asset class."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "extensions": {
        "whatif": {
            "steps": [
                {
                    "kind": "shock",
                    "column": "price",
                    "op": "pct",
                    "value": -4,
                    "where": "sector == 'Government'",
                },
                {
                    "kind": "shock",
                    "column": "price",
                    "op": "pct",
                    "value": -2,
                    "where": "asset_class == 'Fixed Income' and sector != 'Government'",
                },
            ]
        }
    },
    "query": {
        "derive": [
            {"name": "fund", "expr": "round(price * quantity * fx_rate, 2)"},
            {"name": "bench", "expr": "round(price * bench_quantity * fx_rate, 2)"},
        ],
        "group_by": ["asset_class"],
        "rollup": True,
        "measures": [
            {"name": "fund", "fn": "sum", "of": "fund"},
            {"name": "bench", "fn": "sum", "of": "bench"},
        ],
        "sort": [{"by": "asset_class"}],
    },
}

result = engine().compare(REQUEST)
print(table(result.frame.select("asset_class", "__level", "^fund.*$", "^bench.*$")))
