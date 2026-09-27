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
make install                 # uv sync --all-packages + pre-commit install
make check                   # lint + typecheck + test (what CI runs)
make lint / make fmt         # ruff check + ruff format (--check vs. fix)
make typecheck               # mypy --strict over packages/*/src
make test                    # all tests
make test PKG=core           # one package's tests
uv run pytest packages/core/tests/test_text.py::test_name   # single test
make build PKG=core          # wheel + sdist into dist/
make new PKG=foo             # scaffold packages/foo -> dist pylibs-foo, import pylibs_foo
make bump PKG=core PART=minor
```

`PKG` is always the folder name under `packages/`; the distribution name is `pylibs-<PKG>` and the
import name is `pylibs_<PKG>`.

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
  Pre-commit also runs `uv-lock`, so `uv.lock` must stay in sync (CI uses `--locked`).

## Releasing

Each package is released independently by pushing a tag `<package-dir>/v<version>`
(e.g. `core/v0.2.0`). `.github/workflows/release.yml` runs `scripts/release_info.py`, which maps the
tag to the package and fails if the tag version doesn't match that package's `pyproject.toml`
version — so bump with `make bump` and commit before tagging. It then tests/builds only that package
and publishes to TestPyPI, then PyPI, via Trusted Publishing (no API tokens), and creates a GitHub
Release. The default branch is `master`.
