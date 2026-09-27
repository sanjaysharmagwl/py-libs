"""Higher-level helpers built on pylibs-core."""

from importlib.metadata import version

from pylibs_utils.files import make_filename

__all__ = ["__version__", "make_filename"]
__version__ = version("pylibs-utils")
