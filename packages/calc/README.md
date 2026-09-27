# pylibs-calc

An embeddable **what-if calculation engine** on [Polars](https://pola.rs), for the grids that
finance teams slice, edit and aggregate. It is a library, not a service. You embed it in your own
FastAPI (or any Python) service, and it gives you:

- **Row changes:** filters, derived columns, overrides of individual cells, and bulk shocks ("price +5% where sector is Tech").
- **Aggregation:** group-by with measures (including filtered measures and weighted averages), ratios computed after aggregation, subtotals (rollup) and pivots.
- **Scenarios:** saved, versioned, forkable what-if scenarios, compared against the base data or each other.
- **Exact decimals:** exact `Decimal` arithmetic with explicit rounding rules.
- **Reproducible results:** a fingerprint on every result, and a pure-Python reference evaluator to check the engine against.
- **Integrations:** an adapter for the AG Grid server-side row model, a FastAPI router, and a Redis scenario store.

```bash
pip install pylibs-calc              # engine only (polars + pydantic)
pip install "pylibs-calc[fastapi]"   # + FastAPI router
pip install "pylibs-calc[redis]"     # + Redis scenario store
```

## Quick start

```python
import polars as pl
from pylibs_calc import Catalog, CalcEngine, InMemoryScenarioStore

catalog = Catalog()
catalog.register_frame("positions", df, key_columns=["position_id"], version="2026-09-26")
engine = CalcEngine(catalog, InMemoryScenarioStore())

result = engine.run(
    {
        "dataset": "positions",
        "what_if": [
            {
                "kind": "shock",
                "column": "price",
                "op": "pct",
                "value": 5,
                "where": "sector == 'Tech'",
            }
        ],
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

A request is plain JSON (or the equivalent pydantic models: `CalcRequest`, `Query`, `Shock`, ...).
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

**Scenarios** are saved, append-only logs of steps. Every step keeps all the rows:

| Step | What it does |
| --- | --- |
| `override` | Sets cells by key (`{"key": {"position_id": 7}, "column": "price", "value": "101.5"}`). |
| `shock` | `add`, `mul` or `pct` on a numeric column, optionally `where` a condition holds. |
| `formula` | A derived column. It is recomputed after all value changes, so a later override of `price` still flows into `notional = price * quantity`. |
| `disable` | Undoes an earlier step by its sequence number. |

A scenario is pinned to the dataset version it was created on. Scenarios store changes, not copies of the data, and a scenario only rewrites the columns it changes. You can also send one-off `what_if` steps with any request, on top of a saved scenario or without one.

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

1. The dataset version, after the caller's row filter.
2. The scenario's value changes, in log order.
3. The scenario's formulas.
4. The one-off `what_if` steps.
5. The query.

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
- **Functions:** `abs round floor ceil sqrt log exp min max coalesce lower upper contains starts_with ends_with`.
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

**Shocks:**
- On decimal columns, the result is rounded to the column's scale.
- On integer columns, a non-integral factor needs `"round": true`.

**Float sums** can differ in the last bits between runs, because Polars adds values in parallel.
Pass `"options": {"deterministic": true}` to sum in sorted order; it's slower but reproducible.
Decimal results are always exact.

## Scenarios, versions and concurrency

```python
s = engine.scenarios.create("positions", "tech rally", ctx=CalcContext(principal="ana"))
s = engine.scenarios.append(s.id, [shock_step], expected_version=0, client_op_id="uuid-1")
engine.run({"dataset": "positions", "scenario": s.id})  # latest version
engine.run({"dataset": "positions", "scenario": {"id": s.id, "version": 0}})  # any version
fork = engine.scenarios.fork(s.id, name="what if we hedge")  # copy, then diverge
engine.scenarios.verify(s.id)  # hash chain intact?
```

**Versions:**
- `version` is the log length, so `(id, version)` always names the same content.
- An append with a stale `expected_version` fails with 409 `version_conflict`.
- Retrying with the same `client_op_id` is a no-op, so retries are safe.
- Steps are validated against the dataset before they are stored.

**Audit trail:**
- Each log entry is hashed together with the previous one, so any edit to the stored log is detectable.
- Deleting a scenario only hides it, so the audit trail stays intact.

**Stores:**
- `InMemoryScenarioStore` is for tests and single-replica services.
- `RedisScenarioStore` (install the `redis` extra) is shared by all replicas. Its appends are a single atomic Lua script, and its keys use a `{id}` hash tag, so they work on Redis Cluster.

**Compare** runs one query on two sides, for example the base data and a scenario, or two scenarios. It joins the results:

```python
engine.compare(
    {
        "dataset": "positions",
        "scenario": s.id,
        "query": {
            "group_by": ["desk"],
            "measures": [{"name": "mv", "fn": "sum", "of": "price * quantity"}],
            "sort": [{"by": "mv__delta", "desc": True}],
        },
    }
)
```

- Each measure `m` comes back as `m` (the scenario), `m__base`, `m__delta` and `m__pct`.
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
| `POST /aggrid/rows`, `/aggrid/edit` | AG Grid SSRM `getRows`, and cell edits saved as scenario overrides |
| `POST /distinct` | Distinct values of a column (for set filters) |
| `GET /datasets`, `/datasets/{id}/schema` | Columns with type, role (key, dimension or measure) and whether they can be edited |
| `GET/POST /scenarios`, `GET/DELETE /scenarios/{id}` | Create, list, read and delete scenarios |
| `POST /scenarios/{id}/steps`, `/fork` | Append steps (`Idempotency-Key` header supported) and fork |
| `GET /scenarios/{id}/log`, `/verify` | Read the log and check its hash chain |

Routes are plain `def` functions, so FastAPI runs them in its thread pool and Polars never blocks
the event loop. Errors come back as `{"detail": {"code", "message", "path"}}` with the error's HTTP
status:

| Status | Codes |
| --- | --- |
| 422 | `invalid_request`, `formula_syntax`, `unknown_column`, `type_mismatch`, `unmatched_edits`, ... |
| 404 | `dataset_not_found`, `scenario_not_found` |
| 409 | `version_conflict` |
| 413 | `limit_exceeded` |
| 503 | `engine_busy` |
| 504 | `timeout` |

`CalcContext` is how the host enforces access:

- `row_filter` is applied before anything else.
- `allowed_columns` hides every other non-key column.
- `EngineConfig.authorize(ctx, action, scenario)` can refuse scenario actions.
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
      body: JSON.stringify({dataset: 'positions', scenario, request: p.request})})
    .then(r => r.json()).then(d => p.success(d)).catch(() => p.fail()) },
  getRowId: p => p.data.__row_id,
  getServerSideGroupKey: d => d.__group_key,   // typed keys: nulls, dates and decimals round-trip
  serverSidePivotResultFieldSeparator: '_',
  readOnlyEdit: true,                           // edits go to the server as scenario overrides
  onCellEditRequest: e => { /* POST /calc/aggrid/edit, then api.refreshServerSide() */ },
};
```

The server-side row model is an AG Grid **Enterprise** feature. [examples/](examples/) has a
runnable demo with grouping, pivoting, editing and a compare table:

```bash
uv run --with uvicorn uvicorn --app-dir packages/calc/examples app:app --port 8000
```

## Verifiability

**Fingerprints.** Every result's metadata carries:
- a SHA-256 `fingerprint` of the canonical, fully resolved request (dataset version, effective scenario steps, query, numeric settings and caller context)
- the dataset and scenario versions, and the scenario's hash-chain head
- the library versions
- timings, and with `"options": {"audit": true}` the row counts at each stage

The same fingerprint on the same library versions means the same answer, and results are cached under it.

**Explain.** `engine.explain(request)` shows:
- the effective steps
- lineage: which steps changed each column, and the formula behind every derived column
- the output types
- the optimized Polars plan

**The reference evaluator.** `pylibs_calc.verify.reference` evaluates the same logical plans
row by row, with exact `Decimal` arithmetic and no Polars. `verify(engine, request)` runs the
engine and the reference on the same rows and reports every difference. On datasets larger than
`max_rows` it uses a random sample. Use it in a canary job or before upgrading Polars.

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
| scenario (100 overrides, a shock, a formula), then group-by | 989 / 1133 | 838 / 1001 |
| 3-level rollup of an exact-decimal product | 1247 / 1614 | 920 / 1053 |
| next page of a cached aggregate (grid scrolling) | 0.6 / 0.7 | 0.5 / 0.6 |

Guidance:

- **Store dimensions as Categorical.** Grouping is about twice as fast, and the catalog keeps categoricals.
- **Use Decimal columns only where exactness matters.** Decimal sums and products cost 2–7× their float equivalents.
- **Paging is cheap after the first request.** Aggregates are cached by content hash, and later pages are sliced from the cache. Row views push sorting and slicing into Polars, so a page of a large table never builds the whole table in memory.

On Kubernetes:

- **Threads:** set `POLARS_MAX_THREADS` to the pod's CPU limit *before* Polars is imported. `runtime_check()` warns when they differ.
- **Workers and concurrency:** run one uvicorn worker per pod and keep `EngineConfig.max_concurrent` at 1–2, because Polars already uses every thread. Extra requests queue and get a 503 after `queue_timeout_s`.
- **Scaling:** scale out with the HPA. Scenarios in Redis make replicas interchangeable.
- **Startup:** load datasets at startup, and gate the readiness probe on the load finishing.
- **Scale beyond pod memory:** register Parquet or IPC files with `register_scan`. Those scans use Polars' streaming engine automatically and push filters and column selection into the file reads. `storage_options` passes cloud credentials through.
- **Timeouts:** `timeout_s` (per request, or `EngineConfig.default_timeout_s`) cancels long queries with a 504.
- **Limits:** `Limits` caps page size, unpaged rows, group count, pivot columns, expression size and edits (413).

## Not supported yet

- median, quantiles, standard deviation
- `//` and `%`
- comparing more than two sides at once
- pivots in compare
- spreading an edit on a group row down to its leaf rows
- moving a scenario onto a newer dataset version
- AG Grid's advanced filter model
- sorting rollups by a measure
