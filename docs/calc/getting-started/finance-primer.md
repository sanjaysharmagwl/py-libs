# Investment primer: start here

`pylibs-calc` is built for **portfolio managers** (fund managers), **research analysts**, and the
teams around them at an active asset manager: investment risk, investment compliance and client
reporting. The rest of these docs use their vocabulary: *holdings*, *NAV*, *weights*,
*benchmark*, *active weight*, *shocks*, *basis points*. If those words are new to you, read this page
first. It assumes no finance background and takes about fifteen minutes. Every number on it is
computed by the engine from the same example fund that the other pages use.

!!! abstract "The whole idea in one paragraph"
    An asset manager runs **funds**: pools of clients' money, each invested in shares, bonds and cash
    by a **portfolio manager** (PM). Each line of a fund is a **holding**, and the value of all of
    them together is the fund's **net asset value (NAV)**. Every fund is measured against a
    **benchmark**, an index it is trying to beat. What the PM actually decides is each holding's
    **weight**: its share of the NAV. The weight's difference from the benchmark's weight is the
    **active weight**, where the PM is **overweight** or **underweight**. Research **analysts**
    study companies and set **target prices** that feed those decisions. Every day people ask *"how
    is the fund positioned, by sector, country or currency, against its benchmark?"* and *"what
    happens to the fund, and to its lead over the benchmark, **if** markets move?"* A **shock** is
    one of those imagined market moves. `pylibs-calc` answers exactly these questions over a table
    of holdings.

## 1. The fund, column by column

The example is a fictional multi-asset **Global Income Fund**. It reports in US dollars, and its
benchmark is a notional blend of 60% global equities and 40% government bonds. Fund and benchmark
share one table, with one row per security that either of them holds:

```python exec="on"
from book import holdings, table

print(table(holdings()))
```

### What each column means

`security_id`
:   A unique number for the row. In the engine it is the **key column**: the thing that identifies a
    row when you edit it.

`security`
:   *What* is held. The fund has three **asset classes**:

    | Asset class | Examples in the fund | What it is |
    | --- | --- | --- |
    | **Equity** (shares) | `Wayne Financial`, `Cyberdyne Systems`, `Kaiju Motors` | Part-ownership of a company. |
    | **Fixed income** (bonds) | `UST 4.25% 2034` (US Treasury), `Bund 2.5% 2033` (German), `Gilt 4.0% 2031` (UK), `JGB 0.9% 2032` (Japanese) | A loan to a government. The name reads *issuer, coupon (yearly interest), year it is repaid*. |
    | | `ACME Corp 5.1% 2030`, `Globex 6.0% 2029` | The same, but lent to a company (**credit**), so riskier and higher-yielding. |
    | **Cash** | `USD Cash` | Money not invested yet, kept for redemptions and new ideas. |

    The company names are made up.

`asset_class`, `sector`, `country`, `region`
:   How the fund is sliced when a PM looks at it. Sectors follow the usual industry classification
    (Information Technology, Financials, Health Care, …), with `Government` for government bonds
    and `Cash` for cash. Regions are North America, UK, Europe ex UK and Japan.

`currency`, `fx_rate`
:   The currency the security is priced in, and what one unit of that currency is worth in US dollars
    (the fund's **base currency**): `1.27` for GBP, `0.0067` for JPY. Foreign holdings carry
    **currency risk**: if the dollar strengthens, they are worth fewer dollars.

`price`
:   What one unit is worth today, in its own currency. Shares are priced per share. Bonds are quoted
    per 100 of face value, so `98.50` means "98.5% of the amount repaid at maturity". The column is
    an exact decimal with 2 places, because money is not rounded casually.

`quantity`
:   How many units **the fund** holds: shares for equities, and 100s of face value for bonds. It is
    `0` for a security that only the benchmark holds. The fund doesn't own `Initech` or the `JGB`,
    so it is completely **underweight** them. Funds like this one are **long-only**: they never hold
    a negative quantity.

`bench_quantity`
:   How many units **the benchmark** would hold if it were a portfolio of about the same size as the
    fund. It is `0` for an **off-benchmark** holding, one the PM bought even though the index
    doesn't contain it, such as the two corporate bonds and the cash.

`rating`, `yield`, `duration`
:   For bonds only.
    - `rating` is a credit agency's grade for how likely the issuer is to repay, from best to worst
      `AAA`, `AA`, `A`, `BBB`, `BB`, … `BBB` and above is **investment grade**; below it is
      **high yield**.
    - `yield` is the yearly return you would earn by buying at today's price and holding to
      maturity, as a fraction: `0.0425` is 4.25%. **When yields rise, bond prices fall.**
    - `duration` (in years) measures how much a bond's price reacts to a change in yields: roughly
      *price change ≈ −duration × yield change*.

`analyst`, `target_price`
:   Research coverage. `analyst` is the analyst who covers the security: `ana` covers equities and
    `raj` covers credit. `target_price` is where the equity analyst expects the share price to be in
    a year. The **upside to target** (`target_price / price − 1`) is one input to the PM's decisions.

!!! note "Simplifications this example makes"
    Real portfolio systems hold benchmark **weights** from an index provider, account for accrued
    interest on bonds and hedge some of the currency risk. The example keeps everything as
    `price × quantity × fx_rate`, so you can follow the arithmetic by hand. The engine doesn't care
    what the numbers mean: it computes exactly what you ask for.

## 2. Numbers you compute from the holdings

**Market value** (in the base currency) is how much money a holding represents:
`price × quantity × fx_rate`. The fund's **NAV** is the sum of all its market values. A holding's
**weight** is its market value divided by the NAV. In the engine that division is
[`total()`](../scenarios/weights.md), which is the same measure over the whole fund:

```python exec="on"
from book import engine, table

result = engine().run(
    {
        "dataset": "holdings",
        "query": {
            "filter": "quantity > 0",
            "derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}],
            "group_by": ["security", "currency"],
            "measures": [{"name": "mv", "fn": "sum", "of": "mv"}],
            "post": [
                {"name": "nav", "expr": "total(mv)"},
                {"name": "weight_pct", "expr": "round(100 * mv / total(mv), 2)"},
            ],
            "sort": [{"by": "weight_pct", "desc": True}],
            "page": {"limit": 6},
        },
    }
)
print(table(result))
```

The same holding means two different things, depending on what you compare it with:

- **Weight** answers *"how much of the fund is in it?"* Wayne Financial is 11.5% of the fund.
- **Active weight** answers *"how different is the fund from its benchmark?"* It is the fund's
  weight minus the benchmark's weight. A positive active weight is an **overweight**, a bet that
  the holding will do better than the index. A negative one is an **underweight**. Managers are
  usually judged, and constrained, on active weights, not on weights.

```python exec="on"
from book import engine, request_of, table

print(table(engine().run(request_of("19_weights.py"))))
```

Read the last row: the benchmark has almost 31% in Information Technology and the fund has less
than 16%, so the fund is **15 points underweight tech**. If tech sells off, the fund loses less than
its benchmark; if tech rallies, it falls behind.

Other numbers you will meet:

- **Weighted average yield and duration**: the average across bonds, where bigger holdings count
  more. The engine calls this `wavg`; see [Measures](../scenarios/measures.md).
- **Upside to target** for a region or sector: total target value ÷ total value − 1. This is a
  **ratio of sums**, computed after adding up, not by averaging each stock's upside. See
  [Ratios after aggregation](../scenarios/post-ratios.md).
- **Subtotals**: a weight per asset class, then per sector inside it, then the whole fund, all in
  one grid. In the engine this is a [rollup](../scenarios/rollup.md).
- **Pivot**: a matrix, such as asset classes down the side and currencies across the top, to see
  currency exposure. See [Pivot](../scenarios/pivot.md).
- **Concentration and active-weight limits**: rules like "no single holding above 10% of the fund"
  or "no sector more than 5 points away from the benchmark". See [Having](../scenarios/having.md).

## 3. Asking "what if?"

This is the reason the engine exists. PMs and analysts rarely want only today's numbers; they want
to know what happens to them under a change.

**Base**
:   The fund as it really is, before any change. Every "what if" is measured against it.

**Override**
:   Changing **one cell**. An analyst who thinks the price of an illiquid bond is stale marks it
    down, or a PM tries "what if I bought 10,000 Initech?". See [Override a cell](../scenarios/override.md).

**Shock**
:   Changing **a whole column at once**, optionally only on some rows: "every tech stock −10%",
    "every bond yield +25bp", "the dollar +5%". A shock is an imagined market move. The engine has
    three kinds: `pct` (move by a percentage), `add` (add an amount) and `mul` (multiply). See
    [Shock a column](../scenarios/shock.md).

**Basis point (bp)**
:   One hundredth of a percent: 0.01%, or `0.0001` as a fraction. Yields move in small steps, so
    people say "+25bp" rather than "+0.25%". "Yields +25bp" is the shock
    `{"op": "add", "value": "0.0025"}` on the `yield` column.

**Stress test**
:   A large, deliberately painful set of shocks ("equities −20%, credit −5%, government bonds +3%")
    to see how the fund would behave in a crisis.

**Sensitivity**
:   A small shock (often +1bp or +1%) to measure how much the fund reacts to one market variable.

**Scenario**
:   A named, saved list of overrides and shocks (the engine calls each one a **step**). A PM can
    build "Global recession", share it with the risk team, come back to it tomorrow, or copy it
    (**fork** it) to try a variation. See [Saved scenarios and forks](../scenarios/saved-scenarios.md).

**Impact, and relative impact**
:   The **impact** of a scenario is how much the fund's value changes compared with the base. For
    an active manager, the **relative** impact, the fund against its benchmark, matters as much. A
    fund that falls 1% while its benchmark falls 3% has done its job. In the engine you get both
    from a [compare](../scenarios/compare.md), which adds `__base`, `__delta` and `__pct` columns
    next to every number.

Here is a what-if end to end: *"what if tech stocks fall 10%?"*

```python exec="on"
from book import engine, table

result = engine().compare(
    {
        "dataset": "holdings",
        "extensions": {
            "whatif": {
                "steps": [
                    {
                        "kind": "shock",
                        "column": "price",
                        "op": "pct",
                        "value": -10,
                        "where": "sector == 'Information Technology' and asset_class == 'Equity'",
                    }
                ]
            }
        },
        "query": {
            "derive": [
                {"name": "fund", "expr": "round(price * quantity * fx_rate, 2)"},
                {"name": "bench", "expr": "round(price * bench_quantity * fx_rate, 2)"},
            ],
            "measures": [
                {"name": "fund", "fn": "sum", "of": "fund"},
                {"name": "bench", "fn": "sum", "of": "bench"},
            ],
        },
    }
)
print(table(result))
```

How to read it:

- `fund` is the NAV **after** the shock, `fund__base` is the NAV **before** it, and `fund__delta`
  is the change in dollars.
- `fund__pct` is about −0.96%, and `bench__pct` is about −3.08%. The fund loses much less than its
  benchmark because it is underweight tech, so it **outperforms by about 2.1 points** in this
  scenario. This relative view is how a PM reads every stress test.

!!! warning "Shocks don't know finance"
    The engine moves exactly the column you shock. Shocking `yield` up does **not** lower bond
    prices by itself (duration would tell you by how much), and shocking `price` does not change
    `yield`. If you want linked moves, shock both columns, or compute one from the other with a
    [formula column](../scenarios/formula.md).

## 4. The people involved

Knowing who asks the questions makes the example requests easier to read:

| Who | What they do with the engine |
| --- | --- |
| **Portfolio manager** | Owns the fund's positioning: weights, active weights, concentration. Runs what-ifs on trades and market moves, and compares the fund with its benchmark. |
| **Equity analyst** | Covers a list of companies. Maintains target prices, and checks upside to target and how much of the fund sits in their names. |
| **Credit analyst** | Covers bond issuers. Updates ratings and prices of hard-to-value bonds (overrides), and watches yield and duration. |
| **Investment risk** | Builds stress-test scenarios, compares them with the base and the benchmark, and checks limits. |
| **Investment compliance** | Checks rules such as concentration limits, and needs to prove where a reported figure came from. See [Audit a number](../scenarios/audit.md). |
| **Client reporting** | Produces factsheets (top ten holdings, sector and currency breakdowns) and must never see analysts' internal views. |

People are usually allowed to see only part of the data: an analyst sees their own coverage, and
client reporting doesn't see target prices. This is **entitlements**, covered in
[Access control](../scenarios/access-control.md).

## 5. Cheat sheet: finance word → what to type

| You want… | Finance word | In a request |
| --- | --- | --- |
| Rows of the fund | holdings | the `holdings` dataset, no `group_by` |
| Only what the fund owns | holdings | `"filter": "quantity > 0"` |
| Value of each holding in USD | market value | `"derive": [{"name": "mv", "expr": "round(price * quantity * fx_rate, 2)"}]` |
| Totals per sector | exposure by sector | `"group_by": ["sector"]` + a `sum` measure |
| Share of the fund | weight | `"post": [{"name": "weight", "expr": "mv / total(mv)"}]` |
| Fund vs benchmark | active weight | two measures and `total()`; see [Weights and active weights](../scenarios/weights.md) |
| Equities and bonds side by side | asset mix | `sum` measures with `"where": "asset_class == 'Equity'"` … |
| Size-weighted yield | weighted average yield | `{"fn": "wavg", "of": "yield", "weight": "float(mv)"}` |
| Totals and subtotals | subtotals | `"rollup": true` |
| Asset class × currency matrix | currency exposure | `"pivot": {"on": ["currency"]}` |
| Holdings over 10% | concentration limit | `"having": "weight_pct > 10"` |
| Largest holdings first | top ten holdings | `"sort"` on the weight, `"page": {"limit": 10}` |
| Fix one price | mark down a price | a [what-if](../whatif/index.md) step with `"kind": "override"` |
| Move a whole column | shock | a [what-if](../whatif/index.md) step with `"kind": "shock"` |
| +25bp on yields | basis points | `{"kind": "shock", "column": "yield", "op": "add", "value": "0.0025"}` |
| A stronger dollar | currency shock | a `pct` shock on `fx_rate` where `currency != 'USD'` |
| Before vs after | impact | `engine.compare(...)` or `POST /calc/compare` → `__delta` columns |
| Keep a what-if | scenario | [Saved scenarios](../scenarios/saved-scenarios.md) |

The [Glossary](../glossary.md) has short definitions of all of these, plus the engine's own terms.

## Next steps

1. [Quick start](quickstart.md): run the same kind of requests yourself in Python.
2. [Run the demo grid](run-the-demo.md): click around a live grid of 200,000 holdings, no Python
   needed.
3. [Scenarios by feature](../scenarios/index.md): one page per feature, each starting from a
   question a PM or analyst would ask, which you can now read.
