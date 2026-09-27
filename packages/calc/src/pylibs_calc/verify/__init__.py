"""Cross-check the engine against the pure-Python reference evaluator.

``verify(engine, request)`` resolves the request exactly as ``engine.run`` would, takes the
dataset rows (a random sample of ``max_rows`` if there are more), runs the Polars engine and the
reference evaluator on those same rows and reports any difference. Use it in tests, in a
canary job, or before trusting a new Polars version in production.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from pylibs_calc.compile.mutations import apply_mutations as polars_mutations
from pylibs_calc.compile.query import TOTAL, leaf_frame
from pylibs_calc.config import CalcContext
from pylibs_calc.spec.canonical import fingerprint
from pylibs_calc.spec.query import CalcRequest

from . import reference
from .invariants import check_pages, check_rollup_totals

if TYPE_CHECKING:
    from pylibs_calc.engine import CalcEngine

__all__ = ["VerifyReport", "check_pages", "check_rollup_totals", "reference", "verify"]


@dataclass(frozen=True)
class VerifyReport:
    ok: bool
    fingerprint: str
    input_rows: int
    sampled: bool
    result_rows: int
    problems: tuple[str, ...]


def verify(
    engine: CalcEngine,
    request: CalcRequest | Mapping[str, Any],
    *,
    ctx: CalcContext | None = None,
    max_rows: int = 20_000,
    seed: int = 0,
    rel_tol: float = 1e-9,
    abs_tol: float = 1e-9,
) -> VerifyReport:
    req = engine.parse(CalcRequest, request)
    ctx = ctx or CalcContext()
    query = req.query.model_copy(update={"page": None})
    with engine._executor.slot():
        side = engine._resolve_side(req.dataset, req.scenario, req.what_if, ctx, False, None)
        logical = engine._plan_query(query, side)
        base = side.base.collect()
        sampled = base.height > max_rows
        if sampled:
            base = base.sample(n=max_rows, seed=seed)
        frame = polars_mutations(base.lazy(), side.mutations)
        if logical.aggregated:
            finished = engine.evaluate_aggregate(
                frame,
                logical,
                engine="in-memory",
                deadline=None,
                deterministic=req.options.deterministic,
            )
            actual = finished.frame.to_dicts()
            columns = finished.columns
            fields = finished.pivot_fields
        else:
            limits = engine.config.limits
            df = leaf_frame(frame, logical, limits, row_limit=max_rows + 1).collect()
            actual = df.drop(TOTAL).to_dicts()
            columns = dict(logical.output)
            fields = None
    rows = reference.apply_mutations(base.to_dicts(), side.mutations)
    expected = reference.run_query(rows, logical)
    problems = []
    if fields != expected.pivot_fields:
        problems.append(f"pivot fields differ: engine {fields}, reference {expected.pivot_fields}")
    if list(columns) != list(expected.columns):
        problems.append(
            f"columns differ: engine {list(columns)}, reference {list(expected.columns)}"
        )
    problems += reference.diff_rows(
        actual, expected.rows, expected.columns, rel_tol=rel_tol, abs_tol=abs_tol
    )
    identity = {"dataset": side.identity(), "query": query, "sample": [sampled, seed, max_rows]}
    return VerifyReport(
        ok=not problems,
        fingerprint=fingerprint(identity),
        input_rows=base.height,
        sampled=sampled,
        result_rows=len(actual),
        problems=tuple(problems),
    )
