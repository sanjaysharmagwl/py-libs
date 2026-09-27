---
covers:
  - packages/calc/src/pylibs_calc/spec/scenario.py
  - packages/calc/src/pylibs_calc/compile/logical.py
---

# Formula columns

!!! question "The business question"
    *"My scenario defines notional as price × quantity. If someone later corrects a price, does
    notional follow?"*

A **formula step** defines a column that belongs to the scenario, so every query on that scenario sees it. Unlike a query's `derive`, it is **recomputed after all value changes**, whatever their order in the log.

## Try it

=== "Python"

    ```python
    --8<-- "11_formula.py"
    ```

=== "JSON (curl)"

    ```python exec="on"
    from book import curl

    print(curl("11_formula.py"))
    ```

## Result

```python exec="on"
--8<-- "11_formula.py"
```

## What to notice

- The formula comes **before** the override in the list, yet Stark Industries' notional is 300.00 × 400 = **120,000.00**, using the new price.
- Value changes (overrides and shocks) are applied in log order first. Then the formulas are evaluated, in dependency order, so a formula can use another formula.
- A later formula step with the same `name` **redefines** the column.

## `derive` or `formula`?

| | Query `derive` | Scenario `formula` |
| --- | --- | --- |
| Lives in | One request's query | A scenario (or a request's `what_if`) |
| Seen by | That query | Every query on the scenario, and compares |
| Can be edited or shocked | No | No: it is always computed |
| Typical use | A one-off view column | A business definition you want everyone to share |

## Gotchas

- A formula column can't be the target of an override or a shock (`422 unknown_column`), because it is always computed. Change its inputs instead.
- Formulas can't form a cycle, where `a` uses `b` and `b` uses `a`. That is a `422 formula_cycle`.
