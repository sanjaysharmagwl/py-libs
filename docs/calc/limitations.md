# Assumptions and limitations

This page is written in the spirit of model documentation, as risk teams expect for any calculation that feeds a decision. It says what the engine assumes, and what it deliberately doesn't do yet.

## Assumptions

- **The input data is correct.** The engine checks types and keys, not business validity (for example, that a price is positive).
- **Numbers.** Decimal columns are exact at their registered scale. Results are rounded half-to-even at the scales described in [Numbers, types and nulls](concepts/numbers-types-nulls.md). Float columns follow IEEE-754, and float sums are only reproducible bit for bit with `deterministic: true`.
- **Nulls** follow SQL semantics everywhere. Invalid arithmetic (`x / 0`, `sqrt(-1)`, `log(0)`) gives null.
- **Scenarios** change values, never which rows exist. A shock applies the same factor to every matching row; there are no path-dependent or cross-row calculations.
- **Versions.** A result is reproducible when the dataset version and the scenario version are both pinned, on the same library versions (`meta.versions`).
- **Entitlements** are only as good as the `CalcContext` the host builds. The engine enforces the context; it doesn't authenticate anyone.

## Not supported yet

- median, quantiles, standard deviation
- the `//` and `%` operators
- comparing more than two sides at once
- pivots in compare, and `having` together with `pivot`
- spreading an edit on a group row down to its leaf rows
- moving a scenario onto a newer dataset version
- AG Grid's advanced filter model
- sorting rollups by a measure

## Out of scope

- **Pricing models.** Shocks move inputs such as prices, yields and quantities. The engine doesn't reprice instruments from curves or volatilities; feed it prices from your pricing library.
- **Persistence of datasets.** The catalog holds what you register. Loading and refreshing data is the host's job.
