# Graph Report - py-libs  (2026-09-27)

## Corpus Check
- 17 files · ~2,087 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 5, .typed 2, .lock 1)

## Summary
- 52 nodes · 55 edges · 9 communities (5 shown, 4 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b9e0d051`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- release_info.py
- pylibs_core/__init__.py
- py-libs
- make_filename
- AGENTS.md
- pylibs-core
- core/README.md
- utils/README.md

## God Nodes (most connected - your core abstractions)
1. `make_filename()` - 7 edges
2. `slugify()` - 6 edges
3. `py-libs` - 5 edges
4. `test_slugify()` - 3 edges
5. `Development` - 3 edges
6. `test_slugify_custom_separator()` - 2 edges
7. `test_make_filename()` - 2 edges
8. `test_make_filename_strips_leading_dot()` - 2 edges
9. `test_make_filename_empty_title()` - 2 edges
10. `resolve()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `test_slugify_custom_separator()` --calls--> `slugify()`  [INFERRED]
  packages/core/tests/test_text.py → packages/core/src/pylibs_core/text.py
- `make_filename()` --calls--> `slugify()`  [INFERRED]
  packages/utils/src/pylibs_utils/files.py → packages/core/src/pylibs_core/text.py
- `test_make_filename()` --calls--> `make_filename()`  [INFERRED]
  packages/utils/tests/test_files.py → packages/utils/src/pylibs_utils/files.py
- `test_make_filename_empty_title()` --calls--> `make_filename()`  [INFERRED]
  packages/utils/tests/test_files.py → packages/utils/src/pylibs_utils/files.py
- `test_make_filename_strips_leading_dot()` --calls--> `make_filename()`  [INFERRED]
  packages/utils/tests/test_files.py → packages/utils/src/pylibs_utils/files.py

## Import Cycles
- None detected.

## Communities (9 total, 4 thin omitted)

### Community 0 - "release_info.py"
Cohesion: 0.29
Nodes (7): os, pathlib, main(), Resolve a release tag like ``core/v0.2.0`` to the package it releases.…, resolve(), sys, tomllib

### Community 1 - "pylibs_core/__init__.py"
Cohesion: 0.21
Nodes (9): importlib_metadata, Core utilities shared across py-libs packages., Convert ``value`` to a lowercase, URL-safe slug., slugify(), test_slugify(), test_slugify_custom_separator(), parametrize, pytest (+1 more)

### Community 2 - "py-libs"
Cohesion: 0.22
Nodes (8): Adding a package, Building, Development, Layout, License, One-time setup, py-libs, Releasing

### Community 3 - "make_filename"
Cohesion: 0.33
Nodes (6): make_filename(), Build a safe file name from a human-readable ``title``., Higher-level helpers built on pylibs-core., test_make_filename(), test_make_filename_empty_title(), test_make_filename_strips_leading_dot()

### Community 4 - "AGENTS.md"
Cohesion: 0.29
Nodes (5): Architecture and conventions, Code knowledge graph (graphify), Commands, Releasing, What this is

## Knowledge Gaps
- **14 isolated node(s):** `pylibs-core`, `pylibs-utils`, `What this is`, `Commands`, `Code knowledge graph (graphify)` (+9 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 30 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `slugify()` connect `pylibs_core/__init__.py` to `make_filename`?**
  _High betweenness centrality (0.129) - this node is a cross-community bridge._
- **Why does `make_filename()` connect `make_filename` to `pylibs_core/__init__.py`?**
  _High betweenness centrality (0.097) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `make_filename()` (e.g. with `slugify()` and `test_make_filename()`) actually correct?**
  _`make_filename()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `slugify()` (e.g. with `test_slugify()` and `test_slugify_custom_separator()`) actually correct?**
  _`slugify()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `pylibs-core`, `pylibs-utils`, `What this is` to the rest of the system?**
  _14 weakly-connected nodes found - possible documentation gaps or missing edges._