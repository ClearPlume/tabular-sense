from importlib.metadata import version, PackageNotFoundError

from .interface import ColumnClassifier

try:
    __version__ = version("tabular-sense")
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = [ColumnClassifier]
