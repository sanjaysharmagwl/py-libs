"""FastAPI router exposing a :class:`CalcEngine` (``pip install 'pylibs-calc[fastapi]'``).

::

    app = FastAPI()
    app.include_router(create_router(engine, prefix="/calc", context_resolver=my_auth))

Routes are plain ``def`` functions, so FastAPI runs them in its thread pool and the event loop
stays free while Polars computes. Errors come back as ``{"detail": {"code", "message", "path"}}``
with the status of the :class:`~pylibs_calc.errors.CalcError`.
"""

# No ``from __future__ import annotations`` here: FastAPI must see the route annotations, which
# refer to aliases defined inside ``create_router``, as real objects rather than strings.

from collections.abc import Callable, Sequence
from typing import Annotated, Any, Literal, TypeVar

try:
    from fastapi import APIRouter, Body, Depends, Header, HTTPException, Query, Request, Response
    from fastapi.params import Depends as DependsParam
    from fastapi.responses import JSONResponse
except ImportError as exc:  # pragma: no cover - exercised only without the extra
    raise ImportError(
        "the FastAPI integration needs fastapi: pip install 'pylibs-calc[fastapi]'"
    ) from exc

from pylibs_calc.adapters.aggrid import AgGridAdapter, CellEdit
from pylibs_calc.config import CalcContext
from pylibs_calc.engine import CalcEngine
from pylibs_calc.errors import CalcError, LimitExceeded
from pylibs_calc.result import CalcResult

ARROW_STREAM = "application/vnd.apache.arrow.stream"
T = TypeVar("T")
ContextResolver = Callable[[Request], CalcContext]
JsonBody = Annotated[dict[str, Any], Body()]


def _call(fn: Callable[[], T]) -> T:
    try:
        return fn()
    except CalcError as exc:
        raise HTTPException(status_code=exc.status, detail=exc.to_dict()) from exc


def _result_response(
    result: CalcResult, accept: str | None, decimals: Literal["float", "str"]
) -> Response:
    headers = {
        "X-Calc-Fingerprint": result.meta.fingerprint,
        "X-Calc-Total-Rows": str(result.meta.total_rows),
    }
    if accept and ARROW_STREAM in accept:
        return Response(result.to_arrow_ipc(), media_type=ARROW_STREAM, headers=headers)
    return JSONResponse(result.to_dict(decimals=decimals), headers=headers)


def create_router(
    engine: CalcEngine,
    *,
    prefix: str = "",
    tags: Sequence[str] = ("calc",),
    dependencies: Sequence[DependsParam] = (),
    context_resolver: ContextResolver | None = None,
    aggrid: AgGridAdapter | None = None,
    decimals: Literal["float", "str"] = "float",
    max_body_bytes: int = 5 * 1024 * 1024,
) -> APIRouter:
    """Build the router. ``context_resolver(request)`` turns your auth into a
    :class:`CalcContext` (principal, row filter, visible columns); ``dependencies`` run first,
    e.g. your authentication dependency."""
    adapter = aggrid or AgGridAdapter()

    def body_limit(request: Request) -> None:
        length = request.headers.get("content-length")
        if length is not None and length.isdigit() and int(length) > max_body_bytes:
            error = LimitExceeded(f"request body is larger than {max_body_bytes} bytes")
            raise HTTPException(status_code=error.status, detail=error.to_dict())

    def context(request: Request) -> CalcContext:
        return context_resolver(request) if context_resolver else CalcContext()

    router = APIRouter(
        prefix=prefix,
        tags=list(tags),
        dependencies=[*dependencies, Depends(body_limit)],
    )
    Ctx = Annotated[CalcContext, Depends(context)]
    Accept = Annotated[str | None, Header()]
    IdempotencyKey = Annotated[str | None, Header(alias="Idempotency-Key")]

    @router.get("/datasets")
    def list_datasets(ctx: Ctx) -> list[dict[str, Any]]:
        return [
            s.restrict(ctx.allowed_columns).model_dump(mode="json") for s in engine.catalog.list()
        ]

    @router.get("/datasets/{dataset_id}/schema")
    def dataset_schema(
        dataset_id: str, ctx: Ctx, version: Annotated[str | None, Query()] = None
    ) -> dict[str, Any]:
        return _call(lambda: engine.schema(dataset_id, version, ctx=ctx).model_dump(mode="json"))

    @router.post("/query")
    def run_query(body: JsonBody, ctx: Ctx, accept: Accept = None) -> Response:
        """Evaluate a CalcRequest; ``Accept: application/vnd.apache.arrow.stream`` for Arrow."""
        return _result_response(_call(lambda: engine.run(body, ctx)), accept, decimals)

    @router.post("/compare")
    def run_compare(body: JsonBody, ctx: Ctx, accept: Accept = None) -> Response:
        return _result_response(_call(lambda: engine.compare(body, ctx)), accept, decimals)

    @router.post("/explain")
    def run_explain(body: JsonBody, ctx: Ctx) -> dict[str, Any]:
        return _call(lambda: engine.explain(body, ctx))

    @router.post("/distinct")
    def distinct(body: JsonBody, ctx: Ctx) -> dict[str, Any]:
        """Body: ``{"dataset", "column", "scenario"?, "filter"?, "limit"?}``."""

        def run() -> dict[str, Any]:
            if "dataset" not in body or "column" not in body:
                raise CalcError("dataset and column are required", code="invalid_request")
            values = engine.distinct_values(
                body["dataset"],
                body["column"],
                scenario=body.get("scenario"),
                what_if=body.get("what_if") or (),
                filter=body.get("filter"),
                limit=int(body.get("limit", 1000)),
                ctx=ctx,
            )
            from pylibs_calc.result import json_safe

            return {"values": [json_safe(v, decimals) for v in values]}

        return _call(run)

    @router.post("/aggrid/rows")
    def aggrid_rows(body: JsonBody, ctx: Ctx) -> dict[str, Any]:
        """Body: ``{"dataset", "scenario"?, "what_if"?, "request": <SSRM getRows request>}``."""

        def run() -> dict[str, Any]:
            if "dataset" not in body or "request" not in body:
                raise CalcError("dataset and request are required", code="invalid_request")
            from pylibs_calc.scenario.manager import parse_steps

            response = adapter.rows(
                engine,
                body["request"],
                dataset=body["dataset"],
                scenario=body.get("scenario"),
                what_if=parse_steps(body.get("what_if") or [], "/what_if"),
                ctx=ctx,
            )
            return response.model_dump(mode="json")

        return _call(run)

    @router.post("/aggrid/edit")
    def aggrid_edit(
        body: JsonBody, ctx: Ctx, idempotency_key: IdempotencyKey = None
    ) -> dict[str, Any]:
        """Body: ``{"scenario", "expected_version", "edit": <cell edit event>, "note"?}``."""

        def run() -> dict[str, Any]:
            scenario = engine.scenarios.get(str(body.get("scenario")), ctx=ctx)
            schema = engine.schema(scenario.dataset.id, scenario.dataset.version, ctx=ctx)
            step = adapter.edit_to_override(CellEdit.model_validate(body.get("edit") or {}), schema)
            updated = engine.scenarios.append(
                scenario.id,
                [step],
                expected_version=int(body.get("expected_version", -1)),
                note=body.get("note"),
                client_op_id=idempotency_key,
                ctx=ctx,
            )
            return updated.model_dump(mode="json")

        return _call(run)

    @router.get("/scenarios")
    def list_scenarios(
        ctx: Ctx, dataset: Annotated[str | None, Query()] = None
    ) -> list[dict[str, Any]]:
        return _call(
            lambda: [
                s.model_dump(mode="json") for s in engine.scenarios.list(dataset=dataset, ctx=ctx)
            ]
        )

    @router.post("/scenarios", status_code=201)
    def create_scenario(body: JsonBody, ctx: Ctx) -> dict[str, Any]:
        """Body: ``{"dataset", "name", "description"?}``."""
        return _call(
            lambda: engine.scenarios.create(
                body.get("dataset", ""),
                str(body.get("name", "")),
                description=body.get("description"),
                ctx=ctx,
            ).model_dump(mode="json")
        )

    @router.get("/scenarios/{scenario_id}")
    def get_scenario(scenario_id: str, ctx: Ctx) -> dict[str, Any]:
        return _call(lambda: engine.scenarios.get(scenario_id, ctx=ctx).model_dump(mode="json"))

    @router.get("/scenarios/{scenario_id}/log")
    def scenario_log(
        scenario_id: str, ctx: Ctx, upto: Annotated[int | None, Query(ge=0)] = None
    ) -> list[dict[str, Any]]:
        return _call(
            lambda: [
                e.model_dump(mode="json")
                for e in engine.scenarios.log(scenario_id, upto=upto, ctx=ctx)
            ]
        )

    @router.post("/scenarios/{scenario_id}/steps")
    def append_steps(
        scenario_id: str, body: JsonBody, ctx: Ctx, idempotency_key: IdempotencyKey = None
    ) -> dict[str, Any]:
        """Body: ``{"steps", "expected_version", "note"?}``; 409 if the version is stale."""
        return _call(
            lambda: engine.scenarios.append(
                scenario_id,
                body.get("steps") or [],
                expected_version=int(body.get("expected_version", -1)),
                note=body.get("note"),
                client_op_id=idempotency_key,
                ctx=ctx,
            ).model_dump(mode="json")
        )

    @router.post("/scenarios/{scenario_id}/fork", status_code=201)
    def fork_scenario(scenario_id: str, body: JsonBody, ctx: Ctx) -> dict[str, Any]:
        """Body: ``{"name", "at_version"?, "description"?}``."""
        return _call(
            lambda: engine.scenarios.fork(
                scenario_id,
                name=str(body.get("name", "")),
                at_version=body.get("at_version"),
                description=body.get("description"),
                ctx=ctx,
            ).model_dump(mode="json")
        )

    @router.delete("/scenarios/{scenario_id}", status_code=204)
    def delete_scenario(scenario_id: str, ctx: Ctx) -> Response:
        _call(lambda: engine.scenarios.delete(scenario_id, ctx=ctx))
        return Response(status_code=204)

    @router.get("/scenarios/{scenario_id}/verify")
    def verify_scenario(scenario_id: str, ctx: Ctx) -> dict[str, Any]:
        """Recompute the scenario's hash chain."""

        def run() -> dict[str, Any]:
            engine.scenarios.get(scenario_id, ctx=ctx)
            return {"scenario": scenario_id, "intact": engine.scenarios.verify(scenario_id)}

        return _call(run)

    return router
