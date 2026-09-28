"""A custom plugin: report in USD with FX rates by region, and an FX sensitivity ladder."""

import statistics
from collections.abc import Mapping
from decimal import Decimal
from typing import Any

import polars as pl
from book import positions, table
from pydantic import Field

from pylibs_calc import (
    AggregateDef,
    BindContext,
    Bound,
    CalcContext,
    CalcEngine,
    CalcRequest,
    CalcResult,
    Catalog,
    FunctionDef,
    Kernel,
    OperationDef,
    PlanContext,
    Plugin,
    Registry,
    SpecError,
    TransformDef,
    TransformPlan,
)
from pylibs_calc.ext import FLOAT, NUMERIC, LType, Model
from pylibs_calc.verify import verify

# --8<-- [start:function]


def numbers_to_float(args: Any) -> LType:
    if any(a.kind not in NUMERIC for a in args):
        raise ValueError("needs numbers")
    return FLOAT


BPS = FunctionDef(
    name="bps",  # yield in basis points: bps(yield)
    typecheck=numbers_to_float,
    polars=lambda x: x * 10_000,
    reference=lambda x: float(x) * 10_000,
)

MEDIAN = AggregateDef(
    name="median",  # a measure: {"fn": "median", "of": "price"}
    typecheck=lambda arg: numbers_to_float([arg]),
    polars=lambda x: x.cast(pl.Float64).median(),
    reference=lambda values: statistics.median(float(v) for v in values),
)
# --8<-- [end:function]

# --8<-- [start:transform]


class Fx(Model):
    """The request block: ``{"fx": {"rates": {"EMEA": "1.08", ...}, "default": "1"}}``."""

    rates: dict[str, Decimal] = Field(default_factory=dict)
    default: Decimal = Decimal(1)


class FxPlan(TransformPlan):
    """Adds ``usd``: price x quantity x the rate of the row's region."""

    def __init__(self, fx: Fx, env: Mapping[str, LType]) -> None:
        self.fx = fx
        self.env = {**env, "usd": FLOAT}  # the columns after the transform
        self.canonical = [  # the identity of what it does, part of every fingerprint
            {"kind": "fx", "rates": {k: str(v) for k, v in sorted(fx.rates.items())}}
            | {"default": str(fx.default)}
        ]

    def apply(self, lf: pl.LazyFrame) -> pl.LazyFrame:  # Polars
        rate = pl.col("region").replace_strict(
            {k: float(v) for k, v in self.fx.rates.items()},
            default=float(self.fx.default),
            return_dtype=pl.Float64,
        )
        usd = pl.col("price").cast(pl.Float64) * pl.col("quantity") * rate
        return lf.with_columns(usd.alias("usd"))

    def apply_reference(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:  # Python
        out = []
        for r in rows:
            rate = float(self.fx.rates.get(r["region"], self.fx.default))
            usd = None
            if r["price"] is not None and r["quantity"] is not None:
                usd = float(r["price"]) * r["quantity"] * rate
            out.append({**r, "usd": usd})
        return out

    def meta(self) -> dict[str, Any]:  # reported in result.meta.extensions["fx"]
        return {"regions": sorted(self.fx.rates)}


class FxBound(Bound):
    def __init__(self, fx: Fx, path: str) -> None:
        self.fx = fx
        self.path = path

    @property
    def identity(self) -> Any:  # plans are cached under this
        return self.fx

    def plan(self, env: Mapping[str, LType], frame: pl.LazyFrame, pc: PlanContext) -> FxPlan:
        for column in ("region", "price", "quantity"):
            if column not in env:
                raise SpecError(
                    f"fx needs a {column} column", code="unknown_column", path=self.path
                )
        return FxPlan(self.fx, env)


def bind_fx(fx: Fx, bc: BindContext) -> FxBound:
    return FxBound(fx, bc.path)


# --8<-- [end:transform]

# --8<-- [start:operation]


class Ladder(Model):
    """``engine.call("fx_ladder", {...})``: the query at FX moves of each size, in percent."""

    dataset: str
    fx: Fx
    moves: tuple[Decimal, ...]
    query: dict[str, Any]


def fx_ladder(kernel: Kernel, req: Ladder, ctx: CalcContext) -> CalcResult:
    frames = []
    base = kernel.parse(CalcRequest, {"dataset": req.dataset, "query": req.query})
    with kernel.slot():  # one execution slot for the whole ladder
        deadline = kernel.deadline(base.options)
        for move in req.moves:
            factor = 1 + move / 100
            moved = Fx(
                rates={k: v * factor for k, v in req.fx.rates.items()},
                default=req.fx.default * factor,
            )
            view = kernel.resolve_view(base.dataset, {"fx": moved}, ctx, deadline=deadline)
            result = kernel.query(view, base.query, base.options, ctx, deadline=deadline)
            frames.append(result.frame.with_columns(pl.lit(float(move)).alias("fx_move_pct")))
    ladder = pl.concat(frames)
    meta = result.meta.model_copy(update={"rows": ladder.height, "total_rows": ladder.height})
    return kernel.finish(CalcResult(ladder, meta), ctx)


# --8<-- [end:operation]

# --8<-- [start:plugin]


class FxPlugin(Plugin):
    name = "fx"
    version = "1.0"  # part of cache keys: bump it when results change

    def register(self, registry: Registry) -> None:
        registry.add_function(BPS)
        registry.add_aggregate(MEDIAN)
        registry.add_transform(TransformDef("fx", Fx, bind_fx))
        registry.add_operation(OperationDef("fx_ladder", Ladder, fx_ladder))
        registry.add_routes(self.routes)

    def routes(self, router: Any, kit: Any) -> None:
        @router.get("/fx/functions")
        def functions() -> list[str]:
            return sorted(kit.engine.registry.functions)


catalog = Catalog()
catalog.register_frame("positions", positions(), key_columns=["position_id"])
engine = CalcEngine(catalog, plugins=[FxPlugin()])
# --8<-- [end:plugin]

# --8<-- [start:use]
REQUEST = {
    "dataset": "positions",
    "extensions": {"fx": {"rates": {"EMEA": "1.08", "APAC": "0.0067"}, "default": "1"}},
    "query": {
        "filter": "yield is not None",
        "derive": [{"name": "yield_bps", "expr": "bps(yield)"}],
        "group_by": ["region"],
        "measures": [
            {"name": "usd", "fn": "sum", "of": "usd"},
            {"name": "median_bps", "fn": "median", "of": "yield_bps"},
        ],
        "sort": [{"by": "region"}],
    },
}
result = engine.run(REQUEST)
ladder = engine.call(
    "fx_ladder",
    {
        "dataset": "positions",
        "fx": REQUEST["extensions"]["fx"],
        "moves": [-10, 0, 10],
        "query": {"measures": [{"name": "usd", "fn": "sum", "of": "usd"}]},
    },
)
# --8<-- [end:use]

print("**`engine.run(REQUEST)`**\n")
print(table(result))
print(f"`meta.extensions`: `{result.meta.extensions}`\n")
print("**`engine.call('fx_ladder', ...)`**\n")
print(table(ladder))
print(f"**Reference evaluator agrees**: {verify(engine, REQUEST).ok}")
