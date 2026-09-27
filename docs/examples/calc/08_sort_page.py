"""Sort and page: the five largest positions by absolute market value, then the next page."""

from book import engine, table

REQUEST = {
    "dataset": "positions",
    "query": {
        "derive": [{"name": "abs_mv", "expr": "abs(price * quantity)"}],
        "select": ["position_id", "instrument", "desk", "abs_mv"],
        "sort": [{"by": "abs_mv", "desc": True}],
        "page": {"offset": 0, "limit": 5},
    },
}

calc = engine()
first = calc.run(REQUEST)
print(table(first))
print(f"`total_rows` = {first.meta.total_rows}, `rows` = {first.meta.rows}\n")

second_page = {**REQUEST, "query": {**REQUEST["query"], "page": {"offset": 5, "limit": 5}}}
print(table(calc.run(second_page)))
