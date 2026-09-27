"""Resolve a release tag like ``core/v0.2.0`` to the package it releases.

Validates that the package exists and that the tag version matches the version in its
pyproject.toml. Prints ``key=value`` lines, and appends them to ``$GITHUB_OUTPUT`` when set.
"""

import os
import re
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAG_RE = re.compile(r"^(?P<dir>[A-Za-z0-9_.-]+)/v(?P<version>\d[^/]*)$")


def resolve(tag: str) -> dict[str, str]:
    match = TAG_RE.match(tag)
    if match is None:
        raise ValueError(f"Tag {tag!r} does not match '<package-dir>/v<version>'")

    package_dir = Path("packages") / match["dir"]
    pyproject_path = ROOT / package_dir / "pyproject.toml"
    if not pyproject_path.is_file():
        raise ValueError(f"No package at {package_dir} (missing pyproject.toml)")

    project = tomllib.loads(pyproject_path.read_text())["project"]
    if project["version"] != match["version"]:
        raise ValueError(
            f"Tag version {match['version']} != {project['name']} version {project['version']} "
            f"in {package_dir}/pyproject.toml"
        )

    return {"name": project["name"], "version": project["version"], "path": str(package_dir)}


def main() -> int:
    tag = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GITHUB_REF_NAME", "")
    try:
        info = resolve(tag)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    lines = [f"{key}={value}" for key, value in info.items()]
    print("\n".join(lines))
    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a") as fh:
            fh.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
