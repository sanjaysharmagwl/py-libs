---
covers:
  - packages/calc/src/pylibs_calc/plugins.py
  - packages/calc/src/pylibs_calc/testing.py
---

# Write a plugin

!!! question "The business question"
    *"The fund reports in US dollars, but it also has a sterling share class for UK investors.
    We want the fund valued in the share class currency, a couple of analytics functions, and an
    FX sensitivity ladder, in the same engine and the same API as everything else."*

This page builds `ShareClassPlugin`, which uses every extension point. Read [Plugins](../concepts/plugins.md) first for the concepts. The whole plugin is one runnable file, [`docs/examples/calc/18_custom_plugin.py`](https://github.com/sanjaysharmagwl/py-libs/blob/master/docs/examples/calc/18_custom_plugin.py), and the docs build runs it.

## 1. Functions and aggregates

A function or an aggregate is a name, a type rule, a Polars implementation and a plain Python one:

```python
--8<-- "18_custom_plugin.py:function"
```

- `typecheck` receives the argument types (`LType`) and returns the result type. Raise `ValueError` to refuse: the caller gets a `422 type_mismatch` pointing at the call.
- The engine casts the result to the declared type and makes non-finite floats null, in both implementations, so you don't have to.
- `min_args` / `max_args` default to one argument; `nulls="pass"` hands nulls to your code instead of short-circuiting to null.

## 2. A transform

A transform changes the data before the query. Requests switch it on with a block under `extensions` named after it, here `{"extensions": {"share_class": {...}}}`. It adds `mv_sc`, each holding's market value in the share class currency, converted with a rate table keyed by the row's `currency` column:

```python
--8<-- "18_custom_plugin.py:transform"
```

- **`ShareClass`** is the block's pydantic model. `Model` (from `pylibs_calc.ext`) is frozen and rejects unknown fields, like every part of the request.
- **`bind`** is called per request. Resolve references here (a saved scenario, today's FX rates snapshot), cheaply.
- **`Bound.identity`** must capture everything `plan` depends on: the engine caches the plan under it.
- **`plan`** validates against the incoming column types and raises `SpecError`s with a `path` inside the block.
- **`TransformPlan`** declares the columns afterwards (`env`) and its identity (`canonical`, part of every fingerprint), and implements the change twice: `apply` for Polars and `apply_reference` in plain Python.

## 3. An operation

An operation is a new engine call. It gets the [`Kernel`](../concepts/plugins.md#operations), so it can resolve views and run queries with the engine's slots, deadlines and cache:

```python
--8<-- "18_custom_plugin.py:operation"
```

Take one `kernel.slot()` for the whole operation, and don't call `engine.run` inside it (that would wait for a second slot).

## 4. The plugin

The plugin registers everything, and can add HTTP routes:

```python
--8<-- "18_custom_plugin.py:plugin"
```

## 5. Use it

```python
--8<-- "18_custom_plugin.py:use"
```

```python exec="on"
--8<-- "18_custom_plugin.py"
```

The ladder shows the sterling value of the fund if sterling moves 10% either way against every other currency: a stronger pound (`+10`) makes the fund's dollar, euro and yen holdings worth fewer pounds.

Over HTTP, `create_router(engine)` serves the transform through `/query`, `/compare` and the rest, the ladder as `POST /operations/fx_ladder`, and the plugin's own `GET /share_class/functions`.

## Test it against the reference

`pylibs_calc.testing` (the `testing` extra) has the Hypothesis strategies the engine's own property tests use. Generate random datasets and queries, switch your transform on, and check that the Polars and Python implementations agree:

```python
from hypothesis import given, strategies as st

from pylibs_calc import CalcEngine, Catalog
from pylibs_calc.testing import assert_matches_reference, frames, queries


@given(data=st.data())
def test_my_plugin_matches_the_reference(data):
    catalog = Catalog()
    catalog.register_frame("t", data.draw(frames()), key_columns=["k"])
    engine = CalcEngine(catalog, plugins=[MyPlugin()])
    request = {"dataset": "t", "extensions": {"mine": {...}}, "query": data.draw(queries())}
    assert_matches_reference(engine, request)
```

When this repository's own tests did this for a small `clip()` function, Hypothesis found in seconds that its Python version disagreed with Polars when the lower bound was above the upper one. That is the kind of mismatch it is there to catch.

## Package it

Ship the plugin as its own distribution that depends on `pylibs-calc`, and advertise it so that `discover_plugins()` finds it:

```toml
[project]
name = "my-calc-plugin"
dependencies = ["pylibs-calc>=0.2,<0.3"]

[project.entry-points."pylibs_calc.plugins"]
share_class = "my_calc_plugin:ShareClassPlugin"
```

`pylibs-calc-whatif` ([source](https://github.com/sanjaysharmagwl/py-libs/tree/master/packages/calc_whatif)) is a complete example, with saved scenarios, a Redis store, routes and its own property tests.

## Checklist

- [ ] Every computation has a Polars and a reference implementation, and a property test compares them.
- [ ] `Bound.identity` covers everything the plan depends on, and `canonical` everything the result depends on.
- [ ] Errors are `CalcError`s with a stable `code` and a `path` into the request.
- [ ] Only `pylibs_calc`, `pylibs_calc.ext`, `pylibs_calc.integrations.fastapi` and `pylibs_calc.testing` are imported.
- [ ] `version` is bumped whenever results would change, so cached results are not reused.
