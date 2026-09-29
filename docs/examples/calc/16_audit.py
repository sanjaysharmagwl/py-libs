"""Audit a number: fingerprint, explain, and the independent reference evaluator."""

from book import engine

from pylibs_calc.verify import verify

REQUEST = {
    "dataset": "holdings",
    "extensions": {
        "whatif": {
            "steps": [
                {
                    "kind": "shock",
                    "column": "price",
                    "op": "pct",
                    "value": -10,
                    "where": "sector == 'Information Technology' and asset_class == 'Equity'",
                }
            ]
        }
    },
    "query": {
        "derive": [
            {"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"},
            {"name": "bench_mv", "expr": "round(price * bench_quantity * fx_rate, 2)"},
        ],
        "group_by": ["sector"],
        "measures": [
            {"name": "fund", "fn": "sum", "of": "mv"},
            {"name": "bench", "fn": "sum", "of": "bench_mv"},
        ],
        "post": [
            {
                "name": "active_pct",
                "expr": "round(100 * (fund / total(fund) - bench / total(bench)), 2)",
            }
        ],
        "sort": [{"by": "sector"}],
    },
    "options": {"audit": True},
}

calc = engine()
result = calc.run(REQUEST)
meta = result.meta
it = next(r for r in result.frame.to_dicts() if r["sector"] == "Information Technology")
print(f"- **active weight in IT after the shock**: {it['active_pct']}%")
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
print(f"- **what-if lineage**: `{plan['extensions']['whatif']}`")
print(f"- **output types**: `{plan['columns']}`")

report = verify(calc, REQUEST)
print(f"- **reference evaluator agrees**: {report.ok} ({report.input_rows} rows checked)")
print(f"- **differences found**: {list(report.problems)}")
