# Glossary

Short definitions. New to finance? The [Finance primer](getting-started/finance-primer.md) explains these terms with worked examples.

Finance terms
:   **Position**: one row of the book: a quantity of one instrument held by one desk.
:   **Book**: the full set of positions.
:   **Desk**: the trading team that owns a position (Rates, Credit, Equities, FX, Commodities).
:   **Notional**: the size of a position in money, here `price × quantity`.
:   **Mark**: the current price used to value a position. A trader who "corrects a mark" makes an [override](scenarios/override.md).
:   **Long / short**: a positive / negative quantity.
:   **Gross / net**: the sum of absolute exposures / the signed sum.
:   **Basis point (bp)**: 0.01%. "+25bp on yields" is an `add` shock of `0.0025`.
:   **Shock**: a hypothetical bulk move in a market variable. See [Shock a column](scenarios/shock.md).
:   **Weighted average yield**: yields averaged by position size, `wavg` in this engine.
:   **P&L impact**: the change in value between a scenario and the base: `m__delta` in [compare](scenarios/compare.md).

Engine terms
:   **Dataset**: a registered table with an immutable **version**. See [Datasets](concepts/datasets.md).
:   **Key columns**: the columns that identify a row, such as `position_id`.
:   **Scenario**: a saved, append-only log of steps over one dataset version.
:   **Step**: an override, shock, formula or disable.
:   **What-if**: steps sent with one request instead of saved.
:   **Side**: a dataset version with a scenario and what-ifs applied, as one caller sees it. Compare has two sides.
:   **Row view / aggregated view**: a query without / with `group_by` or measures.
:   **Measure**: an aggregate computed per group.
:   **Post expression**: a value computed from measures after aggregation, such as a ratio.
:   **Rollup**: subtotal rows for every level of `group_by`. `__level` 0 is the grand total.
:   **Fingerprint**: a SHA-256 of the fully resolved request. The same fingerprint means the same answer.
:   **Reference evaluator**: an independent, pure-Python implementation used to check the engine.
:   **Context**: `CalcContext`, meaning who is asking and what they may see.
:   **Fork**: a new scenario that starts from a copy of another one's steps.
