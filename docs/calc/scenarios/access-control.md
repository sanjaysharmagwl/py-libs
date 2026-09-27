---
covers:
  - packages/calc/src/pylibs_calc/config.py
  - packages/calc/src/pylibs_calc/schema.py
---

# Access control

!!! question "The business question"
    *"A Rates trader should see only Rates positions, and no yields, whatever query they send."*

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

- **`row_filter`** is applied to the dataset **before anything else**: before scenarios, shocks, filters and aggregation. Totals only ever include rows the caller may see.
- **`allowed_columns`** hides every other non-key column, from queries, schemas and results. A query that mentions `yield` gets `422 unknown_column`, as if the column did not exist.
- **Key columns** (`position_id`) are always visible, because edits and row identity need them.
- **`principal`** is recorded as the author of scenario changes.
- The context is part of the **cache key**, so two users with different entitlements never share a cached result.

## Wiring it into FastAPI

```python
create_router(
    engine,
    context_resolver=lambda req: CalcContext(
        principal=req.state.user,
        row_filter=f"desk in {tuple(req.state.desks)!r}",
        allowed_columns=frozenset(req.state.columns),
    ),
)
```

## Scenario permissions

`EngineConfig.authorize(ctx, action, scenario)` is called for `scenario.read`, `scenario.write`, `scenario.create` and `scenario.delete`. Raise `Forbidden` to refuse (`403`). For example, you might let only a scenario's owner append to it:

```python
from pylibs_calc import EngineConfig, Forbidden


def authorize(ctx, action, scenario):
    if action == "scenario.write" and scenario is not None and scenario.owner != ctx.principal:
        raise Forbidden("only the owner can change this scenario")


engine = CalcEngine(catalog, store, EngineConfig(authorize=authorize))
```
