"""The fund every documentation example runs against.

A fictional multi-asset "Global Income Fund" (base currency USD) and its benchmark, a notional
60/40 blend of global equities and government bonds, in one dataset of fourteen securities.
``quantity`` is what the fund holds; ``bench_quantity`` is what the benchmark would hold if it
were a portfolio of about the same size. A security the fund doesn't own has ``quantity`` 0 (an
underweight); one outside the benchmark has ``bench_quantity`` 0 (an off-benchmark position).

Prices are in the security's own currency: per share for equities, per 100 of face value for
bonds (so bond quantities count 100s of face value), and 1.00 for cash. ``fx_rate`` turns one unit
of that currency into US dollars, so ``price * quantity * fx_rate`` is the market value in USD.
Only bonds have a ``rating``, ``yield`` and ``duration``; only equities have an analyst
``target_price``. Prices and rates are exact decimals, as they would be in a portfolio system.

The demo service in ``packages/calc_whatif/examples/app.py`` generates a large book with the same
columns, so the JSON requests in the docs also work against it with curl (with other numbers).
"""

from __future__ import annotations

import ast
import json
from decimal import Decimal
from pathlib import Path
from typing import Any

import polars as pl

from pylibs_calc import CalcEngine, CalcResult, Catalog
from pylibs_calc_whatif import InMemoryScenarioStore, WhatIfPlugin

HERE = Path(__file__).resolve().parent
DATASET_VERSION = "2026-09-30"

# The editable columns: what an override or a shock may change.
EDITABLE = ["price", "fx_rate", "quantity", "yield", "rating", "target_price"]

USD, EUR, GBP, JPY = "1.000000", "1.090000", "1.270000", "0.006700"

# security, asset class, sector, country, region, currency, fx, rating, price, quantity,
# bench_quantity, yield, duration, analyst, target price
_ROWS: list[tuple[Any, ...]] = [
    ("UST 4.25% 2034", "Fixed Income", "Government", "United States", "North America", "USD", USD,
     "AAA", "98.50", 18000, 16000, 0.0425, 7.9, None, None),
    ("Bund 2.5% 2033", "Fixed Income", "Government", "Germany", "Europe ex UK", "EUR", EUR,
     "AAA", "101.20", 8000, 9000, 0.025, 7.4, None, None),
    ("Gilt 4.0% 2031", "Fixed Income", "Government", "United Kingdom", "UK", "GBP", GBP,
     "AA", "99.10", 6000, 3000, 0.04, 5.2, None, None),
    ("JGB 0.9% 2032", "Fixed Income", "Government", "Japan", "Japan", "JPY", JPY,
     "A", "99.80", 0, 1350000, 0.009, 7.6, None, None),
    ("ACME Corp 5.1% 2030", "Fixed Income", "Information Technology", "United States",
     "North America", "USD", USD, "BBB", "97.25", 6000, 0, 0.051, 3.8, "raj", None),
    ("Globex 6.0% 2029", "Fixed Income", "Energy", "United Kingdom", "UK", "GBP", GBP,
     "BB", "88.40", 4000, 0, 0.062, 2.9, "raj", None),
    ("Umbrella Health", "Equity", "Health Care", "United States", "North America", "USD", USD,
     None, "45.60", 20000, 15000, None, None, "ana", "52.00"),
    ("Stark Industries", "Equity", "Industrials", "United States", "North America", "USD", USD,
     None, "312.75", 2500, 2000, None, None, "ana", "340.00"),
    ("Wayne Financial", "Equity", "Financials", "United Kingdom", "UK", "GBP", GBP,
     None, "58.10", 15000, 8000, None, None, "ana", "55.00"),
    ("Kaiju Motors", "Equity", "Consumer Discretionary", "Japan", "Japan", "JPY", JPY,
     None, "2450.00", 40000, 30000, None, None, "ana", "2900.00"),
    ("Nordwind Energie", "Equity", "Energy", "Germany", "Europe ex UK", "EUR", EUR,
     None, "38.20", 12000, 10000, None, None, "ana", "44.00"),
    ("Cyberdyne Systems", "Equity", "Information Technology", "United States", "North America",
     "USD", USD, None, "185.40", 5000, 8000, None, None, "ana", "210.00"),
    ("Initech", "Equity", "Information Technology", "United States", "North America", "USD", USD,
     None, "64.30", 0, 23000, None, None, "ana", "70.00"),
    ("USD Cash", "Cash", "Cash", "United States", "North America", "USD", USD,
     None, "1.00", 300000, 0, None, None, None, None),
]  # fmt: skip

_COLUMNS = [
    "security", "asset_class", "sector", "country", "region", "currency", "fx_rate", "rating",
    "price", "quantity", "bench_quantity", "yield", "duration", "analyst", "target_price",
]  # fmt: skip


def holdings() -> pl.DataFrame:
    """The fourteen securities, keyed by ``security_id``."""
    data: dict[str, list[Any]] = {"security_id": list(range(1, len(_ROWS) + 1))}
    for i, name in enumerate(_COLUMNS):
        data[name] = [row[i] for row in _ROWS]
    for name in ("price", "fx_rate", "target_price"):
        data[name] = [None if v is None else Decimal(v) for v in data[name]]
    return pl.DataFrame(
        data,
        schema_overrides={
            "fx_rate": pl.Decimal(18, 6),
            "price": pl.Decimal(18, 2),
            "target_price": pl.Decimal(18, 2),
            "quantity": pl.Int64,
            "bench_quantity": pl.Int64,
        },
    )


def engine() -> CalcEngine:
    """An engine with the fund registered as ``holdings`` and the what-if plugin installed,
    with an in-memory scenario store."""
    catalog = Catalog()
    catalog.register_frame(
        "holdings",
        holdings(),
        key_columns=["security_id"],
        version=DATASET_VERSION,
        editable=EDITABLE,
    )
    return CalcEngine(catalog, plugins=[WhatIfPlugin(store=InMemoryScenarioStore())])


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
        if abs(value) >= 100_000:  # money: no exponent, cents
            return f"{value:.2f}"
        return f"{value + 0.0:.6g}"  # + 0.0 turns -0.0 into 0.0
    return _escape(str(value))


def _escape(text: str) -> str:
    return text.replace("|", "\\|")
