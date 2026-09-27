---
covers:
  - packages/calc/src/pylibs_calc/verify/__init__.py
  - packages/calc/src/pylibs_calc/verify/reference.py
  - packages/calc/src/pylibs_calc/spec/canonical.py
  - packages/calc/src/pylibs_calc/result.py
---

# Audit a number

!!! question "The business question"
    *"Model risk is asking how this desk total was produced, and whether we can reproduce it
    next quarter."*

Every result carries the information needed to **reproduce**, **explain** and **independently check** it.

## Try it

```python
--8<-- "16_audit.py"
```

## Result

```python exec="on"
--8<-- "16_audit.py"
```

## The three tools

**1. The fingerprint.** `meta.fingerprint` is a SHA-256 of the canonical, fully resolved request:

- the dataset version
- the effective scenario steps
- the query
- the numeric settings
- the caller's entitlements

`canonical_json(request)` shows exactly what is hashed. Formulas are stored as expression trees, so `price*quantity` and `price * quantity` give the same fingerprint. **The same fingerprint on the same library versions (`meta.versions`) means the same answer.** Results are cached under it. Log it next to any number you publish.

**2. Explain.** `engine.explain(request)` (or `POST /calc/explain`) returns:

- `steps`: the steps that actually apply, after disables
- `lineage.changed_by`: which steps changed each column
- `lineage.formulas` and `lineage.derived`: the formula behind every computed column
- `columns`: the output types
- `plan`: the optimized Polars plan

**3. The reference evaluator.** `verify(engine, request)` evaluates the same request a second way: row by row, in pure Python, with exact `Decimal` arithmetic and no Polars. It then reports every difference. Datasets larger than `max_rows` (20,000 by default) are checked on a random sample. Run it:

- in a canary job
- in CI
- before upgrading Polars

The test suite fuzzes thousands of random datasets and requests through it.

## Also useful

- **`"options": {"audit": true}`** adds `meta.stage_rows`, the number of rows after each stage.
- **`EngineConfig(on_result=...)`** receives every result's metadata and the caller's context, so you can write an audit log.
- **`engine.scenarios.verify(id)`** checks a saved scenario's hash chain.
