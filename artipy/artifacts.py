"""Module containing Artifact classes."""

from __future__ import annotations

import random
from collections.abc import Callable
from itertools import starmap

from artipy import MAX_RARITY, UPGRADE_STEP
from artipy.stats import MainStat, SubStat, create_substat
from artipy.types import VALID_ARTIFACT_SETS, ArtifactSet, ArtifactSlot, StatType

from .utils import choose

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
    artifact.mainstat.set_value_by_level(new_level)


def upgrade_artifact(artifact: Artifact) -> None:
    """Upgrade the artifact's level."""
    _level_up_artifact(artifact)


def pick_stat(artifact: Artifact) -> SubStat:
    stats = [s.name for s in (artifact.mainstat, *artifact.substats)]
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
        self._mainstat: MainStat
        self._substats: list[SubStat] = []
        self._level: int = 0
        self._rarity: int = 0
        self._set: ArtifactSet = ArtifactSet.RESOLUTION_OF_SOJOURNER
        self._slot: ArtifactSlot = ArtifactSlot.FLOWER

    @property
    def mainstat(self) -> MainStat:
        """The mainstat of the artifact."""
        return self._mainstat

    @mainstat.setter
    def mainstat(self, mainstat: MainStat) -> None:
        """Set the mainstat of the artifact.

        If the rarity of the artifact is greater than 0, set the rarity of the mainstat.
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
    def artifact_slot(self) -> ArtifactSlot:
        """The artifact slot of the artifact.

        Returns:
            artipy.types.ArtifactSlot | None: The artifact slot of the artifact.
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
        """The upgrade strategy of the artifact.

        If the rarity is 1, the strategy is to only upgrade the artifact's level. Otherwise, if the number of substats
        is less than the rarity - 1, the strategy is to add a new substat. Otherwise, the strategy is to upgrade a
        random substat.

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


class ArtifactBuilder:
    """Builder class for creating an Artifact object.

    Parameters:
        - with_mainstat: Set the mainstat of the artifact
        - with_substat: Add a substat to the artifact
        - with_substats: Add multiple substats to the artifact
        - with_level: Set the level of the artifact
        - with_rarity: Set the rarity of the artifact
        - with_set: Set the artifact set
        - with_slot: Set the artifact slot

    Methods:
        - build: Build the artifact object based on the parameters passed into the builder.
    """

    def __init__(self) -> None:
        self._artifact: Artifact = Artifact()

    def with_mainstat(
        self,
        stat: StatType,
        value: float = 0,
    ) -> ArtifactBuilder:
        """Set the mainstat of the artifact.

        Args:
            stat (artipy.types.StatType): The mainstat to set.
            value (float | int, optional): The value of the mainstat. Defaults to 0.

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        self._artifact.mainstat = MainStat(stat, value)
        self._artifact.mainstat.set_value_by_level(self._artifact.level)
        return self

    def with_substat(self, stat: StatType, value: float) -> ArtifactBuilder:
        """Set a single substat of the artifact.

        Args:
            stat (artipy.types.StatType): The substat to set.
            value (float | int): The value of the substat.

        Raises:
            ValueError: If the substats are already full

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        if (rarity := self._artifact.rarity) > 0 and len(self._artifact.substats) >= rarity - 1:
            msg = "Substats are already full."
            raise ValueError(msg)
        self._artifact.add_substat(SubStat(stat, value))
        return self

    def with_substats(
        self,
        substats: list[tuple[StatType, float]] | None = None,
        *,
        amount: int = 0,
    ) -> ArtifactBuilder:
        """Set the substats of the artifact. If no substats are provided, generate
        random substats based on the rarity of the artifact.

        Args:
            substats (list[tuple[artipy.types.StatType, float]], optional): The
                substats to set. Defaults to None.
            amount (int, optional): The amount of stats to generate. Defaults to 0.

        Raises:
            ValueError: If the amount is not within the valid range
            ValueError: If the number of substats exceeds the rarity of the artifact

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        rarity = self._artifact.rarity
        if substats is not None:
            if len(substats) > rarity - 1 and rarity > 0:
                msg = "Too many substats provided."
                raise ValueError(msg)
            self._artifact.substats = list(starmap(SubStat, substats))

        else:
            substats = []
            valid_range = range(1, rarity)
            if amount not in valid_range:
                msg = f"Amount must be between {min(valid_range)} and {max(valid_range)}"
                raise ValueError(msg)

            for _ in range(amount):
                new_stat = pick_stat(self._artifact)
                self._artifact.add_substat(new_stat)

        return self

    def with_level(self, level: int) -> ArtifactBuilder:
        """Set the level of the artifact. The level determines the value of the
        mainstat.

        Args:
            level (int): The level to set.

        Raises:
            ValueError: If the level is not within the valid range
            ValueError: If there is a substat length mismatch with the rarity

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        if (rarity := self._artifact.rarity) > 0:
            expected_range = range(self._artifact.max_level + 1)
            if level not in expected_range:
                msg = (
                    f"Invalid level '{level}' for rarity '{rarity}'. "
                    f"(Expected {min(expected_range)}-{max(expected_range)})"
                )
                raise ValueError(msg)

            if (substat_length := len(self._artifact.substats)) >= rarity:
                msg = (
                    f"Substat length mismatch with rarity '{rarity}' (Expected {rarity} substats, got {substat_length})"
                )
                raise ValueError(msg)
            self._artifact.mainstat.set_value_by_level(level)

        self._artifact.level = level
        return self

    def with_rarity(self, rarity: int) -> ArtifactBuilder:
        """Set the rarity of the artifact. The rarity determines the number of substats.

        Args:
            rarity (int): The rarity to set.

        Raises:
            ValueError: If the number of substats exceeds the rarity of the artifact
            ValueError: If the rarity is not within the valid range
            ValueError: If the substats are already full

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        if (level := self._artifact.level) > 0:
            max_level = rarity * UPGRADE_STEP if rarity > 2 else UPGRADE_STEP  # noqa: PLR2004
            expected_range = range(max_level + 1)
            if level not in expected_range:
                msg = (
                    f"Invalid rarity '{rarity}' for current level '{level}'. "
                    f"(Expected {min(expected_range)}-{max(expected_range)})"
                )
                raise ValueError(msg)

        if rarity not in range(1, MAX_RARITY + 1):
            msg = f"Invalid rarity '{rarity}' for artifact."
            raise ValueError(msg)

        if len(self._artifact.substats) >= rarity:
            msg = "Substats are already full."
            raise ValueError(msg)

        self._artifact.rarity = rarity
        return self

    def with_set(self, artifact_set: ArtifactSet) -> ArtifactBuilder:
        """Set the artifact set.

        Args:
            artifact_set (artipy.types.ArtifactSet): The artifact set to set.

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        set_data = VALID_ARTIFACT_SETS[artifact_set]
        if (slot := self._artifact.artifact_slot) not in set_data.pieces:
            msg = f"Invalid slot '{slot}' for set '{artifact_set}' (expected: {set_data.pieces})"
            raise ValueError(msg)
        self._artifact.artifact_set = artifact_set
        return self

    def with_slot(self, artifact_slot: ArtifactSlot) -> ArtifactBuilder:
        """Set the artifact slot.

        Args:
            artifact_slot (artipy.types.ArtifactSlot): The artifact slot to set.

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        self._artifact.artifact_slot = artifact_slot
        return self

    def build(self) -> Artifact:
        """Build the artifact object based on the parameters passed into the builder.

        Returns:
            artipy.artifacts.Artifact: The artifact object
        """
        return self._artifact
