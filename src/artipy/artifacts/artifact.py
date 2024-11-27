"""Module containing the Artifact class."""

from __future__ import annotations

import random
from collections.abc import Callable
from typing import TYPE_CHECKING

from artipy import UPGRADE_STEP
from artipy.stats.substat import create_substat
from artipy.types import VALID_ARTIFACT_SETS, ArtifactSet, ArtifactSlot, StatType

from .utils import choose

if TYPE_CHECKING:
    from artipy.stats import MainStat, SubStat

substat_weights: dict[StatType, float] = {
    StatType.HP: 6,
    StatType.ATK: 6,
    StatType.DEF: 6,
    StatType.HP_PERCENT: 4,
    StatType.ATK_PERCENT: 4,
    StatType.DEF_PERCENT: 4,
    StatType.ENERGY_RECHARGE: 4,
    StatType.ELEMENTAL_MASTERY: 4,
    StatType.CRIT_RATE: 3,
    StatType.CRIT_DMG: 3,
}

type UpgradeMethod = Callable[[Artifact], None]


def _level_up_artifact(artifact: Artifact) -> None:
    new_level = artifact.level + 1
    artifact.level = new_level
    if artifact.mainstat is not None:
        artifact.mainstat.set_value_by_level(new_level)


def upgrade_artifact(artifact: Artifact) -> None:
    """Upgrade the artifact's level."""
    _level_up_artifact(artifact)


def pick_stat(artifact: Artifact) -> SubStat:
    stats = [s.name for s in (artifact.mainstat, *artifact.substats) if s is not None]
    pool = {s: w for s, w in substat_weights.items() if s not in stats}
    population, weights = map(tuple, zip(*pool.items(), strict=False))
    new_stat_name = choose(population, weights)
    new_stat = create_substat(name=new_stat_name, rarity=artifact.rarity)
    return new_stat


def upgrade_artifact_new_stat(artifact: Artifact) -> None:
    """Upgrade the artifact's level and add a new substat if the level is divisible by the upgrade step."""
    if artifact.level % UPGRADE_STEP == 0:
        new_stat = pick_stat(artifact)
        artifact.add_substat(new_stat)
    _level_up_artifact(artifact)


def upgrade_artifact_upgrade_stat(artifact: Artifact) -> None:
    """Upgrade the artifact's level and upgrade a random substat if the level is divisible by the upgrade step."""
    if artifact.level % UPGRADE_STEP == 0:
        substat = random.choice(artifact.substats)
        substat.upgrade()
    _level_up_artifact(artifact)


class Artifact:
    """Class representing an artifact in Genshin Impact."""

    __slots__ = ("_level", "_mainstat", "_rarity", "_set", "_slot", "_substats")

    def __init__(self) -> None:
        self._mainstat: MainStat | None = None
        self._substats: list[SubStat] = []
        self._level: int = 0
        self._rarity: int = 0
        self._set: ArtifactSet | None = None
        self._slot: ArtifactSlot | None = None

    @property
    def mainstat(self) -> MainStat | None:
        """The mainstat of the artifact. Return a placeholder mainstat if the mainstat
        is None.

        Returns:
            Optional[artipy.stats.MainStat]: The mainstat of the artifact.
        """
        return self._mainstat

    @mainstat.setter
    def mainstat(self, mainstat: MainStat) -> None:
        """Set the mainstat of the artifact. If the rarity of the artifact is greater
        than 0, set the rarity of the mainstat.

        Args:
            mainstat (artipy.stats.MainStat): The mainstat to set.
        """
        if self.rarity > 0:
            mainstat.rarity = self.rarity
        self._mainstat = mainstat

    @property
    def substats(self) -> list[SubStat]:
        """The substats of the artifact.

        Returns:
            list[artipy.stats.SubStat]: The substats of the artifact.
        """
        return self._substats

    @substats.setter
    def substats(self, substats: list[SubStat]) -> None:
        """Set the substats of the artifact. If the rarity of the artifact is greater
        than 0, set the rarity of the substats.

        Args:
            substats (list[artipy.stats.SubStat]): _description_
        """
        if self.rarity > 0:
            for substat in substats:
                substat.rarity = self.rarity
        self._substats = substats

    def add_substat(self, substat: SubStat) -> None:
        """Add a substat to the artifact. If the rarity of the artifact is greater
        than 0, set the rarity of the substat.

        Args:
            substat (artipy.stats.SubStat): The substat to add.
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
        stats: list[MainStat | SubStat | None] = [self.mainstat, *self.substats]
        for stat in stats:
            try:
                if stat is not None:
                    stat.rarity = rarity
            except AttributeError:
                continue

    @property
    def artifact_set(self) -> ArtifactSet | None:
        """The artifact set of the artifact.

        Returns:
            Optional[artipy.types.ArtifactSet]: The artifact set of the artifact.
        """
        return self._set

    @artifact_set.setter
    def artifact_set(self, artifact_set: ArtifactSet) -> None:
        """Set the artifact set of the artifact.

        Args:
            artifact_set (artipy.types.ArtifactSet): The artifact set to set.
        """
        self._set = artifact_set

    @property
    def artifact_slot(self) -> ArtifactSlot | None:
        """The artifact slot of the artifact.

        Returns:
            Optional[artipy.types.ArtifactSlot]: The artifact slot of the artifact.
        """
        return self._slot

    @artifact_slot.setter
    def artifact_slot(self, slot: ArtifactSlot) -> None:
        """Set the artifact slot of the artifact.

        Args:
            slot (artipy.types.ArtifactSlot): The artifact slot to set.
        """
        self._slot = slot

    @property
    def upgrade_method(self) -> UpgradeMethod:
        """The upgrade strategy of the artifact. If the rarity is 1, the strategy
        inheriters are skipped in favor of the default strategy. Otherwise, if the
        number of substats is less than the rarity - 1, the add stat strategy is
        returned. Otherwise, the upgrade stat strategy is returned.

        Returns:
            UpgradeMethod: The upgrade strategy of the artifact.
        """
        if self.rarity == 1:
            return upgrade_artifact
        if len(self.substats) < self.rarity - 1:
            return upgrade_artifact_new_stat
        return upgrade_artifact_upgrade_stat

    @property
    def max_level(self) -> int:
        return self.rarity * UPGRADE_STEP if self.rarity > 2 else UPGRADE_STEP  # noqa: PLR2004

    def upgrade(self) -> None:
        """Upgrade the artifact."""
        if self.level < self.max_level:
            self.upgrade_method(self)

    def __str__(self) -> str:
        set_name = VALID_ARTIFACT_SETS[self.artifact_set].set_name if self.artifact_set is not None else "Example"
        return (
            f"{self.artifact_slot} [+{self.level}]\n"
            f"{set_name} {'★' * self.rarity}\n"
            f"{self.mainstat}\n{'\n'.join(str(s) for s in self.substats)}"
        )
