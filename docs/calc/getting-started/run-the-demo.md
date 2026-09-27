# Run the demo grid

The repository includes a small service: `pylibs-calc` behind FastAPI, with an AG Grid page on top. It is the quickest way for **business users and QA** to see the engine working, with no code to write.

## Start it

```bash
make install
uv run --with uvicorn uvicorn --app-dir packages/calc/examples app:app --port 8000
```

Open <http://localhost:8000>.

| Environment variable | Default | Effect |
| --- | --- | --- |
| `ROWS` | `200000` | Size of the generated book of positions |
| `REDIS_URL` | *(unset)* | Keep scenarios in Redis instead of process memory |
| `POLARS_MAX_THREADS` | all cores | Polars threads (set it **before** starting) |

The data is a deterministic synthetic book with the columns `position_id`, `desk`, `sector`, `region`, `rating`, `price`, `quantity` and `yield`. These are the same columns as the [example book](../scenarios/index.md#the-example-book), so every **JSON (curl)** tab in these docs works against it.

## Things to try

1. **Group and pivot.** Drag `desk` and `sector` to the row groups, and turn on pivot mode with `region`. The server computes every group; the browser never holds the 200,000 rows.
2. **Edit a price.** Double-click a `price` cell and type a new value. The edit is saved as an [override](../scenarios/override.md) in a new scenario, and every subtotal is recomputed.
3. **Shock.** Click **Shock Tech price +5%**, which appends a [shock](../scenarios/shock.md) step to the scenario.
4. **Compare.** The table under the grid shows the scenario against the base data, per desk. See [Compare two sides](../scenarios/compare.md).
5. **Switch views.** **View base data** toggles between the scenario and the untouched data.
6. **Explore the API.** FastAPI's interactive docs are at <http://localhost:8000/docs>. Every route can be tried from the browser.

!!! note "AG Grid Enterprise"
    The server-side row model is an AG Grid Enterprise feature. The demo loads it from a CDN, so without a licence key it shows a watermark. That is fine for evaluation.
