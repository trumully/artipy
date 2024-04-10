from dataclasses import dataclass

from .stats import Stat
from .utils import possible_mainstat_values as possible_values


@dataclass
class MainStat(Stat):
    """Mainstat dataclass for a Genshin Impact artifact."""

    rarity: int = 5

    def set_value(self, level: int) -> None:
        """Set the value of the mainstat based on the level of the artifact."""
        self.value = possible_values(self.name, self.rarity)[level - 1]

    def __str__(self) -> str:
        return f"• {super().__str__()}"
