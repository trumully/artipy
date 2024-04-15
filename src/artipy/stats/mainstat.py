"""Mainstat dataclass for a Genshin Impact artifact."""

from dataclasses import dataclass

from .stats import Stat
from .utils import possible_mainstat_values


@dataclass
class MainStat(Stat):
    """Mainstat dataclass for a Genshin Impact artifact."""

    rarity: int = 5

    def set_value_by_level(self, level: int) -> None:
        """Set the value of the mainstat based on the level of the artifact.

        :param level: The level of the artifact.
        :type level: int
        """
        self.value = possible_mainstat_values(self.name, self.rarity)[level]
