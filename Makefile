# Usage: make <target> [PKG=<package-dir>] [PART=patch|minor|major]
# PKG is the folder name under packages/ (e.g. PKG=core -> distribution pylibs-core).
PREFIX ?= pylibs
PART ?= patch
DIST := $(PREFIX)-$(PKG)

.PHONY: help install lint fmt typecheck test check build build-all bump new clean

help:
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-10s %s\n",$$1,$$2}'

install: ## Sync all workspace packages + dev tools, install git hooks
	uv sync --all-packages
	uv run pre-commit install

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
	uv sync --all-packages

clean: ## Remove build artifacts and caches
	rm -rf dist .pytest_cache .mypy_cache .ruff_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
