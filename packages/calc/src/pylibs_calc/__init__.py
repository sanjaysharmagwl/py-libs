"""Embeddable what-if calculation engine on Polars.

Filters, overrides, shocks, derived columns, group-by, rollup, pivot and saved scenarios, with
exact decimal arithmetic, reproducible fingerprints and a pure-Python reference evaluator.
"""

from importlib.metadata import version

from pylibs_calc.catalog import Catalog, Dataset, DatasetCatalog
from pylibs_calc.config import CalcContext, Limits
from pylibs_calc.dtypes import NumericConfig
from pylibs_calc.engine import CalcEngine, EngineConfig
from pylibs_calc.errors import (
    CalcError,
    CalcTimeout,
    ComputeError,
    DatasetNotFound,
    EngineBusy,
    Forbidden,
    LimitExceeded,
    NotFound,
    ScenarioNotFound,
    SpecError,
    VersionConflict,
)
from pylibs_calc.exec import RuntimeReport, runtime_check
from pylibs_calc.result import CalcResult, ColumnInfo, ResultMeta
from pylibs_calc.scenario import (
    InMemoryScenarioStore,
    LogEntry,
    Scenario,
    ScenarioManager,
    ScenarioStore,
)
from pylibs_calc.schema import ColumnMeta, DatasetSchema
from pylibs_calc.spec.canonical import canonical_json, fingerprint
from pylibs_calc.spec.expr import col, lit
from pylibs_calc.spec.formula import parse_formula, to_formula
from pylibs_calc.spec.query import (
    CalcRequest,
    CompareRequest,
    DatasetRef,
    Derive,
    Measure,
    Options,
    Page,
    Pivot,
    PostAgg,
    Query,
    ScenarioRef,
    SortKey,
)
from pylibs_calc.spec.scenario import Disable, Edit, Formula, Override, Shock

__all__ = [
    "CalcContext",
    "CalcEngine",
    "CalcError",
    "CalcRequest",
    "CalcResult",
    "CalcTimeout",
    "Catalog",
    "ColumnInfo",
    "ColumnMeta",
    "CompareRequest",
    "ComputeError",
    "Dataset",
    "DatasetCatalog",
    "DatasetNotFound",
    "DatasetRef",
    "DatasetSchema",
    "Derive",
    "Disable",
    "Edit",
    "EngineBusy",
    "EngineConfig",
    "Forbidden",
    "Formula",
    "InMemoryScenarioStore",
    "LimitExceeded",
    "Limits",
    "LogEntry",
    "Measure",
    "NotFound",
    "NumericConfig",
    "Options",
    "Override",
    "Page",
    "Pivot",
    "PostAgg",
    "Query",
    "ResultMeta",
    "RuntimeReport",
    "Scenario",
    "ScenarioManager",
    "ScenarioNotFound",
    "ScenarioRef",
    "ScenarioStore",
    "Shock",
    "SortKey",
    "SpecError",
    "VersionConflict",
    "__version__",
    "canonical_json",
    "col",
    "fingerprint",
    "lit",
    "parse_formula",
    "runtime_check",
    "to_formula",
]
__version__ = version("pylibs-calc")
