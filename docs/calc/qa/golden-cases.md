# Golden cases

Each case below pins one rule that is easy to get wrong. The expected results are recorded in [`docs/examples/calc/golden_cases.json`](https://github.com/sanjaysharmagwl/py-libs/blob/master/docs/examples/calc/golden_cases.json), and the docs build re-runs every case against the current engine. The **Status** column is live.

```bash
uv run python docs/examples/calc/golden.py            # PASS/FAIL per case
uv run python docs/examples/calc/golden.py --update   # re-record after an intended change
```

!!! warning "Changing an expected result"
    Only re-record after checking that the new answer is right, and explain why in the commit message. A golden case that changes is a change in behaviour that users will notice.

```python exec="on"
import json
from golden import check

results = check()
print("| Case | Rule | Status |\n| --- | --- | --- |")
for case, ok, _ in results:
    print(f"| [`{case['id']}`](#{case['id']}) | {case['title']} | {'✅ pass' if ok else '❌ FAIL'} |")
print()
for case, ok, actual in results:
    route = "/calc/compare" if case["kind"] == "compare" else "/calc/query"
    kind = "success" if ok else "failure"
    print(f'<a id="{case["id"]}"></a>\n')
    print(f'??? {kind} "{case["title"]}"\n')
    print(f"    {case['why']}\n")
    print(f"    **Request** (`POST {route}`):\n")
    print("    ```json")
    print("\n".join(f"    {line}" for line in json.dumps(case["request"], indent=2).splitlines()))
    print("    ```\n")
    print("    **Expected rows:**\n")
    print("    ```json")
    print("\n".join(f"    {line}" for line in json.dumps(actual, indent=2).splitlines()))
    print("    ```\n")
```
