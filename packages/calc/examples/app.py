"""Demo service: pylibs-calc behind FastAPI with an AG Grid (server-side row model) page.

    uv run --with uvicorn uvicorn --app-dir packages/calc/examples app:app --port 8000

Then open http://localhost:8000. Set ROWS to change the size of the synthetic book, and
REDIS_URL to keep scenarios in Redis instead of process memory.
"""

from __future__ import annotations

import os
from pathlib import Path

import polars as pl
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pylibs_calc import CalcEngine, Catalog, InMemoryScenarioStore, ScenarioStore, runtime_check
from pylibs_calc.integrations.fastapi import create_router


def synthetic_book(rows: int) -> pl.DataFrame:
    """Deterministic pseudo-random positions (no numpy needed)."""
    idx = pl.int_range(rows, dtype=pl.Int64, eager=True)

    def pick(values: list[str], salt: int) -> pl.Series:
        codes = (idx.hash(salt) % len(values)).cast(pl.Int64)
        return codes.replace_strict(list(range(len(values))), values, return_dtype=pl.String)

    unit = (idx.hash(99) % 1_000_000).cast(pl.Float64) / 1_000_000
    return pl.DataFrame(
        {
            "position_id": idx,
            "desk": pick(["Rates", "Credit", "Equities", "FX", "Commodities"], 1),
            "sector": pick(
                ["Tech", "Financials", "Energy", "Health", "Industrials", "Utilities"], 2
            ),
            "region": pick(["EMEA", "AMER", "APAC"], 3),
            "rating": pick(["AAA", "AA", "A", "BBB", "BB"], 4),
            "price": (unit * 200 + 1).round(2).cast(pl.Decimal(18, 2)),
            "quantity": ((idx.hash(5) % 20_000).cast(pl.Int64) - 10_000),
            "yield": (unit * 0.08).round(5),
        }
    ).with_columns(pl.col("desk", "sector", "region", "rating").cast(pl.Categorical))


def scenario_store() -> ScenarioStore:
    url = os.environ.get("REDIS_URL")
    if not url:
        return InMemoryScenarioStore()
    import redis

    from pylibs_calc.scenario.redis_store import RedisScenarioStore

    return RedisScenarioStore(redis.Redis.from_url(url))


runtime_check()
catalog = Catalog()
catalog.register_frame(
    "positions",
    synthetic_book(int(os.environ.get("ROWS", "200000"))),
    key_columns=["position_id"],
    editable=["price", "quantity", "yield", "rating"],
)
engine = CalcEngine(catalog, scenario_store())

app = FastAPI(title="pylibs-calc demo")
app.include_router(create_router(engine, prefix="/calc"))


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return (Path(__file__).parent / "grid.html").read_text()
