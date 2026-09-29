# Graph Report - py-libs  (2026-09-29)

## Corpus Check
- 165 files · ~92,773 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: (none) 6, .typed 4, .lock 1)

## Summary
- 1796 nodes · 5006 edges · 103 communities (90 shown, 13 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 741 edges (avg confidence: 0.93)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `5e5b05f5`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- test_spec.py
- calc/tests/test_fastapi.py
- py-libs
- CalcEngine
- AGENTS.md
- pylibs-core
- core/README.md
- utils/README.md
- compile/query.py
- verify/reference.py
- .register_scan
- Catalog
- Logic
- docs_from_graph.py
- test_totals.py
- adapters/aggrid.py
- ext.py
- 18_custom_plugin.py
- ._keep_kind
- plugin.py
- book.py
- Any
- ShareClassPlan
- exprs.py
- Kernel
- manager.py
- .compare
- TransformPlan
- golden.py
- test_scenarios.py
- runtime_check
- Any
- LType
- normalize
- pylibs_calc/__init__.py
- calc/tests/test_aggrid.py
- calc_whatif/tests/test_fastapi.py
- Investment primer: start here
- FastAPI
- Ratios after aggregation
- Write a plugin
- Compare two sides
- Errors and limits
- Contributing to the docs
- app.py
- ResultCache
- adapters/__init__.py
- Pivot
- compile/__init__.py
- integrations/__init__.py
- spec/__init__.py
- pylibs-calc
- Numbers, types and nulls
- Weights and active weights
- Python API
- Filtered measures
- .register
- DatasetSchema
- build_schema
- Having
- Subtotals (rollup)
- hooks.py
- pytest
- plugins.md
- pylibs-calc-whatif
- Any
- CalcContext
- audit.md
- Formula language
- WhatIfPlugin
- Shock a column
- .resolve_view
- Disable a step
- holdings
- Lit
- .__init__
- AG Grid
- create_router
- Model
- ._from_str
- pylibs-calc
- validate.py
- fingerprint
- Performance
- CalcResult
- Scenario
- add_routes
- engine.py
- testing.py
- Registry
- synthetic_book
- test_plugin.py
- test_examples.py
- Plugin
- FxPlugin
- Formula columns
- calc/tests/test_runtime.py
- engine
- Override a cell
- PluginError
- test_plugins.py

## God Nodes (most connected - your core abstractions)
1. `CalcEngine` - 149 edges
2. `LType` - 103 edges
3. `SpecError` - 75 edges
4. `CalcContext` - 57 edges
5. `Kernel` - 52 edges
6. `Catalog` - 48 edges
7. `Kind` - 45 edges
8. `Model` - 44 edges
9. `AgGridAdapter` - 41 edges
10. `Typed` - 41 edges

## Surprising Connections (you probably didn't know these)
- `Options` --references--> `AgGridAdapter`  [INFERRED]
  docs/calc/integrations/fastapi.md → packages/calc/src/pylibs_calc/adapters/aggrid.py
- `1. Functions and aggregates` --references--> `LType`  [INFERRED]
  docs/calc/extending/write-a-plugin.md → packages/calc/src/pylibs_calc/dtypes.py
- `Errors` --references--> `CalcError`  [INFERRED]
  docs/calc/integrations/fastapi.md → packages/calc/src/pylibs_calc/errors.py
- `Scenario permissions (what-if plugin)` --references--> `Forbidden`  [INFERRED]
  docs/calc/scenarios/access-control.md → packages/calc/src/pylibs_calc/errors.py
- `Functions` --references--> `FunctionDef`  [INFERRED]
  docs/calc/concepts/formula-language.md → packages/calc/src/pylibs_calc/plugins.py

## Import Cycles
- 3-file cycle: `packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py`
- 4-file cycle: `packages/calc/src/pylibs_calc/compile/logical.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/logical.py`
- 4-file cycle: `packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/validate.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/compare.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/compare.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/logical.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/query.py -> packages/calc/src/pylibs_calc/compile/logical.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/query.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/query.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/exprs.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/exprs.py`
- 5-file cycle: `packages/calc/src/pylibs_calc/compile/logical.py -> packages/calc/src/pylibs_calc/compile/validate.py -> packages/calc/src/pylibs_calc/plugins.py -> packages/calc/src/pylibs_calc/integrations/fastapi.py -> packages/calc/src/pylibs_calc/engine.py -> packages/calc/src/pylibs_calc/compile/logical.py`

## Communities (103 total, 13 thin omitted)

### Community 0 - "test_spec.py"
Cohesion: 0.12
Nodes (21): canonical_json(), Any, Version 2 moved what-if into the ``whatif`` plugin: ``scenario``, ``what_if``…, The request's ``spec_version``; a request without one is version 1 if it uses…, Bring a raw request dict up to the current ``spec_version``., JSON-ready canonical form of a model, or of plain data containing models., request_version(), to_canonical() (+13 more)

### Community 1 - "calc/tests/test_fastapi.py"
Cohesion: 0.22
Nodes (13): io, client(), resolve(), fixture, parametrize, TestClient, test_body_limit(), test_context_applies_row_filter() (+5 more)

### Community 2 - "py-libs"
Cohesion: 0.22
Nodes (8): Adding a package, Building, Development, Layout, License, One-time setup, py-libs, Releasing

### Community 3 - "CalcEngine"
Cohesion: 0.12
Nodes (35): CalcEngine, Evaluate calculation requests over a…, check_pages(), Any, Paging through a view yields each row exactly once, in the unpaged order., Any, Evaluate one expression on the row with id 1., run() (+27 more)

### Community 4 - "AGENTS.md"
Cohesion: 0.25
Nodes (6): Architecture and conventions, Code knowledge graph (graphify), Commands, Documentation, Releasing, What this is

### Community 9 - "compile/query.py"
Cohesion: 0.18
Nodes (24): LogicalQuery, agg_frame(), _aggregate(), count_frame(), domain_frame(), _grand_totals(), _hidden(), _input_name() (+16 more)

### Community 10 - "verify/reference.py"
Cohesion: 0.14
Nodes (37): pivot_label(), Any, The internal column that holds ``total(measure)``: the measure over all rows., total_column(), quantize(), aggregate_levels(), _binary(), _cast() (+29 more)

### Community 11 - ".register_scan"
Cohesion: 0.16
Nodes (15): Concepts, Formula language, Measures, Numbers, types and nulls, _check_keys(), _check_names(), content_version(), file_version() (+7 more)

### Community 12 - "Catalog"
Cohesion: 0.08
Nodes (29): Datasets and the catalog, Datasets without a key, Registering data, Versions, Your own catalog, Reporting a problem, Troubleshooting, Catalog (+21 more)

### Community 13 - "Logic"
Cohesion: 0.25
Nodes (14): _blank(), _date(), decode_group_key(), encode_group_key(), _equals(), _literal(), Any, Node (+6 more)

### Community 14 - "docs_from_graph.py"
Cohesion: 0.05
Nodes (60): argparse, numpy, book(), main(), Any, DataFrame, Latency benchmark for typical grid requests on a synthetic book of positions.…, timed() (+52 more)

### Community 15 - "test_totals.py"
Cohesion: 0.18
Nodes (16): Any, DataFrame, parametrize, ``total(m)``: a measure over all the rows a query sees, for weights and shares…, Active weight: two portfolios in one dataset, each with its own denominator., run(), test_each_compare_side_has_its_own_total(), test_having_does_not_change_the_denominator() (+8 more)

### Community 16 - "adapters/aggrid.py"
Cohesion: 0.07
Nodes (43): The life of a request, Python models, json, Quick start, AgGridAdapter, ColumnVO, _Lenient, BaseModel (+35 more)

### Community 17 - "ext.py"
Cohesion: 0.09
Nodes (35): datetime, Enum, field_validator, math, canonical_decimal(), coerce_value(), decimal(), decimal_places() (+27 more)

### Community 18 - "18_custom_plugin.py"
Cohesion: 0.21
Nodes (10): bind_share_class(), fx_ladder(), Ladder, Decimal, A custom plugin: value the fund in a share class currency, and an FX…, ``engine.call("fx_ladder", {...})``: the query with the share class currency…, The request block: ``{"share_class": {"currency": "GBP", "usd_rates": {"GBP":…, ShareClass (+2 more)

### Community 19 - "._keep_kind"
Cohesion: 0.50
Nodes (3): model_serializer, Any, SerializerFunctionWrapHandler

### Community 20 - "plugin.py"
Cohesion: 0.07
Nodes (41): decimal, _editable(), effective_steps(), FormulaDef, LabeledStep, LogicalMutations, OverrideBatch, plan_mutations() (+33 more)

### Community 21 - "book.py"
Cohesion: 0.08
Nodes (23): Quick start: the fund's market value and weight by asset class., Filter + derive: the fund's non-USD holdings, in USD, with the analyst's upside…, Measures: value, counts, simple and value-weighted yield, and longest duration., Filtered measures: the fund's asset mix per region, side by side, like SQL…, Post-aggregation: upside to the analysts' targets per region, as a ratio of…, Having: holdings over a 10% concentration limit, and sectors more than 5 points…, Rollup: fund -> asset class -> sector, with each subtotal's weight in the fund., Pivot: currency exposure by asset class, as weights in the fund, with row… (+15 more)

### Community 22 - "Any"
Cohesion: 0.16
Nodes (6): Fx, FxBound, FxPlan, Named, Any, LazyFrame

### Community 23 - "ShareClassPlan"
Cohesion: 0.19
Nodes (6): numbers_to_float(), Any, LazyFrame, Adds ``mv_sc``: price x quantity, from the row's currency into the share class…, Per row currency: how many share class units one unit of it is worth., ShareClassPlan

### Community 24 - "exprs.py"
Cohesion: 0.17
Nodes (31): What a plugin may import, functools, operator, as_type(), _binary(), _bool(), _cast(), compile_expr() (+23 more)

### Community 25 - "Kernel"
Cohesion: 0.14
Nodes (17): Finished, Kernel, _page(), DataFrame, EngineName, LazyFrame, A dataset version as one caller sees it, after the requested plugin transforms., The engine's machinery, shared by the built-in calls and by plugin operations.… (+9 more)

### Community 26 - "manager.py"
Cohesion: 0.11
Nodes (25): Errors raised by the what-if plugin., Saved what-if scenarios: append-only, hash-chained logs of steps over a dataset…, parse_steps(), Any, ScenarioStep, Creating, editing, forking and auditing scenarios, with validation and…, Copy a scenario's effective steps (at a version) into a new, independent…, Recompute the hash chain; False means the stored log was altered. (+17 more)

### Community 27 - ".compare"
Cohesion: 0.33
Nodes (9): SortSpec, finish_aggregate(), _hierarchical_sort(), _pivot(), DataFrame, Subtotal rows directly after their details; the grand total last., sort_frame(), Run a query on two sides and join them with deltas (see… (+1 more)

### Community 28 - "TransformPlan"
Cohesion: 0.12
Nodes (13): ABC, Bound, DataFrame, LazyFrame, Row, Run a (small) query under the engine's concurrency limit and the request…, A validated transform, ready to run. The engine caches it (see :class:`Bound`).…, The Polars implementation. (+5 more)

### Community 29 - "golden.py"
Cohesion: 0.53
Nodes (5): check(), Any, Golden cases: requests over the example fund with their expected results. Each…, run_case(), update()

### Community 30 - "test_scenarios.py"
Cohesion: 0.20
Nodes (22): fakeredis, prices(), Any, scenarios(), shock(), test_authorization_hook(), authorize(), test_create_append_and_run() (+14 more)

### Community 31 - "runtime_check"
Cohesion: 0.14
Nodes (14): Check the runtime, Install, Working on the library itself, Checklist, Deploying on Kubernetes, Example, Performance and deployment, cgroup_cpu_limit() (+6 more)

### Community 32 - "Any"
Cohesion: 0.10
Nodes (13): Architecture, Design principles, The parts, Two evaluators, one plan, 3. An operation, M, _ms(), Any (+5 more)

### Community 33 - "LType"
Cohesion: 0.08
Nodes (52): BinaryOp, Functions and aggregates, _and(), check_name(), _col(), DerivePlan, HiddenAgg, materializable() (+44 more)

### Community 34 - "normalize"
Cohesion: 0.33
Nodes (6): raw(), scan(), normalize(), DataType, LazyFrame, Cast to the engine's canonical dtypes and turn NaN/infinite floats into nulls.…

### Community 35 - "pylibs_calc/__init__.py"
Cohesion: 0.09
Nodes (36): contextlib, Exception classes, InProcessQuery, _too_many_rows(), CalcError, CalcTimeout, ComputeError, DatasetNotFound (+28 more)

### Community 36 - "calc/tests/test_aggrid.py"
Cohesion: 0.28
Nodes (15): column(), Any, parametrize, rows(), ssrm(), test_custom_aggregation(), test_drill_down_with_null_group_key(), test_filters() (+7 more)

### Community 37 - "calc_whatif/tests/test_fastapi.py"
Cohesion: 0.31
Nodes (8): fastapi_testclient, client(), resolve(), fixture, TestClient, test_aggrid_rows_and_edit(), test_compare_and_distinct_with_what_if(), test_scenario_lifecycle()

### Community 38 - "Investment primer: start here"
Cohesion: 0.25
Nodes (8): 1. The fund, column by column, 2. Numbers you compute from the holdings, 3. Asking "what if?", 4. The people involved, 5. Cheat sheet: finance word → what to type, Investment primer: start here, Next steps, What each column means

### Community 39 - "FastAPI"
Cohesion: 0.25
Nodes (7): Errors, FastAPI, Options, Routes, Routes added by plugins, Threading, RoutesHook

### Community 40 - "Ratios after aggregation"
Cohesion: 0.40
Nodes (5): Gotchas, Ratios after aggregation, Result, Try it, What to notice

### Community 41 - "Write a plugin"
Cohesion: 0.21
Nodes (10): 1. Functions and aggregates, 2. A transform, 4. The plugin, 5. Use it, Checklist, Test it against the reference, Write a plugin, test_bind_context_is_passed() (+2 more)

### Community 42 - "Compare two sides"
Cohesion: 0.33
Nodes (6): Choosing the two sides, Compare two sides, Gotchas, Result, Try it, What to notice

### Community 44 - "Errors and limits"
Cohesion: 0.12
Nodes (15): Minimal requests, Request schema, Versions, Errors and limits, Limits, Result, Time and load, Try it (+7 more)

### Community 45 - "Contributing to the docs"
Cohesion: 0.12
Nodes (12): Adding a feature page, Commands, Contributing to the docs, How the graph keeps the docs in step, Layout, Style, How these docs are organized, py-libs (+4 more)

### Community 46 - "app.py"
Cohesion: 0.25
Nodes (7): fastapi, fastapi_responses, get, os, index(), Demo service: pylibs-calc with the what-if plugin behind FastAPI, and an AG…, scenario_store()

### Community 49 - "Pivot"
Cohesion: 0.33
Nodes (6): Gotchas, Options, Pivot, Result, Try it, What to notice

### Community 54 - "Numbers, types and nulls"
Cohesion: 0.18
Nodes (8): Exact decimals, Float sums and reproducibility, Floats and decimals never mix silently, Invalid arithmetic gives null, Nulls follow SQL, Numbers, types and nulls, Settings, Shocks keep the column's type

### Community 55 - "Weights and active weights"
Cohesion: 0.33
Nodes (6): Gotchas, Result, Try it, Weights and active weights, What "every row the query sees" means, What to notice

### Community 56 - "Python API"
Cohesion: 0.15
Nodes (13): Data, Engine, Errors, Formulas and fingerprints, Integrations, Plugin API, Protocols, Python API (+5 more)

### Community 57 - "Filtered measures"
Cohesion: 0.40
Nodes (5): Filtered measures, Gotchas, Result, Try it, What to notice

### Community 58 - ".register"
Cohesion: 0.33
Nodes (4): fx_routes(), Ladder, The same query at several FX rates, stacked with a ``rate`` column., run_ladder()

### Community 59 - "DatasetSchema"
Cohesion: 0.10
Nodes (14): What registration does, Dataset, DatasetCatalog, Protocol, One immutable version of a dataset., Keyless datasets carry a hidden ``__row`` column so row views have a total…, What the engine needs from a catalog; implement it to serve datasets your own…, AppliedTransform (+6 more)

### Community 60 - "build_schema"
Cohesion: 0.29
Nodes (6): build_schema(), Collection, DataType, Role, The schema as seen by a caller limited to ``allowed`` columns (keys always…, Describe a dataset. Numeric columns default to measures, the rest to…

### Community 61 - "Having"
Cohesion: 0.40
Nodes (5): Gotchas, Having, Result, Try it, What to notice

### Community 62 - "Subtotals (rollup)"
Cohesion: 0.40
Nodes (5): Gotchas, Result, Subtotals (rollup), Try it, What to notice

### Community 63 - "hooks.py"
Cohesion: 0.39
Nodes (7): on_config(), on_page_markdown(), on_pre_build(), Any, MkDocs hooks: make the examples importable, and flag pages the code has moved…, _sync_module(), importlib_util

### Community 64 - "pytest"
Cohesion: 0.12
Nodes (14): DataFrame, test_compare_rejects_pivot(), test_compare_two_dataset_versions(), test_compare_with_itself_has_no_deltas(), test_unknown_extensions_are_rejected(), total() sees the shocked rows, so a sector's weight moves as well as its value., shock(), test_aggregated_compare() (+6 more)

### Community 65 - "plugins.md"
Cohesion: 0.15
Nodes (9): All routes, Call the API with curl, Discover the data, Get exact decimals, or Arrow, Run a query, See how a number is computed, Try a what-if, When something is wrong (+1 more)

### Community 66 - "pylibs-calc-whatif"
Cohesion: 0.33
Nodes (5): Limits, pylibs-calc-whatif, Quick start, Saved scenarios, Steps

### Community 67 - "Any"
Cohesion: 0.40
Nodes (3): Any, JSON data reported in ``ResultMeta.extensions[<transform>]``., JSON data reported by ``engine.explain`` under ``extensions.<transform>``.

### Community 68 - "CalcContext"
Cohesion: 0.07
Nodes (26): Glossary, Assumptions, Assumptions and limitations, Not supported yet, Out of scope, Exploratory testing checklist, Test a service built on the engine, Testing guide (+18 more)

### Community 69 - "audit.md"
Cohesion: 0.20
Nodes (6): Golden cases, Also useful, Audit a number, Result, The three tools, Try it

### Community 70 - "Formula language"
Cohesion: 0.11
Nodes (15): Cheat sheet, Errors, Formula language, Formulas are stored as trees, Functions, Filter and derive, Gotchas, Result (+7 more)

### Community 71 - "WhatIfPlugin"
Cohesion: 0.07
Nodes (23): Coming from version 0.1, In the engine, Limits, The request block, What-if plugin, FixtureRequest, Caps on what-if work; exceeding one is a 413., WhatIfLimits (+15 more)

### Community 72 - "Shock a column"
Cohesion: 0.33
Nodes (6): Gotchas, Result, Shock a column, The operations, Try it, What to notice

### Community 73 - ".resolve_view"
Cohesion: 0.50
Nodes (3): Load the dataset version and apply the transforms named in ``extensions``., BindContext, What a transform sees when a request is resolved (before the dataset is loaded).

### Community 74 - "Disable a step"
Cohesion: 0.40
Nodes (5): Disable a step, Gotchas, Result, Try it, What to notice

### Community 75 - "holdings"
Cohesion: 0.18
Nodes (11): Run the demo grid, Start it, Things to try, Core engine, Pages, Scenarios by feature, The example fund, What-if plugin (+3 more)

### Community 76 - "Lit"
Cohesion: 0.07
Nodes (41): AST, Call, Constant, keyword, _coerce(), IfElse, InList, Lit (+33 more)

### Community 78 - "AG Grid"
Cohesion: 0.50
Nodes (4): AG Grid, Client setup, Customizing the adapter, Gotchas

### Community 79 - "create_router"
Cohesion: 0.13
Nodes (19): ContextResolver, DependsParam, _call(), create_router(), body_limit(), call_operation(), context(), dataset_schema() (+11 more)

### Community 80 - "Model"
Cohesion: 0.12
Nodes (28): Python API at a glance, Model, BaseModel, Frozen pydantic model that rejects unknown fields. Dumps always carry the…, CellEdit, edit_to_override(), BaseModel, AG Grid cell edits as what-if overrides (grid set up with ``readOnlyEdit:… (+20 more)

### Community 82 - "pylibs-calc"
Cohesion: 0.67
Nodes (3): A request at a glance, pylibs-calc, What it does

### Community 83 - "validate.py"
Cohesion: 0.15
Nodes (24): compare_frame(), ComparePlan, plan_compare(), LazyFrame, Two-way compare: join a target and a base result, with deltas typed like any…, Node, The measures named by ``total()`` calls (already type-checked)., _totals_used() (+16 more)

### Community 84 - "fingerprint"
Cohesion: 0.17
Nodes (9): AG Grid (server-side row model), Compare, FastAPI, Not supported yet, pylibs-calc, Verifiability, Describe what a request computes: transform steps, lineage, types and the…, fingerprint() (+1 more)

### Community 87 - "Performance"
Cohesion: 0.50
Nodes (3): Benchmarks, Guidance, Performance

### Community 88 - "CalcResult"
Cohesion: 0.08
Nodes (24): HTTP routes, Operations, The extension points, Transforms, 4. Read the metadata, body_extensions(), aggrid_rows(), run() (+16 more)

### Community 89 - "Scenario"
Cohesion: 0.09
Nodes (26): Durability, How it works, Redis scenario store, Testing, Gotchas, Over HTTP, Result, Saved scenarios and forks (+18 more)

### Community 90 - "add_routes"
Cohesion: 0.24
Nodes (12): add_routes(), aggrid_edit(), run(), append_steps(), create_scenario(), delete_scenario(), fork_scenario(), get_scenario() (+4 more)

### Community 91 - "engine.py"
Cohesion: 0.11
Nodes (30): collections, collections_abc, dataclasses, fastapi_params, glob, hashlib, importlib_metadata, frame_size() (+22 more)

### Community 93 - "testing.py"
Cohesion: 0.06
Nodes (53): From dataset to result, Inside the query, Inside the what-if transform, Order of evaluation, Why the order matters, hypothesis, dec_expr(), dec_literal() (+45 more)

### Community 96 - "Registry"
Cohesion: 0.24
Nodes (4): A dataset transform, enabled per request by ``extensions[name]``. ``model``…, Everything the engine's plugins registered. Names are unique across plugins., Registry, TransformDef

### Community 97 - "synthetic_book"
Cohesion: 0.50
Nodes (3): DataFrame, Deterministic pseudo-random fund holdings (no numpy needed), with the same…, synthetic_book()

### Community 98 - "test_plugin.py"
Cohesion: 0.10
Nodes (20): _imports(), Any, Decimal, LazyFrame, Path, The what-if plugin through the plugin API: request shape, composition,…, test_a_plugin_instance_belongs_to_one_engine(), test_core_does_not_know_the_plugin() (+12 more)

### Community 100 - "test_examples.py"
Cohesion: 0.15
Nodes (17): CaptureFixture, demo_engine(), _load_book(), Any, fixture, parametrize, Run every documentation example, so a change that breaks the docs also breaks…, Every top-level ``*REQUEST = {...}`` literal in the example scripts. (+9 more)

### Community 101 - "Plugin"
Cohesion: 0.22
Nodes (5): P, An installed plugin, by name or by class., Plugin, Base class for plugins. Subclasses set ``name`` and ``version`` and override…, Called once, after every plugin registered.

### Community 102 - "FxPlugin"
Cohesion: 0.25
Nodes (6): fx_engine(), FxPlugin, DataObject, fixture, given, test_plugin_computations_match_reference()

### Community 107 - "Formula columns"
Cohesion: 0.33
Nodes (6): `derive` or `formula`?, Formula columns, Gotchas, Result, Try it, What to notice

### Community 108 - "calc/tests/test_runtime.py"
Cohesion: 0.18
Nodes (8): test_timeout_cancels_the_query(), pathlib, main(), Resolve a release tag like ``core/v0.2.0`` to the package it releases.…, resolve(), subprocess, sys, tomllib

### Community 110 - "engine"
Cohesion: 0.10
Nodes (14): 1. Register data and create an engine, 2. Ask a question, 3. Ask "what if?", Next steps, Quick start, Shocks: tech stocks -10% and bond yields +25bp; then the dollar strengthens 5%., Disable: undo a saved step without rewriting history., Saved scenarios: create, append with optimistic locking, read old versions,… (+6 more)

### Community 112 - "Override a cell"
Cohesion: 0.40
Nodes (5): Gotchas, Override a cell, Result, Try it, What to notice

### Community 113 - "PluginError"
Cohesion: 0.20
Nodes (10): Installing plugins, Plugins, Package it, discover_plugins(), PluginError, Instantiate every installed plugin advertised under the ``pylibs_calc.plugins``…, A plugin is misconfigured (e.g. two plugins register the same name)., Demo (+2 more)

### Community 114 - "test_plugins.py"
Cohesion: 0.15
Nodes (15): _clip_type(), _median_type(), _numeric(), parametrize, The plugin API, exercised by a small FX plugin: a function, an aggregate, a…, test_attach_and_lookup(), test_functions_are_per_engine(), test_operation() (+7 more)

## Knowledge Gaps
- **167 isolated node(s):** `pylibs-calc`, `pylibs-calc-whatif`, `pylibs-core`, `pylibs-utils`, `What this is` (+162 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 617 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CalcEngine` connect `CalcEngine` to `calc/tests/test_fastapi.py`, `Catalog`, `docs_from_graph.py`, `test_totals.py`, `adapters/aggrid.py`, `.compare`, `test_scenarios.py`, `Any`, `LType`, `pylibs_calc/__init__.py`, `calc/tests/test_aggrid.py`, `calc_whatif/tests/test_fastapi.py`, `ResultCache`, `DatasetSchema`, `pytest`, `CalcContext`, `WhatIfPlugin`, `Lit`, `create_router`, `Model`, `fingerprint`, `CalcResult`, `engine.py`, `testing.py`, `Registry`, `test_plugin.py`, `Plugin`, `FxPlugin`, `engine`, `PluginError`, `test_plugins.py`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `CalcContext` connect `CalcContext` to `calc/tests/test_fastapi.py`, `CalcEngine`, `Catalog`, `adapters/aggrid.py`, `18_custom_plugin.py`, `Kernel`, `manager.py`, `.compare`, `test_scenarios.py`, `Any`, `pylibs_calc/__init__.py`, `calc_whatif/tests/test_fastapi.py`, `.register`, `DatasetSchema`, `WhatIfPlugin`, `.resolve_view`, `create_router`, `fingerprint`, `CalcResult`, `Scenario`, `engine.py`, `testing.py`?**
  _High betweenness centrality (0.073) - this node is a cross-community bridge._
- **Why does `SpecError` connect `LType` to `test_spec.py`, `CalcEngine`, `compile/query.py`, `.register_scan`, `Catalog`, `Logic`, `adapters/aggrid.py`, `ext.py`, `plugin.py`, `ShareClassPlan`, `exprs.py`, `Kernel`, `manager.py`, `.compare`, `pylibs_calc/__init__.py`, `Write a plugin`, `DatasetSchema`, `build_schema`, `WhatIfPlugin`, `Lit`, `Model`, `validate.py`, `engine.py`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Are the 27 inferred relationships involving `CalcEngine` (e.g. with `The parts` and `Your own catalog`) actually correct?**
  _`CalcEngine` has 27 INFERRED edges - model-reasoned connections that need verification._
- **Are the 51 inferred relationships involving `LType` (e.g. with `What a plugin may import` and `1. Functions and aggregates`) actually correct?**
  _`LType` has 51 INFERRED edges - model-reasoned connections that need verification._
- **Are the 21 inferred relationships involving `SpecError` (e.g. with `2. A transform` and `Exception classes`) actually correct?**
  _`SpecError` has 21 INFERRED edges - model-reasoned connections that need verification._
- **Are the 19 inferred relationships involving `CalcContext` (e.g. with `Glossary` and `Assumptions`) actually correct?**
  _`CalcContext` has 19 INFERRED edges - model-reasoned connections that need verification._