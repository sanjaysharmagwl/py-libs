# Glossary

Short definitions. New to investing? The [Investment primer](getting-started/finance-primer.md) explains these terms with worked examples.

Investment terms
:   **Fund** (or **portfolio**): a pool of clients' money invested by a portfolio manager.
:   **Holding**: one row of a fund: a quantity of one security.
:   **Asset class**: equity (shares), fixed income (bonds) or cash.
:   **Market value**: what a holding is worth in the fund's base currency, here `price × quantity × fx_rate`.
:   **Base currency**: the currency a fund reports in (US dollars in the examples). `fx_rate` converts each security's own currency into it.
:   **NAV** (net asset value): the market value of the whole fund, `total(mv)`.
:   **Weight**: a holding's (or a sector's) share of the NAV. See [Weights and active weights](scenarios/weights.md).
:   **Benchmark**: the index a fund is measured against.
:   **Active weight**: the fund's weight minus the benchmark's weight. Positive is **overweight**, negative is **underweight**.
:   **Off-benchmark**: a holding the benchmark doesn't contain.
:   **Concentration limit**: a cap on how much of the fund one holding may be, for example 10%. See [Having](scenarios/having.md).
:   **Coverage**: the securities a research analyst follows.
:   **Target price**: where an equity analyst expects a share price to be; **upside to target** is `target_price / price − 1`.
:   **Duration**: how much a bond's price reacts to a change in yields, in years.
:   **Share class**: a version of a fund for a group of investors, often in another currency. See [Write a plugin](extending/write-a-plugin.md).
:   **Basis point (bp)**: 0.01%. "+25bp on yields" is an `add` shock of `0.0025`.
:   **Shock**: a hypothetical bulk move in a market variable. See [Shock a column](scenarios/shock.md).
:   **Stress test**: a set of large shocks that describes a crisis, such as "global recession".
:   **Weighted average yield**: yields averaged by market value, `wavg` in this engine.
:   **Impact**: the change in value between a scenario and the base: `m__delta` in [compare](scenarios/compare.md). The **relative** impact compares the fund's change with its benchmark's.

Engine terms
:   **Dataset**: a registered table with an immutable **version**. See [Datasets](concepts/datasets.md).
:   **Key columns**: the columns that identify a row, such as `security_id`.
:   **Scenario**: a saved, append-only log of steps over one dataset version.
:   **Step**: an override, shock, formula or disable.
:   **What-if**: steps sent with one request instead of saved, in its `extensions.whatif` block.
:   **Plugin**: a package that adds functions, aggregates, transforms, operations or routes to the core engine. What-if is one.
:   **Transform**: a plugin's change to the dataset before the query runs, switched on by a block under the request's `extensions`.
:   **Extensions**: the part of a request that holds one block per plugin transform, e.g. `{"whatif": {...}}`.
:   **Operation**: a new engine call added by a plugin, run with `engine.call(name, request)`.
:   **Side** (or **view**): a dataset version with the plugin transforms applied, as one caller sees it. Compare has two sides.
:   **Row view / aggregated view**: a query without / with `group_by` or measures.
:   **Measure**: an aggregate computed per group.
:   **Post expression**: a value computed from measures after aggregation, such as a ratio or a weight.
:   **`total(m)`**: measure `m` over every row the query sees, used in `post` and `having` for weights and shares.
:   **Rollup**: subtotal rows for every level of `group_by`. `__level` 0 is the grand total.
:   **Fingerprint**: a SHA-256 of the fully resolved request. The same fingerprint means the same answer.
:   **Reference evaluator**: an independent, pure-Python implementation used to check the engine.
:   **Context**: `CalcContext`, meaning who is asking and what they may see.
:   **Fork**: a new scenario that starts from a copy of another one's steps.
