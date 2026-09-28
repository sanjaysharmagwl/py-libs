# Install

`pylibs-calc` needs **Python 3.10 or later**. It installs Polars and pydantic, and nothing else, unless you ask for an extra. Analyses built on top of the engine are separate [plugin](../concepts/plugins.md) packages; what-if analysis is `pylibs-calc-whatif`.

=== "pip"

    ```bash
    pip install pylibs-calc                     # the core engine only
    pip install "pylibs-calc[fastapi]"          # + the FastAPI router
    pip install pylibs-calc-whatif              # + the what-if plugin
    pip install "pylibs-calc-whatif[redis]"     # + its Redis scenario store
    ```

=== "uv"

    ```bash
    uv add pylibs-calc
    uv add "pylibs-calc[fastapi]" "pylibs-calc-whatif[redis]"
    ```

| Package and extra | Adds | Needed for |
| --- | --- | --- |
| `pylibs-calc` | `polars`, `pydantic` | The [core features](../scenarios/index.md#core-engine) and the [plugin API](../concepts/plugins.md) |
| `pylibs-calc[fastapi]` | `fastapi` | [`create_router`](../integrations/fastapi.md) |
| `pylibs-calc[testing]` | `hypothesis` | `pylibs_calc.testing`, for [fuzzing a plugin](../extending/write-a-plugin.md#test-it-against-the-reference) |
| `pylibs-calc-whatif` | `pylibs-calc` | The [what-if features](../scenarios/index.md#what-if-plugin) |
| `pylibs-calc-whatif[redis]` | `redis` | [`RedisScenarioStore`](../integrations/redis.md) |

Importing `pylibs_calc` (or `pylibs_calc_whatif`) never imports an extra. Only the modules that need one do, and they raise an `ImportError` that names the missing extra.

## Working on the library itself

To try the examples in these docs, or to contribute, clone the repository and install the whole workspace:

```bash
git clone https://github.com/sanjaysharmagwl/py-libs.git
cd py-libs
make install          # every package, every extra, the dev tools and the git hooks
make test PKG=calc    # the core test suite, including the property tests
make test PKG=calc_whatif  # the what-if plugin's tests
uv run python docs/examples/calc/00_quickstart.py
```

To browse these docs locally:

```bash
make docs-serve       # http://127.0.0.1:8000, reloads when you edit a page
```

## Check the runtime

Polars sizes its thread pool when it is first imported. Call `runtime_check()` at startup to catch a thread count that doesn't match the container's CPU limit:

```python
from pylibs_calc import runtime_check

report = runtime_check()  # a RuntimeReport; warns if POLARS_MAX_THREADS doesn't match the CPU limit
```

See [Deploying on Kubernetes](../operations/kubernetes.md).
