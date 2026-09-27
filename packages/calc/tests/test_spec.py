from typing import Any

import pytest
from pydantic import ValidationError

from pylibs_calc import CalcRequest, Query, Shock, SpecError, fingerprint
from pylibs_calc.spec.canonical import canonical_json, upgrade


def request(**query: Any) -> dict[str, Any]:
    return {"dataset": "pos", "query": query}


def test_fingerprint_ignores_key_order_and_formula_text() -> None:
    a = CalcRequest.model_validate(request(filter="qty > 1", group_by=["desk"]))
    b = CalcRequest.model_validate(
        {
            "query": {
                "group_by": ["desk"],
                "filter": {
                    "kind": "cmp",
                    "op": "gt",
                    "left": {"kind": "col", "name": "qty"},
                    "right": {"kind": "lit", "type": "int", "value": 1},
                },
            },
            "dataset": {"id": "pos"},
        }
    )
    assert fingerprint(a) == fingerprint(b)


def test_decimal_formatting_is_canonical() -> None:
    a = Shock.model_validate({"column": "p", "op": "pct", "value": "5.00"})
    b = Shock.model_validate({"column": "p", "op": "pct", "value": 5})
    assert canonical_json(a) == canonical_json(b)
    assert fingerprint(CalcRequest.model_validate(request(filter="p > 1.50"))) == fingerprint(
        CalcRequest.model_validate(request(filter="p > 1.5"))
    )


def test_different_requests_differ() -> None:
    a = CalcRequest.model_validate(request(filter="qty > 1"))
    b = CalcRequest.model_validate(request(filter="qty > 2"))
    assert fingerprint(a) != fingerprint(b)


def test_canonical_dump_round_trips_with_kinds() -> None:
    req = CalcRequest.model_validate(
        {
            "dataset": "pos",
            "what_if": [{"kind": "shock", "column": "p", "op": "add", "value": "1.5"}],
            "query": {"derive": [{"name": "n", "expr": "p * q"}]},
        }
    )
    dumped = req.model_dump(mode="json", exclude_defaults=True)
    assert dumped["query"]["derive"][0]["expr"]["kind"] == "binary"
    assert CalcRequest.model_validate(dumped) == req


@pytest.mark.parametrize(
    "query",
    [
        {"post": [{"name": "x", "expr": "1"}]},
        {"rollup": True, "measures": [{"name": "n", "fn": "count_rows"}]},
        {"group_by": ["a"], "select": ["a"]},
        {"measures": [{"name": "n", "fn": "sum"}]},
        {"measures": [{"name": "n", "fn": "count_rows", "of": "a"}]},
        {"measures": [{"name": "n", "fn": "wavg", "of": "a"}]},
        {"derive": [{"name": "x", "expr": "a", "otherwise": "b"}]},
    ],
)
def test_invalid_query_shapes(query: dict[str, Any]) -> None:
    with pytest.raises(ValidationError):
        Query.model_validate(query)


def test_upgrade_rejects_unknown_versions() -> None:
    assert upgrade({"spec_version": 1})["spec_version"] == 1
    with pytest.raises(SpecError, match="unsupported spec_version"):
        upgrade({"spec_version": 99})


def test_unknown_fields_are_rejected() -> None:
    with pytest.raises(ValidationError):
        CalcRequest.model_validate({"dataset": "pos", "querry": {}})
