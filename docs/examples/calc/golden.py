"""Golden cases: requests over the example fund with their expected results.

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

MV = "price * quantity * fx_rate"  # market value in USD

CASES: list[dict[str, Any]] = [
    {
        "id": "sum-of-nothing-is-null",
        "title": "A sum over no rows is null, not 0",
        "why": "The fund holds no bonds in Japan (only bonds have a yield), so the Japan bond "
        "value is null (SQL semantics).",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "query": {
                "filter": "quantity > 0",
                "group_by": ["region"],
                "measures": [
                    {"name": "bonds", "fn": "sum", "of": MV, "where": "yield is not None"}
                ],
                "sort": [{"by": "region"}],
            },
        },
    },
    {
        "id": "null-condition-is-false",
        "title": "A null condition drops the row",
        "why": "yield is null for equities and cash, so `yield > 0` is null for them and they are "
        "filtered out; the six bonds remain.",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "query": {"filter": "yield > 0", "measures": [{"name": "n", "fn": "count_rows"}]},
        },
    },
    {
        "id": "three-valued-or",
        "title": "`null or true` is true",
        "why": "Cash has a null yield, but `or asset_class == 'Cash'` makes the condition true.",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "query": {
                "filter": "yield > 0.05 or asset_class == 'Cash'",
                "select": ["security_id", "security"],
                "sort": [{"by": "security_id"}],
            },
        },
    },
    {
        "id": "half-even-shock",
        "title": "Shocked decimals round half-to-even",
        "why": "98.50 × 1.05 = 103.425, which rounds to 103.42 (even), not 103.43.",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "extensions": {
                "whatif": {"steps": [{"kind": "shock", "column": "price", "op": "pct", "value": 5}]}
            },
            "query": {"filter": "security_id == 1", "select": ["security_id", "price"]},
        },
    },
    {
        "id": "integer-shock-round",
        "title": "Integer shocks need `round`, then round half-to-even",
        "why": "2,500 shares × 1.033 = 2,582.5, which rounds to 2,582.",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "extensions": {
                "whatif": {
                    "steps": [
                        {
                            "kind": "shock",
                            "column": "quantity",
                            "op": "pct",
                            "value": "3.3",
                            "round": True,
                        }
                    ]
                }
            },
            "query": {"filter": "security_id == 8", "select": ["security_id", "quantity"]},
        },
    },
    {
        "id": "ratio-of-sums-at-every-level",
        "title": "Post ratios are ratios of sums at every rollup level",
        "why": "The fund-wide upside to target is total target value / total value − 1, not the "
        "mean of the regional upsides.",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "query": {
                "filter": "asset_class == 'Equity' and quantity > 0",
                "group_by": ["region"],
                "rollup": True,
                "measures": [
                    {"name": "mv", "fn": "sum", "of": MV},
                    {"name": "target_mv", "fn": "sum", "of": "target_price * quantity * fx_rate"},
                ],
                "post": [{"name": "upside", "expr": "target_mv / mv - 1"}],
                "sort": [{"by": "region"}],
            },
        },
    },
    {
        "id": "weights-sum-to-one-at-every-level",
        "title": "`total()` is the whole fund at every rollup level",
        "why": "Each asset class's weight is its share of the whole fund, and the grand total's "
        "weight is exactly 1.",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "query": {
                "filter": "quantity > 0",
                "group_by": ["asset_class"],
                "rollup": True,
                "measures": [{"name": "mv", "fn": "sum", "of": MV}],
                "post": [{"name": "weight", "expr": "mv / total(mv)"}],
                "sort": [{"by": "asset_class"}],
            },
        },
    },
    {
        "id": "wavg-skips-nulls",
        "title": "wavg ignores rows where the value or the weight is null",
        "why": "Only the bonds have yields; the fund-wide weighted yield uses them alone.",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "query": {
                "measures": [
                    {"name": "wavg_yield", "fn": "wavg", "of": "yield", "weight": f"float({MV})"}
                ]
            },
            "options": {"deterministic": True},
        },
    },
    {
        "id": "divide-by-zero-is-null",
        "title": "Division by zero gives null",
        "why": "The benchmark holds no cash, so the fund-to-benchmark ratio for cash is null.",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "query": {
                "filter": "asset_class == 'Cash'",
                "group_by": ["asset_class"],
                "measures": [
                    {"name": "fund", "fn": "sum", "of": MV},
                    {"name": "bench", "fn": "sum", "of": "price * bench_quantity * fx_rate"},
                ],
                "post": [{"name": "ratio", "expr": "fund / bench"}],
            },
        },
    },
    {
        "id": "override-flows-into-formula",
        "title": "Formulas are recomputed after later overrides",
        "why": "The market value formula is written first, the price override second; the market "
        "value uses the new price.",
        "kind": "run",
        "request": {
            "dataset": "holdings",
            "extensions": {
                "whatif": {
                    "steps": [
                        {"kind": "formula", "name": "mv", "expr": MV},
                        {
                            "kind": "override",
                            "edits": [
                                {"key": {"security_id": 1}, "column": "price", "value": "100.00"}
                            ],
                        },
                    ]
                }
            },
            "query": {"filter": "security_id == 1", "select": ["price", "quantity", "mv"]},
        },
    },
    {
        "id": "compare-pct-null-on-zero-base",
        "title": "Compare's percentage is null when the base is 0",
        "why": "The fund holds no Initech; after buying 10,000 shares its value goes from 0 to "
        "643,000, and a change from 0 has no percentage.",
        "kind": "compare",
        "request": {
            "dataset": "holdings",
            "extensions": {
                "whatif": {
                    "steps": [
                        {
                            "kind": "override",
                            "edits": [
                                {"key": {"security_id": 13}, "column": "quantity", "value": 10000}
                            ],
                        }
                    ]
                }
            },
            "query": {
                "filter": "security_id == 13",
                "group_by": ["security"],
                "measures": [{"name": "mv", "fn": "sum", "of": MV}],
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
