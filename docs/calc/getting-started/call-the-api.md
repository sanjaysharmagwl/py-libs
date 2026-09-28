# Call the API with curl

This page is for **QA and business users** who want to try calculations without writing Python. Start the [demo service](run-the-demo.md), then paste these commands into a terminal. Each request is plain JSON.

## Discover the data

```bash
curl -s localhost:8000/calc/datasets
curl -s localhost:8000/calc/datasets/positions/schema
```

The schema lists every column with its type, its role (`key`, `dimension` or `measure`) and whether it can be edited.

## Run a query

```bash
curl -s localhost:8000/calc/query -H 'Content-Type: application/json' -d '{
  "dataset": "positions",
  "query": {
    "group_by": ["desk"],
    "measures": [
      {"name": "mv", "fn": "sum", "of": "price * quantity"},
      {"name": "positions", "fn": "count_rows"}
    ],
    "sort": [{"by": "mv", "desc": true}]
  }
}'
```

The response is `{"rows": [...], "meta": {...}}`. `meta.fingerprint` (also sent as the `X-Calc-Fingerprint` header) identifies the calculation exactly, so note it in a bug report.

## Try a what-if

```bash
curl -s localhost:8000/calc/compare -H 'Content-Type: application/json' -d '{
  "dataset": "positions",
  "extensions": {"whatif": {"steps": [{"kind": "shock", "column": "price", "op": "pct", "value": -5, "where": "sector == '"'"'Energy'"'"'"}]}},
  "query": {
    "group_by": ["sector"],
    "measures": [{"name": "mv", "fn": "sum", "of": "price * quantity"}],
    "sort": [{"by": "mv__delta"}]
  }
}'
```

!!! tip "Quotes inside JSON inside a shell"
    Formulas use single quotes for strings (`sector == 'Energy'`). That clashes with a shell's single-quoted `-d '...'`. The easiest fix is a *heredoc*: write `-d @- <<'JSON'`, paste the JSON on the lines below it, and end with a line containing only `JSON`. The **JSON (curl)** tabs on the scenario pages use that form.

## See how a number is computed

```bash
curl -s localhost:8000/calc/explain -H 'Content-Type: application/json' -d '{
  "dataset": "positions",
  "query": {"derive": [{"name": "notional", "expr": "price * quantity"}], "page": {"limit": 1}}
}'
```

## Get exact decimals, or Arrow

- Decimals come back as JSON numbers by default. A service can return them as exact strings (`"101.25"`) instead, by creating its router with `create_router(..., decimals="str")`.
- Send `Accept: application/vnd.apache.arrow.stream` to `/calc/query` to get an Arrow IPC stream. It keeps exact decimals and is much faster for large results.

## When something is wrong

Errors come back with an HTTP status and a body such as:

```json
{"detail": {"code": "unknown_column", "message": "unknown column: notionl", "path": "/query/measures/0/of"}}
```

`path` points at the part of your request to fix. Every code is listed in [Error codes](../reference/error-codes.md).

## All routes

| Route | Purpose |
| --- | --- |
| `POST /calc/query`, `/compare`, `/explain` | Run, compare or explain a request |
| `POST /calc/distinct` | Distinct values of a column: `{"dataset", "column", "extensions"?, "filter"?, "limit"?}` |
| `GET /calc/datasets`, `/datasets/{id}/schema` | Datasets and their columns |
| `POST /calc/aggrid/rows` | AG Grid server-side row model |
| `GET /calc/operations`, `POST /calc/operations/{name}` | List and run [plugin operations](../concepts/plugins.md#operations) |
| `GET/POST /calc/scenarios`, `GET/DELETE /calc/scenarios/{id}` | What-if plugin: list, create, read and delete saved scenarios |
| `POST /calc/scenarios/{id}/steps`, `/fork` | What-if plugin: append steps (with `expected_version`), and fork |
| `GET /calc/scenarios/{id}/log`, `/verify` | What-if plugin: read the log, and check its hash chain |
| `POST /calc/aggrid/edit` | What-if plugin: save a grid cell edit as a scenario override |

Plugin routes exist only when the plugin is installed in the engine.
