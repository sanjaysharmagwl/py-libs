"""Golden cases: requests over the example book with their expected results.

Each case pins one rule that is easy to get wrong (nulls, rounding, ratios of sums, ...). QA can
run them against a build, and they run in ``make test``:

    uv run python docs/examples/calc/golden.py            # check every case
    uv run python docs/examples/calc/golden.py --update   # re-record (review the diff!)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

from book import engine

CASES_FILE = Path(__file__).resolve().parent / "golden_cases.json"

CASES: list[dict[str, Any]] = [
    {
        "id": "sum-of-nothing-is-null",
        "title": "A sum over no rows is null, not 0",
        "why": "Commodities has no short positions, so its short notional is null (SQL semantics).",
        "kind": "run",
        "request": {
            "dataset": "positions",
            "query": {
                "group_by": ["desk"],
                "measures": [
                    {
                        "name": "short",
                        "fn": "sum",
                        "of": "price * quantity",
                        "where": "quantity < 0",
                    }
                ],
                "sort": [{"by": "desk"}],
            },
        },
    },
    {
        "id": "null-condition-is-false",
        "title": "A null condition drops the row",
        "why": "yield is null for equities, so `yield > 0` is null for them and they are "
        "filtered out.",
        "kind": "run",
        "request": {
            "dataset": "positions",
            "query": {"filter": "yield > 0", "measures": [{"name": "n", "fn": "count_rows"}]},
        },
    },
    {
        "id": "three-valued-or",
        "title": "`null or true` is true",
        "why": "Equities have a null yield, but `or desk == 'Equities'` makes the condition true.",
        "kind": "run",
        "request": {
            "dataset": "positions",
            "query": {
                "filter": "yield > 0.05 or desk == 'Equities'",
                "select": ["position_id", "desk"],
                "sort": [{"by": "position_id"}],
            },
        },
    },
    {
        "id": "half-even-shock",
        "title": "Shocked decimals round half-to-even",
        "why": "102.10 × 1.05 = 107.205, which rounds to 107.20 (even), not 107.21.",
        "kind": "run",
        "request": {
            "dataset": "positions",
            "what_if": [{"kind": "shock", "column": "price", "op": "pct", "value": 5}],
            "query": {"filter": "position_id == 6", "select": ["position_id", "price"]},
        },
    },
    {
        "id": "integer-shock-round",
        "title": "Integer shocks need `round`, then round half-to-even",
        "why": "−500 × 1.033 = −516.5, which rounds to −516.",
        "kind": "run",
        "request": {
            "dataset": "positions",
            "what_if": [
                {"kind": "shock", "column": "quantity", "op": "pct", "value": "3.3", "round": True}
            ],
            "query": {"filter": "position_id == 2", "select": ["position_id", "quantity"]},
        },
    },
    {
        "id": "ratio-of-sums-at-every-level",
        "title": "Post ratios are ratios of sums at every rollup level",
        "why": "The grand-total avg_px is total notional / total quantity, not the mean of the "
        "regional averages.",
        "kind": "run",
        "request": {
            "dataset": "positions",
            "query": {
                "filter": "desk in ('Rates', 'Credit')",
                "group_by": ["region"],
                "rollup": True,
                "measures": [
                    {"name": "notional", "fn": "sum", "of": "price * quantity"},
                    {"name": "quantity", "fn": "sum", "of": "quantity"},
                ],
                "post": [{"name": "avg_px", "expr": "notional / quantity"}],
                "sort": [{"by": "region"}],
            },
        },
    },
    {
        "id": "wavg-skips-nulls",
        "title": "wavg ignores rows where the value or the weight is null",
        "why": "Only the six bonds have yields; the book-wide weighted yield uses them alone.",
        "kind": "run",
        "request": {
            "dataset": "positions",
            "query": {
                "measures": [
                    {
                        "name": "wavg_yield",
                        "fn": "wavg",
                        "of": "yield",
                        "weight": "abs(float(price * quantity))",
                    }
                ]
            },
            "options": {"deterministic": True},
        },
    },
    {
        "id": "divide-by-zero-is-null",
        "title": "Division by zero gives null",
        "why": "The Commodities desk has no shorts, so the count of shorts is 0 and the ratio "
        "is null.",
        "kind": "run",
        "request": {
            "dataset": "positions",
            "query": {
                "filter": "desk == 'Commodities'",
                "group_by": ["desk"],
                "measures": [
                    {"name": "long_qty", "fn": "sum", "of": "quantity", "where": "quantity > 0"},
                    {"name": "short_qty", "fn": "count", "of": "quantity", "where": "quantity < 0"},
                ],
                "post": [{"name": "ratio", "expr": "long_qty / short_qty"}],
            },
        },
    },
    {
        "id": "override-flows-into-formula",
        "title": "Formulas are recomputed after later overrides",
        "why": "The notional formula is written first, the price override second; notional uses "
        "the new price.",
        "kind": "run",
        "request": {
            "dataset": "positions",
            "what_if": [
                {"kind": "formula", "name": "notional", "expr": "price * quantity"},
                {
                    "kind": "override",
                    "edits": [{"key": {"position_id": 1}, "column": "price", "value": "100.00"}],
                },
            ],
            "query": {"filter": "position_id == 1", "select": ["price", "quantity", "notional"]},
        },
    },
    {
        "id": "compare-pct-null-on-zero-base",
        "title": "Compare's percentage is null when the base is 0",
        "why": "Before the override, the short count of Commodities is 0; after it, 1.",
        "kind": "compare",
        "request": {
            "dataset": "positions",
            "what_if": [
                {
                    "kind": "override",
                    "edits": [{"key": {"position_id": 12}, "column": "quantity", "value": -150}],
                }
            ],
            "query": {
                "filter": "desk == 'Commodities'",
                "group_by": ["desk"],
                "measures": [{"name": "shorts", "fn": "count_rows", "where": "quantity < 0"}],
            },
        },
    },
]


def run_case(case: dict[str, Any]) -> list[dict[str, Any]]:
    calc = engine()
    result = (
        calc.compare(case["request"]) if case["kind"] == "compare" else calc.run(case["request"])
    )
    return result.to_records(decimals="str")


def check() -> list[tuple[dict[str, Any], bool, list[dict[str, Any]]]]:
    expected = {c["id"]: c["expected"] for c in json.loads(CASES_FILE.read_text())}
    out = []
    for case in CASES:
        actual = run_case(case)
        out.append((case, expected.get(case["id"]) == actual, actual))
    return out


def update() -> None:
    recorded = [{**case, "expected": run_case(case)} for case in CASES]
    CASES_FILE.write_text(json.dumps(recorded, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    if "--update" in sys.argv:
        update()
        print(f"recorded {len(CASES)} cases in {CASES_FILE.name}")
    else:
        results = check()
        for case, ok, actual in results:
            print(
                f"{'PASS' if ok else 'FAIL'}  {case['id']}"
                + ("" if ok else f"\n      got {actual}")
            )
        sys.exit(0 if all(ok for _, ok, _ in results) else 1)
