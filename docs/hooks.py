"""MkDocs hooks: make the examples importable, and flag pages the code has moved past.

The stale check is the one ``scripts/docs_from_graph.py`` runs, computed from the committed
``graphify-out/graph.json`` and ``docs/.docs-sync.json``, so the banner and ``stale.md`` agree.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
EXAMPLES = ROOT / "docs" / "examples" / "calc"

_stale: dict[str, list[Any]] = {}


def _sync_module() -> Any:
    spec = importlib.util.spec_from_file_location(
        "docs_from_graph", ROOT / "scripts" / "docs_from_graph.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["docs_from_graph"] = module  # dataclasses need the module registered
    spec.loader.exec_module(module)
    return module


def on_config(config: Any) -> Any:
    # markdown-exec runs the examples in this process; they import the shared `book` module.
    if str(EXAMPLES) not in sys.path:
        sys.path.insert(0, str(EXAMPLES))
    return config


def on_pre_build(config: Any) -> None:
    _stale.clear()
    sync = _sync_module()
    if not sync.GRAPH.is_file():
        return
    for item in sync.find_stale(sync.load_graph()):
        _stale.setdefault(item.page, []).append(item)


def on_page_markdown(markdown: str, page: Any, config: Any, files: Any) -> str:
    items = _stale.get(page.file.src_uri)
    if not items:
        return markdown
    depth = page.file.src_uri.count("/")
    link = "../" * depth + "calc/reference/generated/stale.md"
    changed = ", ".join(sorted({f"`{Path(i.file).name}`" for i in items}))
    banner = (
        '!!! warning "This page may be out of date"\n'
        f"    The code it explains ({changed}) has changed since the page was last reviewed. "
        f"See [Docs freshness]({link}) for what changed.\n\n"
    )
    title, sep, body = markdown.partition("\n")
    if title.startswith("# "):  # keep the page title first
        return f"{title}\n\n{banner}{body}"
    return banner + markdown
