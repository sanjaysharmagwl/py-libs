"""Demo service: pylibs-calc with the what-if plugin behind FastAPI, and an AG Grid
(server-side row model) page.

    uv run --with uvicorn uvicorn --app-dir packages/calc_whatif/examples app:app --port 8000

Then open http://localhost:8000. Set ROWS to change the size of the synthetic fund, and
REDIS_URL to keep scenarios in Redis instead of process memory.
"""

from __future__ import annotations

import os
from pathlib import Path

import polars as pl
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pylibs_calc import CalcEngine, Catalog, runtime_check
from pylibs_calc.integrations.fastapi import create_router
from pylibs_calc_whatif import InMemoryScenarioStore, ScenarioStore, WhatIfPlugin

USD_RATES = {"USD": 1.0, "EUR": 1.09, "GBP": 1.27, "JPY": 0.0067}


def synthetic_book(rows: int) -> pl.DataFrame:
    """Deterministic pseudo-random fund holdings (no numpy needed), with the same columns as the
    documentation's example fund (``docs/examples/calc/book.py``)."""
    idx = pl.int_range(rows, dtype=pl.Int64, eager=True)

    def pick(values: list[str], salt: int) -> pl.Series:
        codes = (idx.hash(salt) % len(values)).cast(pl.Int64)
        return codes.replace_strict(list(range(len(values))), values, return_dtype=pl.String)

    unit = (idx.hash(99) % 1_000_000).cast(pl.Float64) / 1_000_000
    frame = pl.DataFrame(
        {
            "security_id": idx + 1,
            "security": "Security " + (idx + 1).cast(pl.String),
            "asset_class": pick(["Equity", "Equity", "Fixed Income", "Cash"], 1),
            "sector": pick(
                [
                    "Information Technology",
                    "Financials",
                    "Health Care",
                    "Industrials",
                    "Energy",
                    "Consumer Discretionary",
                    "Government",
                ],
                2,
            ),
            "country": pick(["United States", "Germany", "United Kingdom", "Japan"], 3),
            "rating": pick(["AAA", "AA", "A", "BBB", "BB"], 4),
            "price": (unit * 200 + 1).round(2).cast(pl.Decimal(18, 2)),
            "quantity": (idx.hash(5) % 20_000).cast(pl.Int64),
            "bench_quantity": (idx.hash(6) % 20_000).cast(pl.Int64),
            "yield": (unit * 0.08).round(5),
            "duration": (unit * 10).round(1),
            "analyst": pick(["ana", "raj", "mei"], 7),
            "target_price": (unit * 220 + 1).round(2).cast(pl.Decimal(18, 2)),
        }
    )
    bond = pl.col("asset_class") == "Fixed Income"
    region = {
        "United States": "North America",
        "Germany": "Europe ex UK",
        "United Kingdom": "UK",
        "Japan": "Japan",
    }
    currency = {"United States": "USD", "Germany": "EUR", "United Kingdom": "GBP", "Japan": "JPY"}
    return frame.with_columns(
        pl.col("country").replace_strict(region).alias("region"),
        pl.col("country").replace_strict(currency).alias("currency"),
        pl.when(bond).then(pl.col("rating", "yield", "duration")),
        pl.when(pl.col("asset_class") == "Equity").then(pl.col("target_price")),
    ).select(
        "security_id",
        pl.col("security", "asset_class", "sector", "country", "region", "currency").cast(
            pl.Categorical
        ),
        pl.col("currency")
        .replace_strict(USD_RATES, return_dtype=pl.Float64)
        .cast(pl.Decimal(18, 6))
        .alias("fx_rate"),
        pl.col("rating").cast(pl.Categorical),
        "price",
        "quantity",
        "bench_quantity",
        "yield",
        "duration",
        pl.col("analyst").cast(pl.Categorical),
        "target_price",
    )


def scenario_store() -> ScenarioStore:
    url = os.environ.get("REDIS_URL")
    if not url:
        return InMemoryScenarioStore()
    import redis

    from pylibs_calc_whatif.scenario.redis_store import RedisScenarioStore

    return RedisScenarioStore(redis.Redis.from_url(url))


runtime_check()
catalog = Catalog()
catalog.register_frame(
    "holdings",
    synthetic_book(int(os.environ.get("ROWS", "200000"))),
    key_columns=["security_id"],
    editable=["price", "fx_rate", "quantity", "yield", "rating", "target_price"],
)
engine = CalcEngine(catalog, plugins=[WhatIfPlugin(store=scenario_store())])

app = FastAPI(title="pylibs-calc what-if demo")
app.include_router(create_router(engine, prefix="/calc"))


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (Path(__file__).parent / "grid.html").read_text()
