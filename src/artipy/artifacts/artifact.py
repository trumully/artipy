from typing import Optional

from artipy.stats import MainStat, StatType, SubStat

from .upgrade_strategy import AddStatStrategy, UpgradeStatStrategy, UpgradeStrategy

PLACEHOLDER_MAINSTAT = MainStat(StatType.HP, 0)


class Artifact:
    """Class representing an artifact in Genshin Impact."""

    __slots__ = ["_mainstat", "_substats", "_level", "_rarity", "_set", "_slot"]

    def __init__(self) -> None:
        self._mainstat: Optional[MainStat] = None
        self._substats: list[SubStat] = []
        self._level: int = 0
        self._rarity: int = 0
        self._set: str = ""
        self._slot: str = ""

    def set_mainstat(self, mainstat: MainStat) -> None:
        if (rarity := self.get_rarity()) > 0:
            mainstat.rarity = rarity
        self._mainstat = mainstat

    def set_substats(self, substats: list[SubStat]) -> None:
        if (rarity := self.get_rarity()) > 0:
            for substat in substats:
                substat.rarity = rarity
        self._substats = substats

    def add_substat(self, substat: SubStat) -> None:
        if (rarity := self.get_rarity()) > 0:
            substat.rarity = rarity
        self._substats.append(substat)

    def set_level(self, level: int) -> None:
        self._level = level

    def set_rarity(self, rarity: int) -> None:
        self._rarity = rarity
        stats: list[MainStat | SubStat] = [self.get_mainstat(), *self.get_substats()]
        for stat in stats:
            try:
                stat.rarity = rarity
            except AttributeError:
                continue

    def set_artifact_set(self, set: str) -> None:
        self._set = set

    def set_artifact_slot(self, slot: str) -> None:
        self._slot = slot

    def get_mainstat(self) -> MainStat:
        if self._mainstat is None:
            return PLACEHOLDER_MAINSTAT
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
            f"{self.get_artifact_slot()} [+{self.get_level()}]\n"
            f"{'★' * self.get_rarity()}\n"
            f"{self.get_mainstat()}\n{'\n'.join(str(s) for s in self.get_substats())}"
        )
