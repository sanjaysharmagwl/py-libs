---
covers:
  - packages/calc_whatif/src/pylibs_calc_whatif/scenario/redis_store.py
  - packages/calc_whatif/src/pylibs_calc_whatif/scenario/store.py
---

# Redis scenario store

The [what-if plugin](../whatif/index.md)'s `InMemoryScenarioStore` keeps scenarios in one process, so they are lost on restart and not shared between replicas. `RedisScenarioStore` shares them across every replica of a service.

```bash
pip install "pylibs-calc-whatif[redis]"
```

```python
import redis
from pylibs_calc import CalcEngine
from pylibs_calc_whatif import WhatIfPlugin
from pylibs_calc_whatif.scenario.redis_store import RedisScenarioStore

store = RedisScenarioStore(redis.Redis.from_url("redis://redis:6379/0"), prefix="calc:scn")
engine = CalcEngine(catalog, plugins=[WhatIfPlugin(store=store)])
```

## How it works

- **One cluster slot per scenario.** Each scenario uses three keys (metadata, log and seen operation ids) that share a `{id}` hash tag, so on Redis Cluster they live in the same slot.
- **Atomic appends.** An append is a **single Lua script**: it checks `expected_version`, checks `client_op_id` for retries, pushes the entries and moves the head. Two replicas can't both append at the same version; one of them gets `409 version_conflict`.
- **Audit trail.** The hash chain is stored with the log, so `verify()` works on any replica.

## Durability

How durable the audit trail is depends on Redis persistence: AOF and replication. For audit-grade retention, implement the `ScenarioStore` protocol on a database. It has six methods: `create`, `append`, `get`, `entries`, `list` and `delete`. `InMemoryScenarioStore` in `pylibs_calc_whatif/scenario/store.py` is a short reference implementation.

## Testing

The test suite runs the Redis store against `fakeredis` with Lua support, so you don't need a Redis server to run `make test`.
