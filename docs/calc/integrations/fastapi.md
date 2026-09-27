---
covers:
  - packages/calc/src/pylibs_calc/integrations/fastapi.py
---

# FastAPI

`create_router` gives you a complete HTTP API over an engine. You plug it into your own FastAPI app, with your own authentication.

```bash
pip install "pylibs-calc[fastapi]"
```

```python
from fastapi import Depends, FastAPI
from pylibs_calc import CalcContext, CalcEngine, Catalog, InMemoryScenarioStore
from pylibs_calc.integrations.fastapi import create_router

catalog = Catalog()
catalog.register_frame("positions", load_positions(), key_columns=["position_id"])
engine = CalcEngine(catalog, InMemoryScenarioStore())

app = FastAPI()
app.include_router(
    create_router(
        engine,
        prefix="/calc",
        dependencies=[Depends(authenticate)],  # your auth runs first
        context_resolver=lambda req: CalcContext(  # then maps the user to entitlements
            principal=req.state.user,
            row_filter=f"desk in {tuple(req.state.desks)!r}",
            allowed_columns=frozenset(req.state.columns),
        ),
    )
)
```

## Options

| Argument | Default | Meaning |
| --- | --- | --- |
| `prefix` | `""` | URL prefix for every route |
| `tags` | `("calc",)` | OpenAPI tags |
| `dependencies` | `()` | FastAPI dependencies run on every route, such as authentication |
| `context_resolver` | anonymous | `request -> CalcContext`. See [Access control](../scenarios/access-control.md) |
| `aggrid` | `AgGridAdapter()` | A customized [AG Grid adapter](aggrid.md) |
| `decimals` | `"float"` | `"str"` returns decimals as exact strings in JSON |
| `max_body_bytes` | 5 MiB | Larger request bodies get `413` |

## Routes

| Route | Purpose |
| --- | --- |
| `POST /query`, `/compare` | Run a request. Answers with JSON, or with Arrow IPC for `Accept: application/vnd.apache.arrow.stream` |
| `POST /explain` | Effective steps, lineage, types and the Polars plan |
| `POST /distinct` | Distinct values of a column (for set filters) |
| `POST /aggrid/rows`, `/aggrid/edit` | AG Grid SSRM `getRows`, and cell edits saved as scenario overrides |
| `GET /datasets`, `/datasets/{id}/schema` | Datasets, and their columns as the caller may see them |
| `GET/POST /scenarios`, `GET/DELETE /scenarios/{id}` | List, create, read and delete scenarios |
| `POST /scenarios/{id}/steps`, `/fork` | Append steps (supports the `Idempotency-Key` header), and fork |
| `GET /scenarios/{id}/log`, `/verify` | Read the log, and check its hash chain |

Result responses carry the `X-Calc-Fingerprint` and `X-Calc-Total-Rows` headers.

## Errors

Every `CalcError` becomes an HTTP error with the error's status and the body `{"detail": {"code", "message", "path"}}`. See [Error codes](../reference/error-codes.md).

## Threading

The routes are plain `def` functions, so FastAPI runs them in its thread pool, and a long Polars query never blocks the event loop. The engine's own slots (`EngineConfig.max_concurrent`) limit how many queries run at once. See [Deploying on Kubernetes](../operations/kubernetes.md).
