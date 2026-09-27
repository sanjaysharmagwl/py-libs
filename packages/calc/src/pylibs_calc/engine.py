"""The calculation engine: resolve the dataset and scenario, plan, execute, cache, describe.

Typical embedding::

    catalog = Catalog()
    catalog.register_frame("positions", df, key_columns=["position_id"])
    engine = CalcEngine(catalog, InMemoryScenarioStore())
    result = engine.run({"dataset": "positions", "query": {"group_by": ["sector"], ...}})

Every method is synchronous and CPU-bound; call it from a worker thread (FastAPI does this for
plain ``def`` endpoints).
"""

from __future__ import annotations

import dataclasses
import hashlib
import time
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from importlib.metadata import version as package_version
from typing import Any, TypeVar

import polars as pl
from pydantic import BaseModel, ValidationError

from pylibs_calc.cache import ResultCache, frame_size
from pylibs_calc.catalog import ROW_INDEX, Dataset, DatasetCatalog
from pylibs_calc.compile.compare import compare_frame, plan_compare
from pylibs_calc.compile.exprs import compile_expr
from pylibs_calc.compile.logical import (
    LEVEL,
    LabeledStep,
    LogicalMutations,
    LogicalQuery,
    SortSpec,
    effective_steps,
    plan_mutations,
    plan_query,
)
from pylibs_calc.compile.mutations import apply_mutations, edit_keys_frame
from pylibs_calc.compile.query import (
    TOTAL,
    Finished,
    agg_frame,
    count_frame,
    domain_frame,
    finish_aggregate,
    leaf_frame,
    rows_frame,
    sort_frame,
    totals_frame,
)
from pylibs_calc.compile.validate import check_predicate
from pylibs_calc.config import CalcContext, Limits
from pylibs_calc.dtypes import LType, NumericConfig, Scalar, json_value
from pylibs_calc.errors import (
    CalcError,
    LimitExceeded,
    SpecError,
    VersionConflict,
    join_path,
)
from pylibs_calc.exec import EngineName, Executor
from pylibs_calc.result import CalcResult, ColumnInfo, ResultMeta
from pylibs_calc.scenario.manager import ScenarioManager
from pylibs_calc.scenario.model import LogEntry, Scenario
from pylibs_calc.scenario.store import ScenarioStore
from pylibs_calc.schema import DatasetSchema
from pylibs_calc.spec.canonical import fingerprint, upgrade
from pylibs_calc.spec.query import (
    CalcRequest,
    CompareRequest,
    DatasetRef,
    Options,
    Page,
    Query,
    ScenarioRef,
)
from pylibs_calc.spec.scenario import ScenarioStep

M = TypeVar("M", bound=BaseModel)
Authorizer = Callable[[CalcContext, str, "Scenario | None"], None]
ResultHook = Callable[[ResultMeta, CalcContext], None]

_FORMULA_CODES = {"formula_syntax", "formula_too_long", "formula_too_complex"}


@dataclass(frozen=True)
class EngineConfig:
    """Engine-wide settings.

    ``authorize(ctx, action, scenario)`` is called for scenario actions (``scenario.read``,
    ``scenario.write``, ``scenario.create``, ``scenario.delete``) and should raise
    :class:`~pylibs_calc.errors.Forbidden` to refuse. ``on_result(meta, ctx)`` sees every result,
    e.g. for an audit log.
    """

    numeric: NumericConfig = NumericConfig()
    limits: Limits = Limits()
    max_concurrent: int = 2
    queue_timeout_s: float = 10.0
    default_timeout_s: float | None = 60.0
    cache_bytes: int = 256 * 1024 * 1024
    authorize: Authorizer | None = None
    on_result: ResultHook | None = None


@dataclass
class Side:
    """A dataset version with a scenario applied, as one caller sees it."""

    dataset: Dataset
    schema: DatasetSchema
    scenario: Scenario | None
    scenario_version: int | None
    scenario_head: str | None
    mutations: LogicalMutations
    steps_fingerprint: str
    base: pl.LazyFrame
    frame: pl.LazyFrame
    unmatched: list[dict[str, Scalar]]

    def identity(self) -> dict[str, Any]:
        return {
            "dataset": [self.dataset.id, self.dataset.version],
            "steps": self.steps_fingerprint,
        }


def validation_error(exc: ValidationError, prefix: str = "") -> SpecError:
    """Turn a pydantic error into a :class:`SpecError` with a JSON-pointer path."""
    errors = exc.errors(include_url=False)
    first = errors[0]
    path = join_path(prefix, *first["loc"]) if first["loc"] else prefix or None
    code = first["type"] if first["type"] in _FORMULA_CODES else "invalid_request"
    message = str(first["msg"]).removeprefix("Value error, ")
    detail = {
        "errors": [
            {"path": join_path(prefix, *e["loc"]), "message": e["msg"], "type": e["type"]}
            for e in errors[:20]
        ]
    }
    return SpecError(message, code=code, path=path, detail=detail)


class CalcEngine:
    def __init__(
        self,
        catalog: DatasetCatalog,
        scenario_store: ScenarioStore | None = None,
        config: EngineConfig | None = None,
    ) -> None:
        self.catalog = catalog
        self.config = config or EngineConfig()
        self._executor = Executor(
            max_concurrent=self.config.max_concurrent, queue_timeout_s=self.config.queue_timeout_s
        )
        self.cache: ResultCache[Any] = ResultCache(self.config.cache_bytes)
        self._plans: ResultCache[Any] = ResultCache(64 * 1024 * 1024)
        self._scenarios = ScenarioManager(self, scenario_store) if scenario_store else None
        self.versions = {
            "pylibs-calc": package_version("pylibs-calc"),
            "polars": pl.__version__,
        }
        self._salt = fingerprint(
            {"versions": self.versions, "numeric": dataclasses.asdict(self.config.numeric)}
        )

    # --- Public API -------------------------------------------------------------------------

    @property
    def scenarios(self) -> ScenarioManager:
        if self._scenarios is None:
            raise CalcError(
                "this engine has no scenario store", code="no_scenario_store", detail={}
            )
        return self._scenarios

    def authorize(self, ctx: CalcContext, action: str, scenario: Scenario | None) -> None:
        if self.config.authorize is not None:
            self.config.authorize(ctx, action, scenario)

    def schema(
        self, dataset_id: str, version: str | None = None, *, ctx: CalcContext | None = None
    ) -> DatasetSchema:
        """The dataset's columns as ``ctx`` may see them."""
        ctx = ctx or CalcContext()
        return self.catalog.get(dataset_id, version).schema.restrict(ctx.allowed_columns)

    def run(
        self, request: CalcRequest | Mapping[str, Any], ctx: CalcContext | None = None
    ) -> CalcResult:
        """Evaluate a request and return the (paged) result with its metadata."""
        started = time.perf_counter()
        req = self.parse(CalcRequest, request)
        ctx = ctx or CalcContext()
        self._check_what_if(req.what_if, "/what_if")
        timings: dict[str, float] = {}
        with self._executor.slot():
            timings["queue"] = _ms(started)
            deadline = self._deadline(req.options)
            mark = time.perf_counter()
            side = self._resolve_side(
                req.dataset, req.scenario, req.what_if, ctx, req.options.strict_edits, deadline
            )
            logical = self._plan_query(req.query, side)
            timings["plan"] = _ms(mark)
            engine = self._engine_name(req.options, side.dataset)
            identity = self._identity(side.identity(), req.query, req.options, ctx)
            mark = time.perf_counter()
            if logical.aggregated:
                key = self._cache_key(identity, drop_page=True)
                finished, cached = self._aggregate(
                    side, logical, key, engine, deadline, req.options
                )
                frame = _page(finished.frame, req.query.page)
                total, columns, fields = (
                    finished.total_rows,
                    finished.columns,
                    finished.pivot_fields,
                )
            else:
                key = self._cache_key(identity, drop_page=False)
                frame, total, cached = self._leaf(side, logical, key, engine, deadline)
                columns, fields = logical.output, None
            timings["execute"] = _ms(mark)
            stage_rows = None
            if req.options.audit:
                stage_rows = self._stage_rows(side, logical, total, engine, deadline)
        timings["total"] = _ms(started)
        meta = self._meta(
            identity, side, frame, total, req.query.page, columns, fields, engine, cached, timings
        )
        if stage_rows is not None:
            meta = meta.model_copy(update={"stage_rows": stage_rows})
        return self._finish(frame, meta, ctx)

    def compare(
        self, request: CompareRequest | Mapping[str, Any], ctx: CalcContext | None = None
    ) -> CalcResult:
        """Run a query on two sides and join them with deltas (see :class:`CompareRequest`)."""
        started = time.perf_counter()
        req = self.parse(CompareRequest, request)
        ctx = ctx or CalcContext()
        self._check_what_if(req.what_if, "/what_if")
        self._check_what_if(req.base_what_if, "/base_what_if")
        timings: dict[str, float] = {}
        core = req.query.model_copy(update={"sort": (), "page": None})
        with self._executor.slot():
            timings["queue"] = _ms(started)
            deadline = self._deadline(req.options)
            strict = req.options.strict_edits
            target = self._resolve_side(
                req.dataset, req.scenario, req.what_if, ctx, strict, deadline
            )
            base = self._resolve_side(
                req.dataset, req.base, req.base_what_if, ctx, strict, deadline
            )
            lt, lb = self._plan_query(core, target), self._plan_query(core, base)
            engine = self._engine_name(req.options, target.dataset)
            identity = self._identity(
                {"compare": [target.identity(), base.identity()]}, req.query, req.options, ctx
            )
            mark = time.perf_counter()
            if lt.aggregated:
                keys = tuple(lt.group_by) + ((LEVEL,) if lt.rollup else ())
                plan = plan_compare(keys, lt.output, lb.output, lt.value_names, self.config.numeric)
                key = self._cache_key(identity, drop_page=True)
                hit = self.cache.get(key)
                cached = hit is not None
                if hit is None:
                    kt = self._cache_key(
                        self._identity(target.identity(), core, req.options, ctx), drop_page=True
                    )
                    kb = self._cache_key(
                        self._identity(base.identity(), core, req.options, ctx), drop_page=True
                    )
                    ft, _ = self._aggregate(target, lt, kt, engine, deadline, req.options)
                    fb, _ = self._aggregate(base, lb, kb, engine, deadline, req.options)
                    joined = compare_frame(ft.frame.lazy(), fb.frame.lazy(), plan).collect()
                    view = _with_sort(lt, req.query.sort, set(plan.output))
                    hit = sort_frame(joined, view)
                    self.cache.put(key, hit, frame_size(hit))
                total = hit.height
                frame = _page(hit, req.query.page)
                columns = plan.output
            else:
                keys = target.dataset.key_columns
                if not keys:
                    raise SpecError(
                        "comparing rows needs a dataset with key columns", code="no_key_columns"
                    )
                values = tuple(c for c in lt.select if c not in keys)
                plan = plan_compare(
                    keys,
                    lt.output | {k: lt.row_env[k] for k in keys},
                    lb.output | {k: lb.row_env[k] for k in keys},
                    values,
                    self.config.numeric,
                )
                view = _with_sort(lt, req.query.sort, set(plan.output))
                lf = compare_frame(
                    rows_frame(target.frame, lt), rows_frame(base.frame, lb), plan
                ).with_columns(pl.len().alias(TOTAL))
                sort_keys = [*view.sort, *(SortSpec(k, False, True) for k in keys)]
                lf = lf.sort(
                    [s.by for s in sort_keys],
                    descending=[s.desc for s in sort_keys],
                    nulls_last=[s.nulls_last for s in sort_keys],
                )
                page = req.query.page
                if page is not None:
                    lf = lf.slice(page.offset, page.limit)
                else:
                    lf = lf.head(self.config.limits.max_unpaged_rows + 1)
                key = self._cache_key(identity, drop_page=False)
                hit_leaf = self.cache.get(key)
                cached = hit_leaf is not None
                if hit_leaf is None:
                    df = self._executor.collect(lf, engine=engine, deadline=deadline)
                    if page is None and df.height > self.config.limits.max_unpaged_rows:
                        raise _too_many_rows(self.config.limits)
                    total = int(df[TOTAL][0]) if df.height else 0
                    hit_leaf = (df.drop(TOTAL), total)
                    self.cache.put(key, hit_leaf, frame_size(hit_leaf[0]))
                frame, total = hit_leaf
                columns = plan.output
            timings["execute"] = _ms(mark)
        timings["total"] = _ms(started)
        meta = self._meta(
            identity, target, frame, total, req.query.page, columns, None, engine, cached, timings
        )
        return self._finish(frame, meta, ctx)

    def explain(
        self, request: CalcRequest | Mapping[str, Any], ctx: CalcContext | None = None
    ) -> dict[str, Any]:
        """Describe what a request computes: effective steps, lineage, types and the Polars plan."""
        req = self.parse(CalcRequest, request)
        ctx = ctx or CalcContext()
        with self._executor.slot():
            deadline = self._deadline(req.options)
            side = self._resolve_side(
                req.dataset, req.scenario, req.what_if, ctx, req.options.strict_edits, deadline
            )
            logical = self._plan_query(req.query, side)
        if logical.aggregated:
            lf = agg_frame(side.frame, logical, deterministic=req.options.deterministic)
        else:
            lf = leaf_frame(side.frame, logical, self.config.limits)
        from pylibs_calc.spec.formula import to_formula

        formulas = {f.name: to_formula(f.typed.node) for f in side.mutations.formulas}
        derives = {d.name: to_formula(d.expr.node) for d in logical.derives}
        identity = self._identity(side.identity(), req.query, req.options, ctx)
        return {
            "fingerprint": fingerprint(identity),
            "dataset": {"id": side.dataset.id, "version": side.dataset.version},
            "scenario": None
            if side.scenario is None
            else {
                "id": side.scenario.id,
                "version": side.scenario_version,
                "head": side.scenario_head,
            },
            "steps": side.mutations.canonical,
            "lineage": {
                "changed_by": side.mutations.lineage,
                "formulas": formulas,
                "derived": derives,
            },
            "columns": {name: str(t) for name, t in logical.output.items()},
            "plan": lf.explain(),
        }

    def distinct_values(
        self,
        dataset: str | DatasetRef,
        column: str,
        *,
        scenario: str | ScenarioRef | None = None,
        what_if: Sequence[ScenarioStep | Mapping[str, Any]] = (),
        filter: str | None = None,
        limit: int = 1000,
        ctx: CalcContext | None = None,
    ) -> list[Any]:
        """Sorted distinct values of a column (nulls last), e.g. for a set filter."""
        request: dict[str, Any] = {
            "dataset": dataset if isinstance(dataset, str) else dataset.model_dump(),
            "what_if": list(what_if),
            "query": {"group_by": [column], "page": {"limit": limit}},
        }
        if scenario is not None:
            request["scenario"] = scenario if isinstance(scenario, str) else scenario.model_dump()
        if filter is not None:
            request["query"]["filter"] = filter
        result = self.run(request, ctx)
        return result.frame[column].to_list()

    def validate_steps(
        self,
        dataset: DatasetRef,
        steps: Sequence[tuple[str, ScenarioStep]],
        ctx: CalcContext,
    ) -> LogicalMutations:
        """Check a full scenario log against its dataset (used before every append)."""
        ds = self.catalog.get(dataset.id, dataset.version)
        labeled = [LabeledStep(label, step) for label, step in steps]
        with self._executor.slot():
            side = self._plan_side(ds, labeled, ctx, True, None, None, None, None)
        return side.mutations

    def parse(self, model: type[M], request: M | Mapping[str, Any]) -> M:
        if isinstance(request, model):
            return request
        if not isinstance(request, Mapping):
            raise SpecError(f"expected a {model.__name__} or a JSON object", code="invalid_request")
        try:
            return model.model_validate(upgrade(dict(request)))
        except ValidationError as exc:
            raise validation_error(exc) from None

    # --- Resolution -------------------------------------------------------------------------

    def _resolve_side(
        self,
        dataset_ref: DatasetRef,
        scenario_ref: ScenarioRef | None,
        what_if: Sequence[ScenarioStep],
        ctx: CalcContext,
        strict: bool,
        deadline: float | None,
    ) -> Side:
        entries: list[LogEntry] = []
        scenario = None
        version = None
        head = None
        if scenario_ref is not None:
            scenario = self.scenarios.get(scenario_ref.id, ctx=ctx)
            if scenario.dataset.id != dataset_ref.id:
                raise SpecError(
                    f"scenario {scenario.id} belongs to dataset {scenario.dataset.id}",
                    code="dataset_mismatch",
                    path="/scenario",
                )
            if dataset_ref.version is not None and dataset_ref.version != scenario.dataset.version:
                raise VersionConflict(
                    f"scenario {scenario.id} is pinned to version {scenario.dataset.version}",
                    path="/dataset/version",
                )
            version = scenario.version if scenario_ref.version is None else scenario_ref.version
            if version > scenario.version:
                raise SpecError(
                    f"scenario {scenario.id} has no version {version}",
                    code="invalid_version",
                    path="/scenario/version",
                )
            entries = self._entries(scenario, version)
            head = entries[-1].hash if entries else scenario.genesis
            dataset = self.catalog.get(scenario.dataset.id, scenario.dataset.version)
        else:
            dataset = self.catalog.get(dataset_ref.id, dataset_ref.version)
        labeled = [LabeledStep(join_path("/scenario/steps", e.seq), e.step) for e in entries]
        labeled += [LabeledStep(join_path("/what_if", i), s) for i, s in enumerate(what_if)]
        return self._plan_side(dataset, labeled, ctx, strict, deadline, scenario, version, head)

    def _plan_side(
        self,
        dataset: Dataset,
        labeled: list[LabeledStep],
        ctx: CalcContext,
        strict: bool,
        deadline: float | None,
        scenario: Scenario | None,
        version: int | None,
        head: str | None,
    ) -> Side:
        cfg = self.config.numeric
        schema = dataset.schema.restrict(ctx.allowed_columns)
        base = dataset.lazy()
        if ctx.allowed_columns is not None:
            visible = [c.name for c in schema.columns]
            base = base.select(visible + ([ROW_INDEX] if dataset.has_row_index else []))
        row_filter = ctx.row_filter_node()
        if row_filter is not None:
            typed = check_predicate(row_filter, schema.ltypes(), cfg, "/context/row_filter")
            base = base.filter(compile_expr(typed))
        plan_key = "plan:" + fingerprint(
            {
                "dataset": [dataset.id, dataset.version],
                "scenario": None if scenario is None else [scenario.id, version, head],
                # A saved scenario is identified by (id, version, head); only extra steps count.
                "steps": [s.step for s in labeled[version or 0 :]]
                if scenario
                else [s.step for s in labeled],
                "ctx": ctx.digest(),
                "salt": self._salt,
            }
        )
        cached = self._plans.get(plan_key)
        if cached is None:
            mutations = plan_mutations(effective_steps(labeled), schema, cfg, self.config.limits)
            steps_fp = fingerprint(mutations.canonical)
            unmatched = self._unmatched(base, mutations, deadline)
            cached = (mutations, steps_fp, unmatched)
            self._plans.put(plan_key, cached, 1024 + 64 * len(mutations.edit_keys))
        mutations, steps_fp, unmatched = cached
        if strict and unmatched:
            raise SpecError(
                f"{len(unmatched)} edit(s) match no row",
                code="unmatched_edits",
                detail={"keys": unmatched[:20]},
            )
        return Side(
            dataset=dataset,
            schema=schema,
            scenario=scenario,
            scenario_version=version,
            scenario_head=head,
            mutations=mutations,
            steps_fingerprint=steps_fp,
            base=base,
            frame=apply_mutations(base, mutations),
            unmatched=unmatched,
        )

    def _unmatched(
        self, base: pl.LazyFrame, mutations: LogicalMutations, deadline: float | None
    ) -> list[dict[str, Scalar]]:
        if not mutations.edit_keys:
            return []
        keys = list(mutations.key_columns)
        check = edit_keys_frame(mutations).lazy().join(base.select(keys), on=keys, how="anti")
        missing = self._executor.collect(check, engine="in-memory", deadline=deadline)
        types = [mutations.base_env[k] for k in keys]
        return [
            {k: json_value(v, t) for k, v, t in zip(keys, row, types, strict=True)}
            for row in missing.iter_rows()
        ]

    def _entries(self, scenario: Scenario, version: int) -> list[LogEntry]:
        key = f"entries:{scenario.id}:{version}"
        cached = self._plans.get(key)
        if cached is None:
            cached = self.scenarios.store.entries(scenario.id, upto=version)
            self._plans.put(key, cached, 512 * (len(cached) + 1))
        return list(cached)

    def _plan_query(self, query: Query, side: Side) -> LogicalQuery:
        return plan_query(
            query,
            side.mutations.env,
            self.config.numeric,
            self.config.limits,
            key_columns=side.dataset.key_columns,
        )

    # --- Execution --------------------------------------------------------------------------

    def _aggregate(
        self,
        side: Side,
        logical: LogicalQuery,
        key: str,
        engine: EngineName,
        deadline: float | None,
        options: Options,
    ) -> tuple[Finished, bool]:
        hit = self.cache.get(key)
        if hit is not None:
            return hit, True
        finished = self.evaluate_aggregate(
            side.frame,
            logical,
            engine=engine,
            deadline=deadline,
            deterministic=options.deterministic,
        )
        self.cache.put(key, finished, frame_size(finished.frame))
        return finished, False

    def evaluate_aggregate(
        self,
        frame: pl.LazyFrame,
        logical: LogicalQuery,
        *,
        engine: EngineName,
        deadline: float | None,
        deterministic: bool,
    ) -> Finished:
        """Aggregate, pivot and sort ``frame`` (no paging, no cache)."""
        collect = self._executor.collect
        agg = collect(
            agg_frame(frame, logical, deterministic=deterministic), engine=engine, deadline=deadline
        )
        domain = totals = None
        if logical.pivot is not None:
            if logical.pivot.domain is None:
                domain = collect(domain_frame(frame, logical), engine=engine, deadline=deadline)
            if logical.pivot.totals:
                totals = collect(
                    totals_frame(frame, logical, deterministic=deterministic),
                    engine=engine,
                    deadline=deadline,
                )
        return finish_aggregate(agg, logical, self.config.limits, domain=domain, totals=totals)

    def _leaf(
        self,
        side: Side,
        logical: LogicalQuery,
        key: str,
        engine: EngineName,
        deadline: float | None,
    ) -> tuple[pl.DataFrame, int, bool]:
        hit = self.cache.get(key)
        if hit is not None:
            return hit[0], hit[1], True
        limits = self.config.limits
        df = self._executor.collect(
            leaf_frame(side.frame, logical, limits), engine=engine, deadline=deadline
        )
        page = logical.page
        if page is None and df.height > limits.max_unpaged_rows:
            raise _too_many_rows(limits)
        if df.height:
            total = int(df[TOTAL][0])
        elif page is None or page.offset == 0:
            total = 0
        else:
            counted = self._executor.collect(
                count_frame(side.frame, logical), engine=engine, deadline=deadline
            )
            total = int(counted[TOTAL][0])
        frame = df.drop(TOTAL)
        self.cache.put(key, (frame, total), frame_size(frame))
        return frame, total, False

    def _stage_rows(
        self,
        side: Side,
        logical: LogicalQuery,
        total: int,
        engine: EngineName,
        deadline: float | None,
    ) -> dict[str, int]:
        collect = self._executor.collect
        base = collect(side.base.select(pl.len()), engine=engine, deadline=deadline).item()
        filtered = collect(count_frame(side.frame, logical), engine=engine, deadline=deadline)
        return {"dataset": int(base), "filtered": int(filtered[TOTAL][0]), "result": total}

    # --- Helpers ----------------------------------------------------------------------------

    def _identity(
        self, side: Mapping[str, Any], query: Query, options: Options, ctx: CalcContext
    ) -> dict[str, Any]:
        return {
            "spec_version": 1,
            "side": dict(side),
            "query": query,
            "deterministic": options.deterministic,
            "numeric": dataclasses.asdict(self.config.numeric),
            "context": ctx.digest(),
        }

    def _cache_key(self, identity: Mapping[str, Any], *, drop_page: bool) -> str:
        data = dict(identity)
        if drop_page:
            query = data["query"]
            assert isinstance(query, Query)
            data["query"] = query.model_copy(update={"page": None})
        return hashlib.sha256((fingerprint(data) + self._salt).encode()).hexdigest()

    def _deadline(self, options: Options) -> float | None:
        timeout = options.timeout_s or self.config.default_timeout_s
        return None if timeout is None else time.monotonic() + timeout

    def _engine_name(self, options: Options, dataset: Dataset) -> EngineName:
        if options.engine != "auto":
            return options.engine
        return "streaming" if dataset.kind == "scan" else "in-memory"

    def _check_what_if(self, steps: Sequence[ScenarioStep], path: str) -> None:
        if len(steps) > self.config.limits.max_what_if_steps:
            raise LimitExceeded(
                f"more than {self.config.limits.max_what_if_steps} what-if steps", path=path
            )

    def _meta(
        self,
        identity: Mapping[str, Any],
        side: Side,
        frame: pl.DataFrame,
        total: int,
        page: Page | None,
        columns: Mapping[str, LType],
        fields: list[str] | None,
        engine: str,
        cached: bool,
        timings: dict[str, float],
    ) -> ResultMeta:
        scenario = None
        if side.scenario is not None:
            scenario = ScenarioRef(id=side.scenario.id, version=side.scenario_version)
        return ResultMeta(
            fingerprint=fingerprint(identity),
            dataset=DatasetRef(id=side.dataset.id, version=side.dataset.version),
            scenario=scenario,
            scenario_head=side.scenario_head,
            total_rows=total,
            offset=page.offset if page else 0,
            rows=frame.height,
            columns=[ColumnInfo.of(n, t) for n, t in columns.items()],
            pivot_fields=fields,
            engine=engine,
            cached=cached,
            timings_ms=timings,
            unmatched_edits=side.unmatched[:100],
            versions=self.versions,
        )

    def _finish(self, frame: pl.DataFrame, meta: ResultMeta, ctx: CalcContext) -> CalcResult:
        if self.config.on_result is not None:
            self.config.on_result(meta, ctx)
        return CalcResult(frame, meta)


def _page(frame: pl.DataFrame, page: Page | None) -> pl.DataFrame:
    return frame if page is None else frame.slice(page.offset, page.limit)


def _with_sort(plan: LogicalQuery, sort: Sequence[Any], allowed: set[str]) -> LogicalQuery:
    specs = []
    for i, key in enumerate(sort):
        if key.by not in allowed:
            raise SpecError(
                f"cannot sort by {key.by}: not a column of this view",
                code="unknown_column",
                path=join_path("/query/sort", i, "by"),
            )
        if plan.rollup and key.by not in plan.group_by:
            raise SpecError(
                "with rollup, only group_by columns can be sorted",
                code="invalid_sort",
                path="/query/sort",
            )
        specs.append(SortSpec(key.by, key.desc, key.nulls_last))
    tiebreak = tuple(g for g in plan.tiebreak if g not in {s.by for s in specs})
    return dataclasses.replace(plan, sort=tuple(specs), tiebreak=tiebreak)


def _too_many_rows(limits: Limits) -> LimitExceeded:
    return LimitExceeded(
        f"the view has more than {limits.max_unpaged_rows} rows; request a page",
        code="too_many_rows",
    )


def _ms(since: float) -> float:
    return round((time.perf_counter() - since) * 1000, 3)
