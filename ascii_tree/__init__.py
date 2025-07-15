"""Top-level package for ascii-tree."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ascii-tree")
except PackageNotFoundError:
    __version__ = "uninstalled"

__author__ = "Eva Maxfield Brown"
__email__ = "evamaxfieldbrown@gmail.com"

from .core import (
    paths_to_tree,
)

# Also name as self
ascii_tree = paths_to_tree

__all__ = [
    "ascii_tree",
    "paths_to_tree",
]