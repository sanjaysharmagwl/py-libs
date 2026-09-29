"""Shocks: tech stocks -10% and bond yields +25bp; then the dollar strengthens 5%."""

from book import engine, table

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
                },
                {
                    "kind": "shock",
                    "column": "yield",
                    "op": "add",
                    "value": "0.0025",
                    "where": "asset_class == 'Fixed Income'",
                },
            ]
        }
    },
    "query": {
        "filter": "sector == 'Information Technology' or asset_class == 'Fixed Income'",
        "select": ["security_id", "security", "sector", "price", "yield"],
        "sort": [{"by": "security_id"}],
    },
}

# A stronger dollar: every non-USD rate falls 5%, so foreign holdings are worth less in USD.
FX_REQUEST = {
    "dataset": "holdings",
    "extensions": {
        "whatif": {
            "steps": [
                {
                    "kind": "shock",
                    "column": "fx_rate",
                    "op": "pct",
                    "value": -5,
                    "where": "currency != 'USD'",
                }
            ]
        }
    },
    "query": {
        "filter": "quantity > 0",
        "derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}],
        "group_by": ["currency"],
        "measures": [{"name": "mv", "fn": "sum", "of": "mv"}],
        "sort": [{"by": "currency"}],
    },
}

calc = engine()
print(table(calc.run(REQUEST)))
print(table(calc.compare(FX_REQUEST)))
