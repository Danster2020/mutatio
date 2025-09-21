from importlib.metadata import version, PackageNotFoundError

__version__ = ""

try:
    __version__ = version("mutatio")  # must match [project].name
except PackageNotFoundError:
    __version__ = "0.0.0-dev"
