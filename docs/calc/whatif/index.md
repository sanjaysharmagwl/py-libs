---
covers:
  - packages/calc_whatif/src/pylibs_calc_whatif/plugin.py
  - packages/calc_whatif/src/pylibs_calc_whatif/spec.py
  - packages/calc_whatif/src/pylibs_calc_whatif/planner.py
---

# What-if plugin

`pylibs-calc-whatif` adds **what-if analysis** to the core engine, as a [plugin](../concepts/plugins.md):

- [override](../scenarios/override.md) cells, [shock](../scenarios/shock.md) columns and add [formula columns](../scenarios/formula.md) that follow later changes;
- save those changes as [scenarios](../scenarios/saved-scenarios.md): append-only, hash-chained logs with optimistic locking, forks and [disables](../scenarios/disable.md), in memory or in [Redis](../integrations/redis.md);
- scenario routes for the [FastAPI router](../integrations/fastapi.md#routes-added-by-plugins), and [AG Grid](../integrations/aggrid.md) cell edits saved as overrides.

```bash
pip install pylibs-calc-whatif            # add [redis] for the Redis scenario store
```

```python
from pylibs_calc import CalcEngine
from pylibs_calc_whatif import InMemoryScenarioStore, WhatIfPlugin

engine = CalcEngine(catalog, plugins=[WhatIfPlugin(store=InMemoryScenarioStore())])
```

Without a `store`, ad-hoc steps work and saved scenarios answer `no_scenario_store`.

## The request block

What-if changes go in the request's `extensions.whatif` block:

| Field | Default | Meaning |
| --- | --- | --- |
| `scenario` | none | A saved scenario: its id, or `{"id": ..., "version": n}` to read it as of version `n` |
| `steps` | `[]` | Extra steps for this request only, applied after the scenario's |
| `strict_edits` | `true` | Refuse overrides whose key matches no row (`422 unmatched_edits`) |

```python exec="on" source="tabbed-left" tabs="Request|Result"
from book import engine, table

result = engine().run({
    "dataset": "holdings",
    "extensions": {
        "whatif": {
            "steps": [
                {"kind": "shock", "column": "price", "op": "pct", "value": -2, "where": "sector == 'Government'"},
                {"kind": "formula", "name": "mv", "expr": "round(price * quantity * fx_rate, 2)"},
            ]
        }
    },
    "query": {"filter": "sector == 'Government'", "select": ["security_id", "security", "price", "mv"]},
})
print(table(result))
print(f"\n`meta.extensions`: `{result.meta.extensions}`")
```

- `meta.extensions.whatif` reports the scenario and its head hash, and any `unmatched_edits` (with `strict_edits: false`).
- `engine.explain(...)["extensions"]["whatif"]` shows which steps changed each column (`changed_by`) and every formula.
- The steps are part of the result's fingerprint, so a what-if result is cached and reproducible like any other.
- [Compare](../scenarios/compare.md) takes a `whatif` block on each side.

## In the engine

The plugin registers one **transform**, `whatif`. For each request it

1. loads the saved scenario's log at the requested version (checking `scenario.read` with your [`authorize` hook](../scenarios/access-control.md#scenario-permissions-what-if-plugin)) and pins the dataset to the scenario's version;
2. drops disabled steps, then validates and types every step against the columns the caller may see, including columns and functions from plugins installed before it;
3. applies the value changes in order, then the formulas, in Polars (`polars.py`) and, for `verify()`, in plain Python (`reference.py`).

`plugin.scenarios` is the `ScenarioManager` for saved scenarios; every append is validated by planning the whole resulting log.

## Python API at a glance

| Name | What it is |
| --- | --- |
| `WhatIfPlugin` | The plugin: `WhatIfPlugin(store=None, limits=WhatIfLimits())`; `.scenarios` is the `ScenarioManager` |
| `WhatIf` | The `extensions.whatif` block; `ScenarioRef` names a saved scenario |
| `Override` (with `Edit`s), `Shock`, `Formula`, `Disable` | The steps; `ScenarioStep` is their union, discriminated by `kind` |
| `WhatIfPlan` | The planned transform of one request; its `mutations` is the validated `LogicalMutations` |
| `Scenario`, `LogEntry`, `ScenarioStore`, `InMemoryScenarioStore` | Saved scenarios and where they are kept; `verify_chain(scenario, entries)` checks a log's hashes |
| `CellEdit`, `edit_to_override` | An AG Grid cell edit, and the override step it becomes |
| `ScenarioNotFound` | `404 scenario_not_found` |

## Limits

| `WhatIfLimits` | Default | Caps |
| --- | --- | --- |
| `max_steps` | 500 | Steps in one request's block |
| `max_scenario_steps` | 10,000 | Steps in a saved scenario's log |
| `max_edits` | 200,000 | Overridden cells in one request (scenario plus extra steps) |

```python
WhatIfPlugin(store=store, limits=WhatIfLimits(max_edits=50_000))
```

Expression size is capped by the engine's own `Limits` (`max_expr_depth`, `max_expr_nodes`).

## Coming from version 0.1

In `pylibs-calc` 0.1, what-if was built into the engine. Old requests still work: a request with top-level `scenario`, `what_if` or `options.strict_edits` is [upgraded](../reference/request-schema.md#versions) to the `extensions.whatif` block, with the same results and fingerprints. In Python:

| 0.1 | Now |
| --- | --- |
| `CalcEngine(catalog, store)` | `CalcEngine(catalog, plugins=[WhatIfPlugin(store)])` |
| `engine.scenarios` | `engine.plugin(WhatIfPlugin).scenarios` |
| `from pylibs_calc import Shock, InMemoryScenarioStore, ...` | `from pylibs_calc_whatif import Shock, InMemoryScenarioStore, ...` |
| `pylibs_calc.scenario.redis_store` | `pylibs_calc_whatif.scenario.redis_store` |
| `Limits(max_what_if_steps=..., max_edits=...)` | `WhatIfLimits(max_steps=..., max_edits=...)` |
| `meta.scenario`, `meta.scenario_head`, `meta.unmatched_edits` | `meta.extensions["whatif"]["scenario" / "scenario_head" / "unmatched_edits"]` |
| `explain(...)["lineage"]["changed_by" / "formulas"]` | `explain(...)["extensions"]["whatif"]["changed_by" / "formulas"]` |
| `AgGridAdapter().edit_to_override(edit, schema)` | `pylibs_calc_whatif.edit_to_override(edit, schema)` |
