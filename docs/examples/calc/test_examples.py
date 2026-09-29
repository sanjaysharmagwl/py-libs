"""Run every documentation example, so a change that breaks the docs also breaks ``make test``."""

import ast
import runpy
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from typing import Any

import pytest

HERE = Path(__file__).resolve().parent
SCRIPTS = sorted(p.name for p in HERE.glob("[0-9][0-9]_*.py"))


@pytest.mark.parametrize("script", SCRIPTS)
def test_example_runs(
    script: str, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.syspath_prepend(str(HERE))
    runpy.run_path(str(HERE / script), run_name="__main__")
    assert capsys.readouterr().out.strip(), f"{script} printed nothing"


def _load_book() -> Any:
    spec = spec_from_file_location("docs_book", HERE / "book.py")
    assert spec is not None and spec.loader is not None
    book = module_from_spec(spec)
    spec.loader.exec_module(book)
    return book


def test_requests_are_literals() -> None:
    book = _load_book()
    for script in SCRIPTS:
        if "REQUEST =" in (HERE / script).read_text():
            assert book.request_of(script)["dataset"] == "holdings"


def _requests() -> list[tuple[str, str]]:
    """Every top-level ``*REQUEST = {...}`` literal in the example scripts."""
    found = []
    for script in SCRIPTS:
        for node in ast.parse((HERE / script).read_text()).body:
            if isinstance(node, ast.Assign) and isinstance(node.value, ast.Dict):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id.endswith("REQUEST"):
                        found.append((script, target.id))
    return found


@pytest.fixture(scope="module")
def demo_engine() -> Any:
    """The demo service's engine, over a small synthetic fund (ROWS is read at import)."""
    app_path = HERE.parents[2] / "packages" / "calc_whatif" / "examples" / "app.py"
    spec = spec_from_file_location("demo_app", app_path)
    assert spec is not None and spec.loader is not None
    app = module_from_spec(spec)
    with pytest.MonkeyPatch.context() as mp:
        mp.setenv("ROWS", "50")
        mp.delenv("REDIS_URL", raising=False)
        spec.loader.exec_module(app)
    return app.engine


@pytest.mark.parametrize(("script", "name"), _requests())
def test_requests_run_against_the_demo(demo_engine: Any, script: str, name: str) -> None:
    """The docs show these requests as curl calls to the demo, so its data must fit them."""
    request = _load_book().request_of(script, name)
    if set(request.get("extensions", {})) - {"whatif"}:
        pytest.skip("needs a plugin the demo doesn't install")
    demo_engine.run(request)


def test_golden_cases(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.syspath_prepend(str(HERE))
    golden = runpy.run_path(str(HERE / "golden.py"))
    failures = [case["id"] for case, ok, _ in golden["check"]() if not ok]
    assert not failures, f"golden cases changed: {failures} (see docs/calc/qa/golden-cases.md)"
