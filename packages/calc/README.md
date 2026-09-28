# pylibs-calc

An embeddable **calculation engine** on [Polars](https://pola.rs), for the grids that finance
teams slice, edit and aggregate, **extensible with plugins**. It is a library, not a service. You
embed it in your own FastAPI (or any Python) service.

The **core engine** does what nearly every analytics service needs:

- **Rows:** filters and derived columns.
- **Aggregation:** group-by with measures (including filtered measures and weighted averages), ratios computed after aggregation, subtotals (rollup) and pivots.
- **Comparison:** the same query on two sides (data versions, or any plugin's transform), with deltas.
- **Exact decimals:** exact `Decimal` arithmetic with explicit rounding rules.
- **Reproducible results:** a fingerprint on every result, and a pure-Python reference evaluator to check the engine against.
- **Integrations:** an adapter for the AG Grid server-side row model and a FastAPI router.

**Plugins** add analyses on top: functions, aggregates, dataset transforms, whole new operations
and HTTP routes. What-if analysis (cell overrides, shocks, formula columns, saved and forkable
scenarios) is the [`pylibs-calc-whatif`](../calc_whatif) plugin.

```bash
pip install pylibs-calc                  # the core engine (polars + pydantic)
pip install "pylibs-calc[fastapi]"       # + FastAPI router
pip install "pylibs-calc[testing]"       # + Hypothesis strategies for testing plugins
pip install pylibs-calc-whatif           # + the what-if plugin
```

**Documentation:** the [docs site](https://github.com/sanjaysharmagwl/py-libs/tree/master/docs/calc)
has a runnable, finance-flavoured scenario for every feature, a QA guide and the API reference.
From a clone, `make install && make docs-serve` serves it locally.

## Quick start

```python
import polars as pl
from pylibs_calc import Catalog, CalcEngine

catalog = Catalog()
catalog.register_frame("positions", df, key_columns=["position_id"], version="2026-09-26")
engine = CalcEngine(catalog)  # plugins=[...] to add analyses

result = engine.run(
    {
        "dataset": "positions",
        "query": {
            "filter": "region == 'EMEA' and quantity != 0",
            "derive": [{"name": "notional", "expr": "price * quantity"}],
            "group_by": ["desk", "sector"],
            "rollup": True,
            "measures": [
                {"name": "notional", "fn": "sum", "of": "notional"},
                {"name": "yield", "fn": "wavg", "of": "yield", "weight": "abs(float(notional))"},
                {"name": "positions", "fn": "count_rows"},
            ],
            "sort": [{"by": "desk"}],
            "page": {"offset": 0, "limit": 100},
        },
    }
)
result.frame  # a polars DataFrame
result.meta.fingerprint  # SHA-256 of the fully resolved request
result.meta.total_rows  # rows before paging (for the grid's row count)
```

A request is plain JSON (or the equivalent pydantic models: `CalcRequest`, `Query`, `Measure`, ...).
Expressions can be written as formulas like `"price * quantity"` or as expression trees. They are
always stored and fingerprinted as trees.

## Concepts

**Datasets** live in a `Catalog`. Each version is immutable:

- **In memory:** `register_frame` takes a DataFrame.
- **Lazily scanned files:** `register_scan` takes Parquet or Arrow IPC, local or on object storage.

Registration also normalizes the data:

- Integers become `Int64`, floats `Float64`, decimals `Decimal(38, s)`, and enums `String`. Categoricals stay categorical.
- NaN and infinities become null.
- Key columns are checked: they must have no nulls and no duplicates.

**Plugins** extend an engine. Each one registers what it adds when the engine is built:

```python
from pylibs_calc_whatif import InMemoryScenarioStore, WhatIfPlugin

engine = CalcEngine(catalog, plugins=[WhatIfPlugin(store=InMemoryScenarioStore())])
engine.run({"dataset": "positions", "extensions": {"whatif": {"steps": [...]}}, "query": {...}})
```

| Extension point | Registered with | Used as |
| --- | --- | --- |
| Functions | `registry.add_function(FunctionDef(...))` | a function in any formula |
| Aggregates | `registry.add_aggregate(AggregateDef(...))` | a measure `fn` |
| Transforms | `registry.add_transform(TransformDef(...))` | a request block under `extensions` |
| Operations | `registry.add_operation(OperationDef(...))` | `engine.call(name, request)`, `POST /operations/{name}` |
| HTTP routes | `registry.add_routes(hook)` | routes on the FastAPI router |

Every computation a plugin adds has a Polars implementation and a plain-Python one for the
reference evaluator; `pylibs_calc.testing` fuzzes the two against each other. Plugins import only
`pylibs_calc`, `pylibs_calc.ext` and `pylibs_calc.integrations.fastapi`. Installed plugin packages
advertise themselves under the `pylibs_calc.plugins` entry point, so `discover_plugins()` finds
them.

**Queries** run their stages in a fixed order:

1. `filter`
2. `derive`
3. `group_by` + `measures`
4. `post` (ratios over measures)
5. `having`
6. `rollup`
7. `pivot`
8. `sort`
9. `page`

The order of evaluation is:

1. The dataset version, after the caller's row filter and column restrictions.
2. The plugin transforms named in `extensions`, in the order the plugins were installed.
3. The query.

### Measures

| `fn` | Meaning |
| --- | --- |
| `sum` | Sum; **null when there is nothing to sum**, as in SQL |
| `mean` | `sum / count` of non-null values |
| `min`, `max` | Also for strings and dates |
| `count` | Non-null values |
| `count_rows` | Rows |
| `count_distinct` | Distinct non-null values |
| `wavg` | `sum(of * weight) / sum(weight)` over rows where both are present |

Any measure can have a `where`, which works like SQL `FILTER (WHERE ...)`. Ratios belong in
`post`, for example `{"name": "avg_px", "expr": "notional / quantity"}`. Post expressions and
`wavg` are computed from sums at every level, so a ratio is always a ratio of sums, never an
average of ratios.

Subtotals: with `rollup`, every level is computed from the base rows. The output has a
`__level` column (0 is the grand total), and subtotal rows sort directly after their details.

Plugins can add more measure functions (a median, a VaR quantile). Like the built-ins, they are
recomputed from the rows at every level.

Pivots: `pivot: {"on": ["region"], "totals": true}` creates columns named `EMEA_notional` and
so on. The pivot values are the sorted distinct values, unless you pass an explicit `domain`.

### Formula language

The formulas use a whitelisted subset of Python's expression syntax, parsed with `ast`. They are never `eval`'d.

- **Columns:** a plain name such as `price` (keywords like `yield` work too), or `col('Market Value')` for any other name.
- **Numbers:** `1.05` is an *exact* decimal.
- **Other literals:** strings, `True`/`False`/`None`, `date('2026-01-31')`, `datetime(...)`.
- **Arithmetic:** `+ - * / **`.
- **Comparisons:** `== != < <= > >=`, including chains like `0 < x <= 1`.
- **Logic:** `and`, `or`, `not`.
- **Membership and nulls:** `x in (...)`, `x not in (...)`, `x is None`, `x is not None`.
- **Conditionals:** `a if cond else b`.
- **Functions:** `abs round floor ceil sqrt log exp min max coalesce lower upper contains starts_with ends_with`, plus any a plugin adds.
- **Casts:** `int() float() str() decimal(x, scale) to_date()`.

### Numbers, types and nulls

The same typing rules are used by the validator, the Polars compiler and the reference evaluator.

**Decimal arithmetic** is exact, and every result is rounded explicitly with **half-to-even**. Precision is always 38. The result scale depends on the operation:

| Operation | Result scale |
| --- | --- |
| `+`, `-` | `max(sa, sb)` |
| `*` | `sa + sb`, capped at `NumericConfig.max_scale` (default 18) |
| `/` | `max(division_scale, sa, sb)` (default 10) |

**Integer division:** `int / int` is an exact decimal at `division_scale`, not a truncating integer division.

**Mixing types:**
- A decimal literal (`1.05`) becomes a float when combined with a float column, so `yield * 1.05` works.
- A float column and a decimal column never mix silently: `price * yield` is a 422 error until you write `float(price) * yield`.

**Nulls follow SQL:**
- Comparisons with null give null.
- A null condition counts as false (in `filter`, `where` and `if`).
- `and` and `or` use three-valued logic.

**Invalid arithmetic** gives null: `x / 0`, `sqrt(-1)` and `log(0)`.

**Float sums** can differ in the last bits between runs, because Polars adds values in parallel.
Pass `"options": {"deterministic": true}` to sum in sorted order; it's slower but reproducible.
Decimal results are always exact.

## Compare

**Compare** runs one query on two sides and joins the results. A side is the dataset (at a
version) with its own plugin `extensions`: two data versions, the base data and a what-if
scenario, or two scenarios.

```python
engine.compare(
    {
        "dataset": {"id": "positions", "version": "2026-09-26"},
        "base": {"version": "2026-09-25"},
        "query": {
            "group_by": ["desk"],
            "measures": [{"name": "mv", "fn": "sum", "of": "price * quantity"}],
            "sort": [{"by": "mv__delta", "desc": True}],
        },
    }
)
```

- Each measure `m` comes back as `m` (the target side), `m__base`, `m__delta` and `m__pct`.
- `m__pct` is null when the base is 0.
- Row-level views are joined on the dataset's key columns.

## FastAPI

```python
from pylibs_calc.integrations.fastapi import create_router

app.include_router(
    create_router(
        engine,
        prefix="/calc",
        dependencies=[Depends(auth)],
        context_resolver=lambda req: CalcContext(
            principal=req.state.user,
            row_filter=f"desk in {tuple(req.state.desks)!r}",
            allowed_columns=req.state.columns,
        ),
    )
)
```

| Route | Purpose |
| --- | --- |
| `POST /query`, `/compare`, `/explain` | Run a request. `/query` also returns Arrow IPC for `Accept: application/vnd.apache.arrow.stream` |
| `POST /aggrid/rows` | AG Grid SSRM `getRows` |
| `POST /distinct` | Distinct values of a column (for set filters) |
| `GET /datasets`, `/datasets/{id}/schema` | Columns with type, role (key, dimension or measure) and whether they can be edited |
| `GET /operations`, `POST /operations/{name}` | List and run plugin operations |

Plugins add their own routes; the what-if plugin adds `/scenarios/...` and `/aggrid/edit`.

Routes are plain `def` functions, so FastAPI runs them in its thread pool and Polars never blocks
the event loop. Errors come back as `{"detail": {"code", "message", "path"}}` with the error's HTTP
status:

| Status | Codes |
| --- | --- |
| 422 | `invalid_request`, `formula_syntax`, `unknown_column`, `type_mismatch`, `unmatched_edits`, ... |
| 404 | `dataset_not_found`, `scenario_not_found` (what-if plugin) |
| 409 | `version_conflict` |
| 413 | `limit_exceeded` |
| 503 | `engine_busy` |
| 504 | `timeout` |

`CalcContext` is how the host enforces access:

- `row_filter` is applied before anything else.
- `allowed_columns` hides every other non-key column.
- `EngineConfig.authorize(ctx, action, resource)` is called by plugins before protected actions (the what-if plugin's scenario actions) and can refuse them.
- `EngineConfig.on_result(meta, ctx)` sees every result, for audit logging.

## AG Grid (server-side row model)

The adapter translates the grid's requests into engine requests:

- `rowGroupCols` and `groupKeys` become group levels.
- `valueCols` become measures.
- `pivotMode` becomes a pivot. The pivot columns are computed once from the filter model, so they stay stable while you drill down.
- `sortModel` becomes sorting.
- The `filterModel` filter types `text`, `number`, `date`, `set`, combined conditions and `multi` are supported.

```js
const gridOptions = {
  rowModelType: 'serverSide',
  serverSideDatasource: { getRows: p => fetch('/calc/aggrid/rows', {method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({dataset: 'positions', extensions, request: p.request})})
    .then(r => r.json()).then(d => p.success(d)).catch(() => p.fail()) },
  getRowId: p => p.data.__row_id,
  getServerSideGroupKey: d => d.__group_key,   // typed keys: nulls, dates and decimals round-trip
  serverSidePivotResultFieldSeparator: '_',
  readOnlyEdit: true,                           // with the what-if plugin: edits become overrides
  onCellEditRequest: e => { /* POST /calc/aggrid/edit, then api.refreshServerSide() */ },
};
```

The server-side row model is an AG Grid **Enterprise** feature. The what-if plugin's
[examples/](../calc_whatif/examples/) has a runnable demo with grouping, pivoting, editing and a
compare table:

```bash
uv run --with uvicorn uvicorn --app-dir packages/calc_whatif/examples app:app --port 8000
```

## Verifiability

**Fingerprints.** Every result's metadata carries:
- a SHA-256 `fingerprint` of the canonical, fully resolved request (dataset version, effective transform steps, query, numeric settings and caller context)
- the dataset version, and what each plugin transform reports (`meta.extensions`)
- the library versions
- timings, and with `"options": {"audit": true}` the row counts at each stage

The same fingerprint on the same library versions means the same answer, and results are cached under it.

**Explain.** `engine.explain(request)` shows:
- the effective transform steps, and what each transform explains (for what-if: which steps changed each column)
- the formula behind every derived column
- the output types
- the optimized Polars plan

**The reference evaluator.** `pylibs_calc.verify.reference` evaluates the same logical plans
row by row, with exact `Decimal` arithmetic and no Polars. `verify(engine, request)` runs the
engine and the reference on the same rows and reports every difference. On datasets larger than
`max_rows` it uses a random sample. Plugin transforms take part through their own reference
implementations. Use it in a canary job or before upgrading Polars.

The test suite runs thousands of randomly generated datasets and requests through it with
Hypothesis. That process found real edge cases before release, including a Polars background-query
panic that the executor now works around.

## Performance and deployment

Measured with [benchmarks/bench.py](benchmarks/bench.py) on 10 million positions,
`POLARS_MAX_THREADS=4`, on an Apple M1. Times are p50 / p95 in milliseconds:

| Request | String dimensions | Categorical dimensions |
| --- | --- | --- |
| filter, 2 derived columns, 3-key group-by, 5 measures | 979 / 1069 | 552 / 602 |
| filter, sort by a derived column, one page of 100 rows | 255 / 272 | 233 / 244 |
| pivot: sector × region, 2 measures, totals | 456 / 545 | 361 / 409 |
| what-if scenario (100 overrides, a shock, a formula), then group-by | 989 / 1133 | 838 / 1001 |
| 3-level rollup of an exact-decimal product | 1247 / 1614 | 920 / 1053 |
| next page of a cached aggregate (grid scrolling) | 0.6 / 0.7 | 0.5 / 0.6 |

Guidance:

- **Store dimensions as Categorical.** Grouping is about twice as fast, and the catalog keeps categoricals.
- **Use Decimal columns only where exactness matters.** Decimal sums and products cost 2–7× their float equivalents.
- **Paging is cheap after the first request.** Aggregates are cached by content hash, and later pages are sliced from the cache. Row views push sorting and slicing into Polars, so a page of a large table never builds the whole table in memory.

On Kubernetes:

- **Threads:** set `POLARS_MAX_THREADS` to the pod's CPU limit *before* Polars is imported. `runtime_check()` warns when they differ.
- **Workers and concurrency:** run one uvicorn worker per pod and keep `EngineConfig.max_concurrent` at 1–2, because Polars already uses every thread. Extra requests queue and get a 503 after `queue_timeout_s`.
- **Scaling:** scale out with the HPA. What-if scenarios in Redis make replicas interchangeable.
- **Startup:** load datasets at startup, and gate the readiness probe on the load finishing.
- **Scale beyond pod memory:** register Parquet or IPC files with `register_scan`. Those scans use Polars' streaming engine automatically and push filters and column selection into the file reads. `storage_options` passes cloud credentials through.
- **Timeouts:** `timeout_s` (per request, or `EngineConfig.default_timeout_s`) cancels long queries with a 504.
- **Limits:** `Limits` caps page size, unpaged rows, group count, pivot columns and expression size (413); plugins have their own (`WhatIfLimits`).

## Not supported yet

- median, quantiles, standard deviation as built-in measures (plugins can add them)
- `//` and `%`
- comparing more than two sides at once
- pivots in compare
- spreading an edit on a group row down to its leaf rows
- AG Grid's advanced filter model
- sorting rollups by a measure
