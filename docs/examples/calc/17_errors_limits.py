"""Errors and limits: every refusal has a stable code, a JSON-pointer path and an HTTP status."""

from book import engine

from pylibs_calc import CalcEngine, CalcError, EngineConfig, Limits


def row(label: str, err: CalcError) -> str:
    path = f"`{err.path}`" if err.path else "—"
    return f"| {label} | {err.status} | `{err.code}` | {path} | {err.message} |"


calc = engine()
BAD_REQUESTS = {
    "a typo in a column name": {
        "dataset": "holdings",
        "query": {"group_by": ["sector"], "measures": [{"name": "q", "fn": "sum", "of": "qty"}]},
    },
    "mixing a float and a decimal": {
        "dataset": "holdings",
        "query": {"derive": [{"name": "x", "expr": "price * yield"}]},
    },
    "a formula that doesn't parse": {
        "dataset": "holdings",
        "query": {"filter": "price >"},
    },
    "total() outside post or having": {
        "dataset": "holdings",
        "query": {"derive": [{"name": "w", "expr": "quantity / total(quantity)"}]},
    },
    "an unknown dataset": {"dataset": "trades"},
    "an override of a key that doesn't exist": {
        "dataset": "holdings",
        "extensions": {
            "whatif": {
                "steps": [
                    {
                        "kind": "override",
                        "edits": [{"key": {"security_id": 99}, "column": "price", "value": 1}],
                    }
                ]
            }
        },
    },
}

print("| Mistake | Status | Code | Path | Message |")
print("| --- | --- | --- | --- | --- |")
for label, request in BAD_REQUESTS.items():
    try:
        calc.run(request)
    except CalcError as err:
        print(row(label, err))

# A host can tighten the limits: here, at most 5 rows per page.
strict = CalcEngine(calc.catalog, config=EngineConfig(limits=Limits(max_page_size=5)))
try:
    strict.run({"dataset": "holdings", "query": {"page": {"limit": 50}}})
except CalcError as err:
    print(row("a page larger than `max_page_size`", err))
