# Python API

Everything below is importable from `pylibs_calc` (or, for the what-if plugin, `pylibs_calc_whatif`) directly, unless a heading shows a longer module path. This page is generated from the docstrings, so it always matches the installed version.

## Engine

::: pylibs_calc.CalcEngine
    options:
      members: [run, compare, explain, distinct_values, schema, call, plugin]

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

::: pylibs_calc.Side

## Plugin API

See [Plugins](../concepts/plugins.md) and [Write a plugin](../extending/write-a-plugin.md).

::: pylibs_calc.Plugin

::: pylibs_calc.Registry
    options:
      members: [add_function, add_aggregate, add_transform, add_operation, add_routes]

::: pylibs_calc.FunctionDef

::: pylibs_calc.AggregateDef

::: pylibs_calc.TransformDef

::: pylibs_calc.Bound

::: pylibs_calc.TransformPlan

::: pylibs_calc.BindContext

::: pylibs_calc.PlanContext

::: pylibs_calc.OperationDef

::: pylibs_calc.Kernel

::: pylibs_calc.View

::: pylibs_calc.discover_plugins

::: pylibs_calc.PluginError

::: pylibs_calc.integrations.fastapi.RouterKit

::: pylibs_calc.ext

::: pylibs_calc.testing

## What-if plugin

::: pylibs_calc_whatif.WhatIfPlugin

::: pylibs_calc_whatif.WhatIf

::: pylibs_calc_whatif.WhatIfLimits

::: pylibs_calc_whatif.ScenarioRef

::: pylibs_calc_whatif.Override

::: pylibs_calc_whatif.Edit

::: pylibs_calc_whatif.Shock

::: pylibs_calc_whatif.Formula

::: pylibs_calc_whatif.Disable

::: pylibs_calc_whatif.ScenarioManager

::: pylibs_calc_whatif.Scenario

::: pylibs_calc_whatif.LogEntry

::: pylibs_calc_whatif.ScenarioStore

::: pylibs_calc_whatif.InMemoryScenarioStore

::: pylibs_calc_whatif.scenario.redis_store.RedisScenarioStore

::: pylibs_calc_whatif.CellEdit

::: pylibs_calc_whatif.edit_to_override

::: pylibs_calc_whatif.ScenarioNotFound

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

::: pylibs_calc.Forbidden

::: pylibs_calc.VersionConflict

::: pylibs_calc.LimitExceeded

::: pylibs_calc.EngineBusy

::: pylibs_calc.CalcTimeout

## Protocols

::: pylibs_calc.DatasetCatalog

::: pylibs_calc.Dataset
