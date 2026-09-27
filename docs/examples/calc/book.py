"""The book of positions every documentation example runs against.

Twelve positions across five desks, with the same columns as the demo service in
``packages/calc/examples/app.py``, so the JSON requests in the docs also work against the demo with
curl (the numbers differ, because the demo generates 200,000 rows).

Negative quantities are short positions. ``yield`` is null where it doesn't apply (equities and
FX). ``price`` is an exact decimal, as a mark would be in a risk system.
"""

from __future__ import annotations

import ast
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

import polars as pl

from pylibs_calc import CalcEngine, CalcResult, Catalog, InMemoryScenarioStore

HERE = Path(__file__).resolve().parent
DATASET_VERSION = "2026-09-30"


def positions() -> pl.DataFrame:
    d = Decimal
    return pl.DataFrame(
        {
            "position_id": list(range(1, 13)),
            "instrument": [
                "UST 4.25% 2034",
                "Bund 2.5% 2033",
                "JGB 0.9% 2032",
                "ACME Corp 5.1% 2030",
                "Globex 6.0% 2029",
                "Initech 4.8% 2031",
                "Umbrella Health",
                "Stark Industries",
                "Wayne Financial",
                "EUR/USD fwd",
                "USD/JPY fwd",
                "Brent Dec-26",
            ],
            "desk": [
                "Rates",
                "Rates",
                "Rates",
                "Credit",
                "Credit",
                "Credit",
                "Equities",
                "Equities",
                "Equities",
                "FX",
                "FX",
                "Commodities",
            ],
            "sector": [
                "Financials",
                "Financials",
                "Financials",
                "Tech",
                "Energy",
                "Tech",
                "Health",
                "Industrials",
                "Financials",
                "Financials",
                "Financials",
                "Energy",
            ],
            "region": [
                "AMER",
                "EMEA",
                "APAC",
                "AMER",
                "EMEA",
                "AMER",
                "AMER",
                "AMER",
                "EMEA",
                "EMEA",
                "APAC",
                "EMEA",
            ],
            "rating": ["AAA", "AAA", "A", "BBB", "BB", "BBB", "A", "AA", "A", "AA", "A", None],
            "price": [
                d("98.50"),
                d("101.20"),
                d("99.80"),
                d("97.25"),
                d("88.40"),
                d("102.10"),
                d("45.60"),
                d("312.75"),
                d("58.10"),
                d("1.09"),
                d("148.30"),
                d("82.15"),
            ],
            "quantity": [1000, -500, 2000, 800, 1200, -300, 5000, 400, -2500, 100000, -50000, 150],
            "yield": [
                0.0425,
                0.025,
                0.009,
                0.051,
                0.062,
                0.048,
                None,
                None,
                None,
                None,
                None,
                None,
            ],
        },
        schema_overrides={"price": pl.Decimal(18, 2)},
    )


def engine() -> CalcEngine:
    """An engine with the book registered as ``positions``, and an in-memory scenario store."""
    catalog = Catalog()
    catalog.register_frame(
        "positions",
        positions(),
        key_columns=["position_id"],
        version=DATASET_VERSION,
        editable=["price", "quantity", "yield", "rating"],
    )
    return CalcEngine(catalog, InMemoryScenarioStore())


def table(result: CalcResult | pl.DataFrame, *, max_rows: int = 20) -> str:
    """A result as a Markdown table (it renders as a table on the docs site)."""
    frame = result.frame if isinstance(result, CalcResult) else result
    header = "| " + " | ".join(_escape(c) for c in frame.columns) + " |"
    rule = "| " + " | ".join("---" for _ in frame.columns) + " |"
    lines = [header, rule]
    for row in frame.head(max_rows).iter_rows():
        lines.append("| " + " | ".join(_cell(v) for v in row) + " |")
    if frame.height > max_rows:
        lines.append(f"\n*… {frame.height - max_rows} more rows*")
    return "\n".join(lines) + "\n"


def request_of(script: str, name: str = "REQUEST") -> Any:
    """Read the literal ``REQUEST = {...}`` from an example script, without running it."""
    tree = ast.parse((HERE / script).read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(t, ast.Name) and t.id == name for t in node.targets
        ):
            return ast.literal_eval(node.value)
    raise KeyError(f"{script} has no top-level {name} = ...")


def curl(script: str, route: str = "/calc/query", name: str = "REQUEST") -> str:
    """The curl call that sends an example's request to the demo service, as a code block."""
    body = json.dumps(request_of(script, name), indent=2)
    return (
        "```bash\n"
        f"curl -s localhost:8000{route} \\\n"
        "  -H 'Content-Type: application/json' \\\n"
        f"  -d @- <<'JSON'\n{body}\nJSON\n```"
    )


def _cell(value: Any) -> str:
    if value is None:
        return "*null*"
    if isinstance(value, float):
        return f"{value + 0.0:.6g}"  # + 0.0 turns -0.0 into 0.0
    return _escape(str(value))


def _escape(text: str) -> str:
    return text.replace("|", "\\|")
