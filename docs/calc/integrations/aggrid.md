---
covers:
  - packages/calc/src/pylibs_calc/adapters/aggrid.py
---

# AG Grid

`AgGridAdapter` translates AG Grid's **server-side row model** (SSRM) into engine requests, and the results back into grid rows. Grouping, pivoting, sorting, filtering and editing are all computed on the server, so the browser never holds the full dataset.

| AG Grid sends | The engine computes |
| --- | --- |
| `rowGroupCols` + `groupKeys` | `group_by` for the level being expanded, filtered to the parent group |
| `valueCols` (`sum`, `avg`, `min`, `max`, `count`, …) | measures |
| `pivotMode` + `pivotCols` | a pivot. Its columns are computed once from the filter model, so they stay stable while you drill down |
| `sortModel` | `sort` |
| `filterModel`: `text`, `number`, `date`, `set`, combined conditions, `multi` | `filter` |
| `startRow` / `endRow` | `page` |
| a cell edit | an [override](../scenarios/override.md) appended to a scenario |

## Client setup

```js
const gridOptions = {
  rowModelType: 'serverSide',
  serverSideDatasource: {
    getRows: p => fetch('/calc/aggrid/rows', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({dataset: 'positions', scenario, request: p.request}),
      })
      .then(r => r.json()).then(d => p.success(d)).catch(() => p.fail()),
  },
  getRowId: p => p.data.__row_id,
  getServerSideGroupKey: d => d.__group_key,   // typed keys: nulls, dates and decimals round-trip
  serverSidePivotResultFieldSeparator: '_',     // must match AgGridAdapter.separator
  readOnlyEdit: true,                           // edits go to the server as scenario overrides
  onCellEditRequest: async e => {
    scenario = await post('/calc/aggrid/edit', {
      scenario: scenario.id, expected_version: scenario.version,
      edit: {colId: e.colDef.field, newValue: e.newValue, data: e.data},
    }, {'Idempotency-Key': crypto.randomUUID()});   // a retried edit is applied once
    e.api.refreshServerSide({purge: false});
  },
};
```

[`packages/calc/examples/grid.html`](https://github.com/sanjaysharmagwl/py-libs/blob/master/packages/calc/examples/grid.html) is a complete working page. See [Run the demo grid](../getting-started/run-the-demo.md).

## Customizing the adapter

```python
from pylibs_calc import Measure
from pylibs_calc.adapters.aggrid import AgGridAdapter

adapter = AgGridAdapter(
    separator="_",
    in_range_inclusive=False,  # must match the grid's inRange filter option
    custom_aggs={  # extra aggFunc names the grid can offer
        "wavg_yield": lambda c: Measure(
            name=c, fn="wavg", of=c, weight="abs(float(price * quantity))"
        ),
    },
)
router = create_router(engine, prefix="/calc", aggrid=adapter)
```

## Gotchas

- The server-side row model is an AG Grid **Enterprise** feature.
- **Group rows can't be edited** (`422 not_editable`); edit the rows inside the group.
- **Only editable columns** can be edited. See [Datasets](../concepts/datasets.md).
- The **advanced filter model** isn't supported yet.
