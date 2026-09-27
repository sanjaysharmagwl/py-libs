"""Logical plans: a validated, typed description of what a request computes.

All validation happens here. The Polars executor (:mod:`.mutations`, :mod:`.query`) and the
pure-Python reference (:mod:`pylibs_calc.verify.reference`) both execute these plans, so their
meaning is defined once.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Literal

from pylibs_calc.config import Limits
from pylibs_calc.dtypes import (
    BOOL,
    INT,
    NUMERIC,
    ORDERABLE,
    Kind,
    LType,
    NumericConfig,
    coerce_value,
    common_type,
    decimal_places,
    json_value,
)
from pylibs_calc.errors import LimitExceeded, SpecError, join_path
from pylibs_calc.schema import DatasetSchema
from pylibs_calc.spec.canonical import to_canonical
from pylibs_calc.spec.expr import Binary, ColRef, IsNull, Logic, Node, columns, replace_columns
from pylibs_calc.spec.query import Page, Query
from pylibs_calc.spec.scenario import Disable, Formula, Override, ScenarioStep, Shock

from .validate import Budget, Typed, check, check_predicate

ROW_INDEX = "__row"
LEVEL = "__level"

# --- Mutations --------------------------------------------------------------------------------


@dataclass(frozen=True)
class LabeledStep:
    """A scenario step plus where it came from (for error paths and lineage)."""

    label: str
    step: ScenarioStep


@dataclass(frozen=True)
class OverrideBatch:
    """Consecutive overrides, compacted: column -> {key tuple: new value}. Last write wins."""

    edits: dict[str, dict[tuple[Any, ...], Any]]
    labels: tuple[str, ...]


@dataclass(frozen=True)
class ShockOp:
    column: str
    ltype: LType
    op: Literal["add", "mul", "pct"]
    amount: Decimal  # the value to add, or the factor to multiply by (pct already converted)
    where: Typed | None
    round: bool
    label: str


@dataclass(frozen=True)
class FormulaDef:
    name: str
    typed: Typed
    ltype: LType
    label: str


@dataclass
class LogicalMutations:
    ops: list[OverrideBatch | ShockOp]
    formulas: list[FormulaDef]
    base_env: dict[str, LType]
    env: dict[str, LType]
    key_columns: tuple[str, ...]
    edit_keys: list[tuple[Any, ...]]
    canonical: list[Any]
    lineage: dict[str, list[str]] = field(default_factory=dict)

    @property
    def empty(self) -> bool:
        return not self.ops and not self.formulas


def effective_steps(steps: Sequence[LabeledStep], first_seq: int = 1) -> list[LabeledStep]:
    """Drop ``Disable`` steps and the steps they disable.

    Sequence numbers start at ``first_seq``.
    """
    disabled: set[int] = set()
    for offset, item in enumerate(steps):
        if isinstance(item.step, Disable):
            target = item.step.seq
            if not first_seq <= target < first_seq + offset:
                raise SpecError(
                    f"step {first_seq + offset} can only disable an earlier step, not {target}",
                    code="invalid_disable",
                    path=item.label,
                )
            if isinstance(steps[target - first_seq].step, Disable):
                raise SpecError(
                    "a disable step cannot itself be disabled",
                    code="invalid_disable",
                    path=item.label,
                )
            disabled.add(target)
    return [
        item
        for offset, item in enumerate(steps)
        if not isinstance(item.step, Disable) and first_seq + offset not in disabled
    ]


def plan_mutations(
    steps: Sequence[LabeledStep],
    schema: DatasetSchema,
    cfg: NumericConfig,
    limits: Limits,
) -> LogicalMutations:
    """Validate scenario steps (``Disable`` already resolved) against a dataset schema."""
    base_env = schema.ltypes()
    keys = schema.key_columns
    key_types = [base_env[k] for k in keys]
    ops: list[OverrideBatch | ShockOp] = []
    batch: dict[str, dict[tuple[Any, ...], Any]] = {}
    batch_labels: list[str] = []
    definitions: dict[str, tuple[Node, str]] = {}
    expanded: dict[str, Node] = {}
    edit_keys: dict[tuple[Any, ...], None] = {}
    canonical: list[Any] = []
    lineage: dict[str, list[str]] = {}
    n_edits = 0

    def flush() -> None:
        if batch:
            ops.append(OverrideBatch({c: dict(v) for c, v in batch.items()}, tuple(batch_labels)))
            batch.clear()
            batch_labels.clear()

    for item in steps:
        step, label = item.step, item.label
        if isinstance(step, Override):
            if not keys:
                raise SpecError(
                    "this dataset has no key columns, so cells cannot be overridden",
                    code="no_key_columns",
                    path=label,
                )
            n_edits += len(step.edits)
            if n_edits > limits.max_edits:
                raise LimitExceeded(f"more than {limits.max_edits} edits", path=label)
            normalized = []
            for i, edit in enumerate(step.edits):
                path = join_path(label, "edits", i)
                target = _editable(schema, edit.column, join_path(path, "column"))
                if set(edit.key) != set(keys):
                    raise SpecError(
                        f"an edit key needs exactly the key columns {list(keys)}",
                        code="invalid_key",
                        path=join_path(path, "key"),
                    )
                key = tuple(
                    coerce_value(edit.key[k], t, what=f"key {k}")
                    for k, t in zip(keys, key_types, strict=True)
                )
                if any(v is None for v in key):
                    raise SpecError("key values cannot be null", code="invalid_key", path=path)
                value = coerce_value(edit.value, target, what=f"value for {edit.column}")
                batch.setdefault(edit.column, {})[key] = value
                edit_keys[key] = None
                lineage.setdefault(edit.column, []).append(label)
                normalized.append(
                    {
                        "key": {
                            k: json_value(v, t)
                            for k, v, t in zip(keys, key, key_types, strict=True)
                        },
                        "column": edit.column,
                        "value": json_value(value, target),
                    }
                )
            batch_labels.append(label)
            canonical.append({"kind": "override", "edits": normalized})
            continue
        flush()
        if isinstance(step, Shock):
            ltype = _editable(schema, step.column, join_path(label, "column"))
            if ltype.kind not in NUMERIC:
                raise SpecError(
                    f"cannot shock non-numeric column {step.column}",
                    code="type_mismatch",
                    path=join_path(label, "column"),
                )
            amount = step.value if step.op == "add" else step.factor()
            if ltype.kind is Kind.INT and not step.round and amount != amount.to_integral_value():
                raise SpecError(
                    f"{step.column} holds whole numbers; set round=true to round shocked values",
                    code="needs_rounding",
                    path=label,
                )
            if ltype.kind is Kind.DECIMAL and (ltype.scale or 0) + decimal_places(amount) > 38:
                raise SpecError("shock value has too many decimal places", code="invalid_value")
            where = None
            if step.where is not None:
                node = replace_columns(step.where, expanded)
                budget = Budget(limits.max_expr_depth, limits.max_expr_nodes)
                where = check_predicate(node, base_env, cfg, join_path(label, "where"), budget)
            ops.append(ShockOp(step.column, ltype, step.op, amount, where, step.round, label))
            lineage.setdefault(step.column, []).append(label)
            canonical.append(to_canonical(step))
        elif isinstance(step, Formula):
            name = step.name
            if name in base_env:
                raise SpecError(
                    f"{name} is a dataset column; a formula needs a new name",
                    code="name_conflict",
                    path=join_path(label, "name"),
                )
            _check_name(name, join_path(label, "name"))
            definitions[name] = (step.expr, label)
            expanded[name] = replace_columns(step.expr, expanded)
            lineage.setdefault(name, []).append(label)
            canonical.append(to_canonical(step))
        else:  # Disable steps are resolved before planning.
            raise SpecError("unresolved disable step", code="invalid_disable", path=label)
    flush()

    formulas = _order_formulas(definitions, base_env, cfg, limits)
    env = dict(base_env)
    for f in formulas:
        env[f.name] = f.ltype
    return LogicalMutations(
        ops=ops,
        formulas=formulas,
        base_env=base_env,
        env=env,
        key_columns=keys,
        edit_keys=list(edit_keys),
        canonical=canonical,
        lineage=lineage,
    )


def _editable(schema: DatasetSchema, column: str, path: str) -> LType:
    meta = schema.column(column) if column in schema.ltypes() else None
    if meta is None:
        raise SpecError(
            f"unknown column: {column}", code="unknown_column", path=path, detail={"column": column}
        )
    if meta.role == "key":
        raise SpecError(f"key column {column} cannot be changed", code="not_editable", path=path)
    if not meta.editable:
        raise SpecError(f"column {column} is not editable", code="not_editable", path=path)
    return meta.ltype


def _check_name(name: str, path: str) -> None:
    if name.startswith("__"):
        raise SpecError(
            f"names starting with '__' are reserved: {name}", code="name_conflict", path=path
        )


def _order_formulas(
    definitions: Mapping[str, tuple[Node, str]],
    base_env: Mapping[str, LType],
    cfg: NumericConfig,
    limits: Limits,
) -> list[FormulaDef]:
    """Type-check formulas in dependency order (ties keep definition order); reject cycles."""
    deps = {name: columns(expr) & set(definitions) for name, (expr, _) in definitions.items()}
    order: list[str] = []
    done: set[str] = set()
    remaining = list(definitions)
    while remaining:
        ready = [n for n in remaining if deps[n] <= done]
        if not ready:
            cycle = sorted(remaining)
            raise SpecError(
                f"formulas depend on each other in a cycle: {cycle}",
                code="formula_cycle",
                path=definitions[cycle[0]][1],
                detail={"formulas": cycle},
            )
        for name in ready:
            order.append(name)
            done.add(name)
        remaining = [n for n in remaining if n not in done]
    env = dict(base_env)
    out = []
    for name in order:
        expr, label = definitions[name]
        budget = Budget(limits.max_expr_depth, limits.max_expr_nodes)
        typed = check(expr, env, cfg, join_path(label, "expr"), budget)
        ltype = _materializable(typed, join_path(label, "expr"))
        env[name] = ltype
        out.append(FormulaDef(name, typed, ltype, label))
    return out


def _materializable(typed: Typed, path: str) -> LType:
    ltype = typed.ltype.rigid()
    if ltype.kind is Kind.NULL:
        raise SpecError(
            "this expression is always null; cast it to give the column a type",
            code="type_mismatch",
            path=path,
        )
    return ltype


# --- Queries ----------------------------------------------------------------------------------

HiddenFn = Literal["sum", "count", "min", "max", "count_distinct", "count_rows"]


@dataclass(frozen=True)
class DerivePlan:
    name: str
    expr: Typed
    where: Typed | None
    otherwise: Typed | None
    ltype: LType


@dataclass(frozen=True)
class HiddenAgg:
    """One aggregate over rows. ``sum`` of no values is null (SQL semantics)."""

    name: str
    fn: HiddenFn
    arg: Typed | None
    where: Typed | None
    ltype: LType


@dataclass(frozen=True)
class MeasurePlan:
    name: str
    hidden: tuple[HiddenAgg, ...]
    final: Typed  # expression over the hidden aggregate columns
    ltype: LType


@dataclass(frozen=True)
class PostPlan:
    name: str
    expr: Typed
    ltype: LType


@dataclass(frozen=True)
class PivotPlan:
    on: tuple[str, ...]
    on_types: tuple[LType, ...]
    values: tuple[str, ...]
    domain: tuple[tuple[Any, ...], ...] | None
    totals: bool
    separator: str
    null_label: str


@dataclass(frozen=True)
class SortSpec:
    by: str
    desc: bool
    nulls_last: bool


@dataclass
class LogicalQuery:
    aggregated: bool
    filter: Typed | None
    derives: tuple[DerivePlan, ...]
    row_env: dict[str, LType]
    select: tuple[str, ...]
    group_by: tuple[str, ...]
    measures: tuple[MeasurePlan, ...]
    post: tuple[PostPlan, ...]
    having: Typed | None
    rollup: bool
    pivot: PivotPlan | None
    sort: tuple[SortSpec, ...]
    tiebreak: tuple[str, ...]
    page: Page | None
    output: dict[str, LType]
    value_types: dict[str, LType] = field(default_factory=dict)

    @property
    def value_names(self) -> tuple[str, ...]:
        return tuple(m.name for m in self.measures) + tuple(p.name for p in self.post)


def plan_query(
    query: Query,
    env: Mapping[str, LType],
    cfg: NumericConfig,
    limits: Limits,
    *,
    key_columns: tuple[str, ...],
    path: str = "/query",
) -> LogicalQuery:
    def budget() -> Budget:
        return Budget(limits.max_expr_depth, limits.max_expr_nodes)

    row_env = {k: v for k, v in env.items() if k != ROW_INDEX}
    visible = list(row_env)
    flt = None
    if query.filter is not None:
        flt = check_predicate(query.filter, row_env, cfg, join_path(path, "filter"), budget())

    derives = []
    for i, d in enumerate(query.derive):
        dpath = join_path(path, "derive", i)
        _check_name(d.name, join_path(dpath, "name"))
        if d.name in row_env:
            raise SpecError(
                f"column {d.name} already exists; derived columns need new names",
                code="name_conflict",
                path=join_path(dpath, "name"),
            )
        expr = check(d.expr, row_env, cfg, join_path(dpath, "expr"), budget())
        where = otherwise = None
        ltype = expr.ltype
        if d.where is not None:
            where = check_predicate(d.where, row_env, cfg, join_path(dpath, "where"), budget())
            if d.otherwise is not None:
                otherwise = check(
                    d.otherwise, row_env, cfg, join_path(dpath, "otherwise"), budget()
                )
                try:
                    ltype = common_type(expr.ltype, otherwise.ltype, "a derive and its otherwise")
                except SpecError as exc:
                    exc.path = dpath
                    raise
        ltype = _materializable(Typed(expr.node, ltype), join_path(dpath, "expr"))
        derives.append(DerivePlan(d.name, expr, where, otherwise, ltype))
        row_env[d.name] = ltype
        visible.append(d.name)

    if not query.aggregated:
        select = tuple(visible) if query.select is None else query.select
        for i, name in enumerate(select):
            if name not in row_env:
                raise _unknown(name, join_path(path, "select", i), row_env)
        sort = _plan_sort(query, path, allowed=set(row_env), fixed=None)
        tiebreak = key_columns or (ROW_INDEX,)
        if query.page is not None and query.page.limit > limits.max_page_size:
            raise LimitExceeded(
                f"page limit is above {limits.max_page_size}", path=join_path(path, "page")
            )
        return LogicalQuery(
            aggregated=False,
            filter=flt,
            derives=tuple(derives),
            row_env=row_env,
            select=select,
            group_by=(),
            measures=(),
            post=(),
            having=None,
            rollup=False,
            pivot=None,
            sort=sort,
            tiebreak=tuple(k for k in tiebreak if k not in {s.by for s in sort}),
            page=query.page,
            output={name: row_env[name] for name in select},
        )

    if len(query.group_by) > limits.max_group_by:
        raise LimitExceeded(f"more than {limits.max_group_by} group_by columns")
    if len(query.measures) + len(query.post) > limits.max_measures:
        raise LimitExceeded(f"more than {limits.max_measures} measures")
    if query.page is not None and query.page.limit > limits.max_page_size:
        raise LimitExceeded(
            f"page limit is above {limits.max_page_size}", path=join_path(path, "page")
        )

    output: dict[str, LType] = {}
    for i, name in enumerate(query.group_by):
        gpath = join_path(path, "group_by", i)
        if name not in row_env:
            raise _unknown(name, gpath, row_env)
        if row_env[name].kind is Kind.OTHER:
            raise SpecError(f"cannot group by {name}", code="unsupported_type", path=gpath)
        if name in output:
            raise SpecError(f"{name} is grouped twice", code="name_conflict", path=gpath)
        output[name] = row_env[name]
    if query.rollup:
        output[LEVEL] = INT

    measures = []
    for i, m in enumerate(query.measures):
        mpath = join_path(path, "measures", i)
        _check_name(m.name, join_path(mpath, "name"))
        if m.name in output:
            raise SpecError(
                f"{m.name} is already an output column", code="name_conflict", path=mpath
            )
        plan = _plan_measure(m, i, row_env, cfg, mpath, budget)
        measures.append(plan)
        output[m.name] = plan.ltype

    post = []
    for i, p in enumerate(query.post):
        ppath = join_path(path, "post", i)
        _check_name(p.name, join_path(ppath, "name"))
        if p.name in output:
            raise SpecError(
                f"{p.name} is already an output column", code="name_conflict", path=ppath
            )
        typed = check(p.expr, output, cfg, join_path(ppath, "expr"), budget())
        ltype = _materializable(typed, join_path(ppath, "expr"))
        post.append(PostPlan(p.name, typed, ltype))
        output[p.name] = ltype

    having = None
    if query.having is not None:
        having = check_predicate(query.having, output, cfg, join_path(path, "having"), budget())

    value_types = {m.name: m.ltype for m in measures} | {p.name: p.ltype for p in post}
    pivot = None
    if query.pivot is not None:
        pivot = _plan_pivot(query, row_env, measures, post, join_path(path, "pivot"))
        index = {k: v for k, v in output.items() if k in query.group_by or k == LEVEL}
        if pivot.totals:
            index.update({v: output[v] for v in pivot.values})
        allowed_sort = None  # pivot result fields are only known once the domain is
        output = index
    else:
        allowed_sort = set(output)
    fixed = set(query.group_by) if query.rollup else None
    sort = _plan_sort(query, path, allowed=allowed_sort, fixed=fixed)
    return LogicalQuery(
        aggregated=True,
        filter=flt,
        derives=tuple(derives),
        row_env=row_env,
        select=(),
        group_by=query.group_by,
        measures=tuple(measures),
        post=tuple(post),
        having=having,
        rollup=query.rollup,
        pivot=pivot,
        sort=sort,
        tiebreak=tuple(g for g in query.group_by if g not in {s.by for s in sort}),
        page=query.page,
        output=output,
        value_types=value_types,
    )


def _unknown(name: str, path: str, env: Mapping[str, LType]) -> SpecError:
    return SpecError(
        f"unknown column: {name}",
        code="unknown_column",
        path=path,
        detail={"column": name, "available": sorted(env)[:100]},
    )


def _plan_measure(
    m: Any, index: int, env: Mapping[str, LType], cfg: NumericConfig, path: str, budget: Any
) -> MeasurePlan:
    def hidden(j: int) -> str:
        return f"__m{index}_{j}"

    where = None
    if m.where is not None:
        where = check_predicate(m.where, env, cfg, join_path(path, "where"), budget())
    if m.fn == "count_rows":
        agg = HiddenAgg(hidden(0), "count_rows", None, where, INT)
        return MeasurePlan(m.name, (agg,), _col(agg.name, INT), INT)

    of_node: Node = m.of
    if not columns(of_node):
        raise SpecError(
            "a measure must read at least one column",
            code="invalid_measure",
            path=join_path(path, "of"),
        )
    if m.fn == "wavg":
        of_node = Binary(op="mul", left=m.of, right=m.weight)
        both = Logic(
            op="and",
            args=(IsNull(arg=m.of, negate=True), IsNull(arg=m.weight, negate=True)),
        )
        guard = check_predicate(both, env, cfg, path, budget())
        where = guard if where is None else _and(where, guard)
    arg = check(of_node, env, cfg, join_path(path, "of"), budget())
    arg_type = arg.ltype.rigid()
    fn = m.fn
    if fn in ("sum", "mean", "wavg") and arg_type.kind not in NUMERIC:
        raise SpecError(f"{fn} needs numbers, got {arg_type}", code="type_mismatch", path=path)
    if fn in ("min", "max") and arg_type.kind not in ORDERABLE:
        raise SpecError(f"{fn} needs orderable values", code="type_mismatch", path=path)

    if fn in ("sum", "min", "max"):
        agg = HiddenAgg(hidden(0), fn, arg, where, arg_type)
        return MeasurePlan(m.name, (agg,), _col(agg.name, arg_type), arg_type)
    if fn in ("count", "count_distinct"):
        agg = HiddenAgg(hidden(0), fn, arg, where, INT)
        return MeasurePlan(m.name, (agg,), _col(agg.name, INT), INT)
    if fn == "mean":
        total = HiddenAgg(hidden(0), "sum", arg, where, arg_type)
        count = HiddenAgg(hidden(1), "count", arg, where, INT)
        return _ratio(m.name, total, count, cfg, path)
    weight = check(m.weight, env, cfg, join_path(path, "weight"), budget())
    weight_type = weight.ltype.rigid()
    if weight_type.kind not in NUMERIC:
        raise SpecError("wavg weight must be numeric", code="type_mismatch", path=path)
    num = HiddenAgg(hidden(0), "sum", arg, where, arg_type)
    den = HiddenAgg(hidden(1), "sum", weight, where, weight_type)
    return _ratio(m.name, num, den, cfg, path)


def _ratio(name: str, num: HiddenAgg, den: HiddenAgg, cfg: NumericConfig, path: str) -> MeasurePlan:
    node = Binary(op="div", left=ColRef(name=num.name), right=ColRef(name=den.name))
    final = check(node, {num.name: num.ltype, den.name: den.ltype}, cfg, path)
    ltype = final.ltype.rigid()
    return MeasurePlan(name, (num, den), final, ltype)


def _col(name: str, ltype: LType) -> Typed:
    return Typed(ColRef(name=name), ltype)


def _and(a: Typed, b: Typed) -> Typed:
    return Typed(Logic(op="and", args=(a.node, b.node)), BOOL, (a, b))


def _plan_pivot(
    query: Query,
    env: Mapping[str, LType],
    measures: Sequence[MeasurePlan],
    post: Sequence[PostPlan],
    path: str,
) -> PivotPlan:
    spec = query.pivot
    assert spec is not None
    on_types = []
    for i, name in enumerate(spec.on):
        if name not in env:
            raise _unknown(name, join_path(path, "on", i), env)
        if name in query.group_by:
            raise SpecError(f"{name} is both grouped and pivoted", code="name_conflict", path=path)
        if env[name].kind is Kind.OTHER:
            raise SpecError(f"cannot pivot on {name}", code="unsupported_type", path=path)
        on_types.append(env[name])
    names = [m.name for m in measures] + [p.name for p in post]
    values = tuple(names) if spec.values is None else spec.values
    for i, value in enumerate(values):
        if value not in names:
            raise SpecError(
                f"pivot value {value} is not a measure",
                code="unknown_column",
                path=join_path(path, "values", i),
            )
    domain = None
    if spec.domain is not None:
        domain = tuple(
            tuple(
                coerce_value(v, t, what="pivot domain value")
                for v, t in zip(combo, on_types, strict=True)
            )
            for combo in spec.domain
        )
    return PivotPlan(
        on=spec.on,
        on_types=tuple(on_types),
        values=values,
        domain=domain,
        totals=spec.totals,
        separator=spec.separator,
        null_label=spec.null_label,
    )


def _plan_sort(
    query: Query, path: str, *, allowed: set[str] | None, fixed: set[str] | None
) -> tuple[SortSpec, ...]:
    seen: set[str] = set()
    out = []
    for i, key in enumerate(query.sort):
        spath = join_path(path, "sort", i, "by")
        if key.by in seen:
            raise SpecError(f"{key.by} is sorted twice", code="invalid_sort", path=spath)
        if allowed is not None and key.by not in allowed:
            raise SpecError(
                f"cannot sort by {key.by}: not a column of this view",
                code="unknown_column",
                path=spath,
            )
        if fixed is not None and key.by not in fixed:
            raise SpecError(
                "with rollup, only group_by columns can be sorted",
                code="invalid_sort",
                path=spath,
            )
        seen.add(key.by)
        out.append(SortSpec(key.by, key.desc, key.nulls_last))
    return tuple(out)
