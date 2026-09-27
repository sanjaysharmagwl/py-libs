import io

import polars as pl
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from pylibs_calc import CalcContext, CalcEngine
from pylibs_calc.integrations.fastapi import ARROW_STREAM, create_router


@pytest.fixture
def client(engine: CalcEngine) -> TestClient:
    def resolve(request: Request) -> CalcContext:
        user = request.headers.get("X-User")
        rows = "desk == 'rates'" if user == "rates-trader" else None
        return CalcContext(principal=user, row_filter=rows)

    app = FastAPI()
    app.include_router(
        create_router(engine, prefix="/calc", context_resolver=resolve, max_body_bytes=20_000)
    )
    return TestClient(app)


def test_query_json(client: TestClient) -> None:
    body = {
        "dataset": "pos",
        "query": {"group_by": ["sector"], "measures": [{"name": "q", "fn": "sum", "of": "qty"}]},
    }
    response = client.post("/calc/query", json=body)
    assert response.status_code == 200
    data = response.json()
    assert data["rows"] == [
        {"sector": "Energy", "q": 40},
        {"sector": "Fin", "q": 80},
        {"sector": "Tech", "q": 90},
    ]
    assert data["meta"]["total_rows"] == 3
    assert response.headers["X-Calc-Fingerprint"] == data["meta"]["fingerprint"]


def test_query_arrow(client: TestClient) -> None:
    response = client.post(
        "/calc/query",
        json={"dataset": "pos", "query": {"select": ["id", "price"]}},
        headers={"Accept": ARROW_STREAM},
    )
    assert response.headers["content-type"] == ARROW_STREAM
    frame = pl.read_ipc_stream(io.BytesIO(response.content))
    assert frame.schema["price"] == pl.Decimal(38, 2)
    assert frame.height == 6


def test_context_applies_row_filter(client: TestClient) -> None:
    response = client.post(
        "/calc/query", json={"dataset": "pos"}, headers={"X-User": "rates-trader"}
    )
    assert [r["id"] for r in response.json()["rows"]] == [1, 2]


@pytest.mark.parametrize(
    ("body", "status", "code"),
    [
        ({"dataset": "nope"}, 404, "dataset_not_found"),
        ({"dataset": "pos", "query": {"filter": "qty >"}}, 422, "formula_syntax"),
        ({"dataset": "pos", "query": {"filter": "nope > 1"}}, 422, "unknown_column"),
        ({"dataset": "pos", "querry": {}}, 422, "invalid_request"),
        ({"dataset": "pos", "query": {"page": {"limit": 10**9}}}, 413, "limit_exceeded"),
    ],
)
def test_errors(client: TestClient, body: dict[str, object], status: int, code: str) -> None:
    response = client.post("/calc/query", json=body)
    assert response.status_code == status
    assert response.json()["detail"]["code"] == code


def test_body_limit(client: TestClient) -> None:
    body = {"dataset": "pos", "query": {"filter": " or ".join(["qty > 1"] * 3000)}}
    response = client.post("/calc/query", json=body)
    assert response.status_code == 413


def test_scenario_lifecycle(client: TestClient) -> None:
    created = client.post(
        "/calc/scenarios", json={"dataset": "pos", "name": "s"}, headers={"X-User": "ana"}
    )
    assert created.status_code == 201
    scenario = created.json()
    assert scenario["owner"] == "ana"
    url = f"/calc/scenarios/{scenario['id']}"
    step = {"kind": "shock", "column": "qty", "op": "add", "value": 1}
    appended = client.post(
        f"{url}/steps",
        json={"steps": [step], "expected_version": 0},
        headers={"Idempotency-Key": "k1"},
    )
    assert appended.json()["version"] == 1
    retried = client.post(
        f"{url}/steps",
        json={"steps": [step], "expected_version": 0},
        headers={"Idempotency-Key": "k1"},
    )
    assert retried.json()["version"] == 1
    stale = client.post(f"{url}/steps", json={"steps": [step], "expected_version": 0})
    assert stale.status_code == 409 and stale.json()["detail"]["code"] == "version_conflict"
    assert len(client.get(f"{url}/log").json()) == 1
    assert client.get(f"{url}/verify").json()["intact"] is True
    fork = client.post(f"{url}/fork", json={"name": "copy"})
    assert fork.status_code == 201 and fork.json()["version"] == 1
    run = client.post(
        "/calc/query",
        json={"dataset": "pos", "scenario": scenario["id"], "query": {"filter": "id == 1"}},
    )
    assert run.json()["rows"][0]["qty"] == 11
    assert client.delete(url).status_code == 204
    assert client.get(url).status_code == 404
    assert [s["name"] for s in client.get("/calc/scenarios", params={"dataset": "pos"}).json()] == [
        "copy"
    ]


def test_aggrid_rows_and_edit(client: TestClient) -> None:
    scenario = client.post("/calc/scenarios", json={"dataset": "pos", "name": "grid"}).json()
    edit = client.post(
        "/calc/aggrid/edit",
        json={
            "scenario": scenario["id"],
            "expected_version": 0,
            "edit": {"colId": "qty", "newValue": "99", "data": {"id": 1}},
        },
    )
    assert edit.status_code == 200 and edit.json()["version"] == 1
    response = client.post(
        "/calc/aggrid/rows",
        json={
            "dataset": "pos",
            "scenario": scenario["id"],
            "request": {
                "startRow": 0,
                "endRow": 50,
                "rowGroupCols": [{"id": "desk", "field": "desk"}],
                "valueCols": [{"id": "qty", "field": "qty", "aggFunc": "sum"}],
                "groupKeys": [],
            },
        },
    )
    data = response.json()
    assert data["rowCount"] == 4
    assert next(r for r in data["rowData"] if r["desk"] == "rates")["qty"] == 119


def test_schema_distinct_and_explain(client: TestClient) -> None:
    schema = client.get("/calc/datasets/pos/schema").json()
    assert schema["key_columns"] == ["id"]
    assert {c["name"]: c["type"] for c in schema["columns"]}["price"] == "decimal(2)"
    assert [d["dataset"] for d in client.get("/calc/datasets").json()] == ["pos"]
    values = client.post("/calc/distinct", json={"dataset": "pos", "column": "desk"}).json()
    assert values == {"values": ["credit", "equity", "rates", None]}
    explained = client.post(
        "/calc/explain", json={"dataset": "pos", "query": {"filter": "qty > 1"}}
    ).json()
    assert "plan" in explained and len(explained["fingerprint"]) == 64
    compared = client.post(
        "/calc/compare",
        json={
            "dataset": "pos",
            "what_if": [{"kind": "shock", "column": "qty", "op": "mul", "value": 2}],
            "query": {"measures": [{"name": "q", "fn": "sum", "of": "qty"}]},
        },
    ).json()
    assert compared["rows"] == [{"q": 420, "q__base": 210, "q__delta": 210, "q__pct": 100.0}]
