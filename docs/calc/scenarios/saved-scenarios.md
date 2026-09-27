---
covers:
  - packages/calc/src/pylibs_calc/scenario/manager.py
  - packages/calc/src/pylibs_calc/scenario/model.py
  - packages/calc/src/pylibs_calc/scenario/store.py
---

# Saved scenarios and forks

!!! question "The business question"
    *"Save a 'Tech rally' scenario that my team can reopen. Then branch it to try a hedge,
    without touching the original."*

A **saved scenario** is a named, append-only log of steps ([overrides](override.md), [shocks](shock.md), [formulas](formula.md) and [disables](disable.md)), pinned to one version of a dataset. It stores the changes, not a copy of the data.

## Try it

```python
--8<-- "13_saved_scenarios.py"
```

## Result

```python exec="on"
--8<-- "13_saved_scenarios.py"
```

## What to notice

- **`version` is the length of the log.** `(scenario id, version)` always names exactly the same content, so you can re-run a report "as of version 3" at any time.
- **Optimistic locking.** An append must say which version it expects (`expected_version`). If someone else appended in the meantime, you get `409 version_conflict`: reload and retry. Nobody's work is overwritten silently.
- **Safe retries.** A retry with the same `client_op_id` (the `Idempotency-Key` header over HTTP) returns the stored result instead of appending twice.
- **Forks are independent.** The hedged fork copies the effective steps and then diverges; the original is unchanged.
- **Tamper-evident.** Each log entry is hashed together with the previous one. `verify()` recomputes the chain, and any edit to the stored log shows up.

`engine.scenarios` is the `ScenarioManager`: `create`, `append`, `fork`, `get`, `log`, `list`, `delete` and `verify`. `log()` returns `LogEntry` records (sequence number, step, author, time, note and hash).

## Over HTTP

```bash
# create
curl -s localhost:8000/calc/scenarios -H 'Content-Type: application/json' \
  -d '{"dataset": "positions", "name": "tech rally"}'
# append (use the id from the response)
curl -s localhost:8000/calc/scenarios/$ID/steps -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: op-1' \
  -d '{"expected_version": 0, "steps": [{"kind": "shock", "column": "price", "op": "pct", "value": 8, "where": "sector == '\''Tech'\''"}]}'
# query it
curl -s localhost:8000/calc/query -H 'Content-Type: application/json' \
  -d '{"dataset": "positions", "scenario": "'$ID'", "query": {"group_by": ["sector"], "measures": [{"name": "mv", "fn": "sum", "of": "price * quantity"}]}}'
# fork, read the log, check the hash chain
curl -s localhost:8000/calc/scenarios/$ID/fork -H 'Content-Type: application/json' -d '{"name": "hedged"}'
curl -s localhost:8000/calc/scenarios/$ID/log
curl -s localhost:8000/calc/scenarios/$ID/verify
```

## Gotchas

- **Pinned to a dataset version.** A scenario keeps working after a data refresh for as long as the catalog keeps the old version (`Catalog(max_versions=2)` keeps two). Moving a scenario onto a newer dataset version is not supported yet.
- **Validated on every append.** Every step is checked against the dataset before it is stored, together with the whole log, so a bad step is refused rather than breaking later queries.
- **Deleting only hides a scenario**, so the audit trail stays.
- `InMemoryScenarioStore` loses everything on restart. In production, use the [Redis store](../integrations/redis.md).
