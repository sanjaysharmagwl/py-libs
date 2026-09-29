---
covers:
  - packages/calc/src/pylibs_calc/spec/query.py
  - packages/calc/src/pylibs_calc/engine.py
  - packages/calc/src/pylibs_calc/cache.py
---

# Sort and page

!!! question "The business question"
    *"List the fund's holdings from the largest weight down, five at a time, like the top ten
    holdings on a factsheet."*

`sort` orders the result, and `page` returns a slice of it. `meta.total_rows` tells a grid how many rows there are in total.

## Try it

=== "Python"

    ```python
    --8<-- "08_sort_page.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("08_sort_page.py"))
    ```

## Result

```python exec="on"
--8<-- "08_sort_page.py"
```

## What to notice

- **The sort is always a total order.** Ties are broken by the group columns (in a row view, by the dataset's key columns), so paging never skips or repeats a row.
- **Weights are computed before paging.** `total(mv)` is the whole fund, so the second page's weights are still shares of the whole fund, not of the page.
- **`nulls_last`** defaults to `true` for each sort key. Set `desc: true` for descending order.
- **Later pages of an aggregate come from the cache.** Aggregates are cached by the request's fingerprint without the page, so scrolling a grid slices the cached result in well under a millisecond.
- **Row views push sorting and slicing into Polars**, so a page of a very large table never builds the whole table in memory.

## Gotchas

- `page.limit` may be at most `Limits.max_page_size` (50,000 by default).
- A request without a `page` may return at most `Limits.max_unpaged_rows` rows (100,000 by default).
