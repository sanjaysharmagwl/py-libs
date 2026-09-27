# Testing guide

This page is for **QA engineers** testing `pylibs-calc` itself, or a service built on it.

## What to test, and how

| Layer | Tool | Where |
| --- | --- | --- |
| Business rules (nulls, rounding, ratios) | [Golden cases](golden-cases.md) | `docs/examples/calc/golden.py` |
| Every documented example | The docs build and `make test` | `docs/examples/calc/test_examples.py` |
| Engine vs an independent implementation | `verify(engine, request)` | [Audit a number](../scenarios/audit.md) |
| Randomized edge cases | Hypothesis property tests | `packages/calc/tests/test_property.py` |
| HTTP contract | FastAPI test client | `packages/calc/tests/test_fastapi.py` |
| Scenario concurrency and retries | Unit tests with a fake Redis | `packages/calc/tests/test_scenarios.py` |

```bash
make test PKG=calc                              # the library's test suite
uv run python docs/examples/calc/golden.py      # the golden cases, PASS/FAIL per case
uv run pytest docs/examples                     # every docs example
```

## Test a service built on the engine

1. **Check a result against the reference evaluator.** For any request your service sends, `verify()` recomputes the answer without Polars:

    ```python
    from pylibs_calc.verify import verify

    report = verify(engine, request, ctx=ctx)
    assert report.ok, report.problems
    ```

2. **Use the fingerprint as a regression key.** Store `meta.fingerprint` together with the expected result. The same fingerprint on the same library versions must give the same numbers. If the numbers change while the fingerprint stays the same, that is a bug.
3. **Test entitlements through the context.** Build the `CalcContext` your resolver would build for a restricted user, and assert that:
    - totals only include that user's rows
    - hidden columns are `unknown_column`
4. **Test the error contract.** Assert on `code` and `path`, never on `message`: codes are stable, messages may be reworded. See [Error codes](../reference/error-codes.md).
5. **Test concurrency.** Two appends at the same `expected_version` must give exactly one success and one `409`. A retry with the same `Idempotency-Key` must not append twice.

## Exploratory testing checklist

Try each of these against the [demo](../getting-started/run-the-demo.md) or your service:

- [ ] Nulls in every position: group values, measure inputs, filter columns and pivot values
- [ ] Empty results: a filter that matches nothing, with and without `group_by`
- [ ] Very large and very small decimals, and negative quantities
- [ ] Shocks with `where` conditions that are null for some rows
- [ ] An override on a key that doesn't exist (expect `422 unmatched_edits`)
- [ ] Paging past the end, `limit: 0`, and `offset` beyond `total_rows`
- [ ] A pivot with a null value in the pivot column (it shows as `(blank)`)
- [ ] Rollup subtotals equal the sum of their details, for sums and counts
- [ ] Compare with no changes: every delta 0, every `__pct` 0 or null
- [ ] Two browser tabs editing the same scenario (expect a `409` in one of them)
