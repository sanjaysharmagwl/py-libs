# Finance primer: start here

`pylibs-calc` is built for trading and risk teams, and the rest of these docs use their vocabulary:
*positions*, *desks*, *notional*, *shocks*, *basis points*, *P&L impact*. If those words are new to
you, read this page first. It assumes no finance background, takes about fifteen minutes, and
every number on it is computed by the engine from the same twelve-row example book the other pages use.

!!! abstract "The whole idea in one paragraph"
    A bank or fund holds a list of things it owns (or owes): bonds, shares, currencies, oil.
    Each line of that list is a **position**, and the list is the **book**. Teams called
    **desks** manage different parts of the book. Every day people ask *"what is all of this
    worth, broken down by desk or region?"* and, more importantly, *"what would it be worth
    **if** the market moved?"* A **shock** is one of those imagined market moves, and the
    difference it makes is the **P&L impact**. `pylibs-calc` answers exactly these questions over
    a table of positions.

## 1. The book, column by column

Here is the example book. Each row is one position:

```python exec="on"
from book import positions, table

print(table(positions()))
```

### What each column means

`position_id`
:   A unique number for the row. In the engine it is the **key column**: the thing that identifies a
    row when you edit it.

`instrument`
:   *What* is held. The book has five kinds, one per desk:

    | Kind | Examples in the book | What it is |
    | --- | --- | --- |
    | **Government bond** | `UST 4.25% 2034` (US Treasury), `Bund 2.5% 2033` (German), `JGB 0.9% 2032` (Japanese) | A loan to a government. The name reads *issuer, coupon (yearly interest rate), year it is repaid*. |
    | **Corporate bond** | `ACME Corp 5.1% 2030`, `Globex 6.0% 2029` | The same, but lent to a company, so riskier. |
    | **Equity** (a stock or share) | `Umbrella Health`, `Stark Industries` | Part-ownership of a company. |
    | **FX forward** | `EUR/USD fwd`, `USD/JPY fwd` | An agreement to swap one currency for another at a fixed rate on a future date. FX means *foreign exchange*. |
    | **Commodity future** | `Brent Dec-26` | An agreement to buy or sell a raw material (here Brent crude oil) in December 2026. |

`desk`
:   The **team** (and its traders) responsible for the position. Desks are usually organised by asset class:
    **Rates** trades government bonds (their value depends on interest rates), **Credit** trades corporate
    bonds (their value depends on whether companies repay), **Equities** trades stocks, **FX**
    trades currencies, and **Commodities** trades raw materials. "Show me each desk" is the most common
    question anyone asks, which is why it appears in almost every example.

`sector`
:   The part of the economy the issuer is in: Tech, Energy, Health, Financials, Industrials. Used to
    ask things like "what if Tech falls?"

`region`
:   Where the issuer is: **AMER** (the Americas), **EMEA** (Europe, Middle East and Africa) and
    **APAC** (Asia-Pacific).

`rating`
:   A credit agency's grade for how likely the issuer is to repay, from best to worst:
    `AAA`, `AA`, `A`, `BBB`, `BB`, … `BBB` and above is **investment grade**, and below it is
    **high yield** (sometimes called "junk"). It is null for oil, which has no issuer to rate.

`price`
:   What one unit is worth today. The price used to value a position is called its **mark**, and
    updating it is **marking** the book. Bonds are quoted per 100 of face value, so `98.50` means "98.5% of
    the amount repaid at maturity". The column is an exact decimal with 2 places, because money is not
    rounded casually.

`quantity`
:   How many units are held. **Positive means long** (you own it and gain when the price rises).
    **Negative means short** (you owe it, or sold it without owning it, and you *gain* when the price
    falls).

`yield`
:   For bonds only, the yearly return you would earn by buying at today's price and holding to
    maturity, as a fraction: `0.0425` is 4.25%. **When yields rise, bond prices fall**, and vice versa.
    It is null for anything that isn't a bond.

!!! note "Simplifications this book makes"
    Real systems value each instrument type with its own formula, convert everything into one
    currency, and handle bond face value properly. The example book simply uses
    `price × quantity` for everything, so you can follow the arithmetic by hand. That is why the
    `USD/JPY fwd` row looks enormous: 148.30 yen per dollar × −50,000 is a number in yen, not
    dollars. The engine doesn't care what the numbers mean. It computes what you ask for, exactly.

## 2. Numbers you compute from the book

**Market value** (also called **notional** or **exposure** on these pages) is how much money a position
represents: `price × quantity`. It is negative for a short position.

```python exec="on"
from book import engine, table

result = engine().run(
    {
        "dataset": "positions",
        "query": {
            "derive": [{"name": "market_value", "expr": "price * quantity"}],
            "select": ["position_id", "instrument", "desk", "price", "quantity", "market_value"],
            "filter": "desk in ('Rates', 'Equities')",
            "sort": [{"by": "position_id"}],
        },
    }
)
print(table(result))
```

Adding positions up per desk gives two different totals, and both matter:

- **Net** is the signed sum: longs and shorts cancel. It answers *"which way are we betting, and how much?"*
- **Gross** is the sum of absolute values: nothing cancels. It answers *"how big is our activity?"*
  Risk **limits** are often set on gross, because a desk that is long 1m and short 1m nets to zero
  but can still lose money on both.

```python exec="on"
from book import engine, table

result = engine().run(
    {
        "dataset": "positions",
        "query": {
            "group_by": ["desk"],
            "measures": [
                {"name": "net", "fn": "sum", "of": "price * quantity"},
                {"name": "gross", "fn": "sum", "of": "abs(price * quantity)"},
                {"name": "positions", "fn": "count_rows"},
            ],
            "sort": [{"by": "desk"}],
        },
    }
)
print(table(result))
```

Equities is a good one to read: long Umbrella and Stark, short Wayne, so net (207,850) is much smaller
than gross (498,350).

Other summary numbers you will meet:

- **Weighted average yield**: the average yield of a desk's bonds, where bigger positions count
  more. A plain average would let a tiny bond count as much as a huge one. The engine calls this
  `wavg`; see [Measures](../scenarios/measures.md).
- **Ratio of sums**: e.g. *average price = total value ÷ total quantity*, computed after adding up, not by averaging the prices. See [Ratios after aggregation](../scenarios/post-ratios.md).
- **Subtotals**: a total per region, then per desk inside it, then a grand total, all in one grid.
  In the engine this is a [rollup](../scenarios/rollup.md).
- **Pivot**: a matrix, such as desks down the side and regions across the top. See [Pivot](../scenarios/pivot.md).
- **Limit breach**: a desk whose exposure is over the limit risk has set for it. See [Having](../scenarios/having.md).

## 3. Asking "what if?"

This is the reason the engine exists. People rarely only want today's numbers; they want to know what
happens to them under a change.

**Base**
:   The book as it really is, before any change. Every "what if" is measured against it.

**Override**
:   Changing **one cell**. A trader who believes a price is stale "corrects the mark" on one position.
    See [Override a cell](../scenarios/override.md).

**Shock**
:   Changing **a whole column at once**, optionally only on some rows: "every Tech price −5%",
    "every yield +25bp". A shock is an imagined market move. The engine has three kinds: `pct` (move by
    a percentage), `add` (add an amount) and `mul` (multiply). See [Shock a column](../scenarios/shock.md).

**Basis point (bp)**
:   One hundredth of a percent: 0.01%, or `0.0001` as a fraction. Interest rates and yields move in small
    steps, so people say "+25bp" rather than "+0.25%". "Yields +25bp" is the shock
    `{"op": "add", "value": "0.0025"}` on the `yield` column.

**Stress test**
:   A large, deliberately painful set of shocks ("equities −20%, credit −5%, oil +30%") to see how
    much the firm could lose in a crisis.

**Sensitivity**
:   A small shock (often +1bp or +1%) to measure how much a position reacts to one market variable.

**Scenario**
:   A named, saved list of overrides and shocks (the engine calls each one a **step**), so a
    risk manager can build "Oil crisis 2026", share it, come back to it tomorrow, or copy it
    (**fork** it) to try a variation. See [Saved scenarios and forks](../scenarios/saved-scenarios.md).

**P&L and P&L impact**
:   P&L means *profit and loss*. The **P&L impact** of a scenario is how much the book's value changes
    compared with the base. In the engine you get it by running a [compare](../scenarios/compare.md), which adds
    `__base`, `__delta` and `__pct` columns next to every number.

Here is a what-if end to end: *"what if the Equities desk's stocks all fall 10%?"*

```python exec="on"
from book import engine, table

result = engine().compare(
    {
        "dataset": "positions",
        "what_if": [
            {"kind": "shock", "column": "price", "op": "pct", "value": -10, "where": "desk == 'Equities'"}
        ],
        "query": {
            "filter": "desk == 'Equities'",
            "group_by": ["instrument"],
            "measures": [{"name": "mv", "fn": "sum", "of": "price * quantity"}],
            "sort": [{"by": "instrument"}],
        },
    }
)
print(table(result))
```

How to read it:

- `mv` is the value **after** the shock and `mv__base` is the value **before** it.
- `mv__delta` is the P&L impact. The two **long** positions lose money.
- **Wayne Financial is short** (−2,500 shares), so the fall *makes* money: its delta is positive. This is
  the whole point of being short, and a good sanity check when you try your own shocks.
- Stark Industries shows −9.9984% rather than −10% because 312.75 × 0.9 = 281.475 has to be rounded
  back to a 2-decimal price. The engine never silently drops precision; see
  [Numbers, types and nulls](../concepts/numbers-types-nulls.md).

!!! warning "Shocks don't know finance"
    The engine moves exactly the column you shock. Shocking `yield` up does **not** lower bond prices
    by itself, and shocking `price` does not change `yield`. If you want linked moves, shock both
    columns, or compute one from the other with a [formula column](../scenarios/formula.md).

## 4. The people involved

Knowing who asks the questions makes the example requests easier to read:

| Who | What they do with the engine |
| --- | --- |
| **Trader** | Owns positions on one desk; corrects marks (overrides) and checks their own exposure. |
| **Risk manager** | Watches the whole book; builds stress-test scenarios, compares them with the base and checks limits. |
| **Desk head** | Sees their desk's totals, subtotals and limit breaches. |
| **Auditor / controller** | Needs to prove where a reported figure came from. See [Audit a number](../scenarios/audit.md). |

People are usually only allowed to see some of the book, for example just their own desk. This is
**entitlements**, covered in [Access control](../scenarios/access-control.md).

## 5. Cheat sheet: finance word → what to type

| You want… | Finance word | In a request |
| --- | --- | --- |
| Rows of the book | positions | the `positions` dataset, no `group_by` |
| Value of each position | market value, notional | `"derive": [{"name": "mv", "expr": "price * quantity"}]` |
| Totals per desk | exposure by desk | `"group_by": ["desk"]` + a `sum` measure |
| Longs and shorts separately | long / short | `sum` measures with `"where": "quantity > 0"` / `"quantity < 0"` |
| Size ignoring direction | gross | `abs(price * quantity)` |
| Size-weighted yield | weighted average yield | `{"fn": "wavg", "of": "yield", "weight": "..."}` |
| Totals and subtotals | subtotals | `"rollup": true` |
| Desk × region matrix | pivot | `"pivot": {"on": ["region"]}` |
| Desks over a limit | limit breach | `"having": "gross > 400000"` |
| Fix one price | correct a mark | a `what_if` step with `"kind": "override"` |
| Move a whole column | shock | a `what_if` step with `"kind": "shock"` |
| +25bp on yields | basis points | `{"kind": "shock", "column": "yield", "op": "add", "value": "0.0025"}` |
| Before vs after | P&L impact | `engine.compare(...)` or `POST /calc/compare` → `__delta` columns |
| Keep a what-if | scenario | [Saved scenarios](../scenarios/saved-scenarios.md) |

The [Glossary](../glossary.md) has short definitions of all of these, plus the engine's own terms.

## Next steps

1. [Quick start](quickstart.md): run the same kind of requests yourself in Python.
2. [Run the demo grid](run-the-demo.md): click around a live grid of 200,000 positions, no Python needed.
3. [Scenarios by feature](../scenarios/index.md): one page per feature, each starting from a business question you can now read.
