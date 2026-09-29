---
covers:
  - packages/calc/src/pylibs_calc/exec.py
  - packages/calc/src/pylibs_calc/engine.py
---

# Deploying on Kubernetes

## Checklist

- [ ] **Threads.** Set `POLARS_MAX_THREADS` to the pod's CPU limit **before** Polars is imported (in the container environment, not in code). `runtime_check()` warns at startup when they differ.
- [ ] **One worker per pod.** Run one uvicorn worker per pod, because Polars already uses every thread.
- [ ] **Concurrency.** Keep `EngineConfig.max_concurrent` at 1–2. Extra requests queue, and get `503 engine_busy` after `queue_timeout_s`.
- [ ] **Scale out, not up.** Use the HPA. With scenarios in [Redis](../integrations/redis.md), every replica can serve every request.
- [ ] **Readiness.** Load datasets at startup, and gate the readiness probe on the load finishing.
- [ ] **Timeouts.** Set `EngineConfig.default_timeout_s` (60 s by default) below your ingress timeout, so the engine answers `504` itself.
- [ ] **Limits.** Tune `Limits` to the pod's memory. See [Errors and limits](../scenarios/errors-limits.md).
- [ ] **Memory.** Budget for the datasets, plus `cache_bytes`, plus the working memory of the largest query.
- [ ] **Data larger than memory.** Register Parquet or IPC files with `register_scan`, and pass cloud credentials with `storage_options`.
- [ ] **Audit.** Wire `EngineConfig.on_result` to your audit log, to record who computed which fingerprint.

## Example

```yaml
containers:
  - name: calc
    image: registry.example.com/portfolio-calc:1.4.0
    command: ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
    env:
      - {name: POLARS_MAX_THREADS, value: "4"}
      - {name: REDIS_URL, value: "redis://calc-redis:6379/0"}
    resources:
      requests: {cpu: "4", memory: 8Gi}
      limits: {cpu: "4", memory: 8Gi}
    readinessProbe:
      httpGet: {path: /ready, port: 8000}
```

```python
engine = CalcEngine(
    catalog,
    EngineConfig(max_concurrent=2, queue_timeout_s=10, default_timeout_s=30),
    plugins=[WhatIfPlugin(store=RedisScenarioStore(redis.Redis.from_url(os.environ["REDIS_URL"])))],
)
```
