# Graph Report - py-libs  (2026-09-28)

## Corpus Check
- 158 files · ~77,440 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 6, .typed 4, .lock 1)

## Summary
- 1672 nodes · 4627 edges · 119 communities (102 shown, 17 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 661 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1fd42018`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- canonical.py
- importlib_metadata
- py-libs
- CalcEngine
- AGENTS.md
- pylibs-core
- core/README.md
- utils/README.md
- engine.py
- verify/reference.py
- .register_scan
- Catalog
- adapters/aggrid.py
- docs_from_graph.py
- CalcContext
- Model
- ext.py
- Compare two sides
- ._keep_kind
- LogicalMutations
- book.py
- test_plugins.py
- create_router
- exprs.py
- Kernel
- manager.py
- calc/tests/test_fastapi.py
- PlanContext
- golden.py
- Redis scenario store
- .collect
- View
- logical.py
- from_polars
- pylibs_calc/__init__.py
- calc/tests/test_runtime.py
- engine
- Limits
- columns
- Subtotals (rollup)
- Ratios after aggregation
- LType
- Errors and limits
- Contributing to the docs
- fastapi.py
- ResultCache
- adapters/__init__.py
- audit.md
- compile/__init__.py
- integrations/__init__.py
- spec/__init__.py
- pylibs-calc
- Numbers, types and nulls
- exec.py
- Python API
- Filtered measures
- bench.py
- DatasetSchema
- build_schema
- expr.py
- Dataset
- hooks.py
- fastapi.md
- Call the API with curl
- Pivot
- body_extensions
- Access control
- Assumptions and limitations
- Executor
- WhatIfPlugin
- Shock a column
- FastAPI
- Disable a step
- positions
- validate.py
- request_of
- AG Grid
- _call
- pylibs_calc_whatif/__init__.py
- Run the demo grid
- pylibs-calc
- Typed
- pylibs-calc
- model_validator
- Formula language
- model.py
- CalcResult
- Scenario
- add_routes
- plugins.py
- typing
- assert_matches_reference
- plugin.py
- LimitExceeded
- Registry
- measures
- test_plugin.py
- UsdBound
- pathlib
- Plugin
- OperationDef
- what_if
- calc/tests/conftest.py
- calc_whatif/tests/conftest.py
- calc_whatif/tests/test_fastapi.py
- Formula columns
- release_info.py
- TransformDef
- Quick start
- ResultMeta
- Override a cell
- discover_plugins
- FxPlugin
- Order of evaluation
- .__init__
- .call
- 15_access_control.py

## God Nodes (most connected - your core abstractions)
1. `CalcEngine` - 137 edges
2. `LType` - 98 edges
3. `SpecError` - 73 edges
4. `CalcContext` - 56 edges
5. `Kernel` - 48 edges
6. `Catalog` - 47 edges
7. `Kind` - 45 edges
8. `AgGridAdapter` - 41 edges
9. `Typed` - 40 edges
10. `Model` - 40 edges

## Surprising Connections (you probably didn't know these)
- `Options` --references--> `AgGridAdapter`  [INFERRED]
  docs/calc/integrations/fastapi.md → packages/calc/src/pylibs_calc/adapters/aggrid.py
- `Limits` --references--> `Limits`  [INFERRED]
  docs/calc/scenarios/errors-limits.md → packages/calc/src/pylibs_calc/config.py
- `Assumptions` --references--> `CalcContext`  [INFERRED]
  docs/calc/limitations.md → packages/calc/src/pylibs_calc/config.py
- `Test a service built on the engine` --references--> `CalcContext`  [INFERRED]
  docs/calc/qa/testing-guide.md → packages/calc/src/pylibs_calc/config.py
- `Errors` --references--> `CalcError`  [INFERRED]
  docs/calc/integrations/fastapi.md → packages/calc/src/pylibs_calc/errors.py

## Import Cycles
- 3-file cycle: `packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py`
- 4-file cycle: `packages/calc/src/pylibs_calc/compile/logical.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/logical.py`
- 4-file cycle: `packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/validate.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/compare.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/compare.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/logical.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/query.py -> packages/calc/src/pylibs_calc/compile/logical.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/exprs.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/exprs.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/logical.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/logical.py`

## Communities (119 total, 17 thin omitted)

### Community 0 - "canonical.py"
Cohesion: 0.14
Nodes (20): Limits and per-request context., canonical_json(), fingerprint(), Any, Canonical JSON, fingerprints and spec-version upgrades. The canonical form of a…, SHA-256 of the canonical JSON, as hex., The request's ``spec_version``; a request without one is version 1 if it uses…, Bring a raw request dict up to the current ``spec_version``. (+12 more)

### Community 1 - "importlib_metadata"
Cohesion: 0.17
Nodes (12): importlib_metadata, Core utilities shared across py-libs packages., Convert ``value`` to a lowercase, URL-safe slug., slugify(), test_slugify_custom_separator(), make_filename(), Build a safe file name from a human-readable ``title``., Higher-level helpers built on pylibs-core. (+4 more)

### Community 2 - "py-libs"
Cohesion: 0.22
Nodes (8): Adding a package, Building, Development, Layout, License, One-time setup, py-libs, Releasing

### Community 3 - "CalcEngine"
Cohesion: 0.05
Nodes (84): fakeredis, CalcEngine, Evaluate calculation requests over a…, column(), Any, parametrize, rows(), ssrm() (+76 more)

### Community 4 - "AGENTS.md"
Cohesion: 0.25
Nodes (6): Architecture and conventions, Code knowledge graph (graphify), Commands, Documentation, Releasing, What this is

### Community 9 - "engine.py"
Cohesion: 0.14
Nodes (27): compare_frame(), LazyFrame, materialize(), Compile and cast to the canonical dtype of the (rigid) result type., agg_frame(), _aggregate(), domain_frame(), _hidden() (+19 more)

### Community 10 - "verify/reference.py"
Cohesion: 0.14
Nodes (36): Enum, functools, math, pivot_label(), Any, Kind, aggregate_levels(), _binary() (+28 more)

### Community 11 - ".register_scan"
Cohesion: 0.12
Nodes (18): Benchmarks, Guidance, Performance, Concepts, Formula language, Measures, Numbers, types and nulls, _check_keys() (+10 more)

### Community 12 - "Catalog"
Cohesion: 0.16
Nodes (15): Catalog, Thread-safe in-process catalog of in-memory frames and lazily scanned files.…, DataFrame, parametrize, Path, test_categorical_keys_become_strings_and_enums_become_strings(), test_editable_and_roles(), test_normalizes_dtypes_and_nan() (+7 more)

### Community 13 - "adapters/aggrid.py"
Cohesion: 0.13
Nodes (29): AgGridAdapter, _blank(), ColumnVO, _date(), _equals(), _Lenient, _literal(), Any (+21 more)

### Community 14 - "docs_from_graph.py"
Cohesion: 0.10
Nodes (40): ack(), _clean(), _code(), digest(), find_stale(), front_matter_list(), generate(), Graph (+32 more)

### Community 15 - "CalcContext"
Cohesion: 0.12
Nodes (15): Glossary, Gotchas, Over HTTP, Result, Saved scenarios and forks, Try it, What to notice, CalcContext (+7 more)

### Community 16 - "Model"
Cohesion: 0.08
Nodes (33): The life of a request, Python models, Quick start, Model, BaseModel, Base model for every spec object: immutable, strict about unknown fields, self-…, Frozen pydantic model that rejects unknown fields. Dumps always carry the…, CalcRequest (+25 more)

### Community 17 - "ext.py"
Cohesion: 0.14
Nodes (26): BinaryOp, field_validator, arith_result(), canonical_decimal(), coerce_value(), common_type(), _conflict(), decimal() (+18 more)

### Community 18 - "Compare two sides"
Cohesion: 0.33
Nodes (6): Choosing the two sides, Compare two sides, Gotchas, Result, Try it, What to notice

### Community 19 - "._keep_kind"
Cohesion: 0.50
Nodes (3): model_serializer, Any, SerializerFunctionWrapHandler

### Community 20 - "LogicalMutations"
Cohesion: 0.09
Nodes (27): LogicalMutations, OverrideBatch, flush(), Consecutive overrides, compacted: column -> {key tuple: new value}. Last write…, ShockOp, Any, LazyFrame, Scalar (+19 more)

### Community 21 - "book.py"
Cohesion: 0.12
Nodes (15): Quick start: total exposure per desk., Measures: exposure, counts and weighted yield per desk., Filtered measures: long and short notional side by side, like SQL FILTER (WHERE…, Rollup: book -> region -> desk subtotals in one result., Pivot: a desk x region exposure matrix, with row totals., Sort and page: the five largest positions by absolute market value, then the…, Override: a trader corrects two marks, and only those cells change., Shocks: Tech prices +5%, and yields +25bp on every bond. (+7 more)

### Community 22 - "test_plugins.py"
Cohesion: 0.10
Nodes (20): _clip_type(), Fx, FxBound, FxPlan, Ladder, _median_type(), Named, _numeric() (+12 more)

### Community 23 - "create_router"
Cohesion: 0.15
Nodes (11): ContextResolver, DependsParam, Check the runtime, Install, Working on the library itself, create_router(), body_limit(), context() (+3 more)

### Community 24 - "exprs.py"
Cohesion: 0.22
Nodes (23): operator, as_type(), _binary(), _bool(), _cast(), compile_expr(), _convert_value(), dec_dtype() (+15 more)

### Community 25 - "Kernel"
Cohesion: 0.14
Nodes (17): LogicalQuery, count_frame(), Finished, Kernel, _page(), DataFrame, EngineName, LazyFrame (+9 more)

### Community 26 - "manager.py"
Cohesion: 0.12
Nodes (16): Errors raised by the what-if plugin., ScenarioNotFound, Saved what-if scenarios: append-only, hash-chained logs of steps over a dataset…, Creating, editing, forking and auditing scenarios, with validation and…, LogEntry, BaseModel, datetime, Redis-backed scenario store: shared by every replica of a service. Needs the… (+8 more)

### Community 27 - "calc/tests/test_fastapi.py"
Cohesion: 0.20
Nodes (14): fastapi_testclient, io, client(), resolve(), fixture, parametrize, TestClient, test_body_limit() (+6 more)

### Community 28 - "PlanContext"
Cohesion: 0.08
Nodes (18): ABC, Bound, PlanContext, Any, DataFrame, LazyFrame, Row, What a transform sees when it is planned against a dataset version. (+10 more)

### Community 29 - "golden.py"
Cohesion: 0.31
Nodes (7): check(), Any, Golden cases: requests over the example book with their expected results. Each…, run_case(), update(), json, test_grid_rows_see_a_scenario()

### Community 30 - "Redis scenario store"
Cohesion: 0.50
Nodes (4): Durability, How it works, Redis scenario store, Testing

### Community 31 - ".collect"
Cohesion: 0.18
Nodes (9): InProcessQuery, _abandon(), _polars_message(), DataFrame, EngineName, Exception, LazyFrame, Collect ``lf``; past ``deadline`` (a ``time.monotonic()`` value) cancel and… (+1 more)

### Community 32 - "View"
Cohesion: 0.11
Nodes (12): The parts, M, AppliedTransform, _ms(), Any, A dataset version as one caller sees it, after the requested plugin transforms., Validate a request; versioned requests (``spec_version``) are upgraded first., Load the dataset version and apply the transforms named in ``extensions``. (+4 more)

### Community 33 - "logical.py"
Cohesion: 0.16
Nodes (26): _and(), _col(), DerivePlan, HiddenAgg, MeasurePlan, PivotPlan, _plan_measure(), _plan_pivot() (+18 more)

### Community 34 - "from_polars"
Cohesion: 0.21
Nodes (11): raw(), scan(), normalize(), DataType, LazyFrame, Cast to the engine's canonical dtypes and turn NaN/infinite floats into nulls.…, from_polars(), normalized_dtype() (+3 more)

### Community 35 - "pylibs_calc/__init__.py"
Cohesion: 0.23
Nodes (16): Exception classes, CalcError, CalcTimeout, ComputeError, DatasetNotFound, EngineBusy, Forbidden, NotFound (+8 more)

### Community 36 - "calc/tests/test_runtime.py"
Cohesion: 0.20
Nodes (6): Path, test_cgroup_limits(), test_timeout_cancels_the_query(), subprocess, sys, time

### Community 37 - "engine"
Cohesion: 0.12
Nodes (10): Filter + derive: the EMEA positions and their notional., Post-aggregation: average price as a ratio of sums, and gross leverage per…, Having: only the desks whose gross exposure is over their limit of 400,000., Saved scenarios: create, append with optimistic locking, read old versions,…, Compare: the P&L impact of a rates sell-off, by desk, against the base book., Audit a number: fingerprint, explain, and the independent reference evaluator., Errors and limits: every refusal has a stable code, a JSON-pointer path and an…, row() (+2 more)

### Community 38 - "Limits"
Cohesion: 0.15
Nodes (14): Checklist, Deploying on Kubernetes, Example, Reporting a problem, Troubleshooting, Limits, Hard caps that keep a single request from exhausting a pod. Exceeding one is a…, EngineConfig (+6 more)

### Community 39 - "columns"
Cohesion: 0.36
Nodes (8): children(), columns(), depth(), Node, Names of all columns an expression reads., Substitute column references (used to inline formula definitions)., replace_columns(), walk()

### Community 40 - "Subtotals (rollup)"
Cohesion: 0.40
Nodes (5): Gotchas, Result, Subtotals (rollup), Try it, What to notice

### Community 41 - "Ratios after aggregation"
Cohesion: 0.40
Nodes (5): Gotchas, Ratios after aggregation, Result, Try it, What to notice

### Community 42 - "LType"
Cohesion: 0.09
Nodes (29): decode_group_key(), encode_group_key(), ComparePlan, plan_compare(), Two-way compare: join a target and a base result, with deltas typed like any…, check_name(), materializable(), Reject names reserved for the engine's internal columns. (+21 more)

### Community 44 - "Errors and limits"
Cohesion: 0.12
Nodes (14): Minimal requests, Request schema, Errors and limits, Limits, Result, Time and load, Try it, What to notice (+6 more)

### Community 45 - "Contributing to the docs"
Cohesion: 0.12
Nodes (12): Adding a feature page, Commands, Contributing to the docs, How the graph keeps the docs in step, Layout, Style, How these docs are organized, py-libs (+4 more)

### Community 46 - "fastapi.py"
Cohesion: 0.16
Nodes (11): fastapi, fastapi_params, fastapi_responses, get, FastAPI router exposing a :class:`CalcEngine` (``pip install 'pylibs-…, index(), DataFrame, Demo service: pylibs-calc with the what-if plugin behind FastAPI, and an AG… (+3 more)

### Community 49 - "audit.md"
Cohesion: 0.11
Nodes (13): Architecture, Design principles, Two evaluators, one plan, Golden cases, Exploratory testing checklist, Test a service built on the engine, Testing guide, What to test, and how (+5 more)

### Community 54 - "Numbers, types and nulls"
Cohesion: 0.25
Nodes (8): Exact decimals, Float sums and reproducibility, Floats and decimals never mix silently, Invalid arithmetic gives null, Nulls follow SQL, Numbers, types and nulls, Settings, Shocks keep the column's type

### Community 55 - "exec.py"
Cohesion: 0.20
Nodes (11): contextlib, Performance and deployment, cgroup_cpu_limit(), Running Polars plans: concurrency slots, timeouts with cancellation, runtime…, Compare the Polars thread pool with the container's CPU limit (cgroup v1 or…, CPU limit from cgroup v2 ``cpu.max`` or v1 ``cpu.cfs_quota_us``; None if…, runtime_check(), RuntimeReport (+3 more)

### Community 56 - "Python API"
Cohesion: 0.14
Nodes (13): Data, Engine, Errors, Formulas and fingerprints, Integrations, Protocols, Python API, Requests (+5 more)

### Community 57 - "Filtered measures"
Cohesion: 0.17
Nodes (10): Filtered measures, Gotchas, Result, Try it, What to notice, Gotchas, Having, Result (+2 more)

### Community 58 - "bench.py"
Cohesion: 0.24
Nodes (9): argparse, numpy, book(), main(), Any, DataFrame, Latency benchmark for typical grid requests on a synthetic book of positions.…, timed() (+1 more)

### Community 59 - "DatasetSchema"
Cohesion: 0.12
Nodes (13): Datasets and the catalog, Datasets without a key, Registering data, Versions, What registration does, Your own catalog, DatasetCatalog, Protocol (+5 more)

### Community 60 - "build_schema"
Cohesion: 0.29
Nodes (6): build_schema(), Collection, DataType, Role, The schema as seen by a caller limited to ``allowed`` columns (keys always…, Describe a dataset. Numeric columns default to measures, the rest to…

### Community 61 - "expr.py"
Cohesion: 0.13
Nodes (21): datetime, _coerce(), ColRef, Any, Expression tree: the canonical, JSON-serializable form of every formula.…, _alias_keywords(), parse_formula(), Render an expression tree as formula text (for display, lineage and error… (+13 more)

### Community 62 - "Dataset"
Cohesion: 0.22
Nodes (3): Dataset, One immutable version of a dataset., Keyless datasets carry a hidden ``__row`` column so row views have a total…

### Community 63 - "hooks.py"
Cohesion: 0.39
Nodes (7): on_config(), on_page_markdown(), on_pre_build(), Any, MkDocs hooks: make the examples importable, and flag pages the code has moved…, _sync_module(), importlib_util

### Community 65 - "Call the API with curl"
Cohesion: 0.25
Nodes (8): All routes, Call the API with curl, Discover the data, Get exact decimals, or Arrow, Run a query, See how a number is computed, Try a what-if, When something is wrong

### Community 66 - "Pivot"
Cohesion: 0.33
Nodes (6): Gotchas, Options, Pivot, Result, Try it, What to notice

### Community 67 - "body_extensions"
Cohesion: 0.22
Nodes (8): body_extensions(), aggrid_rows(), run(), distinct(), run(), Any, The ``extensions`` of a request body; version 1 ``scenario``/``what_if`` keys…, A JSON-ready value: results as ``{"rows", "meta"}``, models dumped.

### Community 68 - "Access control"
Cohesion: 0.33
Nodes (6): Access control, Result, Scenario permissions, Try it, What to notice, Wiring it into FastAPI

### Community 69 - "Assumptions and limitations"
Cohesion: 0.40
Nodes (4): Assumptions, Assumptions and limitations, Not supported yet, Out of scope

### Community 71 - "WhatIfPlugin"
Cohesion: 0.12
Nodes (18): FixtureRequest, BindContext, What a transform sees when a request is resolved (before the dataset is loaded)., Caps on what-if work; exceeding one is a 413., WhatIfLimits, What-if analysis: override cells, shock columns and add formula columns, ad hoc…, WhatIfPlugin, Creating, editing, forking and auditing the scenarios of one… (+10 more)

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

### Community 76 - "validate.py"
Cohesion: 0.13
Nodes (28): AST, Call, Constant, Formulas are stored as trees, keyword, _Checker, lit_type(), Type checking: turns an expression tree into a :class:`Typed` tree against a… (+20 more)

### Community 77 - "request_of"
Cohesion: 0.40
Nodes (5): curl(), Any, Read the literal ``REQUEST = {...}`` from an example script, without running it., The curl call that sends an example's request to the demo service, as a code…, request_of()

### Community 78 - "AG Grid"
Cohesion: 0.50
Nodes (4): AG Grid, Client setup, Customizing the adapter, Gotchas

### Community 79 - "_call"
Cohesion: 0.24
Nodes (10): _call(), call_operation(), dataset_schema(), run_compare(), run_explain(), run_query(), T, JSON (or Arrow, if ``accept`` asks for it) with the fingerprint headers. (+2 more)

### Community 80 - "pylibs_calc_whatif/__init__.py"
Cohesion: 0.14
Nodes (18): CellEdit, edit_to_override(), BaseModel, AG Grid cell edits as what-if overrides (grid set up with ``readOnlyEdit:…, The useful part of AG Grid's ``CellEditRequestEvent``., Turn a grid cell edit into an override step (leaf rows only)., What-if analysis for pylibs-calc, as a plugin. :: from pylibs_calc import…, What-if routes for the FastAPI router: scenarios and AG Grid cell edits. Added… (+10 more)

### Community 81 - "Run the demo grid"
Cohesion: 0.67
Nodes (3): Run the demo grid, Start it, Things to try

### Community 82 - "pylibs-calc"
Cohesion: 0.67
Nodes (3): A request at a glance, pylibs-calc, What it does

### Community 83 - "Typed"
Cohesion: 0.33
Nodes (8): check_predicate(), _mismatch(), _need_bool(), _need_kind(), _need_numeric(), Node, An expression node with its result type and the type its operands are cast to., Typed

### Community 84 - "pylibs-calc"
Cohesion: 0.29
Nodes (6): AG Grid (server-side row model), FastAPI, Not supported yet, pylibs-calc, Scenarios, versions and concurrency, Verifiability

### Community 86 - "Formula language"
Cohesion: 0.11
Nodes (14): Cheat sheet, Errors, Formula language, Functions, Filter and derive, Gotchas, Result, Try it (+6 more)

### Community 87 - "model.py"
Cohesion: 0.15
Nodes (16): Copy a scenario's effective steps (at a version) into a new, independent…, Recompute the hash chain; False means the stored log was altered., Start an empty scenario pinned to a dataset version (default: the latest)., entry_hash(), genesis_hash(), make_entries(), now(), datetime (+8 more)

### Community 88 - "CalcResult"
Cohesion: 0.10
Nodes (16): decimal, Hand a result to ``EngineConfig.on_result``; every call should end here., CalcResult, json_safe(), Any, DataFrame, Results: the frame plus metadata that makes it reproducible and auditable., JSON-safe rows: decimals as floats (or exact strings), dates as ISO strings,… (+8 more)

### Community 89 - "Scenario"
Cohesion: 0.19
Nodes (8): Scenario, Any, RedisScenarioStore, _text(), Insert a new scenario (with initial entries when forking)., Raise :class:`ScenarioNotFound` if missing (soft-deleted scenarios are…, Scenarios that are not deleted, oldest first., Redis

### Community 90 - "add_routes"
Cohesion: 0.20
Nodes (14): What plugin route hooks get besides the router (see ``Registry.add_routes``).…, RouterKit, add_routes(), aggrid_edit(), run(), append_steps(), create_scenario(), delete_scenario() (+6 more)

### Community 91 - "plugins.py"
Cohesion: 0.20
Nodes (12): collections, collections_abc, dataclasses, glob, hashlib, A byte-bounded LRU cache of result frames. Keys are content hashes of…, Datasets the engine can query, pinned to immutable versions. A catalog…, The plugin API: how analyses are built on top of the core calculation engine.… (+4 more)

### Community 92 - "typing"
Cohesion: 0.17
Nodes (12): hypothesis, Hypothesis strategies for fuzzing the engine, and plugins, against the…, Any, Cross-check the engine against the pure-Python reference evaluator.…, verify(), VerifyReport, test_plugin_aggregate_with_rollup_and_pivot(), test_plugin_function() (+4 more)

### Community 93 - "assert_matches_reference"
Cohesion: 0.17
Nodes (15): assert_matches_reference(), frames(), DataFrame, Fail unless the engine and the reference evaluator agree on ``request``., A random table: key ``k``, groups ``g1`` (string or categorical) and ``g2``,…, DataObject, given, test_plugin_computations_match_reference() (+7 more)

### Community 94 - "plugin.py"
Cohesion: 0.18
Nodes (11): effective_steps(), FormulaDef, LabeledStep, Planning what-if steps: validate them against a dataset schema into…, Drop ``Disable`` steps and the steps they disable. Sequence numbers start at…, A scenario step plus where it came from (for error paths and lineage)., ScenarioStep, The ``whatif`` plugin: a dataset transform plus saved scenarios, routes and… (+3 more)

### Community 95 - "LimitExceeded"
Cohesion: 0.23
Nodes (13): frame_size(), DataFrame, SortSpec, finish_aggregate(), _hierarchical_sort(), _pivot(), DataFrame, Subtotal rows directly after their details; the grand total last. (+5 more)

### Community 96 - "Registry"
Cohesion: 0.19
Nodes (6): PluginError, Everything the engine's plugins registered. Names are unique across plugins., A plugin is misconfigured (e.g. two plugins register the same name)., Registry, RoutesHook, ValueError

### Community 97 - "measures"
Cohesion: 0.29
Nodes (13): dec_expr(), float_expr(), measures(), predicate(), Any, composite, DrawFn, queries() (+5 more)

### Community 98 - "test_plugin.py"
Cohesion: 0.18
Nodes (12): _imports(), Path, The what-if plugin through the plugin API: request shape, composition,…, test_a_plugin_instance_belongs_to_one_engine(), test_core_does_not_know_the_plugin(), test_empty_block_is_the_plain_dataset(), test_error_paths_point_into_the_block(), test_explain_reports_lineage() (+4 more)

### Community 99 - "UsdBound"
Cohesion: 0.24
Nodes (5): Any, Decimal, LazyFrame, UsdBound, UsdPlan

### Community 100 - "pathlib"
Cohesion: 0.22
Nodes (8): CaptureFixture, parametrize, Run every documentation example, so a change that breaks the docs also breaks…, test_example_runs(), test_golden_cases(), MonkeyPatch, pathlib, runpy

### Community 101 - "Plugin"
Cohesion: 0.22
Nodes (6): P, An installed plugin, by name or by class., build_registry(), Plugin, Base class for plugins. Subclasses set ``name`` and ``version`` and override…, Called once, after every plugin registered.

### Community 102 - "OperationDef"
Cohesion: 0.22
Nodes (6): OperationDef, A new engine call: ``engine.call(name, request, ctx)`` parses ``request`` with…, Version 2 moved what-if into the ``whatif`` plugin: ``scenario``, ``what_if``…, _v1_to_v2(), block(), fx_routes()

### Community 103 - "what_if"
Cohesion: 0.25
Nodes (8): dec_literal(), A decimal literal with one place, e.g. ``"-12.5"``., Any, composite, DrawFn, Up to three random overrides, shocks and formulas over a frame of ``n`` rows., what_if(), SearchStrategy

### Community 104 - "calc/tests/conftest.py"
Cohesion: 0.46
Nodes (7): catalog(), engine(), frame(), positions_frame(), DataFrame, fixture, A small book of positions with every kind of column, nulls included.

### Community 105 - "calc_whatif/tests/conftest.py"
Cohesion: 0.46
Nodes (7): catalog(), engine(), frame(), positions_frame(), DataFrame, fixture, A small book of positions with every kind of column, nulls included.

### Community 106 - "calc_whatif/tests/test_fastapi.py"
Cohesion: 0.36
Nodes (7): client(), resolve(), fixture, TestClient, test_aggrid_rows_and_edit(), test_compare_and_distinct_with_what_if(), test_scenario_lifecycle()

### Community 107 - "Formula columns"
Cohesion: 0.33
Nodes (6): `derive` or `formula`?, Formula columns, Gotchas, Result, Try it, What to notice

### Community 108 - "release_info.py"
Cohesion: 0.40
Nodes (5): os, main(), Resolve a release tag like ``core/v0.2.0`` to the package it releases.…, resolve(), tomllib

### Community 109 - "TransformDef"
Cohesion: 0.33
Nodes (4): A dataset transform, enabled per request by ``extensions[name]``. ``model``…, TransformDef, test_whatif_sees_columns_and_functions_of_earlier_plugins(), UsdPlugin

### Community 110 - "Quick start"
Cohesion: 0.40
Nodes (5): 1. Register data and create an engine, 2. Ask a question, 3. Ask "what if?", Next steps, Quick start

### Community 111 - "ResultMeta"
Cohesion: 0.50
Nodes (5): 4. Read the metadata, ColumnInfo, BaseModel, Everything needed to reproduce, audit or cache a result. ``fingerprint`` is the…, ResultMeta

### Community 112 - "Override a cell"
Cohesion: 0.40
Nodes (5): Gotchas, Override a cell, Result, Try it, What to notice

### Community 113 - "discover_plugins"
Cohesion: 0.40
Nodes (4): discover_plugins(), Instantiate every installed plugin advertised under the ``pylibs_calc.plugins``…, pylibs-calc-whatif, test_discovered_through_the_entry_point()

### Community 114 - "FxPlugin"
Cohesion: 0.40
Nodes (3): fx_engine(), FxPlugin, fixture

### Community 115 - "Order of evaluation"
Cohesion: 0.50
Nodes (4): From dataset to result, Inside the query, Order of evaluation, Why the order matters

## Knowledge Gaps
- **148 isolated node(s):** `pylibs-calc`, `pylibs-calc-whatif`, `pylibs-core`, `pylibs-utils`, `What this is` (+143 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 581 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CalcEngine` connect `CalcEngine` to `engine.py`, `Catalog`, `adapters/aggrid.py`, `CalcContext`, `Model`, `test_plugins.py`, `create_router`, `calc/tests/test_fastapi.py`, `golden.py`, `View`, `pylibs_calc/__init__.py`, `engine`, `Limits`, `LType`, `fastapi.py`, `ResultCache`, `bench.py`, `DatasetSchema`, `body_extensions`, `WhatIfPlugin`, `pylibs_calc_whatif/__init__.py`, `CalcResult`, `add_routes`, `plugins.py`, `typing`, `assert_matches_reference`, `LimitExceeded`, `Registry`, `test_plugin.py`, `Plugin`, `OperationDef`, `calc/tests/conftest.py`, `calc_whatif/tests/conftest.py`, `calc_whatif/tests/test_fastapi.py`, `FxPlugin`, `.call`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Why does `LType` connect `LType` to `engine.py`, `verify/reference.py`, `adapters/aggrid.py`, `ext.py`, `LogicalMutations`, `test_plugins.py`, `exprs.py`, `Kernel`, `PlanContext`, `View`, `logical.py`, `from_polars`, `Errors and limits`, `DatasetSchema`, `validate.py`, `Typed`, `CalcResult`, `plugins.py`, `LimitExceeded`, `UsdBound`, `ResultMeta`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `CalcContext` connect `CalcContext` to `canonical.py`, `CalcEngine`, `engine.py`, `adapters/aggrid.py`, `test_plugins.py`, `create_router`, `Kernel`, `calc/tests/test_fastapi.py`, `PlanContext`, `View`, `pylibs_calc/__init__.py`, `Limits`, `fastapi.py`, `audit.md`, `DatasetSchema`, `Access control`, `Assumptions and limitations`, `WhatIfPlugin`, `pylibs-calc`, `model.py`, `CalcResult`, `add_routes`, `plugins.py`, `typing`, `assert_matches_reference`, `plugin.py`, `LimitExceeded`, `OperationDef`, `calc_whatif/tests/test_fastapi.py`, `.call`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `CalcEngine` (e.g. with `Your own catalog` and `main()`) actually correct?**
  _`CalcEngine` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Are the 49 inferred relationships involving `LType` (e.g. with `AgGridAdapter` and `_blank()`) actually correct?**
  _`LType` has 49 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `SpecError` (e.g. with `Exception classes` and `AgGridAdapter`) actually correct?**
  _`SpecError` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `CalcContext` (e.g. with `Glossary` and `Assumptions`) actually correct?**
  _`CalcContext` has 19 INFERRED edges - model-reasoned connections that need verification._