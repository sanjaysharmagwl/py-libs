# py-libs

A [uv](https://docs.astral.sh/uv/) workspace monorepo for building and publishing multiple
Python packages, each versioned and released independently to PyPI.

| Package | Path | Description |
| --- | --- | --- |
| [`pylibs-core`](packages/core) | `packages/core` | Core utilities shared across packages |
| [`pylibs-utils`](packages/utils) | `packages/utils` | Higher-level helpers (depends on `pylibs-core`) |
| [`pylibs-calc`](packages/calc) | `packages/calc` | What-if calculation engine on Polars (optional `fastapi`, `redis` extras) |

## Layout

```
pyproject.toml          # workspace root: members, dev tools, ruff/mypy/pytest config
uv.lock                 # one lockfile for the whole workspace
Makefile                # common tasks (run `make help`)
scripts/release_info.py # maps a release tag to its package and checks the version
.github/workflows/      # ci.yml (lint/test/build), release.yml (tag -> PyPI)
packages/<name>/        # one distributable package per folder
  pyproject.toml
  src/pylibs_<name>/
  tests/
```

Every folder in `packages/` is picked up by the workspace glob automatically. Packages in the
repo depend on each other through `[tool.uv.sources] <dep> = { workspace = true }`: locally
they're editable installs, and the published wheel lists a normal version requirement.

## Development

Requires [uv](https://docs.astral.sh/uv/getting-started/installation/).

```bash
make install      # uv sync --all-packages --all-extras + install pre-commit hooks
make check        # lint + typecheck + test
make test PKG=core
make fmt
```

### Adding a package

```bash
make new PKG=foo  # creates packages/foo -> distribution pylibs-foo, import pylibs_foo
```

To depend on another package in the workspace, add it to `dependencies` and to `[tool.uv.sources]`
(see [packages/utils/pyproject.toml](packages/utils/pyproject.toml)).

### Building

```bash
make build PKG=core   # dist/pylibs_core-*.whl + sdist
make build-all
```

## Releasing

Each package is released on its own by pushing a tag named `<package-dir>/v<version>`:

```bash
make bump PKG=core PART=minor          # updates packages/core/pyproject.toml
git commit -am "core: release 0.2.0"
git tag core/v0.2.0
git push origin master core/v0.2.0
```

[release.yml](.github/workflows/release.yml) then:

1. checks that the tag version matches the package's `pyproject.toml`,
2. tests and builds that package only,
3. publishes to **TestPyPI**, then **PyPI**, using Trusted Publishing (no API tokens),
4. creates a GitHub Release with the built files attached.

### One-time setup

1. In GitHub, go to **Settings → Environments** and create `testpypi` and `pypi`. Adding required
   reviewers to `pypi` makes every production publish wait for manual approval.
2. For **each package**, add a *pending trusted publisher* on both
   [PyPI](https://pypi.org/manage/account/publishing/) and
   [TestPyPI](https://test.pypi.org/manage/account/publishing/):
   - PyPI project name: e.g. `pylibs-core`
   - Owner: `sanjaysharmagwl`, Repository: `py-libs`
   - Workflow: `release.yml`
   - Environment: `pypi` (on PyPI) / `testpypi` (on TestPyPI)

## License

[Apache-2.0](LICENSE)
