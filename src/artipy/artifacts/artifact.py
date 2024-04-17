"""Module containing the Artifact class."""

from typing import Optional

from artipy import UPGRADE_STEP
from artipy.stats import MainStat, SubStat
from artipy.types import ArtifactSet, ArtifactSlot

from .upgrade_strategy import AddStatStrategy, UpgradeStatStrategy, UpgradeStrategy


class Artifact:
    """Class representing an artifact in Genshin Impact."""

    __slots__ = ["_mainstat", "_substats", "_level", "_rarity", "_set", "_slot"]

    def __init__(self) -> None:
        self._mainstat: Optional[MainStat] = None
        self._substats: list[SubStat] = []
        self._level: int = 0
        self._rarity: int = 0
        self._set: Optional[ArtifactSet] = None
        self._slot: Optional[ArtifactSlot] = None

    @property
    def mainstat(self) -> Optional[MainStat]:
        """The mainstat of the artifact. Return a placeholder mainstat if the mainstat
        is None.

        Returns:
            Optional[MainStat]: The mainstat of the artifact.
        """
        return self._mainstat

    @mainstat.setter
    def mainstat(self, mainstat: MainStat) -> None:
        """Set the mainstat of the artifact. If the rarity of the artifact is greater
        than 0, set the rarity of the mainstat.

        Args:
            mainstat (MainStat): The mainstat to set.
        """
        if self.rarity > 0:
            mainstat.rarity = self.rarity
        self._mainstat = mainstat

    @property
    def substats(self) -> list[SubStat]:
        """The substats of the artifact.

        Returns:
            list[SubStat]: The substats of the artifact.
        """
        return self._substats

    @substats.setter
    def substats(self, substats: list[SubStat]) -> None:
        """Set the substats of the artifact. If the rarity of the artifact is greater
        than 0, set the rarity of the substats.
        """
        if self.rarity > 0:
            for substat in substats:
                substat.rarity = self.rarity
        self._substats = substats

    def add_substat(self, substat: SubStat) -> None:
        """Add a substat to the artifact. If the rarity of the artifact is greater
        than 0, set the rarity of the substat.

        Args:
            substat (SubStat): The substat to add.
        """
        if self.rarity > 0:
            substat.rarity = self.rarity
        self._substats.append(substat)

    @property
    def level(self) -> int:
        """The level of the artifact.

        Returns:
            int: The level of the artifact.
        """
        return self._level

    @level.setter
    def level(self, level: int) -> None:
        """Set the level of the artifact.

        Args:
            level (int): The level to set.
        """
        self._level = level

    @property
    def rarity(self) -> int:
        """The rarity of the artifact.

        Returns:
            int: The rarity of the artifact.
        """
        return self._rarity

    @rarity.setter
    def rarity(self, rarity: int) -> None:
        """Set the rarity of the artifact. If the rarity of the artifact is greater
        than 0, set the rarity of the mainstat and substats.

        Args:
            rarity (int): The rarity to set.
        """
        self._rarity = rarity
        stats: list[Optional[MainStat] | SubStat] = [self.mainstat, *self.substats]
        for stat in stats:
            try:
                if stat is not None:
                    stat.rarity = rarity
            except AttributeError:
                continue

    @property
    def artifact_set(self) -> Optional[ArtifactSet]:
        """The artifact set of the artifact.

        Returns:
            Optional[ArtifactSet]: The artifact set of the artifact.
        """
        return self._set

    @artifact_set.setter
    def artifact_set(self, artifact_set: ArtifactSet) -> None:
        """Set the artifact set of the artifact.

        Args:
            artifact_set (ArtifactSet): The artifact set to set.
        """
        self._set = artifact_set

    @property
    def artifact_slot(self) -> Optional[ArtifactSlot]:
        """The artifact slot of the artifact.

        Returns:
            Optional[ArtifactSlot]: The artifact slot of the artifact.
        """
        return self._slot

    @artifact_slot.setter
    def artifact_slot(self, slot: ArtifactSlot) -> None:
        """Set the artifact slot of the artifact.

        Args:
            slot (ArtifactSlot): The artifact slot to set.
        """
        self._slot = slot

    @property
    def strategy(self) -> UpgradeStrategy:
        """The upgrade strategy of the artifact. If the rarity is 1, the strategy
        inheriters are skipped in favor of the default strategy. Otherwise, if the
        number of substats is less than the rarity - 1, the add stat strategy is
        returned. Otherwise, the upgrade stat strategy is returned.

        Returns:
            UpgradeStrategy: The upgrade strategy of the artifact.
        """
        if self.rarity == 1:
            return UpgradeStrategy()
        if len(self.substats) < self.rarity - 1:
            return AddStatStrategy()
        return UpgradeStatStrategy()

    @property
    def max_level(self) -> int:
        return self.rarity * UPGRADE_STEP if self.rarity > 2 else UPGRADE_STEP

    def upgrade(self) -> None:
        """Upgrade the artifact."""
        if self.level < self.max_level:
            self.strategy.upgrade(self)

    def __str__(self) -> str:
        # Black can't format f-strings with double quotes in them
        return (
            f"{self.artifact_slot} [+{self.level}]\n"
            f"{'★' * self.rarity}\n"  # pylint: disable=inconsistent-quotes
            f"{self.mainstat}\n{'\n'.join(str(s) for s in self.substats)}"  # pylint: disable=inconsistent-quotes
        )
