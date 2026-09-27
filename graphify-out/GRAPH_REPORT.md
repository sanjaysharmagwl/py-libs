# Graph Report - py-libs  (2026-09-27)

## Corpus Check
- 139 files · ~69,332 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 6, .typed 3, .lock 1)

## Summary
- 1364 nodes · 3852 edges · 94 communities (81 shown, 13 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 545 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `580901aa`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- engine.py
- pytest
- py-libs
- CalcEngine
- AGENTS.md
- pylibs-core
- core/README.md
- utils/README.md
- compile/query.py
- reference.py
- .register_scan
- Catalog
- DatasetRef
- docs_from_graph.py
- CalcContext
- pylibs_calc/__init__.py
- Measure
- test_property.py
- fingerprint
- aggrid.py
- book.py
- Scenario
- create_router
- exprs.py
- ScenarioManager
- VersionConflict
- mutations.py
- manager.py
- test_fastapi.py
- ScenarioStore
- .collect
- Logic
- logical.py
- catalog.py
- errors.py
- exec.py
- spec/query.py
- ResultCache
- .append
- expr.py
- Ratios after aggregation
- LType
- scenarios/index.md
- Formula language
- Contributing to the docs
- fastapi.py
- engine
- adapters/__init__.py
- audit.md
- compile/__init__.py
- integrations/__init__.py
- spec/__init__.py
- pylibs-calc
- Numbers, types and nulls
- Limits
- Python API
- Filtered measures
- bench.py
- DatasetCatalog
- build_schema
- ColRef
- Dataset
- hooks.py
- fastapi.md
- Call the API with curl
- golden.py
- Lit
- Access control
- Pivot
- SpecError
- Saved scenarios and forks
- Shock a column
- FastAPI
- Disable a step
- positions
- _Converter
- request_of
- AG Grid
- .__init__
- InMemoryScenarioStore
- Run the demo grid
- pylibs-calc
- ._check
- pylibs-calc
- columns
- filter-derive.md
- Executor
- CalcResult
- Errors and limits
- ._keep_kind
- Performance
- _result_response
- 07_pivot.py

## God Nodes (most connected - your core abstractions)
1. `CalcEngine` - 135 edges
2. `LType` - 85 edges
3. `SpecError` - 70 edges
4. `CalcContext` - 45 edges
5. `Kind` - 45 edges
6. `AgGridAdapter` - 43 edges
7. `Scenario` - 39 edges
8. `Catalog` - 37 edges
9. `Typed` - 37 edges
10. `compile_expr()` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Options` --references--> `AgGridAdapter`  [INFERRED]
  docs/calc/integrations/fastapi.md → packages/calc/src/pylibs_calc/adapters/aggrid.py
- `Limits` --references--> `Limits`  [INFERRED]
  docs/calc/scenarios/errors-limits.md → packages/calc/src/pylibs_calc/config.py
- `Glossary` --references--> `CalcContext`  [INFERRED]
  docs/calc/glossary.md → packages/calc/src/pylibs_calc/config.py
- `Assumptions` --references--> `CalcContext`  [INFERRED]
  docs/calc/limitations.md → packages/calc/src/pylibs_calc/config.py
- `Test a service built on the engine` --references--> `CalcContext`  [INFERRED]
  docs/calc/qa/testing-guide.md → packages/calc/src/pylibs_calc/config.py

## Import Cycles
- None detected.

## Communities (94 total, 13 thin omitted)

### Community 0 - "engine.py"
Cohesion: 0.14
Nodes (20): collections, collections_abc, dataclasses, frame_size(), DataFrame, A byte-bounded LRU cache of result frames. Keys are content hashes of…, compare_frame(), LazyFrame (+12 more)

### Community 1 - "pytest"
Cohesion: 0.07
Nodes (30): CaptureFixture, parametrize, Run every documentation example, so a change that breaks the docs also breaks…, test_example_runs(), test_golden_cases(), hypothesis, importlib_metadata, MonkeyPatch (+22 more)

### Community 2 - "py-libs"
Cohesion: 0.22
Nodes (8): Adding a package, Building, Development, Layout, License, One-time setup, py-libs, Releasing

### Community 3 - "CalcEngine"
Cohesion: 0.06
Nodes (74): decimal, fakeredis, CalcEngine, column(), Any, parametrize, rows(), ssrm() (+66 more)

### Community 4 - "AGENTS.md"
Cohesion: 0.25
Nodes (6): Architecture and conventions, Code knowledge graph (graphify), Commands, Documentation, Releasing, What this is

### Community 9 - "compile/query.py"
Cohesion: 0.13
Nodes (35): materialize(), Compile and cast to the canonical dtype of the (rigid) result type., LogicalQuery, SortSpec, agg_frame(), _aggregate(), count_frame(), domain_frame() (+27 more)

### Community 10 - "reference.py"
Cohesion: 0.16
Nodes (32): functools, pivot_label(), Any, quantize(), aggregate_levels(), apply_mutations(), _binary(), _cast() (+24 more)

### Community 11 - ".register_scan"
Cohesion: 0.16
Nodes (15): Concepts, Formula language, Measures, Numbers, types and nulls, raw(), scan(), _check_keys(), content_version() (+7 more)

### Community 12 - "Catalog"
Cohesion: 0.18
Nodes (13): Catalog, Thread-safe in-process catalog of in-memory frames and lazily scanned files.…, DataFrame, parametrize, Path, test_categorical_keys_become_strings_and_enums_become_strings(), test_editable_and_roles(), test_normalizes_dtypes_and_nan() (+5 more)

### Community 13 - "DatasetRef"
Cohesion: 0.23
Nodes (10): ScenarioStep, The request for the pivot values, filtered by the filter model only (not by…, Translate a column filter model into one expression (``None`` if it filters…, Answer one SSRM ``getRows`` call end to end (engine: a :class:`CalcEngine`)., _type(), DatasetRef, Page, A dataset and, optionally, a pinned version (default: the latest registered). (+2 more)

### Community 14 - "docs_from_graph.py"
Cohesion: 0.11
Nodes (36): ack(), _clean(), _code(), digest(), find_stale(), front_matter_list(), generate(), Graph (+28 more)

### Community 15 - "CalcContext"
Cohesion: 0.11
Nodes (21): Architecture, Design principles, The parts, Two evaluators, one plan, M, CalcContext, Who is asking, and what they may see. Supplied by the host service per request.…, _ms() (+13 more)

### Community 16 - "pylibs_calc/__init__.py"
Cohesion: 0.12
Nodes (24): The life of a request, Python models, Quick start, Embeddable what-if calculation engine on Polars. Filters, overrides, shocks,…, Model, BaseModel, Frozen pydantic model that rejects unknown fields. Dumps always carry the…, CalcRequest (+16 more)

### Community 17 - "Measure"
Cohesion: 0.20
Nodes (6): Measure, Pivot, Any, model_validator, An aggregate per group. ``where`` works like SQL ``FILTER (WHERE ...)``: it…, Split measures into one column per combination of ``on`` values. Result columns…

### Community 18 - "test_property.py"
Cohesion: 0.07
Nodes (48): composite, DataObject, From dataset to result, Inside the query, Order of evaluation, Why the order matters, 1. Register data and create an engine, 2. Ask a question (+40 more)

### Community 19 - "fingerprint"
Cohesion: 0.13
Nodes (18): Node, Fingerprint of everything in the context that changes results (for cache keys)., canonical_json(), fingerprint(), Any, Bring a raw request dict up to the current ``spec_version``., JSON-ready canonical form of a model, or of plain data containing models., SHA-256 of the canonical JSON, as hex. (+10 more)

### Community 20 - "aggrid.py"
Cohesion: 0.11
Nodes (25): AgGridAdapter, CellEdit, ColumnVO, decode_group_key(), encode_group_key(), _Lenient, BaseModel, AG Grid Server-Side Row Model (SSRM) adapter. Pure translation; no web… (+17 more)

### Community 21 - "book.py"
Cohesion: 0.12
Nodes (15): Quick start: total exposure per desk., Measures: exposure, counts and weighted yield per desk., Filtered measures: long and short notional side by side, like SQL FILTER (WHERE…, Post-aggregation: average price as a ratio of sums, and gross leverage per…, Having: only the desks whose gross exposure is over their limit of 400,000., Rollup: book -> region -> desk subtotals in one result., Sort and page: the five largest positions by absolute market value, then the…, Override: a trader corrects two marks, and only those cells change. (+7 more)

### Community 22 - "Scenario"
Cohesion: 0.18
Nodes (8): LogEntry, BaseModel, Scenario, datetime, Scenario storage: the protocol, and a thread-safe in-memory implementation.…, Insert a new scenario (with initial entries when forking)., Append atomically if the log length is still ``expected_version``. Raises…, _Record

### Community 23 - "create_router"
Cohesion: 0.11
Nodes (26): APIRouter, ContextResolver, DependsParam, Check the runtime, Install, Working on the library itself, _call(), create_router() (+18 more)

### Community 24 - "exprs.py"
Cohesion: 0.22
Nodes (24): operator, as_type(), _binary(), _bool(), _cast(), compile_expr(), _convert_value(), dec_dtype() (+16 more)

### Community 25 - "ScenarioManager"
Cohesion: 0.23
Nodes (8): What to notice, effective_steps(), LabeledStep, A scenario step plus where it came from (for error paths and lineage)., Drop ``Disable`` steps and the steps they disable. Sequence numbers start at…, Copy a scenario's effective steps (at a version) into a new, independent…, Recompute the hash chain; False means the stored log was altered., ScenarioManager

### Community 26 - "VersionConflict"
Cohesion: 0.22
Nodes (9): A scenario append used a stale ``expected_version`` or pinned mismatching…, VersionConflict, Any, datetime, Redis-backed scenario store: shared by every replica of a service. Needs the…, RedisScenarioStore, _text(), Redis (+1 more)

### Community 27 - "mutations.py"
Cohesion: 0.13
Nodes (21): LogicalMutations, OverrideBatch, flush(), Consecutive overrides, compacted: column -> {key tuple: new value}. Last write…, ShockOp, apply_mutations(), _apply_overrides(), dtype_of() (+13 more)

### Community 28 - "manager.py"
Cohesion: 0.23
Nodes (13): Saved what-if scenarios: append-only, hash-chained logs of steps over a dataset…, Creating, editing, forking and auditing scenarios, with validation and…, Start an empty scenario pinned to a dataset version (default: the latest)., entry_hash(), genesis_hash(), make_entries(), now(), datetime (+5 more)

### Community 29 - "test_fastapi.py"
Cohesion: 0.19
Nodes (15): fastapi_testclient, io, client(), resolve(), fixture, parametrize, test_aggrid_rows_and_edit(), test_body_limit() (+7 more)

### Community 30 - "ScenarioStore"
Cohesion: 0.13
Nodes (10): FixtureRequest, scenario_store(), Protocol, Raise :class:`ScenarioNotFound` if missing (soft-deleted scenarios are…, Log entries 1..upto (default: all)., Scenarios that are not deleted, oldest first., Soft delete: the log is kept for audit., ScenarioStore (+2 more)

### Community 31 - ".collect"
Cohesion: 0.18
Nodes (9): InProcessQuery, _abandon(), _polars_message(), DataFrame, EngineName, Exception, LazyFrame, Collect ``lf``; past ``deadline`` (a ``time.monotonic()`` value) cancel and… (+1 more)

### Community 32 - "Logic"
Cohesion: 0.38
Nodes (9): _blank(), _date(), _equals(), _literal(), Any, Node, col(), IsNull (+1 more)

### Community 33 - "logical.py"
Cohesion: 0.14
Nodes (32): _and(), _col(), DerivePlan, FormulaDef, HiddenAgg, _materializable(), MeasurePlan, _order_formulas() (+24 more)

### Community 34 - "catalog.py"
Cohesion: 0.19
Nodes (13): glob, hashlib, _check_names(), file_version(), normalize(), DataType, Datasets the engine can query, pinned to immutable versions. A catalog…, Cast to the engine's canonical dtypes and turn NaN/infinite floats into nulls.… (+5 more)

### Community 35 - "errors.py"
Cohesion: 0.23
Nodes (14): Error codes, Exception classes, Scenario permissions, row(), CalcError, CalcTimeout, ComputeError, DatasetNotFound (+6 more)

### Community 36 - "exec.py"
Cohesion: 0.11
Nodes (17): contextlib, math, Performance and deployment, cgroup_cpu_limit(), Running Polars plans: concurrency slots, timeouts with cancellation, runtime…, Compare the Polars thread pool with the container's CPU limit (cgroup v1 or…, CPU limit from cgroup v2 ``cpu.max`` or v1 ``cpu.cfs_quota_us``; None if…, runtime_check() (+9 more)

### Community 37 - "spec/query.py"
Cohesion: 0.21
Nodes (8): datetime, Results: the frame plus metadata that makes it reproducible and auditable., Base model for every spec object: immutable, strict about unknown fields, self-…, Queries (views) and the top-level requests. A query runs its stages in a fixed…, Decimal, Scenario steps: what-if changes that keep every row of the dataset. A scenario…, The multiplier for ``mul``/``pct`` (``pct`` 5 means ``* 1.05``)., pydantic

### Community 39 - ".append"
Cohesion: 0.28
Nodes (8): Turn a pydantic error into a :class:`SpecError` with a JSON-pointer path., validation_error(), run(), parse_steps(), Any, ScenarioStep, Validate and append steps. Fails with a 409 if someone else appended first., ValidationError

### Community 40 - "expr.py"
Cohesion: 0.21
Nodes (19): Formulas are stored as trees, keyword, _Checker, Type checking: turns an expression tree into a :class:`Typed` tree against a…, Binary, Compare, Func, IfElse (+11 more)

### Community 41 - "Ratios after aggregation"
Cohesion: 0.17
Nodes (10): Gotchas, Ratios after aggregation, Result, Try it, What to notice, Gotchas, Result, Subtotals (rollup) (+2 more)

### Community 42 - "LType"
Cohesion: 0.17
Nodes (17): BinaryOp, Enum, arith_result(), common_type(), _conflict(), decimal(), _json_repr(), json_value() (+9 more)

### Community 44 - "Formula language"
Cohesion: 0.18
Nodes (9): Cheat sheet, Errors, Formula language, Functions, Gotchas, Measures, Result, Try it (+1 more)

### Community 45 - "Contributing to the docs"
Cohesion: 0.12
Nodes (12): Adding a feature page, Commands, Contributing to the docs, How the graph keeps the docs in step, Layout, Style, How these docs are organized, py-libs (+4 more)

### Community 46 - "fastapi.py"
Cohesion: 0.18
Nodes (10): fastapi, fastapi_params, fastapi_responses, get, index(), DataFrame, Demo service: pylibs-calc behind FastAPI with an AG Grid (server-side row…, Deterministic pseudo-random positions (no numpy needed). (+2 more)

### Community 47 - "engine"
Cohesion: 0.12
Nodes (9): Filter + derive: the EMEA positions and their notional., Shocks: Tech prices +5%, and yields +25bp on every bond., Disable: undo a saved step without rewriting history., Saved scenarios: create, append with optimistic locking, read old versions,…, Access control: a Rates trader sees only Rates rows and no yields., Audit a number: fingerprint, explain, and the independent reference evaluator., Errors and limits: every refusal has a stable code, a JSON-pointer path and an…, engine() (+1 more)

### Community 49 - "audit.md"
Cohesion: 0.25
Nodes (5): Also useful, Audit a number, Result, The three tools, Try it

### Community 54 - "Numbers, types and nulls"
Cohesion: 0.14
Nodes (12): Exact decimals, Float sums and reproducibility, Floats and decimals never mix silently, Invalid arithmetic gives null, Nulls follow SQL, Numbers, types and nulls, Settings, Shocks keep the column's type (+4 more)

### Community 55 - "Limits"
Cohesion: 0.16
Nodes (14): Checklist, Deploying on Kubernetes, Example, Reporting a problem, Troubleshooting, Limits, Hard caps that keep a single request from exhausting a pod. Exceeding one is a…, EngineConfig (+6 more)

### Community 56 - "Python API"
Cohesion: 0.14
Nodes (13): Data, Engine, Errors, Formulas and fingerprints, Integrations, Protocols, Python API, Requests (+5 more)

### Community 57 - "Filtered measures"
Cohesion: 0.17
Nodes (10): Filtered measures, Gotchas, Result, Try it, What to notice, Gotchas, Having, Result (+2 more)

### Community 58 - "bench.py"
Cohesion: 0.22
Nodes (10): argparse, numpy, book(), main(), Any, DataFrame, Latency benchmark for typical grid requests on a synthetic book of positions.…, timed() (+2 more)

### Community 59 - "DatasetCatalog"
Cohesion: 0.20
Nodes (8): Datasets and the catalog, Datasets without a key, Registering data, Versions, Your own catalog, DatasetCatalog, Protocol, What the engine needs from a catalog; implement it to serve datasets your own…

### Community 60 - "build_schema"
Cohesion: 0.29
Nodes (6): build_schema(), Collection, DataType, Role, The schema as seen by a caller limited to ``allowed`` columns (keys always…, Describe a dataset. Numeric columns default to measures, the rest to…

### Community 61 - "ColRef"
Cohesion: 0.15
Nodes (19): _coerce(), ColRef, Any, _alias_keywords(), parse_formula(), Render an expression tree as formula text (for display, lineage and error…, Parse a formula into an expression tree, or raise :class:`SpecError`., Rename keyword tokens used as column names (``yield``) so Python's parser… (+11 more)

### Community 62 - "Dataset"
Cohesion: 0.22
Nodes (4): Dataset, LazyFrame, One immutable version of a dataset., Keyless datasets carry a hidden ``__row`` column so row views have a total…

### Community 63 - "hooks.py"
Cohesion: 0.39
Nodes (7): on_config(), on_page_markdown(), on_pre_build(), Any, MkDocs hooks: make the examples importable, and flag pages the code has moved…, _sync_module(), importlib_util

### Community 64 - "fastapi.md"
Cohesion: 0.21
Nodes (5): Golden cases, Exploratory testing checklist, Test a service built on the engine, Testing guide, What to test, and how

### Community 65 - "Call the API with curl"
Cohesion: 0.22
Nodes (8): All routes, Call the API with curl, Discover the data, Get exact decimals, or Arrow, Run a query, See how a number is computed, Try a what-if, When something is wrong

### Community 66 - "golden.py"
Cohesion: 0.18
Nodes (13): check(), Any, Golden cases: requests over the example book with their expected results. Each…, run_case(), update(), json, os, pathlib (+5 more)

### Community 67 - "Lit"
Cohesion: 0.14
Nodes (14): field_validator, ComparePlan, plan_compare(), Two-way compare: join a target and a base result, with deltas typed like any…, canonical_decimal(), parse_decimal(), Shortest plain (non-exponent) text for a decimal; ``-0`` becomes ``0``., Parse a JSON number or numeric string into an exact decimal. (+6 more)

### Community 68 - "Access control"
Cohesion: 0.40
Nodes (5): Access control, Result, Try it, What to notice, Wiring it into FastAPI

### Community 69 - "Pivot"
Cohesion: 0.33
Nodes (6): Gotchas, Options, Pivot, Result, Try it, What to notice

### Community 70 - "SpecError"
Cohesion: 0.18
Nodes (14): What registration does, _check_name(), _editable(), plan_mutations(), Validate scenario steps (``Disable`` already resolved) against a dataset schema., coerce_value(), Any, Convert a JSON scalar into the Python value a column of ``ltype`` holds.… (+6 more)

### Community 71 - "Saved scenarios and forks"
Cohesion: 0.40
Nodes (5): Gotchas, Over HTTP, Result, Saved scenarios and forks, Try it

### Community 72 - "Shock a column"
Cohesion: 0.33
Nodes (6): Gotchas, Result, Shock a column, The operations, Try it, What to notice

### Community 73 - "FastAPI"
Cohesion: 0.40
Nodes (5): Errors, FastAPI, Options, Routes, Threading

### Community 74 - "Disable a step"
Cohesion: 0.40
Nodes (5): Disable a step, Gotchas, Result, Try it, What to notice

### Community 75 - "positions"
Cohesion: 0.40
Nodes (5): Pages, Scenarios by feature, The example book, positions(), DataFrame

### Community 76 - "_Converter"
Cohesion: 0.29
Nodes (7): AST, Call, Constant, _Converter, expr, Node, UnaryOp

### Community 77 - "request_of"
Cohesion: 0.40
Nodes (5): curl(), Any, Read the literal ``REQUEST = {...}`` from an example script, without running it., The curl call that sends an example's request to the demo service, as a code…, request_of()

### Community 78 - "AG Grid"
Cohesion: 0.50
Nodes (4): AG Grid, Client setup, Customizing the adapter, Gotchas

### Community 80 - "InMemoryScenarioStore"
Cohesion: 0.24
Nodes (7): Durability, How it works, Redis scenario store, Testing, ScenarioNotFound, InMemoryScenarioStore, Process-local store for tests and single-replica services.

### Community 81 - "Run the demo grid"
Cohesion: 0.67
Nodes (3): Run the demo grid, Start it, Things to try

### Community 82 - "pylibs-calc"
Cohesion: 0.67
Nodes (3): A request at a glance, pylibs-calc, What it does

### Community 83 - "._check"
Cohesion: 0.33
Nodes (6): lit_type(), _mismatch(), _need_bool(), _need_kind(), _need_numeric(), Node

### Community 84 - "pylibs-calc"
Cohesion: 0.29
Nodes (6): AG Grid (server-side row model), FastAPI, Not supported yet, pylibs-calc, Scenarios, versions and concurrency, Verifiability

### Community 85 - "columns"
Cohesion: 0.36
Nodes (8): children(), columns(), depth(), Node, Names of all columns an expression reads., Substitute column references (used to inline formula definitions)., replace_columns(), walk()

### Community 86 - "filter-derive.md"
Cohesion: 0.17
Nodes (10): Filter and derive, Gotchas, Result, Try it, What to notice, Gotchas, Result, Sort and page (+2 more)

### Community 87 - "Executor"
Cohesion: 0.40
Nodes (4): EngineBusy, No execution slot became free before the queue timeout., Executor, Hold one execution slot, or raise :class:`EngineBusy` after the queue timeout.

### Community 88 - "CalcResult"
Cohesion: 0.11
Nodes (14): 4. Read the metadata, Minimal requests, Request schema, What to notice, The measure functions, CalcResult, ColumnInfo, Any (+6 more)

### Community 89 - "Errors and limits"
Cohesion: 0.40
Nodes (5): Errors and limits, Limits, Result, Time and load, Try it

### Community 90 - "._keep_kind"
Cohesion: 0.50
Nodes (3): model_serializer, Any, SerializerFunctionWrapHandler

### Community 91 - "Performance"
Cohesion: 0.50
Nodes (3): Benchmarks, Guidance, Performance

### Community 92 - "_result_response"
Cohesion: 0.50
Nodes (4): run_compare(), run_query(), _result_response(), Response

## Knowledge Gaps
- **146 isolated node(s):** `pylibs-calc`, `pylibs-core`, `pylibs-utils`, `What this is`, `Commands` (+141 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 479 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CalcEngine` connect `CalcEngine` to `engine.py`, `pytest`, `compile/query.py`, `Catalog`, `DatasetRef`, `CalcContext`, `pylibs_calc/__init__.py`, `test_property.py`, `Scenario`, `create_router`, `ScenarioManager`, `VersionConflict`, `mutations.py`, `manager.py`, `test_fastapi.py`, `ScenarioStore`, `errors.py`, `ResultCache`, `LType`, `fastapi.py`, `engine`, `bench.py`, `DatasetCatalog`, `ColRef`, `Dataset`, `SpecError`, `Executor`, `CalcResult`?**
  _High betweenness centrality (0.164) - this node is a cross-community bridge._
- **Why does `CalcContext` connect `CalcContext` to `engine.py`, `CalcEngine`, `DatasetRef`, `pylibs_calc/__init__.py`, `test_property.py`, `fingerprint`, `aggrid.py`, `Scenario`, `create_router`, `ScenarioManager`, `manager.py`, `test_fastapi.py`, `.append`, `scenarios/index.md`, `fastapi.py`, `Numbers, types and nulls`, `Limits`, `fastapi.md`, `Access control`, `pylibs-calc`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Why does `SpecError` connect `SpecError` to `engine.py`, `CalcEngine`, `compile/query.py`, `.register_scan`, `Catalog`, `DatasetRef`, `CalcContext`, `pylibs_calc/__init__.py`, `fingerprint`, `aggrid.py`, `exprs.py`, `ScenarioManager`, `manager.py`, `Logic`, `logical.py`, `catalog.py`, `errors.py`, `.append`, `expr.py`, `LType`, `build_schema`, `ColRef`, `Lit`, `_Converter`, `._check`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Are the 39 inferred relationships involving `CalcEngine` (e.g. with `Your own catalog` and `main()`) actually correct?**
  _`CalcEngine` has 39 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `LType` (e.g. with `AgGridAdapter` and `_blank()`) actually correct?**
  _`LType` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 9 inferred relationships involving `SpecError` (e.g. with `Exception classes` and `AgGridAdapter`) actually correct?**
  _`SpecError` has 9 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `CalcContext` (e.g. with `Glossary` and `Assumptions`) actually correct?**
  _`CalcContext` has 13 INFERRED edges - model-reasoned connections that need verification._