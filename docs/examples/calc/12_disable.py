"""Disable: undo a saved step without rewriting history."""

from book import engine, table

from pylibs_calc import CalcContext, to_formula
from pylibs_calc_whatif import WhatIfPlugin

calc = engine()
scenarios = calc.plugin(WhatIfPlugin).scenarios
ana = CalcContext(principal="ana")
s = scenarios.create("holdings", "global recession", ctx=ana)
s = scenarios.append(
    s.id,
    [
        {
            "kind": "shock",
            "column": "price",
            "op": "pct",
            "value": -20,
            "where": "asset_class == 'Equity'",
        },
        {
            "kind": "shock",
            "column": "price",
            "op": "pct",
            "value": -5,
            "where": "asset_class == 'Fixed Income' and sector != 'Government'",
        },
        {
            "kind": "shock",
            "column": "price",
            "op": "pct",
            "value": 3,
            "where": "sector == 'Government'",
        },
    ],
    expected_version=0,
    ctx=ana,
)
# Step 1 (equities -20%) turns out to be too harsh: disable it. It stays in the log.
s = scenarios.append(s.id, [{"kind": "disable", "seq": 1}], expected_version=3, ctx=ana)

QUERY = {
    "filter": "quantity > 0",
    "derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}],
    "group_by": ["asset_class"],
    "measures": [{"name": "mv", "fn": "sum", "of": "mv"}],
    "sort": [{"by": "asset_class"}],
}
request = {"dataset": "holdings", "extensions": {"whatif": {"scenario": s.id}}, "query": QUERY}
print(table(calc.compare(request)))
print("| seq | author | step |\n| --- | --- | --- |")
for entry in scenarios.log(s.id):
    step = entry.step
    if step.kind == "shock":
        where = f" where {to_formula(step.where)}" if step.where else ""
        text = f"shock {step.column} {step.op} {step.value}{where}"
    else:
        text = f"disable step {step.seq}"
    print(f"| {entry.seq} | {entry.author} | `{text}` |")
