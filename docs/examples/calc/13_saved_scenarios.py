"""Saved scenarios: create, append with optimistic locking, read old versions, fork."""

from book import engine

from pylibs_calc import CalcContext, VersionConflict
from pylibs_calc_whatif import WhatIfPlugin

calc = engine()
scenarios = calc.plugin(WhatIfPlugin).scenarios
ana = CalcContext(principal="ana")

# 1. Create an empty scenario, pinned to today's version of the book.
s = scenarios.create("positions", "tech rally", ctx=ana)

# 2. Append a step. expected_version must match the scenario's current version (0).
tech_rally = {
    "kind": "shock",
    "column": "price",
    "op": "pct",
    "value": 8,
    "where": "sector == 'Tech'",
}
s = scenarios.append(s.id, [tech_rally], expected_version=0, client_op_id="op-1", ctx=ana)

# 3. A retry of the same operation is a no-op; a stale version is a 409.
s = scenarios.append(s.id, [tech_rally], expected_version=0, client_op_id="op-1", ctx=ana)
try:
    scenarios.append(s.id, [tech_rally], expected_version=0, ctx=ana)
except VersionConflict as err:
    print(f"> **{err.status} {err.code}**: {err.message}\n")

# 4. Fork it to try a hedge, without touching the original.
hedge = scenarios.fork(s.id, name="tech rally, hedged", ctx=ana)
hedge = scenarios.append(
    hedge.id,
    [
        {
            "kind": "override",
            "edits": [{"key": {"position_id": 6}, "column": "quantity", "value": -800}],
        }
    ],
    expected_version=hedge.version,
    ctx=ana,
)

QUERY = {
    "filter": "sector == 'Tech'",
    "derive": [{"name": "notional", "expr": "price * quantity"}],
    "group_by": ["sector"],
    "measures": [{"name": "notional", "fn": "sum", "of": "notional"}],
}
for label, ref in [
    ("base book", None),
    ("tech rally, version 0 (empty)", {"id": s.id, "version": 0}),
    ("tech rally, latest", s.id),
    ("tech rally, hedged (fork)", hedge.id),
]:
    request = {"dataset": "positions", "query": QUERY}
    if ref is not None:
        request["extensions"] = {"whatif": {"scenario": ref}}
    notional = calc.run(request).frame["notional"][0]
    print(f"- **{label}**: Tech notional = {notional}")
print(f"\nHash chain intact: {scenarios.verify(s.id)}")
