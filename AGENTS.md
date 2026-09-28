# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Cursor, Copilot, Gemini CLI, etc.) working in this
repository. This is the single source of truth; `CLAUDE.md` imports it and Gemini CLI is pointed at
it via `.gemini/settings.json`.

## What this is

A uv workspace monorepo of independently versioned Python packages published to PyPI. The root
`pyproject.toml` is a *virtual* workspace (not a package): it only holds workspace members
(`packages/*`), the shared `dev` dependency group, and ruff/mypy/pytest config. There is one
`uv.lock` for the whole workspace.

## Commands

All tooling runs through `uv`; the Makefile wraps the common tasks (`make help`).

```bash
make help                    # list every make target
make install                 # uv sync --all-packages --all-extras + pre-commit install (+ graphify hooks)
make check                   # lint + typecheck + test (what CI runs)
make lint / make fmt         # ruff check + ruff format (--check vs. fix)
make typecheck               # mypy --strict over packages/*/src
make test                    # all tests
make test PKG=core           # one package's tests
uv run pytest packages/core/tests/test_text.py::test_name   # single test
make build PKG=core          # wheel + sdist into dist/
make new PKG=foo             # scaffold packages/foo -> dist pylibs-foo, import pylibs_foo
make bump PKG=core PART=minor
make graph                   # rebuild the code knowledge graph (graphify-out/), then docs-sync
make docs-serve              # preview the docs site (MkDocs Material) at http://127.0.0.1:8000
make docs-build              # strict docs build: broken links or failing examples are errors
make docs-sync / docs-check  # regenerate / verify the docs pages generated from graph.json
```

`PKG` is always the folder name under `packages/`; the distribution name is `pylibs-<PKG>` and the
import name is `pylibs_<PKG>`.

## Code knowledge graph (graphify)

`graphify-out/` holds a [graphify](https://github.com/safishamsi/graphify) knowledge graph of the
code (functions, imports, calls, cross-package edges). Use it to find code instead of reading or
grepping whole packages:

- For codebase questions, first run `graphify query "<question>"`. Use `graphify path "<A>" "<B>"`
  for relationships and `graphify explain "<concept>"` for one concept. These return a scoped
  subgraph, usually much smaller than `GRAPH_REPORT.md` or raw grep output.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when query/path/explain
  don't surface enough.
- The graph is code-only (tree-sitter AST, no LLM calls). After changing code, run `make graph`
  (`graphify update .`); add `--force` after refactors that delete code. The post-commit hook also
  rebuilds it, leaving `graph.json` modified to commit along with your next change.
- Only `graph.json` and `GRAPH_REPORT.md` are committed; everything else under `graphify-out/` is
  local. `graph.json` has a union merge driver (set up by `graphify hook install`).
- Setup for a fresh clone: `uv tool install graphifyy`, `graphify install` (Claude Code skill), then
  `make install` (installs the graphify git hooks).

## Documentation

`docs/` is an MkDocs Material site (`mkdocs.yml` at the root, deps in the `docs` dependency group,
local only for now). `docs/contributing.md` is the full guide; the rules that matter:

- **Examples run.** Scenario pages include `docs/examples/calc/NN_*.py` via snippets and execute
  them with markdown-exec, so result tables are real. The scripts share `book.py` (a twelve-row
  position book) and run under pytest (`docs/examples` is in `testpaths`), as do the QA golden
  cases (`golden.py`; re-record with `--update` only for intended behaviour changes).
- **Graph sync.** `scripts/docs_from_graph.py` reads `graphify-out/graph.json` and writes
  `docs/calc/reference/generated/` (never edit by hand). Hand-written pages list the source files
  they explain in `covers:` front matter; when a covered file's public surface changes in the
  graph, the page is flagged in `stale.md` and gets a banner. After reviewing (and updating) the
  page run `uv run python scripts/docs_from_graph.py --ack docs/<page>` and commit
  `docs/.docs-sync.json`. A pre-commit hook re-syncs when `graph.json` is staged; CI runs
  `--check` and `mkdocs build --strict`.
- **When you change calc behaviour**, update the scenario page and example for it, and keep
  every name in `pylibs_calc.__all__` and `pylibs_calc_whatif.__all__` mentioned on some page
  (`stale.md` lists misses). The docs sync covers both packages (`SOURCES` in the script).
- Markdown is excluded from `ruff format` (it would rewrite `--8<--` snippet markers).
- MkDocs is pinned `<2`: MkDocs 2.0 drops the plugin system these docs rely on.

## Architecture and conventions

- **Package layout**: each `packages/<name>/` has its own `pyproject.toml` (hatchling backend),
  `src/pylibs_<name>/` (with a `py.typed` marker) and `tests/`. Every directory under `packages/`
  is automatically a workspace member.
- **Inter-package dependencies**: list the dependency normally in `dependencies`
  (e.g. `pylibs-core>=0.1.0`) *and* add `[tool.uv.sources] pylibs-core = { workspace = true }`.
  Locally it resolves as an editable install; the published wheel keeps the version requirement.
  See `packages/utils/pyproject.toml`. `pylibs-utils` depends on `pylibs-core`.
- **Python versions**: packages target `>=3.10` (ruff `py310`, mypy `3.10`, CI tests 3.10–3.13),
  but the dev interpreter (`.python-version`) and `scripts/` use 3.12 — `tomllib` is treated as
  stdlib for that reason. Don't use >3.10 syntax/stdlib in package sources.
- **Typing**: mypy runs in `strict` mode on package sources.
- **Tests**: pytest uses `--import-mode=importlib`, so test files have no `__init__.py` and
  basenames need not be unique across packages.
- **Lint**: ruff, line length 100, rules `E,F,I,UP,B,SIM`; `pylibs_*` is first-party for isort.
  `ruff format` also formats Python code blocks in Markdown files. `graphify-out/` is excluded.
  Pre-commit also runs `uv-lock`, so `uv.lock` must stay in sync (CI uses `--locked`).
- **Optional extras**: packages may declare `[project.optional-dependencies]` (e.g. `pylibs-calc`'s
  `fastapi` and `testing`, `pylibs-calc-whatif`'s `redis`). CI, release and `make install` sync with `--all-extras`, so mypy and the
  tests always see them; keep extras out of a package's top-level import path (a subprocess test
  in `packages/calc/tests/test_runtime.py` guards this) and raise an `ImportError` naming the
  extra when one is missing. mypy runs with the `pydantic.mypy` plugin.
- **`pylibs-calc` specifics**: a *core engine* plus *plugins*. The core (`packages/calc`) knows
  nothing about what-if; `pylibs-calc-whatif` (`packages/calc_whatif`) is a plugin that uses only
  the public API: `pylibs_calc`, `pylibs_calc.ext`, `pylibs_calc.integrations.fastapi` (and
  `pylibs_calc.testing` in tests). `packages/calc_whatif/tests/test_plugin.py` enforces that
  boundary in both directions; new plugin needs go into `pylibs_calc.ext`/the plugin API
  (`plugins.py`: functions, aggregates, transforms, operations, routes), not into private imports.
  Every calculation is executed twice: by Polars and by the pure-Python reference
  (`verify/reference.py`, and each plugin's `apply_reference`/`reference`). Any change to
  semantics must update both; `test_property.py` in each package fuzzes them against each other
  with `pylibs_calc.testing`. Requests are versioned (`spec_version`, currently 2): an
  incompatible spec change needs an upgrader in `spec/canonical.py` and must keep old requests'
  results and fingerprints. Don't add `from __future__ import annotations` to
  `integrations/fastapi.py` or a plugin's routes module (FastAPI needs the route annotations as
  real objects).
- **Ruff version**: pinned exactly (`ruff==X.Y.Z`) in the root `dev` group, and the
  `astral-sh/ruff-pre-commit` `rev` in `.pre-commit-config.yaml` must be `vX.Y.Z`, so pre-commit,
  `make lint` and CI all run the same ruff. To upgrade, change both, run `uv lock`, then
  `uv run pre-commit run --all-files` and `make check`.

## Releasing

Each package is released independently by pushing a tag `<package-dir>/v<version>`
(e.g. `core/v0.2.0`). `.github/workflows/release.yml` runs `scripts/release_info.py`, which maps the
tag to the package and fails if the tag version doesn't match that package's `pyproject.toml`
version — so bump with `make bump` and commit before tagging. It then tests/builds only that package
and publishes to TestPyPI, then PyPI, via Trusted Publishing (no API tokens), and creates a GitHub
Release. The default branch is `master`.
