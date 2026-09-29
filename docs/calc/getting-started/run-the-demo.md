# Run the demo grid

The repository includes a small service: `pylibs-calc` with the [what-if plugin](../whatif/index.md) behind FastAPI, and an AG Grid page on top. It is the quickest way for **portfolio managers, analysts and QA** to see the engine working, with no code to write.

## Start it

```bash
make install
uv run --with uvicorn uvicorn --app-dir packages/calc_whatif/examples app:app --port 8000
```

Open <http://localhost:8000>.

| Environment variable | Default | Effect |
| --- | --- | --- |
| `ROWS` | `200000` | Number of holdings in the generated fund |
| `REDIS_URL` | *(unset)* | Keep scenarios in Redis instead of process memory |
| `POLARS_MAX_THREADS` | all cores | Polars threads (set it **before** starting) |

The data is a deterministic synthetic fund, registered as `holdings`, with the same columns as the [example fund](../scenarios/index.md#the-example-fund): `security_id`, `security`, `asset_class`, `sector`, `country`, `region`, `currency`, `fx_rate`, `rating`, `price`, `quantity`, `bench_quantity`, `yield`, `duration`, `analyst` and `target_price`. So every **JSON (curl)** tab in these docs works against it (a test checks this).

## Things to try

1. **Group and pivot.** Drag `asset_class` and `sector` to the row groups, and turn on pivot mode with `currency`. The server computes every group; the browser never holds the 200,000 rows.
2. **Edit a price.** Double-click a `price` cell and type a new value. The edit is saved as an [override](../scenarios/override.md) in a new scenario, and every subtotal is recomputed.
3. **Shock.** Click **Shock IT stocks −10%**, which appends a [shock](../scenarios/shock.md) step to the scenario.
4. **Compare.** The table under the grid shows the scenario against the base data, per sector: the fund's value and its [weight](../scenarios/weights.md) before and after. See [Compare two sides](../scenarios/compare.md).
5. **Switch views.** **View base data** toggles between the scenario and the untouched data.
6. **Explore the API.** FastAPI's interactive docs are at <http://localhost:8000/docs>. Every route can be tried from the browser.

!!! note "AG Grid Enterprise"
    The server-side row model is an AG Grid Enterprise feature. The demo loads it from a CDN, so without a licence key it shows a watermark. That is fine for evaluation.
