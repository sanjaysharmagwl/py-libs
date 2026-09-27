"""File name helpers."""

from pylibs_core import slugify


def make_filename(title: str, extension: str) -> str:
    """Build a safe file name from a human-readable ``title``."""
    stem = slugify(title) or "untitled"
    return f"{stem}.{extension.lstrip('.')}"
