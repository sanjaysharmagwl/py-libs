# Troubleshooting

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| `422 type_mismatch` on `price * yield` | A decimal column mixed with a float column | Cast one side: `float(price) * yield`, or `price * decimal(yield, 6)`. See [Numbers](../concepts/numbers-types-nulls.md) |
| `422 unknown_column` for a column that exists | Hidden by the caller's `allowed_columns`, or a formula column targeted by a shock or override | Check the caller's context. Edit a formula's inputs instead of the formula |
| `422 unmatched_edits` | An override's key matches no row | Fix the key, or set `"strict_edits": false` in the `whatif` block |
| `422 unknown_extension` / `unknown_function` / `unknown_aggregate` | The engine doesn't have the plugin that provides it | Install the plugin in the engine (`CalcEngine(..., plugins=[...])`) |
| `422 needs_rounding` | A fractional shock on an integer column | Add `"round": true` |
| `409 version_conflict` | Someone appended to the scenario first | Reload the scenario and retry with its new `version` |
| `413 limit_exceeded` | A page, group count, pivot or expression over a `Limits` cap | Add a `page`, filter more, or raise the limit |
| `503 engine_busy` | Every slot busy for `queue_timeout_s` | Scale out, or look for slow queries (`meta.timings_ms`) |
| `504 timeout` | The query ran past its timeout | Filter earlier, use Categorical dimensions, or raise `timeout_s` |
| A sum is null, not 0 | Nothing to sum: SQL semantics | `coalesce(m, 0)` in `post` |
| A ratio looks wrong at a subtotal | Averaging averages | Use `post` or `wavg`, which are ratios of sums at every level |
| Float totals differ in the last digit between runs | Parallel float addition | `"options": {"deterministic": true}`, or use Decimal |
| A saved scenario gives `dataset_not_found` after a refresh | Its pinned version was dropped from the catalog | Keep more versions (`Catalog(max_versions=...)`) |
| Warnings about threads at startup | `POLARS_MAX_THREADS` doesn't match the CPU limit | Set it in the container environment |

## Reporting a problem

Include:

- the request JSON
- `meta.fingerprint` and `meta.versions` from the response
- the error body, if there is one

Then run `verify(engine, request)` from `pylibs_calc.verify`. If it reports a difference, the engine and the reference evaluator disagree, and that is a bug in the library. See [Audit a number](../scenarios/audit.md).
