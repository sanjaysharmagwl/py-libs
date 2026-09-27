"""Core utilities shared across py-libs packages."""

from importlib.metadata import version

from pylibs_core.text import slugify

__all__ = ["__version__", "slugify"]
__version__ = version("pylibs-core")
