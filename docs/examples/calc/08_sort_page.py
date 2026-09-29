"""Sort and page: the fund's top five holdings by weight, factsheet style, then the next page."""

from book import engine, table

REQUEST = {
    "dataset": "holdings",
    "query": {
        "filter": "quantity > 0",
        "derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}],
        "group_by": ["security", "asset_class"],
        "measures": [{"name": "mv", "fn": "sum", "of": "mv"}],
        "post": [{"name": "weight_pct", "expr": "round(100 * mv / total(mv), 2)"}],
        "sort": [{"by": "weight_pct", "desc": True}],
        "page": {"offset": 0, "limit": 5},
    },
}

calc = engine()
first = calc.run(REQUEST)
print(table(first))
print(f"`total_rows` = {first.meta.total_rows}, `rows` = {first.meta.rows}\n")

second_page = {**REQUEST, "query": {**REQUEST["query"], "page": {"offset": 5, "limit": 5}}}
print(table(calc.run(second_page)))
