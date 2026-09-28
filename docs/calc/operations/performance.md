---
covers:
  - packages/calc/src/pylibs_calc/cache.py
  - packages/calc/src/pylibs_calc/exec.py
---

# Performance

## Benchmarks

These were measured with [`packages/calc/benchmarks/bench.py`](https://github.com/sanjaysharmagwl/py-libs/blob/master/packages/calc/benchmarks/bench.py) on **10 million positions**, with `POLARS_MAX_THREADS=4`, on an Apple M1. Times are p50 / p95 in milliseconds.

| Request | String dimensions | Categorical dimensions |
| --- | --- | --- |
| filter, 2 derived columns, 3-key group-by, 5 measures | 979 / 1069 | 552 / 602 |
| filter, sort by a derived column, one page of 100 rows | 255 / 272 | 233 / 244 |
| pivot: sector × region, 2 measures, totals | 456 / 545 | 361 / 409 |
| what-if scenario (100 overrides, a shock, a formula), then group-by | 989 / 1133 | 838 / 1001 |
| 3-level rollup of an exact-decimal product | 1247 / 1614 | 920 / 1053 |
| next page of a cached aggregate (grid scrolling) | 0.6 / 0.7 | 0.5 / 0.6 |

Run them yourself:

```bash
uv run python packages/calc/benchmarks/bench.py
```

## Guidance

- **Store dimensions as Categorical.** Grouping is about twice as fast, and the catalog keeps categoricals as they are.
- **Use Decimal only where exactness matters.** Decimal sums and products cost 2–7× their float equivalents. Prices and notionals usually deserve it; yields and risk sensitivities usually don't.
- **Paging is cheap after the first request.** Aggregates are cached by content hash (`EngineConfig.cache_bytes`, 256 MiB by default), and later pages are sliced from the cache.
- **Row views push sorting and slicing into Polars**, so one page of a huge table never builds the whole table.
- **Scenarios only rewrite the columns they change**, and store changes rather than copies of the data.
- **Files larger than memory** go through `register_scan`, which uses Polars' streaming engine with filter and column pushdown.
