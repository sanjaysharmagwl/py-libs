# Request schema

A request is JSON. The engine validates it with pydantic, and these JSON Schemas are generated from the same models when the docs are built. Use them to generate typed clients, or to validate requests in a UI before sending them.

Expressions (`filter`, `expr`, `of`, `where`, …) accept a **formula string** or an **expression tree**. The schemas show the tree form, which is what is stored and fingerprinted.

```python exec="on"
import json
from pylibs_calc import CalcRequest, CompareRequest
from pylibs_calc_whatif import Disable, Formula, Override, Shock, WhatIf

models = [
    ("CalcRequest", "the body of `/query` and `/explain`", CalcRequest),
    ("CompareRequest", "the body of `/compare`", CompareRequest),
    ("WhatIf", "the `extensions.whatif` block (what-if plugin)", WhatIf),
    ("Override", "a what-if step", Override),
    ("Shock", "a what-if step", Shock),
    ("Formula", "a what-if step", Formula),
    ("Disable", "a what-if step", Disable),
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

The same structures are pydantic models, importable from `pylibs_calc` (and, for the what-if block, from `pylibs_calc_whatif`), if you prefer typed code to dictionaries:

| JSON | Model |
| --- | --- |
| the whole request | `CalcRequest`, `CompareRequest` |
| `dataset` | `DatasetRef` (or a plain string) |
| `extensions` | a dict: one block per plugin transform, validated by that plugin |
| `base` (compare) | `Side`: `version` and `extensions` of the base side |
| `extensions.whatif` | `WhatIf`: `scenario`, `steps`, `strict_edits` |
| `extensions.whatif.scenario` | `ScenarioRef` (or a plain string) |
| `query` | `Query` |
| `query.derive[]` | `Derive` |
| `query.measures[]` | `Measure` |
| `query.post[]` | `PostAgg` |
| `query.pivot` | `Pivot` |
| `query.sort[]` | `SortKey` |
| `query.page` | `Page` |
| `options` | `Options` |
| `extensions.whatif.steps[]` | `Override` (with `Edit`s), `Shock`, `Formula`, `Disable` |

## Minimal requests

```json
{"dataset": "positions"}
```

This returns every row (up to `max_unpaged_rows`).

```json
{
  "dataset": {"id": "positions", "version": "2026-09-30"},
  "extensions": {"whatif": {"scenario": {"id": "…", "version": 3}}}
}
```

This pins both versions, which makes the result reproducible forever.

An `extensions` key names a plugin transform; an engine without that plugin answers `422 unknown_extension`.

## Versions

The current `spec_version` is `2`. Older requests are upgraded when they are parsed, so they keep working and keep their meaning (and their fingerprints).

| Version 1 | Version 2 |
| --- | --- |
| `"scenario": ...` | `"extensions": {"whatif": {"scenario": ...}}` |
| `"what_if": [...]` | `"extensions": {"whatif": {"steps": [...]}}` |
| `"options": {"strict_edits": false}` | `"extensions": {"whatif": {"strict_edits": false}}` |
| compare: `"base": ...`, `"base_what_if": [...]` | `"base": {"extensions": {"whatif": {"scenario": ..., "steps": [...]}}}` |

A request without `spec_version` is treated as version 1 if it uses any of those version 1 keys, and as the current version otherwise. Error paths follow the version 2 shape (for example `/extensions/whatif/steps/0/column`).
