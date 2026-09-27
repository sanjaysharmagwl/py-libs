"""Run every documentation example, so a change that breaks the docs also breaks ``make test``."""

import runpy
from pathlib import Path

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


def test_requests_are_literals() -> None:
    from importlib.util import module_from_spec, spec_from_file_location

    spec = spec_from_file_location("docs_book", HERE / "book.py")
    assert spec is not None and spec.loader is not None
    book = module_from_spec(spec)
    spec.loader.exec_module(book)
    for script in SCRIPTS:
        if "REQUEST =" in (HERE / script).read_text():
            assert book.request_of(script)["dataset"] == "positions"


def test_golden_cases(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.syspath_prepend(str(HERE))
    golden = runpy.run_path(str(HERE / "golden.py"))
    failures = [case["id"] for case, ok, _ in golden["check"]() if not ok]
    assert not failures, f"golden cases changed: {failures} (see docs/calc/qa/golden-cases.md)"
