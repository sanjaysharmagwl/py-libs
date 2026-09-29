"""A custom plugin: value the fund in a share class currency, and an FX sensitivity ladder."""

import statistics
from collections.abc import Mapping
from decimal import Decimal
from typing import Any

import polars as pl
from book import holdings, table
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


class ShareClass(Model):
    """The request block: ``{"share_class": {"currency": "GBP", "usd_rates": {"GBP": "1.27"}}}``.

    ``usd_rates`` is the value in USD of one unit of each currency (USD itself is always 1).
    """

    currency: str = "USD"
    usd_rates: dict[str, Decimal] = Field(default_factory=dict)

    def rate(self, currency: str) -> Decimal:
        return Decimal(1) if currency == "USD" else self.usd_rates[currency]


class ShareClassPlan(TransformPlan):
    """Adds ``mv_sc``: price x quantity, from the row's currency into the share class currency."""

    def __init__(self, sc: ShareClass, env: Mapping[str, LType]) -> None:
        self.sc = sc
        self.env = {**env, "mv_sc": FLOAT}  # the columns after the transform
        self.canonical = [  # the identity of what it does, part of every fingerprint
            {"kind": "share_class", "currency": sc.currency}
            | {"usd_rates": {k: str(v) for k, v in sorted(sc.usd_rates.items())}}
        ]

    def factors(self) -> dict[str, float]:
        """Per row currency: how many share class units one unit of it is worth."""
        target = self.sc.rate(self.sc.currency)
        return {c: float(r / target) for c, r in {"USD": Decimal(1), **self.sc.usd_rates}.items()}

    def apply(self, lf: pl.LazyFrame) -> pl.LazyFrame:  # Polars
        factor = pl.col("currency").replace_strict(
            self.factors(), default=None, return_dtype=pl.Float64
        )
        mv = pl.col("price").cast(pl.Float64) * pl.col("quantity") * factor
        return lf.with_columns(mv.alias("mv_sc"))

    def apply_reference(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:  # Python
        factors = self.factors()
        out = []
        for r in rows:
            factor = factors.get(r["currency"])
            mv = None
            if factor is not None and r["price"] is not None and r["quantity"] is not None:
                mv = float(r["price"]) * r["quantity"] * factor
            out.append({**r, "mv_sc": mv})
        return out

    def meta(self) -> dict[str, Any]:  # reported in result.meta.extensions["share_class"]
        return {"currency": self.sc.currency}


class ShareClassBound(Bound):
    def __init__(self, sc: ShareClass, path: str) -> None:
        self.sc = sc
        self.path = path

    @property
    def identity(self) -> Any:  # plans are cached under this
        return self.sc

    def plan(
        self, env: Mapping[str, LType], frame: pl.LazyFrame, pc: PlanContext
    ) -> ShareClassPlan:
        for column in ("currency", "price", "quantity"):
            if column not in env:
                raise SpecError(
                    f"share_class needs a {column} column", code="unknown_column", path=self.path
                )
        if self.sc.currency != "USD" and self.sc.currency not in self.sc.usd_rates:
            raise SpecError(
                f"no USD rate for the share class currency {self.sc.currency}",
                code="invalid_value",
                path=self.path,
            )
        return ShareClassPlan(self.sc, env)


def bind_share_class(sc: ShareClass, bc: BindContext) -> ShareClassBound:
    return ShareClassBound(sc, bc.path)


# --8<-- [end:transform]

# --8<-- [start:operation]


class Ladder(Model):
    """``engine.call("fx_ladder", {...})``: the query with the share class currency moved by
    each size, in percent, against every other currency."""

    dataset: str
    share_class: ShareClass
    moves: tuple[Decimal, ...]
    query: dict[str, Any]


def fx_ladder(kernel: Kernel, req: Ladder, ctx: CalcContext) -> CalcResult:
    frames = []
    base = kernel.parse(CalcRequest, {"dataset": req.dataset, "query": req.query})
    sc = req.share_class
    with kernel.slot():  # one execution slot for the whole ladder
        deadline = kernel.deadline(base.options)
        for move in req.moves:
            factor = 1 + move / 100
            rates = dict(sc.usd_rates)
            if sc.currency == "USD":  # a stronger dollar: every other currency is worth less
                rates = {k: v / factor for k, v in rates.items()}
            else:
                rates[sc.currency] = sc.usd_rates[sc.currency] * factor
            moved = ShareClass(currency=sc.currency, usd_rates=rates)
            view = kernel.resolve_view(base.dataset, {"share_class": moved}, ctx, deadline=deadline)
            result = kernel.query(view, base.query, base.options, ctx, deadline=deadline)
            frames.append(result.frame.with_columns(pl.lit(float(move)).alias("fx_move_pct")))
    ladder = pl.concat(frames)
    meta = result.meta.model_copy(update={"rows": ladder.height, "total_rows": ladder.height})
    return kernel.finish(CalcResult(ladder, meta), ctx)


# --8<-- [end:operation]

# --8<-- [start:plugin]


class ShareClassPlugin(Plugin):
    name = "share_class"
    version = "1.0"  # part of cache keys: bump it when results change

    def register(self, registry: Registry) -> None:
        registry.add_function(BPS)
        registry.add_aggregate(MEDIAN)
        registry.add_transform(TransformDef("share_class", ShareClass, bind_share_class))
        registry.add_operation(OperationDef("fx_ladder", Ladder, fx_ladder))
        registry.add_routes(self.routes)

    def routes(self, router: Any, kit: Any) -> None:
        @router.get("/share_class/functions")
        def functions() -> list[str]:
            return sorted(kit.engine.registry.functions)


catalog = Catalog()
catalog.register_frame("holdings", holdings(), key_columns=["security_id"])
engine = CalcEngine(catalog, plugins=[ShareClassPlugin()])
# --8<-- [end:plugin]

# --8<-- [start:use]
REQUEST = {
    "dataset": "holdings",
    "extensions": {
        "share_class": {
            "currency": "GBP",
            "usd_rates": {"EUR": "1.09", "GBP": "1.27", "JPY": "0.0067"},
        }
    },
    "query": {
        "filter": "quantity > 0",
        "derive": [{"name": "yield_bps", "expr": "bps(yield)"}],
        "group_by": ["currency"],
        "measures": [
            {"name": "mv_gbp", "fn": "sum", "of": "mv_sc"},
            {"name": "median_bps", "fn": "median", "of": "yield_bps"},
        ],
        "sort": [{"by": "currency"}],
    },
}
result = engine.run(REQUEST)
ladder = engine.call(
    "fx_ladder",
    {
        "dataset": "holdings",
        "share_class": REQUEST["extensions"]["share_class"],
        "moves": [-10, 0, 10],
        "query": {
            "filter": "quantity > 0",
            "measures": [{"name": "mv_gbp", "fn": "sum", "of": "mv_sc"}],
        },
    },
)
# --8<-- [end:use]

print("**`engine.run(REQUEST)`**\n")
print(table(result))
print(f"`meta.extensions`: `{result.meta.extensions}`\n")
print("**`engine.call('fx_ladder', ...)`**\n")
print(table(ladder))
print(f"**Reference evaluator agrees**: {verify(engine, REQUEST).ok}")
