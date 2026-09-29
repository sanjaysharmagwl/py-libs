"""Access control: an analyst sees only their coverage; client reporting never sees targets."""

from book import engine, table

from pylibs_calc import CalcContext

REQUEST = {
    "dataset": "holdings",
    "query": {
        "select": ["security_id", "security", "sector", "price", "target_price"],
        "sort": [{"by": "security_id"}],
    },
}

credit_analyst = CalcContext(principal="raj", row_filter="analyst == 'raj'")
client_reporting = CalcContext(
    principal="cr-team",
    allowed_columns=frozenset(
        {"security_id", "security", "asset_class", "sector", "country", "region", "currency",
         "price", "fx_rate", "quantity", "bench_quantity", "rating", "yield", "duration"}
    ),
)  # fmt: skip
calc = engine()
print(table(calc.run(REQUEST, credit_analyst)))

visible = [c.name for c in calc.schema("holdings", ctx=client_reporting).columns]
print(f"Columns client reporting can see: `{visible}`")
