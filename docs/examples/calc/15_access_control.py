"""Access control: a Rates trader sees only Rates rows and no yields."""

from book import engine, table

from pylibs_calc import CalcContext

REQUEST = {
    "dataset": "positions",
    "query": {
        "select": ["position_id", "desk", "price", "quantity"],
        "sort": [{"by": "position_id"}],
    },
}

rates_trader = CalcContext(
    principal="raj",
    row_filter="desk == 'Rates'",
    allowed_columns=frozenset({"desk", "instrument", "price", "quantity"}),
)
calc = engine()
print(table(calc.run(REQUEST, rates_trader)))

visible = [c.name for c in calc.schema("positions", ctx=rates_trader).columns]
print(f"Columns this trader can see: `{visible}`")
