"""Disable: undo a saved step without rewriting history."""

from book import engine, table

from pylibs_calc import CalcContext, to_formula

calc = engine()
ana = CalcContext(principal="ana")
s = calc.scenarios.create("positions", "credit stress", ctx=ana)
s = calc.scenarios.append(
    s.id,
    [
        {
            "kind": "shock",
            "column": "price",
            "op": "pct",
            "value": -10,
            "where": "desk == 'Credit'",
        },
        {"kind": "shock", "column": "price", "op": "pct", "value": -3, "where": "desk == 'Rates'"},
    ],
    expected_version=0,
    ctx=ana,
)
# Step 1 (Credit -10%) turns out to be too harsh: disable it. It stays in the log.
s = calc.scenarios.append(s.id, [{"kind": "disable", "seq": 1}], expected_version=2, ctx=ana)

QUERY = {
    "filter": "desk in ('Rates', 'Credit')",
    "select": ["position_id", "desk", "price"],
    "sort": [{"by": "position_id"}],
}
print(table(calc.run({"dataset": "positions", "scenario": s.id, "query": QUERY})))
print("| seq | author | step |\n| --- | --- | --- |")
for entry in calc.scenarios.log(s.id):
    step = entry.step
    if step.kind == "shock":
        where = f" where {to_formula(step.where)}" if step.where else ""
        text = f"shock {step.column} {step.op} {step.value}{where}"
    else:
        text = f"disable step {step.seq}"
    print(f"| {entry.seq} | {entry.author} | `{text}` |")
