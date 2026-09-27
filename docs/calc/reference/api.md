# Python API

Everything below is importable from `pylibs_calc` directly, unless a heading shows a longer module path. This page is generated from the docstrings, so it always matches the installed version.

## Engine

::: pylibs_calc.CalcEngine
    options:
      members: [run, compare, explain, distinct_values, schema, scenarios]

::: pylibs_calc.EngineConfig

::: pylibs_calc.CalcContext

::: pylibs_calc.Limits

::: pylibs_calc.NumericConfig

## Data

::: pylibs_calc.Catalog
    options:
      members: [register_frame, register_scan, get, list, drop]

::: pylibs_calc.DatasetSchema

::: pylibs_calc.ColumnMeta

## Requests

::: pylibs_calc.CalcRequest

::: pylibs_calc.CompareRequest

::: pylibs_calc.Query

::: pylibs_calc.Derive

::: pylibs_calc.Measure

::: pylibs_calc.PostAgg

::: pylibs_calc.Pivot

::: pylibs_calc.SortKey

::: pylibs_calc.Page

::: pylibs_calc.Options

::: pylibs_calc.DatasetRef

::: pylibs_calc.ScenarioRef

## Scenario steps

::: pylibs_calc.Override

::: pylibs_calc.Edit

::: pylibs_calc.Shock

::: pylibs_calc.Formula

::: pylibs_calc.Disable

## Saved scenarios

::: pylibs_calc.ScenarioManager

::: pylibs_calc.Scenario

::: pylibs_calc.LogEntry

::: pylibs_calc.ScenarioStore

::: pylibs_calc.InMemoryScenarioStore

::: pylibs_calc.scenario.redis_store.RedisScenarioStore

## Results

::: pylibs_calc.CalcResult

::: pylibs_calc.ResultMeta

::: pylibs_calc.ColumnInfo

## Formulas and fingerprints

::: pylibs_calc.parse_formula

::: pylibs_calc.to_formula

::: pylibs_calc.col

::: pylibs_calc.lit

::: pylibs_calc.fingerprint

::: pylibs_calc.canonical_json

## Verification

::: pylibs_calc.verify.verify

::: pylibs_calc.verify.VerifyReport

## Runtime

::: pylibs_calc.runtime_check

::: pylibs_calc.RuntimeReport

## Integrations

::: pylibs_calc.integrations.fastapi.create_router

::: pylibs_calc.adapters.aggrid.AgGridAdapter

## Errors

::: pylibs_calc.CalcError

::: pylibs_calc.SpecError

::: pylibs_calc.ComputeError

::: pylibs_calc.NotFound

::: pylibs_calc.DatasetNotFound

::: pylibs_calc.ScenarioNotFound

::: pylibs_calc.Forbidden

::: pylibs_calc.VersionConflict

::: pylibs_calc.LimitExceeded

::: pylibs_calc.EngineBusy

::: pylibs_calc.CalcTimeout

## Protocols

::: pylibs_calc.DatasetCatalog

::: pylibs_calc.Dataset
