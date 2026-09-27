# Request schema

A request is JSON. The engine validates it with pydantic, and these JSON Schemas are generated from the same models when the docs are built. Use them to generate typed clients, or to validate requests in a UI before sending them.

Expressions (`filter`, `expr`, `of`, `where`, …) accept a **formula string** or an **expression tree**. The schemas show the tree form, which is what is stored and fingerprinted.

```python exec="on"
import json
from pylibs_calc import CalcRequest, CompareRequest
from pylibs_calc.spec.scenario import Disable, Formula, Override, Shock

models = [
    ("CalcRequest", "the body of `/query` and `/explain`", CalcRequest),
    ("CompareRequest", "the body of `/compare`", CompareRequest),
    ("Override", "a scenario step", Override),
    ("Shock", "a scenario step", Shock),
    ("Formula", "a scenario step", Formula),
    ("Disable", "a scenario step", Disable),
]
for name, what, model in models:
    schema = json.dumps(model.model_json_schema(), indent=2)
    print(f'??? note "{name}: {what}"\n')
    print("    ```json")
    for line in schema.splitlines():
        print(f"    {line}")
    print("    ```\n")
```

## Python models

The same structures are pydantic models, importable from `pylibs_calc`, if you prefer typed code to dictionaries:

| JSON | Model |
| --- | --- |
| the whole request | `CalcRequest`, `CompareRequest` |
| `dataset` | `DatasetRef` (or a plain string) |
| `scenario`, `base` | `ScenarioRef` (or a plain string) |
| `query` | `Query` |
| `query.derive[]` | `Derive` |
| `query.measures[]` | `Measure` |
| `query.post[]` | `PostAgg` |
| `query.pivot` | `Pivot` |
| `query.sort[]` | `SortKey` |
| `query.page` | `Page` |
| `options` | `Options` |
| `what_if[]` | `Override` (with `Edit`s), `Shock`, `Formula`, `Disable` |

## Minimal requests

```json
{"dataset": "positions"}
```

This returns every row (up to `max_unpaged_rows`).

```json
{"dataset": {"id": "positions", "version": "2026-09-30"}, "scenario": {"id": "…", "version": 3}}
```

This pins both versions, which makes the result reproducible forever.

`spec_version` defaults to `1`. Older request formats are upgraded automatically when a new version appears.
