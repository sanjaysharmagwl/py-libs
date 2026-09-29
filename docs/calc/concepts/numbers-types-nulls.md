---
covers:
  - packages/calc/src/pylibs_calc/dtypes.py
  - packages/calc/src/pylibs_calc/compile/validate.py
  - packages/calc/src/pylibs_calc/compile/exprs.py
---

# Numbers, types and nulls

Fund valuations, weights and client reports have to be right to the cent and reproducible. `pylibs-calc` makes every numeric rule explicit, and the validator, the Polars compiler and the reference evaluator all use the same rules.

## Exact decimals

A `Decimal` column (such as `price`, with 2 places) is computed **exactly**. The result has a defined scale, and it is rounded **half-to-even** (banker's rounding). Precision is always 38 digits.

| Operation | Result scale | Example with `price` (2) and `fx_rate` (6) |
| --- | --- | --- |
| `+`, `-` | `max(sa, sb)` | 2 and 6 → 6 |
| `*` | `sa + sb`, capped at `NumericConfig.max_scale` (18) | 2 and 6 → 8 |
| `/` | `max(division_scale, sa, sb)`; `division_scale` defaults to 10 | → 10 |

Integers count as scale 0. `int / int` gives an **exact decimal** at `division_scale`, not a truncated integer: `7 / 2` is `3.5000000000`.

Here are the types the engine infers for a few formulas over the example fund:

```python exec="on"
from book import engine

calc = engine()
formulas = [
    "price * quantity",
    "price * quantity * fx_rate",
    "round(price * quantity * fx_rate, 2)",
    "price + 0.125",
    "price / quantity",
    "quantity / 3",
    "yield * 1.05",
    "float(price) * yield",
    "round(price * 1.07, 2)",
    "decimal(yield, 4)",
]
derive = [{"name": f"f{i}", "expr": f} for i, f in enumerate(formulas)]
plan = calc.explain({"dataset": "holdings", "query": {"derive": derive, "page": {"limit": 1}}})
print("| Formula | Result type |\n| --- | --- |")
for i, f in enumerate(formulas):
    print(f"| `{f}` | `{plan['columns'][f'f{i}']}` |")
```

## Floats and decimals never mix silently

| Expression | Result |
| --- | --- |
| `yield * 1.05` | ✅ float. A decimal *literal* adapts to the float column |
| `price * 1.05` | ✅ exact decimal |
| `price * yield` | ❌ `422 type_mismatch`: say what you mean |
| `float(price) * yield` | ✅ float |
| `price * decimal(yield, 6)` | ✅ exact decimal |

This rule stops an accidental float from contaminating a number that must be exact.

## Nulls follow SQL

- **Arithmetic** with null gives null: `price * quantity` is null if either is null.
- **Comparisons** with null give null. `yield > 0.03` is null for an equity, which has no yield.
- **A null condition counts as false** in `filter`, a measure's `where`, a shock's `where` and `if`.
- **`and` and `or` use three-valued logic**: `null and false` is false, and `null or true` is true.
- **Aggregates skip nulls.** `sum` of only nulls is null, `count` counts non-nulls, and `count_rows` counts rows.
- Test for null with `x is None` / `x is not None`. Replace nulls with `coalesce(x, 0)`.

## Invalid arithmetic gives null

`x / 0`, `sqrt(-1)` and `log(0)` return **null** rather than an error or infinity, so one bad row can't fail a whole report. Where it matters, count those rows with a measure such as `{"fn": "count_rows", "where": "quantity == 0"}`.

## Shocks keep the column's type

- **Decimal columns** are rounded half-to-even back to the column's scale.
- **Integer columns** refuse a fractional result unless the shock has `"round": true`.

## Float sums and reproducibility

Polars adds floats in parallel, so a float sum can differ in the last bits from run to run. When that matters, pass `"options": {"deterministic": true}`: values are then summed in sorted order, which is slower but gives the same answer every time. **Decimal sums are always exact**, whatever the option.

## Settings

```python
from pylibs_calc import CalcEngine, EngineConfig, NumericConfig

engine = CalcEngine(catalog, EngineConfig(numeric=NumericConfig(max_scale=18, division_scale=12)))
```

The numeric settings are part of every fingerprint, so changing them can't return a stale cached result.
