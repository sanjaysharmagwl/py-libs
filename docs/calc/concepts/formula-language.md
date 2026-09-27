---
covers:
  - packages/calc/src/pylibs_calc/spec/formula.py
  - packages/calc/src/pylibs_calc/spec/expr.py
---

# Formula language

Wherever a request takes an expression (in `filter`, `derive`, `of`, `weight`, `where`, `post`, `having` and formula steps), you can write a **formula**: a small, safe subset of Python's expression syntax. It is parsed with Python's `ast` module against a whitelist and **never evaluated as code**.

## Cheat sheet

| What | Syntax | Example |
| --- | --- | --- |
| Column | a plain name | `price`, `yield` (keywords work too) |
| Column with any name | `col('...')` | `col('Market Value')` |
| Number | digits | `1.05` is an **exact decimal**, `100` an integer |
| String | quotes | `'EMEA'` |
| Boolean, null | | `True`, `False`, `None` |
| Date, timestamp | | `date('2026-01-31')`, `datetime('2026-01-31T12:00:00')` |
| Arithmetic | `+ - * / **` | `price * quantity` |
| Comparison | `== != < <= > >=`, and chains | `0 < yield <= 0.05` |
| Logic | `and or not` | `region == 'EMEA' and not quantity < 0` |
| Membership | `in`, `not in` | `desk in ('Rates', 'Credit')` |
| Null test | `is None`, `is not None` | `yield is not None` |
| Conditional | `a if cond else b` | `'long' if quantity > 0 else 'short'` |
| Cast | `int() float() str() decimal(x, scale) to_date()` | `decimal(yield, 6)` |

## Functions

```python exec="on"
from pylibs_calc.spec.expr import FUNC_ARITY


def arity(lo, hi):
    if hi is None:
        return f"{lo} or more"
    return str(lo) if lo == hi else f"{lo}–{hi}"


print("| Function | Arguments |\n| --- | --- |")
for name, (lo, hi) in FUNC_ARITY.items():
    print(f"| `{name}` | {arity(lo, hi)} |")
```

- `round(x, n)` rounds half-to-even.
- `min` and `max` compare their arguments across a row. They are not aggregates; for those, use a [measure](../scenarios/measures.md).
- `coalesce(a, b, …)` returns the first non-null argument.
- `contains`, `starts_with` and `ends_with` test strings.

## Formulas are stored as trees

A formula is parsed into an **expression tree**, which is what gets stored, fingerprinted and sent to both evaluators. You can send the tree instead of the text, which is useful when a UI builds expressions:

```python exec="on" source="tabbed-left" tabs="Python|Output"
from pylibs_calc import parse_formula, to_formula

tree = parse_formula("0 < yield <= 0.05 and desk in ('Rates', 'Credit')")
print("```json")
print(tree.model_dump_json(indent=2)[:600] + "\n  ...")
print("```")
print(f"Back to text: `{to_formula(tree)}`")
```

In Python, `col("price")` and `lit(1.05)` build the leaves of a tree, and `pylibs_calc.spec.expr` has the node classes (`Binary`, `Compare`, `Func`, …). In practice, formula strings are the easiest to read and review.

## Errors

A formula that doesn't parse is a `422 formula_syntax`, with a `path` to the field. An unknown name is `422 unknown_column`. Formulas are also capped in length and complexity (`formula_too_long`, `formula_too_complex`), so one request can't exhaust the parser.
