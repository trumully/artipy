"""Module for handling stats and their data."""

from .mainstat import MainStat
from .substat import SubStat, create_substat

__all__ = (
    "MainStat",
    "SubStat",
    "create_substat",
)
