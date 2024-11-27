"""Substats for Genshin Impact artifacts."""

import random
from dataclasses import dataclass
from decimal import Decimal

from artipy.types import VALID_SUBSTATS, StatType

from .stats import Stat
from .utils import possible_substat_values as possible_values


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
        values = possible_values(self.name, self.rarity)
        return random.choice(values)

    def upgrade(self) -> None:
        self.value += self.roll()

    def __str__(self) -> str:
        return f"• {Stat.__str__(self)}"


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
