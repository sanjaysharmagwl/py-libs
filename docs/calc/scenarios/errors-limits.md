---
covers:
  - packages/calc/src/pylibs_calc/errors.py
  - packages/calc/src/pylibs_calc/config.py
---

# Errors and limits

!!! question "The business question"
    *"When a request is wrong, what does the caller get back, and how do I fix it?"*

Every refusal is a `CalcError` with:

- a stable **`code`** that clients can branch on
- a **`path`**: a JSON pointer to the part of the request at fault
- a human-readable **`message`**
- the HTTP **`status`** that the [FastAPI integration](../integrations/fastapi.md) answers with

## Try it

```python
--8<-- "17_errors_limits.py"
```

## Result

```python exec="on"
--8<-- "17_errors_limits.py"
```

## What to notice

- **`path` points at the exact field.** `/query/measures/0/of` is the `of` of the first measure, so a UI can highlight it.
- **Type mistakes are caught before anything runs**, with a message that says how to fix them.
- **Over HTTP**, the body is `{"detail": {"code": ..., "message": ..., "path": ...}}`.

The full list is in [Error codes](../reference/error-codes.md).

## Limits

`Limits` keeps a single request from exhausting a pod. Exceeding a limit is a `413 limit_exceeded`. The defaults:

| Limit | Default |
| --- | --- |
| `max_page_size` | 50,000 rows |
| `max_unpaged_rows` | 100,000 rows |
| `max_groups` | 2,000,000 |
| `max_pivot_columns` | 2,000 |
| `max_measures` | 200 |
| `max_group_by` | 32 columns |
| `max_expr_depth` / `max_expr_nodes` | 64 / 5,000 |

Pass your own with `CalcEngine(catalog, EngineConfig(limits=Limits(...)))`. Plugins have their own limits; the what-if plugin's are in `WhatIfLimits` (`max_steps` 500 per request, `max_scenario_steps` 10,000, `max_edits` 200,000), passed as `WhatIfPlugin(limits=WhatIfLimits(...))`.

## Time and load

| Setting | Effect |
| --- | --- |
| `EngineConfig.default_timeout_s` (60) or `options.timeout_s` | Cancels a long query: `504 timeout` |
| `EngineConfig.max_concurrent` (2) | Queries running at once. Others wait in a queue |
| `EngineConfig.queue_timeout_s` (10) | How long a query may wait for a slot: `503 engine_busy` |
