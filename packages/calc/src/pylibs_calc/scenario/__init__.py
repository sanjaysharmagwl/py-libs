"""Saved what-if scenarios: append-only, hash-chained logs of steps over a dataset version."""

from pylibs_calc.scenario.manager import ScenarioManager
from pylibs_calc.scenario.model import LogEntry, Scenario, verify_chain
from pylibs_calc.scenario.store import InMemoryScenarioStore, ScenarioStore

__all__ = [
    "InMemoryScenarioStore",
    "LogEntry",
    "Scenario",
    "ScenarioManager",
    "ScenarioStore",
    "verify_chain",
]
