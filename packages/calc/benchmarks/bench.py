"""Latency benchmark for typical grid requests on a synthetic book of positions.

    uv run --with numpy python packages/calc/benchmarks/bench.py --rows 10_000_000 --repeat 7

Set POLARS_MAX_THREADS to the CPU count you deploy with to get representative numbers.
"""

from __future__ import annotations

import argparse
import statistics
import time
from collections.abc import Callable
from typing import Any

import numpy as np
import polars as pl

from pylibs_calc import CalcEngine, Catalog, EngineConfig, InMemoryScenarioStore


def book(rows: int, seed: int = 7, *, categorical: bool = False) -> pl.DataFrame:
    rng = np.random.default_rng(seed)
    frame = pl.DataFrame(
        {
            "id": np.arange(rows, dtype=np.int64),
            "desk": rng.choice([f"desk{i}" for i in range(8)], rows),
            "sector": rng.choice([f"sector{i}" for i in range(11)], rows),
            "region": rng.choice(["EMEA", "AMER", "APAC", "LATAM"], rows),
            "book": rng.choice([f"book{i}" for i in range(200)], rows),
            "price": pl.Series(np.round(rng.uniform(1, 500, rows), 4)).cast(pl.Decimal(18, 4)),
            "qty": rng.integers(-10_000, 10_000, rows),
            "fx": rng.uniform(0.5, 2.0, rows),
            "yield": rng.uniform(0.0, 0.1, rows),
        }
    )
    if categorical:
        frame = frame.with_columns(pl.col("desk", "sector", "region", "book").cast(pl.Categorical))
    return frame


def timed(fn: Callable[[], Any], repeat: int) -> tuple[float, float]:
    samples = []
    for _ in range(repeat):
        started = time.perf_counter()
        fn()
        samples.append((time.perf_counter() - started) * 1000)
    samples.sort()
    p95 = samples[min(len(samples) - 1, round(0.95 * (len(samples) - 1)))]
    return statistics.median(samples), p95


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=lambda s: int(s.replace("_", "")), default=1_000_000)
    parser.add_argument("--repeat", type=int, default=7)
    parser.add_argument(
        "--categorical", action="store_true", help="store dimension columns as Categorical"
    )
    args = parser.parse_args()

    started = time.perf_counter()
    frame = book(args.rows, categorical=args.categorical)
    catalog = Catalog()
    catalog.register_frame("book", frame, key_columns=["id"], version="bench")
    dims = "categorical" if args.categorical else "string"
    print(
        f"{args.rows:,} rows, {dims} dimensions, {pl.thread_pool_size()} Polars threads, "
        f"setup {time.perf_counter() - started:.1f}s"
    )

    store = InMemoryScenarioStore()
    uncached = CalcEngine(catalog, store, EngineConfig(cache_bytes=0))
    cached = CalcEngine(catalog, store)
    aggregate = {
        "dataset": "book",
        "query": {
            "filter": "region != 'LATAM' and qty != 0",
            "derive": [
                {"name": "notional", "expr": "float(price) * qty * fx"},
                {"name": "carry", "expr": "notional * yield"},
            ],
            "group_by": ["desk", "sector", "region"],
            "measures": [
                {"name": "notional", "fn": "sum", "of": "notional"},
                {"name": "carry", "fn": "sum", "of": "carry"},
                {"name": "yld", "fn": "wavg", "of": "yield", "weight": "abs(notional)"},
                {"name": "px", "fn": "mean", "of": "price"},
                {"name": "n", "fn": "count_rows"},
            ],
            "sort": [{"by": "notional", "desc": True}],
            "page": {"limit": 100},
        },
    }
    scenario = cached.scenarios.create("book", "bench")
    edits = [
        {"key": {"id": i}, "column": "qty", "value": 100}
        for i in range(0, min(args.rows, 1_000_000), max(1, args.rows // 1000))
    ]
    cached.scenarios.append(
        scenario.id,
        [
            {"kind": "override", "edits": edits},
            {
                "kind": "shock",
                "column": "price",
                "op": "pct",
                "value": 5,
                "where": "sector == 'sector3'",
            },
            {"kind": "formula", "name": "mv", "expr": "price * qty"},
        ],
        expected_version=0,
    )
    scenario_request = {
        "dataset": "book",
        "scenario": scenario.id,
        "query": {
            "group_by": ["desk"],
            "measures": [
                {"name": "mv", "fn": "sum", "of": "mv"},
                {"name": "n", "fn": "count_rows"},
            ],
        },
    }
    cases: list[tuple[str, Callable[[], Any]]] = [
        (
            "aggregate: filter, 2 derived, 3-key group-by, 5 measures",
            lambda: uncached.run(aggregate),
        ),
        (
            "row page: filter + sort by derived column, 100 rows",
            lambda: uncached.run(
                {
                    "dataset": "book",
                    "query": {
                        "filter": "desk == 'desk1'",
                        "derive": [{"name": "mv", "expr": "price * qty"}],
                        "sort": [{"by": "mv", "desc": True}],
                        "page": {"offset": 200, "limit": 100},
                    },
                }
            ),
        ),
        (
            "pivot: sector x region, 2 measures, totals",
            lambda: uncached.run(
                {
                    "dataset": "book",
                    "query": {
                        "group_by": ["sector"],
                        "measures": [
                            {"name": "q", "fn": "sum", "of": "qty"},
                            {"name": "px", "fn": "max", "of": "price"},
                        ],
                        "pivot": {"on": ["region"], "totals": True},
                    },
                }
            ),
        ),
        (
            f"scenario: {len(edits)} overrides + shock + formula, group-by",
            lambda: uncached.run(scenario_request),
        ),
        (
            "rollup: desk > sector > region subtotals (exact decimals)",
            lambda: uncached.run(
                {
                    "dataset": "book",
                    "query": {
                        "group_by": ["desk", "sector", "region"],
                        "rollup": True,
                        "measures": [{"name": "mv", "fn": "sum", "of": "price * qty"}],
                    },
                }
            ),
        ),
    ]
    cached.run(aggregate)  # warm the cache
    page_two = {**aggregate, "query": {**aggregate["query"], "page": {"offset": 100, "limit": 100}}}
    cases.append(("cached aggregate, next page (SSRM scrolling)", lambda: cached.run(page_two)))

    print(f"{'case':<62} {'p50 ms':>9} {'p95 ms':>9}")
    for name, fn in cases:
        fn()  # warm-up
        p50, p95 = timed(fn, args.repeat)
        print(f"{name:<62} {p50:>9.1f} {p95:>9.1f}")


if __name__ == "__main__":
    main()
