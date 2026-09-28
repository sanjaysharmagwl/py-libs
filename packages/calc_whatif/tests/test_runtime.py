import subprocess
import sys


def test_importing_the_plugin_skips_optional_extras() -> None:
    code = (
        "import sys, pylibs_calc_whatif; "
        "from pylibs_calc import CalcEngine, Catalog; "
        "CalcEngine(Catalog(), plugins=[pylibs_calc_whatif.WhatIfPlugin()]); "
        "bad = [m for m in ('fastapi', 'starlette', 'redis', 'hypothesis') if m in sys.modules]; "
        "print(','.join(bad))"
    )
    out = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    assert out.stdout.strip() == ""
