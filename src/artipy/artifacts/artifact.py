"""Module containing the Artifact class."""

from typing import Optional

from artipy import UPGRADE_STEP
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
        """Set the mainstat of the artifact.

        :param mainstat: The mainstat to set.
        :type mainstat: MainStat
        """
        if (rarity := self.get_rarity()) > 0:
            mainstat.rarity = rarity
        self._mainstat = mainstat

    def set_substats(self, substats: list[SubStat]) -> None:
        """Set the substats of the artifact.

        :param substats: The substats to set.
        :type substats: list[SubStat]
        """
        if (rarity := self.get_rarity()) > 0:
            for substat in substats:
                substat.rarity = rarity
        self._substats = substats

    def add_substat(self, substat: SubStat) -> None:
        """Add a substat to the artifact.

        :param substat: The substat to add.
        :type substat: SubStat
        """
        if (rarity := self.get_rarity()) > 0:
            substat.rarity = rarity
        self._substats.append(substat)

    def set_level(self, level: int) -> None:
        """Set the level of the artifact.

        :param level: The level to set.
        :type level: int
        """
        self._level = level

    def set_rarity(self, rarity: int) -> None:
        """Set the rarity of the artifact.

        :param rarity: The rarity to set.
        :type rarity: int
        """
        self._rarity = rarity
        stats: list[MainStat | SubStat] = [self.get_mainstat(), *self.get_substats()]
        for stat in stats:
            try:
                stat.rarity = rarity
            except AttributeError:
                continue

    def set_artifact_set(self, artifact_set: str) -> None:
        """Set the artifact set of the artifact.

        :param set: The set to set.
        :type set: str
        """
        self._set = artifact_set

    def set_artifact_slot(self, slot: str) -> None:
        """Set the artifact slot of the artifact.

        :param slot: The slot to set.
        :type slot: str
        """
        self._slot = slot

    def get_mainstat(self) -> MainStat:
        """Get the mainstat of the artifact. If the mainstat is None, return a
        placeholder.

        :return: The mainstat of the artifact.
        :rtype: MainStat
        """
        if self._mainstat is None:
            return PLACEHOLDER_MAINSTAT
        return self._mainstat

    def get_substats(self) -> list[SubStat]:
        """Get the substats of the artifact.

        :return: The substats of the artifact.
        :rtype: list[SubStat]
        """
        return self._substats

    def get_level(self) -> int:
        """Get the level of the artifact.

        :return: The level of the artifact.
        :rtype: int
        """
        return self._level

    def get_rarity(self) -> int:
        """Get the rarity of the artifact.

        :return: The rarity of the artifact.
        :rtype: int
        """
        return self._rarity

    def get_artifact_set(self) -> str:
        """Get the artifact set of the artifact.

        :return: The artifact set of the artifact.
        :rtype: str
        """
        return self._set

    def get_artifact_slot(self) -> str:
        """Get the artifact slot of the artifact.

        :return: The artifact slot of the artifact.
        :rtype: str
        """
        return self._slot

    def get_strategy(self) -> UpgradeStrategy:
        """Get the upgrade strategy for the artifact. If the number of substats
        is less than the rarity, return an AddStatStrategy, otherwise return an
        UpgradeStatStrategy.

        :return: The upgrade strategy for the artifact.
        :rtype: UpgradeStrategy
        """
        if self.get_rarity() == 1:
            return UpgradeStrategy()
        if len(self.get_substats()) < self.get_rarity() - 1:
            return AddStatStrategy()
        return UpgradeStatStrategy()

    @property
    def max_level(self) -> int:
        rarity = self.get_rarity()
        return rarity * UPGRADE_STEP if rarity > 2 else UPGRADE_STEP

    def upgrade(self) -> None:
        """Upgrade the artifact."""
        if self.get_level() < self.max_level:
            self.get_strategy().upgrade(self)

    def __str__(self) -> str:
        # Black can't format f-strings with double quotes in them
        return (
            f"{self.get_artifact_slot()} [+{self.get_level()}]\n"
            f"{'★' * self.get_rarity()}\n"  # pylint: disable=inconsistent-quotes
            f"{self.get_mainstat()}\n{'\n'.join(str(s) for s in self.get_substats())}"  # pylint: disable=inconsistent-quotes
        )
