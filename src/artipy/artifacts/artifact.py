from typing import Optional

from artipy.stats import MainStat, SubStat
from .upgrade_strategy import UpgradeStrategy, AddStatStrategy, UpgradeStatStrategy


class Artifact:
    """Class representing an artifact in Genshin Impact."""

    def __init__(self) -> None:
        self._mainstat: Optional[MainStat] = None
        self._substats: list[SubStat] = []
        self._level: int = 0
        self._rarity: int = 0
        self._set: str = ""
        self._slot: str = ""

    def set_mainstat(self, mainstat: MainStat) -> None:
        mainstat.rarity = self.get_rarity()
        self._mainstat = mainstat

    def set_substats(self, substats: list[SubStat]) -> None:
        for substat in substats:
            substat.rarity = self.get_rarity()
        self._substats = substats

    def add_substat(self, substat: SubStat) -> None:
        substat.rarity = self.get_rarity()
        self._substats.append(substat)

    def set_level(self, level: int) -> None:
        self._level = level

    def set_rarity(self, rarity: int) -> None:
        self._rarity = rarity
        stats: list[MainStat | SubStat] = [self.get_mainstat(), *self.get_substats()]
        for stat in stats:
            stat.rarity = rarity

    def set_artifact_set(self, set: str) -> None:
        self._set = set

    def set_artifact_slot(self, slot: str) -> None:
        self._slot = slot

    def get_mainstat(self) -> MainStat:
        if self._mainstat is None:
            raise ValueError("MainStat is not set.")
        return self._mainstat

    def get_substats(self) -> list[SubStat]:
        return self._substats

    def get_level(self) -> int:
        return self._level

    def get_rarity(self) -> int:
        return self._rarity

    def get_artifact_set(self) -> str:
        return self._set

    def get_artifact_slot(self) -> str:
        return self._slot

    def get_strategy(self) -> UpgradeStrategy:
        if len(self.get_substats()) < self.get_rarity() - 1:
            return AddStatStrategy()
        return UpgradeStatStrategy()

    def upgrade(self) -> None:
        self.get_strategy().upgrade(self)

    def __str__(self) -> str:
        return (
            f"{self._slot} [+{self._level}]\n{'★' * self._rarity}\n"
            f"{self._mainstat}\n{'\n'.join(str(s) for s in self._substats)}"
        )
