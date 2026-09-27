"""Text helpers."""

import re

_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def slugify(value: str, separator: str = "-") -> str:
    """Convert ``value`` to a lowercase, URL-safe slug."""
    return _NON_ALNUM.sub(separator, value.lower()).strip(separator)
