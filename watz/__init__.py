"""The Watz Python SDK."""

from importlib.metadata import version

__version__ = version("watz")

from . import endpoints
from .client import Client

__all__ = ["endpoints", "Client"]
