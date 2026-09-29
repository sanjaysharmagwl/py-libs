---
covers:
  - packages/calc/src/pylibs_calc/config.py
  - packages/calc/src/pylibs_calc/schema.py
---

# Access control

!!! question "The business question"
    *"A credit analyst should see only the bonds they cover. Client reporting must never see
    our analysts' target prices, whatever query they send."*

The host service describes **who is asking** with a `CalcContext`, built from its own authentication for every request. The engine enforces it, so no query can get around it.

## Try it

```python
--8<-- "15_access_control.py"
```

## Result

```python exec="on"
--8<-- "15_access_control.py"
```

## What to notice

- **`row_filter`** is applied to the dataset **before anything else**: before plugin transforms (such as what-if scenarios and shocks), filters and aggregation. Totals only ever include rows the caller may see.
- **`raj` sees two rows**: the two corporate bonds they cover. Their weights, totals and scenarios can only ever include those rows.
- **`allowed_columns`** hides every other non-key column, from queries, schemas and results. For client reporting, `target_price` and `analyst` are gone; a query that mentions `target_price` gets `422 unknown_column`, as if the column did not exist.
- **Key columns** (`security_id`) are always visible, because edits and row identity need them.
- **`principal`** identifies the caller to your `authorize` hook and to plugins; the what-if plugin records it as the author of scenario changes.
- The context is part of the **cache key**, so two users with different entitlements never share a cached result.

## Wiring it into FastAPI

```python
create_router(
    engine,
    context_resolver=lambda req: CalcContext(
        principal=req.state.user,
        row_filter=f"analyst in {tuple(req.state.coverage)!r}",
        allowed_columns=frozenset(req.state.columns),
    ),
)
```

## Scenario permissions (what-if plugin)

`EngineConfig.authorize(ctx, action, resource)` is called by plugins before protected actions. The what-if plugin calls it for `scenario.read`, `scenario.write`, `scenario.create` and `scenario.delete`, with the scenario as the resource. Raise `Forbidden` to refuse (`403`). For example, you might let only a scenario's owner append to it:

```python
from pylibs_calc import CalcEngine, EngineConfig, Forbidden
from pylibs_calc_whatif import WhatIfPlugin


def authorize(ctx, action, scenario):
    if action == "scenario.write" and scenario is not None and scenario.owner != ctx.principal:
        raise Forbidden("only the owner can change this scenario")


engine = CalcEngine(catalog, EngineConfig(authorize=authorize), plugins=[WhatIfPlugin(store)])
```
