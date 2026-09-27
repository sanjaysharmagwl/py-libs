# Graph Report - py-libs  (2026-09-27)

## Corpus Check
- 68 files · ~39,775 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 9 file(s) not represented in the graph (top: (none) 5, .typed 3, .lock 1)

## Summary
- 995 nodes · 3202 edges · 54 communities (42 shown, 12 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 438 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f6144b84`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- engine.py
- test_runtime.py
- py-libs
- CalcEngine
- AGENTS.md
- pylibs-core
- core/README.md
- utils/README.md
- exprs.py
- LType
- SpecError
- Catalog
- compile/query.py
- reference.py
- .compare
- pylibs_calc/__init__.py
- formula.py
- test_property.py
- fingerprint
- AgGridAdapter
- aggrid.py
- Scenario
- create_router
- expr.py
- CalcContext
- VersionConflict
- ColRef
- manager.py
- test_fastapi.py
- ScenarioStore
- Executor
- Logic
- CalcResult
- logical.py
- CalcError
- Measure
- Query
- ResultCache
- .append
- run
- pylibs-calc
- HiddenAgg
- DatasetRef
- _abandon
- ._keep_kind
- synthetic_book
- model_validator
- adapters/__init__.py
- frame_size
- compile/__init__.py
- integrations/__init__.py
- spec/__init__.py
- pylibs-calc

## God Nodes (most connected - your core abstractions)
1. `CalcEngine` - 133 edges
2. `LType` - 85 edges
3. `SpecError` - 69 edges
4. `Kind` - 45 edges
5. `AgGridAdapter` - 41 edges
6. `CalcContext` - 41 edges
7. `Scenario` - 39 edges
8. `Typed` - 37 edges
9. `compile_expr()` - 35 edges
10. `Model` - 35 edges

## Surprising Connections (you probably didn't know these)
- `FastAPI` --references--> `CalcContext`  [INFERRED]
  packages/calc/README.md → packages/calc/src/pylibs_calc/config.py
- `Verifiability` --references--> `fingerprint()`  [INFERRED]
  packages/calc/README.md → packages/calc/src/pylibs_calc/spec/canonical.py
- `Concepts` --references--> `Catalog`  [INFERRED]
  packages/calc/README.md → packages/calc/src/pylibs_calc/catalog.py
- `Performance and deployment` --references--> `Limits`  [INFERRED]
  packages/calc/README.md → packages/calc/src/pylibs_calc/config.py
- `Scenarios, versions and concurrency` --references--> `RedisScenarioStore`  [INFERRED]
  packages/calc/README.md → packages/calc/src/pylibs_calc/scenario/redis_store.py

## Import Cycles
- None detected.

## Communities (54 total, 12 thin omitted)

### Community 0 - "engine.py"
Cohesion: 0.09
Nodes (37): collections, collections_abc, contextlib, dataclasses, datetime, decimal, fastapi_params, fastapi_responses (+29 more)

### Community 1 - "test_runtime.py"
Cohesion: 0.05
Nodes (39): hypothesis, importlib_metadata, Performance and deployment, cgroup_cpu_limit(), Compare the Polars thread pool with the container's CPU limit (cgroup v1 or…, CPU limit from cgroup v2 ``cpu.max`` or v1 ``cpu.cfs_quota_us``; None if…, runtime_check(), RuntimeReport (+31 more)

### Community 2 - "py-libs"
Cohesion: 0.22
Nodes (8): Adding a package, Building, Development, Layout, License, One-time setup, py-libs, Releasing

### Community 3 - "CalcEngine"
Cohesion: 0.06
Nodes (77): fakeredis, json, CalcEngine, The dataset's columns as ``ctx`` may see them., check_pages(), Any, Paging through a view yields each row exactly once, in the unpaged order., column() (+69 more)

### Community 4 - "AGENTS.md"
Cohesion: 0.29
Nodes (5): Architecture and conventions, Code knowledge graph (graphify), Commands, Releasing, What this is

### Community 9 - "exprs.py"
Cohesion: 0.08
Nodes (55): Enum, functools, operator, as_type(), _binary(), _bool(), _cast(), compile_expr() (+47 more)

### Community 10 - "LType"
Cohesion: 0.09
Nodes (45): BinaryOp, ComparePlan, plan_compare(), Two-way compare: join a target and a base result, with deltas typed like any…, _and(), _col(), FormulaDef, _materializable() (+37 more)

### Community 11 - "SpecError"
Cohesion: 0.07
Nodes (35): raw(), scan(), _check_keys(), _check_names(), content_version(), Dataset, file_version(), normalize() (+27 more)

### Community 12 - "Catalog"
Cohesion: 0.07
Nodes (32): argparse, numpy, book(), main(), Any, DataFrame, Latency benchmark for typical grid requests on a synthetic book of positions.…, timed() (+24 more)

### Community 13 - "compile/query.py"
Cohesion: 0.15
Nodes (30): LogicalQuery, SortSpec, agg_frame(), _aggregate(), count_frame(), domain_frame(), finish_aggregate(), Finished (+22 more)

### Community 14 - "reference.py"
Cohesion: 0.17
Nodes (31): pivot_label(), Any, quantize(), aggregate_levels(), apply_mutations(), _binary(), _cast(), compare_rows() (+23 more)

### Community 15 - ".compare"
Cohesion: 0.12
Nodes (17): M, compare_frame(), LazyFrame, _ms(), _page(), Any, DataFrame, A dataset version with a scenario applied, as one caller sees it. (+9 more)

### Community 16 - "pylibs_calc/__init__.py"
Cohesion: 0.12
Nodes (23): Embeddable what-if calculation engine on Polars. Filters, overrides, shocks,…, Model, BaseModel, Base model for every spec object: immutable, strict about unknown fields, self-…, Frozen pydantic model that rejects unknown fields. Dumps always carry the…, CompareRequest, Derive, PostAgg (+15 more)

### Community 17 - "formula.py"
Cohesion: 0.16
Nodes (18): AST, Call, Constant, keyword, IfElse, InList, ``arg in (values...)``; the values are non-null literals., ``then if cond else otherwise``; a null condition picks ``otherwise``. (+10 more)

### Community 18 - "test_property.py"
Cohesion: 0.16
Nodes (26): composite, DataObject, DrawFn, given, Concepts, Formula language, Measures, Numbers, types and nulls (+18 more)

### Community 19 - "fingerprint"
Cohesion: 0.11
Nodes (19): DatasetCatalog, Protocol, What the engine needs from a catalog; implement it to serve datasets your own…, canonical_json(), fingerprint(), Any, Bring a raw request dict up to the current ``spec_version``., JSON-ready canonical form of a model, or of plain data containing models. (+11 more)

### Community 20 - "AgGridAdapter"
Cohesion: 0.17
Nodes (17): AgGridAdapter, ScenarioStep, Translate SSRM requests into engine requests and results back into grid rows.…, The request for the pivot values, filtered by the filter model only (not by…, Translate a column filter model into one expression (``None`` if it filters…, Answer one SSRM ``getRows`` call end to end (engine: a :class:`CalcEngine`)., ``IServerSideGetRowsRequest`` as AG Grid sends it., ServerSideRequest (+9 more)

### Community 21 - "aggrid.py"
Cohesion: 0.13
Nodes (20): CellEdit, ColumnVO, decode_group_key(), encode_group_key(), _Lenient, BaseModel, AG Grid Server-Side Row Model (SSRM) adapter. Pure translation; no web…, The useful part of AG Grid's ``CellEditRequestEvent``. (+12 more)

### Community 22 - "Scenario"
Cohesion: 0.19
Nodes (10): ScenarioNotFound, LogEntry, BaseModel, Scenario, InMemoryScenarioStore, datetime, Scenario storage: the protocol, and a thread-safe in-memory implementation.…, Append atomically if the log length is still ``expected_version``. Raises… (+2 more)

### Community 23 - "create_router"
Cohesion: 0.14
Nodes (21): APIRouter, ContextResolver, DependsParam, _call(), create_router(), append_steps(), body_limit(), create_scenario() (+13 more)

### Community 24 - "expr.py"
Cohesion: 0.15
Nodes (19): field_validator, canonical_decimal(), parse_decimal(), Shortest plain (non-exponent) text for a decimal; ``-0`` becomes ``0``., Parse a JSON number or numeric string into an exact decimal., children(), _coerce(), columns() (+11 more)

### Community 25 - "CalcContext"
Cohesion: 0.16
Nodes (12): effective_steps(), LabeledStep, A scenario step plus where it came from (for error paths and lineage)., Drop ``Disable`` steps and the steps they disable. Sequence numbers start at…, CalcContext, Node, Who is asking, and what they may see. Supplied by the host service per request.…, Fingerprint of everything in the context that changes results (for cache keys). (+4 more)

### Community 26 - "VersionConflict"
Cohesion: 0.22
Nodes (9): A scenario append used a stale ``expected_version`` or pinned mismatching…, VersionConflict, Any, datetime, Redis-backed scenario store: shared by every replica of a service. Needs the…, RedisScenarioStore, _text(), Redis (+1 more)

### Community 27 - "ColRef"
Cohesion: 0.19
Nodes (17): ColRef, _alias_keywords(), parse_formula(), Render an expression tree as formula text (for display, lineage and error…, Parse a formula into an expression tree, or raise :class:`SpecError`., Rename keyword tokens used as column names (``yield``) so Python's parser…, to_formula(), test_filter_translation_is_readable() (+9 more)

### Community 28 - "manager.py"
Cohesion: 0.23
Nodes (13): Saved what-if scenarios: append-only, hash-chained logs of steps over a dataset…, Creating, editing, forking and auditing scenarios, with validation and…, Start an empty scenario pinned to a dataset version (default: the latest)., entry_hash(), genesis_hash(), make_entries(), now(), datetime (+5 more)

### Community 29 - "test_fastapi.py"
Cohesion: 0.19
Nodes (15): fastapi_testclient, io, client(), resolve(), fixture, parametrize, test_aggrid_rows_and_edit(), test_body_limit() (+7 more)

### Community 30 - "ScenarioStore"
Cohesion: 0.12
Nodes (10): FixtureRequest, scenario_store(), Protocol, Insert a new scenario (with initial entries when forking)., Raise :class:`ScenarioNotFound` if missing (soft-deleted scenarios are…, Log entries 1..upto (default: all)., Scenarios that are not deleted, oldest first., Soft delete: the log is kept for audit. (+2 more)

### Community 31 - "Executor"
Cohesion: 0.15
Nodes (13): CalcTimeout, ComputeError, EngineBusy, Polars failed while evaluating a valid request (overflow, bad cast in the data)., No execution slot became free before the queue timeout., Executor, _polars_message(), DataFrame (+5 more)

### Community 32 - "Logic"
Cohesion: 0.37
Nodes (10): _blank(), _date(), _equals(), _literal(), Any, Node, col(), Compare (+2 more)

### Community 33 - "CalcResult"
Cohesion: 0.19
Nodes (8): How to decorate result rows for the grid., Shape, CalcResult, json_safe(), Any, DataFrame, JSON-safe rows: decimals as floats (or exact strings), dates as ISO strings,…, The frame as an Arrow IPC stream (exact decimals, no JSON overhead).

### Community 34 - "logical.py"
Cohesion: 0.35
Nodes (11): _check_name(), DerivePlan, PivotPlan, _plan_pivot(), plan_query(), _plan_sort(), PostPlan, Logical plans: a validated, typed description of what a request computes. All… (+3 more)

### Community 35 - "CalcError"
Cohesion: 0.22
Nodes (7): CalcError, Forbidden, Any, Exception, Return the JSON body an API should send for this error., Base class for every error the engine raises on purpose. ``code`` is stable and…, authorize()

### Community 36 - "Measure"
Cohesion: 0.22
Nodes (6): Measure, Pivot, Any, model_validator, An aggregate per group. ``where`` works like SQL ``FILTER (WHERE ...)``: it…, Split measures into one column per combination of ``on`` values. Result columns…

### Community 37 - "Query"
Cohesion: 0.22
Nodes (6): Quick start, Query, Decimal, Change a column in bulk: ``add`` a value, ``mul`` by a factor or move by…, The multiplier for ``mul``/``pct`` (``pct`` 5 means ``* 1.05``)., Shock

### Community 39 - ".append"
Cohesion: 0.32
Nodes (7): Turn a pydantic error into a :class:`SpecError` with a JSON-pointer path., validation_error(), parse_steps(), Any, ScenarioStep, Validate and append steps. Fails with a 409 if someone else appended first., ValidationError

### Community 40 - "run"
Cohesion: 0.25
Nodes (6): aggrid_edit(), aggrid_rows(), run(), distinct(), run(), verify_scenario()

### Community 41 - "pylibs-calc"
Cohesion: 0.29
Nodes (6): AG Grid (server-side row model), FastAPI, Not supported yet, pylibs-calc, Scenarios, versions and concurrency, Verifiability

### Community 42 - "HiddenAgg"
Cohesion: 0.38
Nodes (7): HiddenAgg, One aggregate over rows. ``sum`` of no values is null (SQL semantics)., _hidden(), _input_name(), _inputs(), Expr, One column per aggregate: its argument, null wherever the measure's ``where``…

### Community 43 - "DatasetRef"
Cohesion: 0.40
Nodes (4): ScenarioStep, Sorted distinct values of a column (nulls last), e.g. for a set filter., DatasetRef, A dataset and, optionally, a pinned version (default: the latest registered).

### Community 44 - "_abandon"
Cohesion: 0.50
Nodes (3): InProcessQuery, _abandon(), Cancel a background query and keep its handle alive until the worker is done.…

### Community 45 - "._keep_kind"
Cohesion: 0.50
Nodes (3): model_serializer, Any, SerializerFunctionWrapHandler

### Community 46 - "synthetic_book"
Cohesion: 0.50
Nodes (3): DataFrame, Deterministic pseudo-random positions (no numpy needed)., synthetic_book()

## Knowledge Gaps
- **20 isolated node(s):** `pylibs-calc`, `pylibs-core`, `pylibs-utils`, `What this is`, `Commands` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 311 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CalcEngine` connect `CalcEngine` to `engine.py`, `test_runtime.py`, `exprs.py`, `LType`, `SpecError`, `Catalog`, `compile/query.py`, `.compare`, `pylibs_calc/__init__.py`, `test_property.py`, `fingerprint`, `AgGridAdapter`, `Scenario`, `create_router`, `CalcContext`, `VersionConflict`, `ColRef`, `manager.py`, `test_fastapi.py`, `ScenarioStore`, `Executor`, `CalcResult`, `CalcError`, `Query`, `ResultCache`, `DatasetRef`?**
  _High betweenness centrality (0.189) - this node is a cross-community bridge._
- **Why does `SpecError` connect `SpecError` to `engine.py`, `CalcEngine`, `exprs.py`, `LType`, `Catalog`, `compile/query.py`, `.compare`, `pylibs_calc/__init__.py`, `formula.py`, `fingerprint`, `AgGridAdapter`, `aggrid.py`, `expr.py`, `CalcContext`, `ColRef`, `manager.py`, `Logic`, `logical.py`, `CalcError`, `.append`?**
  _High betweenness centrality (0.085) - this node is a cross-community bridge._
- **Why does `LType` connect `LType` to `Logic`, `CalcResult`, `logical.py`, `engine.py`, `CalcEngine`, `exprs.py`, `HiddenAgg`, `SpecError`, `compile/query.py`, `reference.py`, `.compare`, `AgGridAdapter`, `aggrid.py`?**
  _High betweenness centrality (0.067) - this node is a cross-community bridge._
- **Are the 38 inferred relationships involving `CalcEngine` (e.g. with `main()` and `ResultCache`) actually correct?**
  _`CalcEngine` has 38 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `LType` (e.g. with `AgGridAdapter` and `_blank()`) actually correct?**
  _`LType` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `SpecError` (e.g. with `AgGridAdapter` and `Catalog`) actually correct?**
  _`SpecError` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 32 inferred relationships involving `Kind` (e.g. with `AgGridAdapter` and `_blank()`) actually correct?**
  _`Kind` has 32 INFERRED edges - model-reasoned connections that need verification._