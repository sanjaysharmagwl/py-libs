---
covers:
  - packages/calc_whatif/src/pylibs_calc_whatif/spec.py
  - packages/calc_whatif/src/pylibs_calc_whatif/scenario/manager.py
---

# Disable a step

!!! question "The business question"
    *"The −10% credit shock in our stress scenario is too harsh. Take it out, but keep a record
    that it was there."*

!!! info "What-if plugin"
    This feature comes from the [what-if plugin](../whatif/index.md) (`pylibs-calc-whatif`). Its
    steps go in a request's `extensions.whatif` block.

Scenarios are **append-only**, so you never edit or delete a step. A **disable** step undoes an earlier step by its sequence number. The log keeps both, which gives you an audit trail of what was tried.

## Try it

```python
--8<-- "12_disable.py"
```

## Result

```python exec="on"
--8<-- "12_disable.py"
```

## What to notice

- The Rates prices are 3% lower (98.50 → 95.54), and the Credit prices are back to their base values, because step 1 is disabled.
- The log still shows all three steps, who made them, and in what order.
- The same thing over HTTP is a `POST /calc/scenarios/{id}/steps` with body `{"steps": [{"kind": "disable", "seq": 1}], "expected_version": 2}`.

## Gotchas

- `seq` is **1-based**: the first step of a scenario is `seq` 1.
- A disable step can't itself be disabled (`422`). To bring a disabled change back, append the step again.
