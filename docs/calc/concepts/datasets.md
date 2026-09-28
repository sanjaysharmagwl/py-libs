---
covers:
  - packages/calc/src/pylibs_calc/catalog.py
  - packages/calc/src/pylibs_calc/schema.py
---

# Datasets and the catalog

A **dataset** is a table the engine calculates over, such as a book of positions or a set of trades. You register datasets in a `Catalog`, and every registration is an immutable **version**.

## Registering data

=== "An in-memory frame"

    ```python
    from pylibs_calc import Catalog

    catalog = Catalog()
    catalog.register_frame(
        "positions",
        df,  # a polars DataFrame
        key_columns=["position_id"],  # unique, non-null: identifies a row
        version="2026-09-30",  # default: a hash of the contents
        editable=["price", "quantity"],  # default: every non-key column
    )
    ```

=== "Parquet or Arrow files (lazily scanned)"

    ```python
    catalog.register_scan(
        "trades",
        "s3://risk/trades/2026-09-30/*.parquet",
        format="parquet",
        key_columns=["trade_id"],
        version="snapshot-8812",  # required for remote files, e.g. an ETag
        storage_options={"aws_region": "eu-west-1"},
    )
    ```

Scanned files are never loaded as a whole. Polars' streaming engine reads them, and filters and column selection are pushed into the reads, so a dataset can be larger than the pod's memory.

## What registration does

- **Normalizes types**:
    - integers become `Int64`, and floats become `Float64`
    - decimals become `Decimal(38, s)`
    - enums become `String`, while categoricals stay categorical
- **Cleans floats.** NaN and ±infinity become null, so every calculation sees SQL-style nulls.
- **Checks the keys.** Key columns must have no nulls and no duplicates. `register_scan` checks them only with `validate_keys=True`.
- **Builds the schema** (a `DatasetSchema` of `ColumnMeta` entries). Each column gets a role (`key`, `dimension` or `measure`) and an editable flag. A UI reads it with `engine.schema("positions")` or `GET /calc/datasets/positions/schema`.

## Versions

```python
catalog = Catalog(max_versions=2)  # keep the two most recent versions of each dataset
```

- A request uses the **latest** version unless it pins one: `{"dataset": {"id": "positions", "version": "2026-09-29"}}`.
- A [saved scenario](../scenarios/saved-scenarios.md) (what-if plugin) is pinned to the version it was created on, so it keeps working after the next refresh for as long as the catalog keeps that version.
- Each result records the version it used, in `meta.dataset`.

## Datasets without a key

Key columns are optional, but without them:

- [overrides](../scenarios/override.md) (what-if plugin) can't find rows
- [row-level compare](../scenarios/compare.md) can't join the two sides

The engine adds a hidden row index so that sorting and paging stay stable.

## Your own catalog

`CalcEngine` accepts anything that implements the `DatasetCatalog` protocol (`get(dataset_id, version)` and `list()`). You can load datasets on demand from your own metadata service.
