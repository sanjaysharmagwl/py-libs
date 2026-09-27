"""Audit a number: fingerprint, explain, and the independent reference evaluator."""

from book import engine

from pylibs_calc.verify import verify

REQUEST = {
    "dataset": "positions",
    "what_if": [
        {"kind": "shock", "column": "price", "op": "pct", "value": 5, "where": "sector == 'Tech'"}
    ],
    "query": {
        "derive": [{"name": "notional", "expr": "price * quantity"}],
        "group_by": ["desk"],
        "measures": [{"name": "notional", "fn": "sum", "of": "notional"}],
        "sort": [{"by": "desk"}],
    },
    "options": {"audit": True},
}

calc = engine()
result = calc.run(REQUEST)
meta = result.meta
print(f"- **fingerprint**: `{meta.fingerprint}`")
print(f"- **dataset**: `{meta.dataset.id}` version `{meta.dataset.version}`")
print(f"- **library versions**: `{meta.versions}`")
print(f"- **rows at each stage**: `{meta.stage_rows}`")

# The same request gives the same fingerprint, and is served from the cache.
again = calc.run(REQUEST)
same = again.meta.fingerprint == meta.fingerprint
print(f"- **same fingerprint again**: {same}, served from cache: {again.meta.cached}")

plan = calc.explain(REQUEST)
print(f"- **effective steps**: `{plan['steps']}`")
print(f"- **lineage**: `{plan['lineage']}`")
print(f"- **output types**: `{plan['columns']}`")

report = verify(calc, REQUEST)
print(f"- **reference evaluator agrees**: {report.ok} ({report.input_rows} rows checked)")
print(f"- **differences found**: {list(report.problems)}")
