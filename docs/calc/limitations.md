# Assumptions and limitations

This page is written in the spirit of model documentation, as investment risk and model validation teams expect for any calculation that feeds an investment decision. It says what the engine assumes, and what it deliberately doesn't do yet.

## Assumptions

- **The input data is correct.** The engine checks types and keys, not business validity (for example, that a price is positive).
- **Numbers.** Decimal columns are exact at their registered scale. Results are rounded half-to-even at the scales described in [Numbers, types and nulls](concepts/numbers-types-nulls.md). Float columns follow IEEE-754, and float sums are only reproducible bit for bit with `deterministic: true`.
- **Nulls** follow SQL semantics everywhere. Invalid arithmetic (`x / 0`, `sqrt(-1)`, `log(0)`) gives null.
- **What-if scenarios** change values, never which rows exist. A shock applies the same factor to every matching row; there are no path-dependent or cross-row calculations.
- **Weights** come from `total()`, the grand total of the rows a query sees. Filters and entitlements change it; `having`, subtotals, pivots and pages don't. See [Weights and active weights](scenarios/weights.md).
- **Currencies.** Each row carries one FX rate into the base currency, as a column the data provides. There are no forward rates or hedges; a currency move is a shock on that column.
- **Plugins** are trusted code running in your process. The engine checks the names they register and runs their transforms after the caller's entitlements, but it can't check that a plugin's Polars and reference implementations agree; test them with `pylibs_calc.testing` and `verify()`.
- **Versions.** A result is reproducible when the dataset version and the scenario version are both pinned, on the same library versions (`meta.versions`).
- **Entitlements** are only as good as the `CalcContext` the host builds. The engine enforces the context; it doesn't authenticate anyone.

## Not supported yet

- median, quantiles, standard deviation as built-in measures (a plugin can add them with an `AggregateDef`)
- a share of a parent level (a stock's weight within its sector): `total()` is always the grand total
- the `//` and `%` operators
- comparing more than two sides at once
- pivots in compare, and `having` together with `pivot`
- spreading an edit on a group row down to its leaf rows
- moving a scenario onto a newer dataset version
- AG Grid's advanced filter model
- sorting rollups by a measure

## Out of scope

- **Pricing models.** Shocks move inputs such as prices, yields, FX rates and quantities. The engine doesn't reprice instruments from curves or volatilities (a yield shock doesn't move a bond's price); feed it prices from your pricing library.
- **Performance and risk analytics.** There are no time series: no returns over a period, no performance attribution (for example Brinson), no tracking error and no factor risk model. The engine computes holdings and what-ifs at one point in time; feed those analytics from your performance and risk systems.
- **Benchmark data.** The examples hold the benchmark as a notional portfolio of units next to the fund (`bench_quantity`). Index constituents and weights come from your index provider; loading them is the host's job, as is looking through fund-of-fund holdings.
- **Persistence of datasets.** The catalog holds what you register. Loading and refreshing data is the host's job.
