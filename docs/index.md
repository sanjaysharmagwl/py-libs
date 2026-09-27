# py-libs

A monorepo of independently versioned Python packages, published to PyPI.

| Package | What it is | Docs |
| --- | --- | --- |
| **`pylibs-calc`** | An embeddable what-if calculation engine on Polars, for finance grids | [pylibs-calc](calc/index.md) |
| `pylibs-core` | Small core utilities shared across packages | [pylibs-core](packages/core.md) |
| `pylibs-utils` | Higher-level helpers built on `pylibs-core` | [pylibs-utils](packages/utils.md) |

## How these docs are organized

The pages follow the [Diátaxis](https://diataxis.fr/) framework:

| You want to… | Read |
| --- | --- |
| **learn** by doing | *Getting started* and *Scenarios by feature*: every example runs when the site is built, so the outputs shown are real |
| **solve** a specific problem | *Integrations*, *Operations* and *QA* |
| **look up** a detail | *Reference*: the API from docstrings, the request schema from the pydantic models, error codes found by scanning the source, and a component map from the code knowledge graph |
| **understand** why | *Concepts*, and *Assumptions and limitations* |

The docs are kept in step with the code. When the code changes, the [components page](calc/reference/generated/components.md) is regenerated from the code knowledge graph, and any page whose code has moved on is flagged in [Docs freshness](calc/reference/generated/stale.md). See [Contributing to the docs](contributing.md).
