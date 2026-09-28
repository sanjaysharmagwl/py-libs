# pylibs-calc-whatif

What-if analysis for [`pylibs-calc`](../calc), as a plugin. It adds:

- **Steps** that change values but keep every row: overrides of individual cells, bulk shocks
  ("price +5% where sector is Tech") and formula columns that follow later changes.
- **Saved scenarios:** append-only, hash-chained logs of steps over a pinned dataset version,
  with optimistic locking, idempotent retries, forks and disables, in memory or in Redis.
- **Routes** for the core FastAPI router (`/scenarios/...`), and AG Grid cell edits saved as
  overrides (`/aggrid/edit`).

```bash
pip install pylibs-calc-whatif              # the plugin
pip install "pylibs-calc-whatif[redis]"     # + RedisScenarioStore
pip install "pylibs-calc-whatif[fastapi]"   # + the core FastAPI router
```

## Quick start

```python
from pylibs_calc import Catalog, CalcEngine
from pylibs_calc_whatif import InMemoryScenarioStore, WhatIfPlugin

engine = CalcEngine(catalog, plugins=[WhatIfPlugin(store=InMemoryScenarioStore())])

result = engine.run(
    {
        "dataset": "positions",
        "extensions": {
            "whatif": {
                "steps": [
                    {
                        "kind": "shock",
                        "column": "price",
                        "op": "pct",
                        "value": 5,
                        "where": "sector == 'Tech'",
                    },
                    {"kind": "formula", "name": "notional", "expr": "price * quantity"},
                ]
            }
        },
        "query": {
            "group_by": ["desk"],
            "measures": [{"name": "notional", "fn": "sum", "of": "notional"}],
        },
    }
)
result.meta.extensions["whatif"]  # {"scenario": None, "scenario_head": None, "unmatched_edits": []}
```

The `extensions.whatif` block takes a saved `scenario` (an id, or `{"id", "version"}`), extra
`steps` for this request only, and `strict_edits` (default `true`: an override whose key matches
no row is an error). Requests in the `pylibs-calc` 0.1 shape (`"scenario"`, `"what_if"` at the top
level) are upgraded automatically, with the same results and fingerprints.

## Steps

| Step | What it does |
| --- | --- |
| `override` | Sets cells by key (`{"key": {"position_id": 7}, "column": "price", "value": "101.5"}`). |
| `shock` | `add`, `mul` or `pct` on a numeric column, optionally `where` a condition holds. |
| `formula` | A derived column. It is recomputed after all value changes, so a later override of `price` still flows into `notional = price * quantity`. |
| `disable` | Undoes an earlier step by its sequence number. |

- Value changes apply in order: the saved scenario's, then the request's own. Formulas are
  evaluated afterwards, in dependency order.
- On decimal columns, shocked values are rounded half-to-even to the column's scale. On integer
  columns, a non-integral factor needs `"round": true`.
- Only editable, non-key columns can be changed.
- Steps can use columns and functions of plugins installed before this one.

## Saved scenarios

```python
scenarios = engine.plugin(WhatIfPlugin).scenarios
s = scenarios.create("positions", "tech rally", ctx=CalcContext(principal="ana"))
s = scenarios.append(s.id, [shock_step], expected_version=0, client_op_id="uuid-1")
engine.run({"dataset": "positions", "extensions": {"whatif": {"scenario": s.id}}})
engine.run({"dataset": "positions", "extensions": {"whatif": {"scenario": {"id": s.id, "version": 0}}}})
fork = scenarios.fork(s.id, name="what if we hedge")  # copy, then diverge
scenarios.verify(s.id)  # hash chain intact?
```

- `version` is the log length, so `(id, version)` always names the same content.
- An append with a stale `expected_version` fails with 409 `version_conflict`; retrying with the
  same `client_op_id` (`Idempotency-Key` over HTTP) is a no-op.
- Every append validates the whole resulting log against the dataset first.
- Each log entry is hashed together with the previous one, so any edit to the stored log is
  detectable. Deleting only hides a scenario.
- A scenario is pinned to the dataset version it was created on.
- `InMemoryScenarioStore` is for tests and single-replica services. `RedisScenarioStore` is
  shared by all replicas: appends are one atomic Lua script, and keys share a `{id}` hash tag, so
  it works on Redis Cluster.
- `EngineConfig.authorize(ctx, action, scenario)` is called for `scenario.read`,
  `scenario.write`, `scenario.create` and `scenario.delete`.

## Limits

`WhatIfPlugin(limits=WhatIfLimits(max_steps=500, max_scenario_steps=10_000, max_edits=200_000))`.
Exceeding one is a 413.

## Demo

[examples/](examples/) is a FastAPI service with an AG Grid page: grouping, pivoting, cell edits
saved to a scenario, shocks and a compare table.

```bash
uv run --with uvicorn uvicorn --app-dir packages/calc_whatif/examples app:app --port 8000
```

The plugin is advertised under the `pylibs_calc.plugins` entry point, so
`pylibs_calc.discover_plugins()` finds it (without a scenario store). See the pylibs-calc
documentation for the full guide.
