# Usage: make <target> [PKG=<package-dir>] [PART=patch|minor|major]
# PKG is the folder name under packages/ (e.g. PKG=core -> distribution pylibs-core).
PREFIX ?= pylibs
PART ?= patch
DIST := $(PREFIX)-$(PKG)

.PHONY: help install lint fmt typecheck test check build build-all bump new graph docs-serve docs-build docs-sync docs-check clean

help:
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-10s %s\n",$$1,$$2}'

install: ## Sync all workspace packages (with extras) + dev tools, install git hooks
	uv sync --all-packages --all-extras
	uv run pre-commit install
	@if command -v graphify >/dev/null; then graphify hook install; \
	else echo "graphify not found; skipping graph hooks (uv tool install graphifyy)"; fi

lint: ## Lint and check formatting
	uv run ruff check .
	uv run ruff format --check .

fmt: ## Auto-fix lint issues and format
	uv run ruff check --fix .
	uv run ruff format .

typecheck: ## Run mypy over all package sources
	uv run mypy packages/*/src

test: ## Run all tests (or one package's with PKG=core)
	uv run pytest $(if $(PKG),packages/$(PKG))

check: lint typecheck test ## lint + typecheck + test

build: ## Build one package: make build PKG=core
	@test -n "$(PKG)" || (echo "PKG is required, e.g. make build PKG=core" && exit 1)
	uv build --package $(DIST) -o dist/

build-all: ## Build every package into dist/
	uv build --all-packages -o dist/

bump: ## Bump a version: make bump PKG=core PART=minor
	@test -n "$(PKG)" || (echo "PKG is required, e.g. make bump PKG=core" && exit 1)
	uv version --package $(DIST) --bump $(PART)

new: ## Scaffold a new package: make new PKG=foo
	@test -n "$(PKG)" || (echo "PKG is required, e.g. make new PKG=foo" && exit 1)
	@test ! -e packages/$(PKG) || (echo "packages/$(PKG) already exists" && exit 1)
	uv init --lib --build-backend hatch --name $(DIST) --no-workspace --no-pin-python --vcs none packages/$(PKG)
	sed -i.bak -e 's/^requires-python = .*/requires-python = ">=3.10"/' \
		-e 's/^readme = "README.md"/&\nlicense = "Apache-2.0"/' packages/$(PKG)/pyproject.toml
	rm packages/$(PKG)/pyproject.toml.bak
	mkdir -p packages/$(PKG)/tests
	uv sync --all-packages --all-extras

graph: ## Rebuild the code knowledge graph in graphify-out/ (AST only), then sync the docs
	graphify update .
	$(MAKE) docs-sync

docs-serve: ## Preview the docs site at http://127.0.0.1:8000 (reloads on edit)
	uv run --group docs mkdocs serve

docs-build: ## Build the docs site into site/ (strict: warnings and failing examples are errors)
	uv run --group docs mkdocs build --strict

docs-sync: ## Regenerate the docs pages built from graphify-out/graph.json
	uv run python scripts/docs_from_graph.py

docs-check: ## Fail if the generated docs pages are out of date with graph.json
	uv run python scripts/docs_from_graph.py --check

clean: ## Remove build artifacts and caches
	rm -rf dist site .pytest_cache .mypy_cache .ruff_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
