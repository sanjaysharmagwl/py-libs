"""Weights: the fund's weight, the benchmark's weight and the active weight in each sector."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "query": {
        "derive": [
            {"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"},
            {"name": "bench_mv", "expr": "round(price * bench_quantity * fx_rate, 2)"},
        ],
        "group_by": ["sector"],
        "measures": [
            {"name": "fund", "fn": "sum", "of": "mv"},
            {"name": "bench", "fn": "sum", "of": "bench_mv"},
        ],
        "post": [
            {"name": "fund_pct", "expr": "round(100 * fund / total(fund), 2)"},
            {"name": "bench_pct", "expr": "round(100 * bench / total(bench), 2)"},
            {"name": "active_pct", "expr": "fund_pct - bench_pct"},
        ],
        "sort": [{"by": "active_pct", "desc": True}],
    },
}

result = engine().run(REQUEST)
print(table(result))
