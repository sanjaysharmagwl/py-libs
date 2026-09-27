# Install

`pylibs-calc` needs **Python 3.10 or later**. It installs Polars and pydantic, and nothing else, unless you ask for an extra.

=== "pip"

    ```bash
    pip install pylibs-calc              # the engine only
    pip install "pylibs-calc[fastapi]"   # + the FastAPI router
    pip install "pylibs-calc[redis]"     # + the Redis scenario store
    ```

=== "uv"

    ```bash
    uv add pylibs-calc
    uv add "pylibs-calc[fastapi,redis]"
    ```

| Extra | Adds | Needed for |
| --- | --- | --- |
| *(none)* | `polars`, `pydantic` | Everything in [Scenarios by feature](../scenarios/index.md) |
| `fastapi` | `fastapi` | [`create_router`](../integrations/fastapi.md) |
| `redis` | `redis` | [`RedisScenarioStore`](../integrations/redis.md) |

Importing `pylibs_calc` never imports an extra. Only the modules that need one do, and they raise an `ImportError` that names the missing extra.

## Working on the library itself

To try the examples in these docs, or to contribute, clone the repository and install the whole workspace:

```bash
git clone https://github.com/sanjaysharmagwl/py-libs.git
cd py-libs
make install          # every package, every extra, the dev tools and the git hooks
make test PKG=calc    # the calc test suite, including the property tests
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
