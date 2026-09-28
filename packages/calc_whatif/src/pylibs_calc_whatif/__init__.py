"""What-if analysis for pylibs-calc, as a plugin.

::

    from pylibs_calc import CalcEngine
    from pylibs_calc_whatif import InMemoryScenarioStore, WhatIfPlugin

    engine = CalcEngine(catalog, plugins=[WhatIfPlugin(store=InMemoryScenarioStore())])
    engine.run({
        "dataset": "positions",
        "extensions": {"whatif": {"steps": [{"kind": "shock", "column": "price", "op": "pct",
                                             "value": 5}]}},
        "query": {"group_by": ["sector"], "measures": [...]},
    })

Steps (:class:`Override`, :class:`Shock`, :class:`Formula`, :class:`Disable`) change values but
keep every row. They come ad hoc in a request's ``extensions.whatif`` block, or from a saved
scenario: an append-only, hash-chained log over a pinned dataset version, managed through
``plugin.scenarios``.
"""

from importlib.metadata import version

from pylibs_calc_whatif.aggrid import CellEdit, edit_to_override
from pylibs_calc_whatif.errors import ScenarioNotFound
from pylibs_calc_whatif.planner import LogicalMutations, WhatIfLimits
from pylibs_calc_whatif.plugin import WhatIfPlan, WhatIfPlugin
from pylibs_calc_whatif.scenario import (
    InMemoryScenarioStore,
    LogEntry,
    Scenario,
    ScenarioManager,
    ScenarioStore,
    verify_chain,
)
from pylibs_calc_whatif.spec import (
    Disable,
    Edit,
    Formula,
    Override,
    ScenarioRef,
    ScenarioStep,
    Shock,
    WhatIf,
)

__all__ = [
    "CellEdit",
    "Disable",
    "Edit",
    "Formula",
    "InMemoryScenarioStore",
    "LogEntry",
    "LogicalMutations",
    "Override",
    "Scenario",
    "ScenarioManager",
    "ScenarioNotFound",
    "ScenarioRef",
    "ScenarioStep",
    "ScenarioStore",
    "Shock",
    "WhatIf",
    "WhatIfLimits",
    "WhatIfPlan",
    "WhatIfPlugin",
    "__version__",
    "edit_to_override",
    "verify_chain",
]
__version__ = version("pylibs-calc-whatif")
