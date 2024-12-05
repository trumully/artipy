"""Stat types and data for Genshin Impact artifacts."""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from decimal import Decimal

from artipy.types import STAT_NAMES, VALID_SUBSTATS, StatType

from .utils import possible_mainstat_values, possible_substat_values

__all__ = (
    "MainStat",
    "SubStat",
    "create_substat",
)


def get_stat_str(name: str, value: float | Decimal, *, is_pct: bool) -> str:
    return f"{name}+{value:.1%}" if is_pct else f"{name}+{value:,.0f}"


@dataclass(slots=True)
class Stat:
    """Dataclass for a stat in Genshin Impact."""

    name: StatType
    _value: float | Decimal = field(default=Decimal(0), repr=False)

    @property
    def value(self) -> Decimal:
        return Decimal(self._value)

    @value.setter
    def value(self, value: Decimal) -> None:
        self._value = Decimal(value)

    def __format__(self, format_spec: str) -> str:
        return (
            f"{self.name} = {self.value}"
            if format_spec in {"v", "verbose"}
            else str(self)
        )

    def __str__(self) -> str:
        name, *_ = STAT_NAMES[self.name].split("%")
        return get_stat_str(name, self.value, is_pct=self.name.is_pct)


@dataclass(slots=True)
class MainStat(Stat):
    """Mainstat dataclass for a Genshin Impact artifact."""

    rarity: int = 5

    def set_value_by_level(self, level: int) -> None:
        """Set the value of the mainstat based on the level of the artifact."""
        self.value = possible_mainstat_values(self.name, self.rarity)[level]

@dataclass(slots=True)
class SubStat(Stat):
    """Substat dataclass for a Genshin Impact artifact."""

    rarity: int = 5

    def roll(self) -> Decimal:
        """Roll a random value for the substat.

        This is used when initially creating the substat and when upgrading it.
        """
        values = possible_substat_values(self.name, self.rarity)
        return random.choice(values)

    def upgrade(self) -> None:
        self.value += self.roll()

    def __str__(self) -> str:
        name, *_ = STAT_NAMES[self.name].split("%")
        return f"• {get_stat_str(name, self.value, is_pct=self.name.is_pct)}"


def create_substat(
    *,
    name: StatType | None = None,
    rarity: int,
) -> SubStat:
    """Create a substat.

    Args:
        rarity (int): The rarity of the artifact.
        name (StatType, optional): The name of the substat. If not given, defaults to a random valid substat.

    Returns:
        SubStat: The substat object.
    """
    if name is None:
        name = StatType(random.choice(VALID_SUBSTATS))
    stat = SubStat(name, Decimal(0), rarity)
    stat.value = stat.roll()
    return stat
