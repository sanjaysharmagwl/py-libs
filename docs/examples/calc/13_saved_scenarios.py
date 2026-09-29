"""Saved scenarios: create, append with optimistic locking, read old versions, fork."""

from book import engine

from pylibs_calc import CalcContext, VersionConflict
from pylibs_calc_whatif import WhatIfPlugin

calc = engine()
scenarios = calc.plugin(WhatIfPlugin).scenarios
ana = CalcContext(principal="ana")

# 1. Create an empty scenario, pinned to today's version of the holdings.
s = scenarios.create("holdings", "AI rally", ctx=ana)

# 2. Append a step. expected_version must match the scenario's current version (0).
ai_rally = {
    "kind": "shock",
    "column": "price",
    "op": "pct",
    "value": 8,
    "where": "sector == 'Information Technology' and asset_class == 'Equity'",
}
s = scenarios.append(s.id, [ai_rally], expected_version=0, client_op_id="op-1", ctx=ana)

# 3. A retry of the same operation is a no-op; a stale version is a 409.
s = scenarios.append(s.id, [ai_rally], expected_version=0, client_op_id="op-1", ctx=ana)
try:
    scenarios.append(s.id, [ai_rally], expected_version=0, ctx=ana)
except VersionConflict as err:
    print(f"> **{err.status} {err.code}**: {err.message}\n")

# 4. Fork it to try closing some of the underweight (buy Initech), without touching the original.
closer = scenarios.fork(s.id, name="AI rally, buy Initech", ctx=ana)
closer = scenarios.append(
    closer.id,
    [
        {
            "kind": "override",
            "edits": [{"key": {"security_id": 13}, "column": "quantity", "value": 10000}],
        }
    ],
    expected_version=closer.version,
    ctx=ana,
)

QUERY = {
    "derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}],
    "group_by": ["sector"],
    "measures": [{"name": "mv", "fn": "sum", "of": "mv"}],
    "post": [{"name": "weight_pct", "expr": "round(100 * mv / total(mv), 2)"}],
}
for label, ref in [
    ("current fund", None),
    ("AI rally, version 0 (empty)", {"id": s.id, "version": 0}),
    ("AI rally, latest", s.id),
    ("AI rally, buy Initech (fork)", closer.id),
]:
    request = {"dataset": "holdings", "query": QUERY}
    if ref is not None:
        request["extensions"] = {"whatif": {"scenario": ref}}
    rows = calc.run(request).frame.to_dicts()
    it = next(r for r in rows if r["sector"] == "Information Technology")
    print(f"- **{label}**: IT = {it['mv']} USD, {it['weight_pct']}% of the fund")
print(f"\nHash chain intact: {scenarios.verify(s.id)}")
