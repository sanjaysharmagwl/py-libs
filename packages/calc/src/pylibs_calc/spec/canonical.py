"""Canonical JSON, fingerprints and spec-version upgrades.

The canonical form of a spec object is its JSON dump without default values, with sorted keys
and no whitespace. Two requests that mean the same thing (key order, ``"1.50"`` vs ``1.5``, a
formula string vs its tree) have the same canonical form and therefore the same fingerprint.
"""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel

from pylibs_calc.errors import SpecError

SPEC_VERSION = 1

# Upgraders turn a raw request of version N into version N + 1. Register one whenever the spec
# changes incompatibly, so old requests keep working and keep their meaning.
UPGRADERS: dict[int, Callable[[dict[str, Any]], dict[str, Any]]] = {}


def upgrade(raw: dict[str, Any]) -> dict[str, Any]:
    """Bring a raw request dict up to the current ``spec_version``."""
    version = raw.get("spec_version", SPEC_VERSION)
    if not isinstance(version, int) or version < 1 or version > SPEC_VERSION:
        raise SpecError(
            f"unsupported spec_version {version!r}; this engine speaks up to {SPEC_VERSION}",
            code="unsupported_spec_version",
            path="/spec_version",
        )
    while version < SPEC_VERSION:
        raw = {**UPGRADERS[version](raw), "spec_version": version + 1}
        version += 1
    return raw


def to_canonical(value: Any) -> Any:
    """JSON-ready canonical form of a model, or of plain data containing models."""
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", exclude_defaults=True)
    if isinstance(value, dict):
        return {str(k): to_canonical(v) for k, v in value.items()}
    if isinstance(value, list | tuple):
        return [to_canonical(v) for v in value]
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(
        to_canonical(value), sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def fingerprint(value: Any) -> str:
    """SHA-256 of the canonical JSON, as hex."""
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()
