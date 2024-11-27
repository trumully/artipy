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
        """Get the value of the stat.

        :return: The value of the stat.
        :rtype: Decimal
        """
        return Decimal(self._value)

    @value.setter
    def value(self, value: Decimal) -> None:
        """Set the value of the stat.

        :param value: The value to set the stat to.
        :type value: float | int | Decimal
        """
        self._value = Decimal(value)

    def __format__(self, format_spec: str) -> str:
        return f"{self.name} = {self.value}" if format_spec in ("v", "verbose") else str(self)  # noqa: PLR6201 tuple is slightly faster

    def __str__(self) -> str:
        name, *_ = STAT_NAMES[self.name].split("%")
        return get_stat_str(name, self.value, is_pct=self.name.is_pct)


@dataclass(slots=True)
class MainStat(Stat):
    """Mainstat dataclass for a Genshin Impact artifact."""

    rarity: int = 5

    def set_value_by_level(self, level: int) -> None:
        """Set the value of the mainstat based on the level of the artifact.

        :param level: The level of the artifact.
        :type level: int
        """
        self.value = possible_mainstat_values(self.name, self.rarity)[level]


@dataclass(slots=True)
class SubStat(Stat):
    """Substat dataclass for a Genshin Impact artifact."""

    rarity: int = 5

    def roll(self) -> Decimal:
        """Roll a random value for the substat. This is used when initially creating
        the substat and when upgrading it.

        :return: A random value for the substat.
        :rtype: Decimal
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
    """Create a new SubStat object.

    The stat type is either randomly chosen or specified. The rarity is required to
    determine the possible values for the substat.

    :param name: The stat name, defaults to random.choice(StatType)
    :type name: StatType, optional
    :param rarity: The rarity of the artifact
    :type rarity: int
    :return: A new SubStat object
    :rtype: SubStat
    """
    if name is None:
        name = StatType(random.choice(VALID_SUBSTATS))
    stat = SubStat(name, Decimal(0), rarity)
    stat.value = stat.roll()
    return stat
