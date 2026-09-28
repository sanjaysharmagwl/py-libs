# Graph Report - py-libs  (2026-09-28)

## Corpus Check
- 162 files · ~84,312 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 6, .typed 4, .lock 1)

## Summary
- 1776 nodes · 4753 edges · 120 communities (100 shown, 20 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 627 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `598d1832`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- canonical.py
- pytest
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
- AgGridAdapter
- docs_from_graph.py
- ScenarioManager
- spec/query.py
- ext.py
- BindContext
- Model
- plan_mutations
- book.py
- Any
- create_router
- exprs.py
- Kernel
- Scenario
- adapters/aggrid.py
- TransformPlan
- golden.py
- test_scenarios.py
- exec.py
- CalcContext
- SpecError
- from_polars
- pylibs_calc/__init__.py
- calc/tests/test_aggrid.py
- 17_errors_limits.py
- EngineConfig
- LType
- Ratios after aggregation
- Write a plugin
- compare.py
- scenarios/index.md
- Errors and limits
- Contributing to the docs
- fastapi.py
- ResultCache
- adapters/__init__.py
- testing-guide.md
- compile/__init__.py
- integrations/__init__.py
- spec/__init__.py
- pylibs-calc
- Numbers, types and nulls
- PlanContext
- Python API
- Filtered measures
- json_safe
- DatasetSchema
- build_schema
- expr.py
- Dataset
- hooks.py
- calc/tests/test_compare.py
- plugins.md
- pylibs-calc-whatif
- body_extensions
- Access control
- Audit a number
- Sort and page
- ScenarioStore
- Shock a column
- calc_whatif/tests/test_compare.py
- Disable a step
- positions
- formula.py
- request_of
- AG Grid
- _call
- WhatIfPlugin
- Run the demo grid
- pylibs-calc
- validate.py
- Concepts
- model_validator
- Filter and derive
- Performance
- CalcResult
- RedisScenarioStore
- add_routes
- dtypes.py
- verify
- measures
- plugin.py
- check_pages
- Registry
- synthetic_book
- test_plugin.py
- UsdBound
- pathlib
- plugins.py
- .register
- Architecture
- calc/tests/conftest.py
- engine
- .schema
- Formula columns
- release_info.py
- check_rollup_totals
- Quick start
- .attach
- Override a cell
- PluginError
- test_plugins.py
- EngineName
- Exception
- Scalar
- DataType
- Protocol

## God Nodes (most connected - your core abstractions)
1. `CalcEngine` - 136 edges
2. `SpecError` - 75 edges
3. `CalcContext` - 57 edges
4. `Kernel` - 48 edges
5. `WhatIfPlugin` - 40 edges
6. `Typed` - 39 edges
7. `AgGridAdapter` - 38 edges
8. `Scenario` - 38 edges
9. `compile_expr()` - 35 edges
10. `LType` - 35 edges

## Surprising Connections (you probably didn't know these)
- `Functions` --references--> `FunctionDef`  [INFERRED]
  docs/calc/concepts/formula-language.md → packages/calc/src/pylibs_calc/plugins.py
- `1. Functions and aggregates` --references--> `LType`  [INFERRED]
  docs/calc/extending/write-a-plugin.md → packages/calc/src/pylibs_calc/dtypes.py
- `Check the runtime` --references--> `runtime_check()`  [INFERRED]
  docs/calc/getting-started/install.md → packages/calc/src/pylibs_calc/exec.py
- `Glossary` --references--> `CalcContext`  [INFERRED]
  docs/calc/glossary.md → packages/calc/src/pylibs_calc/config.py
- `Gotchas` --references--> `edit_to_override()`  [INFERRED]
  docs/calc/integrations/aggrid.md → packages/calc_whatif/src/pylibs_calc_whatif/aggrid.py

## Import Cycles
- 3-file cycle: `packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py`
- 4-file cycle: `packages/calc/src/pylibs_calc/compile/logical.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/logical.py`
- 4-file cycle: `packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/validate.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/logical.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/query.py -> packages/calc/src/pylibs_calc/compile/logical.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/compare.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/compare.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/exprs.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/exprs.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/logical.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/logical.py`

## Communities (120 total, 20 thin omitted)

### Community 0 - "canonical.py"
Cohesion: 0.13
Nodes (22): hashlib, canonical_json(), fingerprint(), Any, Canonical JSON, fingerprints and spec-version upgrades. The canonical form of a…, SHA-256 of the canonical JSON, as hex., The request's ``spec_version``; a request without one is version 1 if it uses…, Bring a raw request dict up to the current ``spec_version``. (+14 more)

### Community 1 - "pytest"
Cohesion: 0.07
Nodes (35): fastapi_testclient, io, client(), resolve(), fixture, parametrize, TestClient, test_body_limit() (+27 more)

### Community 2 - "py-libs"
Cohesion: 0.22
Nodes (8): Adding a package, Building, Development, Layout, License, One-time setup, py-libs, Releasing

### Community 3 - "CalcEngine"
Cohesion: 0.12
Nodes (35): CalcEngine, Evaluate calculation requests over a…, Any, Evaluate one expression on the row with id 1., run(), test_audit_counts_stages(), test_bad_formula_reports_a_path(), test_context_row_filter_and_columns() (+27 more)

### Community 4 - "AGENTS.md"
Cohesion: 0.25
Nodes (6): Architecture and conventions, Code knowledge graph (graphify), Commands, Documentation, Releasing, What this is

### Community 9 - "engine.py"
Cohesion: 0.13
Nodes (38): LogicalQuery, SortSpec, agg_frame(), _aggregate(), count_frame(), domain_frame(), finish_aggregate(), Finished (+30 more)

### Community 10 - "verify/reference.py"
Cohesion: 0.08
Nodes (52): ComparePlan, Assumptions, Assumptions and limitations, Not supported yet, Out of scope, Choosing the two sides, Compare two sides, Gotchas (+44 more)

### Community 11 - ".register_scan"
Cohesion: 0.17
Nodes (14): Checklist, Deploying on Kubernetes, Example, _check_keys(), _check_names(), content_version(), file_version(), Collection (+6 more)

### Community 12 - "Catalog"
Cohesion: 0.19
Nodes (13): Catalog, Thread-safe in-process catalog of in-memory frames and lazily scanned files.…, DataFrame, parametrize, Path, test_categorical_keys_become_strings_and_enums_become_strings(), test_editable_and_roles(), test_normalizes_dtypes_and_nan() (+5 more)

### Community 13 - "AgGridAdapter"
Cohesion: 0.30
Nodes (15): AgGridAdapter, _blank(), _date(), _equals(), _literal(), Any, LType, Node (+7 more)

### Community 14 - "docs_from_graph.py"
Cohesion: 0.08
Nodes (49): argparse, numpy, book(), main(), Any, DataFrame, Latency benchmark for typical grid requests on a synthetic book of positions.…, timed() (+41 more)

### Community 15 - "ScenarioManager"
Cohesion: 0.12
Nodes (15): Gotchas, Over HTTP, Result, Saved scenarios and forks, Try it, What to notice, In the engine, parse_steps() (+7 more)

### Community 16 - "spec/query.py"
Cohesion: 0.09
Nodes (31): The life of a request, Python models, Quick start, DatasetSchema, The request for the pivot values, filtered by the filter model only (not by…, _type(), CalcRequest, CompareRequest (+23 more)

### Community 17 - "ext.py"
Cohesion: 0.14
Nodes (16): field_validator, canonical_decimal(), decimal(), parse_decimal(), Shortest plain (non-exponent) text for a decimal; ``-0`` becomes ``0``., Parse a JSON number or numeric string into an exact decimal., AppliedTransform, Turn a pydantic error into a :class:`SpecError` with a JSON-pointer path. (+8 more)

### Community 18 - "BindContext"
Cohesion: 0.10
Nodes (17): bind_fx(), Fx, fx_ladder(), FxBound, FxPlan, FxPlugin, Ladder, numbers_to_float() (+9 more)

### Community 19 - "Model"
Cohesion: 0.29
Nodes (6): model_serializer, Model, Any, BaseModel, Frozen pydantic model that rejects unknown fields. Dumps always carry the…, SerializerFunctionWrapHandler

### Community 20 - "plan_mutations"
Cohesion: 0.09
Nodes (34): DataType, decimal_places(), _editable(), FormulaDef, LogicalMutations, OverrideBatch, plan_mutations(), flush() (+26 more)

### Community 21 - "book.py"
Cohesion: 0.09
Nodes (24): Quick start: total exposure per desk., Filter + derive: the EMEA positions and their notional., Measures: exposure, counts and weighted yield per desk., Filtered measures: long and short notional side by side, like SQL FILTER (WHERE…, Post-aggregation: average price as a ratio of sums, and gross leverage per…, Having: only the desks whose gross exposure is over their limit of 400,000., Rollup: book -> region -> desk subtotals in one result., Pivot: a desk x region exposure matrix, with row totals. (+16 more)

### Community 22 - "Any"
Cohesion: 0.17
Nodes (10): _clip_type(), Fx, FxPlan, Ladder, _median_type(), _numeric(), Any, LazyFrame (+2 more)

### Community 23 - "create_router"
Cohesion: 0.15
Nodes (11): ContextResolver, DependsParam, Check the runtime, Install, Working on the library itself, create_router(), body_limit(), context() (+3 more)

### Community 24 - "exprs.py"
Cohesion: 0.17
Nodes (30): Formulas are stored as trees, operator, as_type(), _binary(), _bool(), _cast(), compile_expr(), _convert_value() (+22 more)

### Community 25 - "Kernel"
Cohesion: 0.13
Nodes (16): Dataset, EngineName, frame_size(), DataFrame, Kernel, _page(), DataFrame, LazyFrame (+8 more)

### Community 26 - "Scenario"
Cohesion: 0.11
Nodes (25): Errors raised by the what-if plugin., Saved what-if scenarios: append-only, hash-chained logs of steps over a dataset…, Creating, editing, forking and auditing scenarios, with validation and…, Start an empty scenario pinned to a dataset version (default: the latest)., entry_hash(), genesis_hash(), LogEntry, make_entries() (+17 more)

### Community 27 - "adapters/aggrid.py"
Cohesion: 0.12
Nodes (22): ColumnVO, decode_group_key(), encode_group_key(), _Lenient, BaseModel, AG Grid Server-Side Row Model (SSRM) adapter. Pure translation; no web…, How to decorate result rows for the grid., Answer one SSRM ``getRows`` call end to end (engine: a :class:`CalcEngine`). (+14 more)

### Community 28 - "TransformPlan"
Cohesion: 0.09
Nodes (19): ABC, HTTP routes, Operations, The extension points, Transforms, Bound, Any, LazyFrame (+11 more)

### Community 29 - "golden.py"
Cohesion: 0.31
Nodes (7): check(), Any, Golden cases: requests over the example book with their expected results. Each…, run_case(), update(), json, test_grid_rows_see_a_scenario()

### Community 30 - "test_scenarios.py"
Cohesion: 0.23
Nodes (21): fakeredis, engine(), prices(), Any, Catalog, scenarios(), shock(), test_authorization_hook() (+13 more)

### Community 31 - "exec.py"
Cohesion: 0.08
Nodes (23): contextlib, InProcessQuery, math, _abandon(), cgroup_cpu_limit(), _polars_message(), DataFrame, EngineName (+15 more)

### Community 32 - "CalcContext"
Cohesion: 0.09
Nodes (17): The parts, 3. An operation, M, CalcContext, Node, Who is asking, and what they may see. Supplied by the host service per request.…, Fingerprint of everything in the context that changes results (for cache keys)., _ms() (+9 more)

### Community 33 - "SpecError"
Cohesion: 0.12
Nodes (35): Functions and aggregates, _and(), check_name(), _col(), DerivePlan, HiddenAgg, materializable(), MeasurePlan (+27 more)

### Community 34 - "from_polars"
Cohesion: 0.21
Nodes (11): raw(), scan(), normalize(), DataType, LazyFrame, Cast to the engine's canonical dtypes and turn NaN/infinite floats into nulls.…, from_polars(), normalized_dtype() (+3 more)

### Community 35 - "pylibs_calc/__init__.py"
Cohesion: 0.13
Nodes (23): Error codes, Exception classes, Exception, CalcError, CalcTimeout, ComputeError, DatasetNotFound, EngineBusy (+15 more)

### Community 36 - "calc/tests/test_aggrid.py"
Cohesion: 0.28
Nodes (15): column(), Any, parametrize, rows(), ssrm(), test_custom_aggregation(), test_drill_down_with_null_group_key(), test_filters() (+7 more)

### Community 38 - "EngineConfig"
Cohesion: 0.21
Nodes (9): DatasetCatalog, EngineConfig, Engine-wide settings. ``authorize(ctx, action, resource)`` is called by plugins…, Catalog, test_engine_busy(), test_group_limit(), test_on_result_hook(), test_pivot_with_explicit_domain_and_limits() (+1 more)

### Community 39 - "LType"
Cohesion: 0.23
Nodes (10): BinaryOp, arith_result(), common_type(), _conflict(), LType, _numeric_common(), The type two values are compared, coalesced or chosen between as (no scale…, Result type of ``a <op> b``. Operands are cast to ``common_type`` first (see… (+2 more)

### Community 40 - "Ratios after aggregation"
Cohesion: 0.17
Nodes (10): Gotchas, Ratios after aggregation, Result, Try it, What to notice, Gotchas, Result, Subtotals (rollup) (+2 more)

### Community 41 - "Write a plugin"
Cohesion: 0.28
Nodes (7): 1. Functions and aggregates, 2. A transform, 4. The plugin, 5. Use it, Checklist, Test it against the reference, Write a plugin

### Community 42 - "compare.py"
Cohesion: 0.31
Nodes (7): compare_frame(), ComparePlan, plan_compare(), LazyFrame, Two-way compare: join a target and a base result, with deltas typed like any…, NumericConfig, Engine-wide numeric settings; they are part of every result fingerprint.

### Community 44 - "Errors and limits"
Cohesion: 0.09
Nodes (20): Cheat sheet, Errors, Formula language, Functions, Minimal requests, Request schema, Versions, Errors and limits (+12 more)

### Community 45 - "Contributing to the docs"
Cohesion: 0.12
Nodes (12): Adding a feature page, Commands, Contributing to the docs, How the graph keeps the docs in step, Layout, Style, How these docs are organized, py-libs (+4 more)

### Community 46 - "fastapi.py"
Cohesion: 0.24
Nodes (8): fastapi, fastapi_params, fastapi_responses, get, FastAPI router exposing a :class:`CalcEngine` (``pip install 'pylibs-…, index(), Demo service: pylibs-calc with the what-if plugin behind FastAPI, and an AG…, scenario_store()

### Community 49 - "testing-guide.md"
Cohesion: 0.29
Nodes (5): Golden cases, Exploratory testing checklist, Test a service built on the engine, Testing guide, What to test, and how

### Community 54 - "Numbers, types and nulls"
Cohesion: 0.17
Nodes (10): Exact decimals, Float sums and reproducibility, Floats and decimals never mix silently, Invalid arithmetic gives null, Nulls follow SQL, Numbers, types and nulls, Settings, Shocks keep the column's type (+2 more)

### Community 55 - "PlanContext"
Cohesion: 0.22
Nodes (5): PlanContext, DataFrame, NumericConfig, What a transform sees when it is planned against a dataset version., Run a (small) query under the engine's concurrency limit and the request…

### Community 56 - "Python API"
Cohesion: 0.15
Nodes (13): Data, Engine, Errors, Formulas and fingerprints, Integrations, Plugin API, Protocols, Python API (+5 more)

### Community 57 - "Filtered measures"
Cohesion: 0.17
Nodes (10): Filtered measures, Gotchas, Result, Try it, What to notice, Gotchas, Having, Result (+2 more)

### Community 58 - "json_safe"
Cohesion: 0.38
Nodes (4): A JSON-ready value: results as ``{"rows", "meta"}``, models dumped., json_safe(), Any, JSON-safe rows: decimals as floats (or exact strings), dates as ISO strings,…

### Community 59 - "DatasetSchema"
Cohesion: 0.15
Nodes (12): Datasets and the catalog, Datasets without a key, Registering data, Versions, What registration does, Your own catalog, DatasetCatalog, Protocol (+4 more)

### Community 60 - "build_schema"
Cohesion: 0.29
Nodes (6): build_schema(), Collection, DataType, Role, The schema as seen by a caller limited to ``allowed`` columns (keys always…, Describe a dataset. Numeric columns default to measures, the rest to…

### Community 61 - "expr.py"
Cohesion: 0.12
Nodes (29): children(), _coerce(), col(), ColRef, columns(), depth(), Node, Expression tree: the canonical, JSON-serializable form of every formula.… (+21 more)

### Community 62 - "Dataset"
Cohesion: 0.22
Nodes (3): Dataset, One immutable version of a dataset., Keyless datasets carry a hidden ``__row`` column so row views have a total…

### Community 63 - "hooks.py"
Cohesion: 0.39
Nodes (7): on_config(), on_page_markdown(), on_pre_build(), Any, MkDocs hooks: make the examples importable, and flag pages the code has moved…, _sync_module(), importlib_util

### Community 64 - "calc/tests/test_compare.py"
Cohesion: 0.29
Nodes (6): Catalog, DataFrame, test_compare_rejects_pivot(), test_compare_two_dataset_versions(), test_compare_with_itself_has_no_deltas(), test_unknown_extensions_are_rejected()

### Community 65 - "plugins.md"
Cohesion: 0.16
Nodes (8): All routes, Call the API with curl, Discover the data, Get exact decimals, or Arrow, Run a query, See how a number is computed, Try a what-if, When something is wrong

### Community 66 - "pylibs-calc-whatif"
Cohesion: 0.33
Nodes (5): Limits, pylibs-calc-whatif, Quick start, Saved scenarios, Steps

### Community 67 - "body_extensions"
Cohesion: 0.29
Nodes (7): body_extensions(), aggrid_rows(), run(), distinct(), run(), Any, The ``extensions`` of a request body; version 1 ``scenario``/``what_if`` keys…

### Community 68 - "Access control"
Cohesion: 0.33
Nodes (6): Access control, Result, Scenario permissions (what-if plugin), Try it, What to notice, Wiring it into FastAPI

### Community 69 - "Audit a number"
Cohesion: 0.40
Nodes (5): Also useful, Audit a number, Result, The three tools, Try it

### Community 70 - "Sort and page"
Cohesion: 0.40
Nodes (5): Gotchas, Result, Sort and page, Try it, What to notice

### Community 71 - "ScenarioStore"
Cohesion: 0.08
Nodes (18): Durability, How it works, Redis scenario store, Testing, Coming from version 0.1, Limits, The request block, What-if plugin (+10 more)

### Community 72 - "Shock a column"
Cohesion: 0.33
Nodes (6): Gotchas, Result, Shock a column, The operations, Try it, What to notice

### Community 73 - "calc_whatif/tests/test_compare.py"
Cohesion: 0.50
Nodes (4): shock(), test_aggregated_compare(), test_compare_two_what_ifs_with_rollup(), test_row_level_compare_and_zero_base()

### Community 74 - "Disable a step"
Cohesion: 0.40
Nodes (5): Disable a step, Gotchas, Result, Try it, What to notice

### Community 75 - "positions"
Cohesion: 0.29
Nodes (7): Core engine, Pages, Scenarios by feature, The example book, What-if plugin, positions(), DataFrame

### Community 76 - "formula.py"
Cohesion: 0.16
Nodes (18): AST, Call, Constant, keyword, IfElse, InList, ``arg in (values...)``; the values are non-null literals., ``then if cond else otherwise``; a null condition picks ``otherwise``. (+10 more)

### Community 77 - "request_of"
Cohesion: 0.40
Nodes (5): curl(), Any, Read the literal ``REQUEST = {...}`` from an example script, without running it., The curl call that sends an example's request to the demo service, as a code…, request_of()

### Community 78 - "AG Grid"
Cohesion: 0.50
Nodes (4): AG Grid, Client setup, Customizing the adapter, Gotchas

### Community 79 - "_call"
Cohesion: 0.24
Nodes (10): _call(), call_operation(), dataset_schema(), run_compare(), run_explain(), run_query(), T, JSON (or Arrow, if ``accept`` asks for it) with the fingerprint headers. (+2 more)

### Community 80 - "WhatIfPlugin"
Cohesion: 0.08
Nodes (36): Python API at a glance, importlib_metadata, CellEdit, edit_to_override(), BaseModel, DatasetSchema, AG Grid cell edits as what-if overrides (grid set up with ``readOnlyEdit:…, The useful part of AG Grid's ``CellEditRequestEvent``. (+28 more)

### Community 81 - "Run the demo grid"
Cohesion: 0.67
Nodes (3): Run the demo grid, Start it, Things to try

### Community 82 - "pylibs-calc"
Cohesion: 0.67
Nodes (3): A request at a glance, pylibs-calc, What it does

### Community 83 - "validate.py"
Cohesion: 0.17
Nodes (21): Kind, Budget, check(), check_predicate(), _Checker, lit_type(), _mismatch(), _need_bool() (+13 more)

### Community 84 - "Concepts"
Cohesion: 0.17
Nodes (11): AG Grid (server-side row model), Compare, Concepts, FastAPI, Formula language, Measures, Not supported yet, Numbers, types and nulls (+3 more)

### Community 86 - "Filter and derive"
Cohesion: 0.40
Nodes (5): Filter and derive, Gotchas, Result, Try it, What to notice

### Community 87 - "Performance"
Cohesion: 0.50
Nodes (3): Benchmarks, Guidance, Performance

### Community 88 - "CalcResult"
Cohesion: 0.15
Nodes (9): Hand a result to ``EngineConfig.on_result``; every call should end here., CalcResult, BaseModel, DataFrame, Everything needed to reproduce, audit or cache a result. ``fingerprint`` is the…, The frame as an Arrow IPC stream (exact decimals, no JSON overhead)., ResultMeta, The same query at several FX rates, stacked with a ``rate`` column. (+1 more)

### Community 89 - "RedisScenarioStore"
Cohesion: 0.28
Nodes (6): ScenarioNotFound, Any, datetime, RedisScenarioStore, _text(), Redis

### Community 90 - "add_routes"
Cohesion: 0.20
Nodes (14): What plugin route hooks get besides the router (see ``Registry.add_routes``).…, RouterKit, add_routes(), aggrid_edit(), run(), append_steps(), create_scenario(), delete_scenario() (+6 more)

### Community 91 - "dtypes.py"
Cohesion: 0.10
Nodes (28): collections, collections_abc, dataclasses, datetime, decimal, A custom plugin: report in USD with FX rates by region, and an FX sensitivity…, Enum, glob (+20 more)

### Community 92 - "verify"
Cohesion: 0.25
Nodes (8): Any, verify(), VerifyReport, test_deterministic_float_sums(), test_plugin_aggregate_with_rollup_and_pivot(), test_plugin_function(), test_transform(), test_composite_keys()

### Community 93 - "measures"
Cohesion: 0.06
Nodes (45): From dataset to result, Inside the query, Inside the what-if transform, Order of evaluation, Why the order matters, Errors, FastAPI, Options (+37 more)

### Community 94 - "plugin.py"
Cohesion: 0.14
Nodes (13): effective_steps(), LabeledStep, Drop ``Disable`` steps and the steps they disable. Sequence numbers start at…, A scenario step plus where it came from (for error paths and lineage)., Any, LazyFrame, LType, The ``whatif`` plugin: a dataset transform plus saved scenarios, routes and… (+5 more)

### Community 95 - "check_pages"
Cohesion: 0.50
Nodes (4): check_pages(), Any, Paging through a view yields each row exactly once, in the unpaged order., test_pages_partition_the_view()

### Community 96 - "Registry"
Cohesion: 0.20
Nodes (5): A dataset transform, enabled per request by ``extensions[name]``. ``model``…, Everything the engine's plugins registered. Names are unique across plugins., Registry, TransformDef, Named

### Community 97 - "synthetic_book"
Cohesion: 0.50
Nodes (3): DataFrame, Deterministic pseudo-random positions (no numpy needed)., synthetic_book()

### Community 98 - "test_plugin.py"
Cohesion: 0.21
Nodes (13): _imports(), Catalog, Model, Path, The what-if plugin through the plugin API: request shape, composition,…, test_a_plugin_instance_belongs_to_one_engine(), test_core_does_not_know_the_plugin(), test_limits() (+5 more)

### Community 99 - "UsdBound"
Cohesion: 0.21
Nodes (6): Any, Decimal, LazyFrame, LType, UsdBound, UsdPlan

### Community 100 - "pathlib"
Cohesion: 0.22
Nodes (8): CaptureFixture, parametrize, Run every documentation example, so a change that breaks the docs also breaks…, test_example_runs(), test_golden_cases(), MonkeyPatch, pathlib, runpy

### Community 101 - "plugins.py"
Cohesion: 0.20
Nodes (8): P, An installed plugin, by name or by class., build_registry(), OperationDef, Plugin, The plugin API: how analyses are built on top of the core calculation engine.…, A new engine call: ``engine.call(name, request, ctx)`` parses ``request`` with…, Base class for plugins. Subclasses set ``name`` and ``version`` and override…

### Community 102 - ".register"
Cohesion: 0.17
Nodes (8): Version 2 moved what-if into the ``whatif`` plugin: ``scenario``, ``what_if``…, _v1_to_v2(), block(), fx_routes(), FxPlugin, DataObject, given, test_plugin_computations_match_reference()

### Community 103 - "Architecture"
Cohesion: 0.67
Nodes (3): Architecture, Design principles, Two evaluators, one plan

### Community 104 - "calc/tests/conftest.py"
Cohesion: 0.46
Nodes (7): catalog(), engine(), frame(), positions_frame(), DataFrame, fixture, A small book of positions with every kind of column, nulls included.

### Community 105 - "engine"
Cohesion: 0.43
Nodes (7): catalog(), engine(), frame(), positions_frame(), DataFrame, fixture, A small book of positions with every kind of column, nulls included.

### Community 107 - "Formula columns"
Cohesion: 0.33
Nodes (6): `derive` or `formula`?, Formula columns, Gotchas, Result, Try it, What to notice

### Community 108 - "release_info.py"
Cohesion: 0.22
Nodes (7): os, main(), Resolve a release tag like ``core/v0.2.0`` to the package it releases.…, resolve(), subprocess, sys, tomllib

### Community 109 - "check_rollup_totals"
Cohesion: 0.67
Nodes (3): check_rollup_totals(), Each subtotal of an additive measure (sum, count) equals the sum of its…, test_rollup_orders_subtotals_after_details()

### Community 110 - "Quick start"
Cohesion: 0.33
Nodes (6): 1. Register data and create an engine, 2. Ask a question, 3. Ask "what if?", 4. Read the metadata, Next steps, Quick start

### Community 112 - "Override a cell"
Cohesion: 0.40
Nodes (5): Gotchas, Override a cell, Result, Try it, What to notice

### Community 113 - "PluginError"
Cohesion: 0.18
Nodes (11): Installing plugins, Plugins, What a plugin may import, Package it, discover_plugins(), PluginError, Instantiate every installed plugin advertised under the ``pylibs_calc.plugins``…, A plugin is misconfigured (e.g. two plugins register the same name). (+3 more)

### Community 114 - "test_plugins.py"
Cohesion: 0.14
Nodes (16): fx_engine(), FxBound, Catalog, fixture, parametrize, The plugin API, exercised by a small FX plugin: a function, an aggregate, a…, test_attach_and_lookup(), test_bind_context_is_passed() (+8 more)

## Knowledge Gaps
- **160 isolated node(s):** `What this is`, `Commands`, `Code knowledge graph (graphify)`, `Documentation`, `Architecture and conventions` (+155 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 613 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CalcEngine` connect `CalcEngine` to `pytest`, `engine.py`, `Catalog`, `docs_from_graph.py`, `spec/query.py`, `book.py`, `create_router`, `golden.py`, `test_scenarios.py`, `CalcContext`, `SpecError`, `pylibs_calc/__init__.py`, `calc/tests/test_aggrid.py`, `EngineConfig`, `fastapi.py`, `ResultCache`, `DatasetSchema`, `expr.py`, `calc/tests/test_compare.py`, `body_extensions`, `calc_whatif/tests/test_compare.py`, `WhatIfPlugin`, `CalcResult`, `add_routes`, `dtypes.py`, `verify`, `measures`, `check_pages`, `Registry`, `plugins.py`, `.register`, `calc/tests/conftest.py`, `engine`, `.schema`, `check_rollup_totals`, `.attach`, `PluginError`, `test_plugins.py`?**
  _High betweenness centrality (0.134) - this node is a cross-community bridge._
- **Why does `SpecError` connect `SpecError` to `canonical.py`, `CalcEngine`, `engine.py`, `.register_scan`, `Catalog`, `AgGridAdapter`, `ScenarioManager`, `spec/query.py`, `ext.py`, `BindContext`, `plan_mutations`, `exprs.py`, `Kernel`, `adapters/aggrid.py`, `pylibs_calc/__init__.py`, `LType`, `Write a plugin`, `compare.py`, `DatasetSchema`, `build_schema`, `expr.py`, `formula.py`, `WhatIfPlugin`, `validate.py`, `dtypes.py`, `plugin.py`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `CalcContext` connect `CalcContext` to `pytest`, `CalcEngine`, `engine.py`, `verify/reference.py`, `AgGridAdapter`, `ScenarioManager`, `BindContext`, `plan_mutations`, `create_router`, `Kernel`, `Scenario`, `adapters/aggrid.py`, `test_scenarios.py`, `pylibs_calc/__init__.py`, `EngineConfig`, `scenarios/index.md`, `fastapi.py`, `testing-guide.md`, `PlanContext`, `Access control`, `Concepts`, `CalcResult`, `add_routes`, `dtypes.py`, `verify`, `measures`, `plugins.py`, `.schema`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 25 inferred relationships involving `CalcEngine` (e.g. with `The parts` and `Your own catalog`) actually correct?**
  _`CalcEngine` has 25 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `SpecError` (e.g. with `2. A transform` and `Exception classes`) actually correct?**
  _`SpecError` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `CalcContext` (e.g. with `Glossary` and `Assumptions`) actually correct?**
  _`CalcContext` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 22 inferred relationships involving `Kernel` (e.g. with `The parts` and `Operations`) actually correct?**
  _`Kernel` has 22 INFERRED edges - model-reasoned connections that need verification._