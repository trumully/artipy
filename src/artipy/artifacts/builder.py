"""Builder class for creating an Artifact object."""

from typing import Optional

from artipy import MAX_RARITY, UPGRADE_STEP
from artipy.stats import MainStat, StatType, SubStat

from .artifact import Artifact
from .upgrade_strategy import AddStatStrategy


class ArtifactBuilder:
    """Builder class for creating an Artifact object.

    Options:
    - with_mainstat: Set the mainstat of the artifact
    - with_substat: Add a substat to the artifact
    - with_substats: Add multiple substats to the artifact
    - with_level: Set the level of the artifact
    - with_rarity: Set the rarity of the artifact
    - with_set: Set the artifact set
    - with_slot: Set the artifact slot
    - build: Build the artifact object based on the parameters passed into the builder
    """

    def __init__(self) -> None:
        self._artifact: Artifact = Artifact()

    def with_mainstat(
        self, stat: StatType, value: float | int = 0
    ) -> "ArtifactBuilder":
        """Set the mainstat of the artifact. The value will be set based on the level of
        the artifact.

        :param stat: The mainstat to set.
        :type stat: StatType
        :param value: The value to set, defaults to 0
        :type value: float | int, optional
        :return: The artifact builder object
        :rtype: ArtifactBuilder
        """
        self._artifact.mainstat = MainStat(stat, value)
        self._artifact.mainstat.set_value_by_level(self._artifact.level)
        return self

    def with_substat(self, stat: StatType, value: float | int) -> "ArtifactBuilder":
        """Add a substat to the artifact.

        :param stat: The substat to add.
        :type stat: StatType
        :param value: The value of the substat.
        :type value: float | int
        :raises ValueError: If the number of substats exceeds the rarity of the artifact
        :return: The artifact builder object
        :rtype: ArtifactBuilder
        """
        if (rarity := self._artifact.rarity) > 0:
            # Constraint: The number of substats can't exceed the rarity of the artifact
            if len(self._artifact.substats) >= rarity - 1:
                raise ValueError("Substats are already full.")
        self._artifact.add_substat(SubStat(stat, value))
        return self

    def with_substats(
        self,
        substats: Optional[list[tuple[StatType, float | int]]] = None,
        *,
        amount: int = 0,
    ) -> "ArtifactBuilder":
        """Add multiple substats to the artifact. If substats is not provided and an
        amount is provided, random substats will be generated.

        :param substats: The substats to add, defaults to None
        :type substats: list[tuple[StatType, float | int]], optional
        :param amount: The amount of substats to add (if none are provided),
                       defaults to 0
        :type amount: int, optional
        :raises ValueError: If the amount is not within the valid range
        :return: The artifact builder object
        :rtype: ArtifactBuilder
        """
        rarity = self._artifact.rarity
        if substats is None:
            substats = []
            # Constraint: The number of substats cannot exceed artifact rarity - 1
            valid_range = range(1, rarity)
            if amount not in valid_range:
                raise ValueError(
                    f"Amount must be between {min(valid_range)} and {max(valid_range)}"
                )

            for _ in range(amount):
                new_stat = AddStatStrategy().pick_stat(self._artifact)
                self._artifact.add_substat(new_stat)
        elif len(substats) > rarity - 1 and rarity > 0:
            # Constraint: The number of substats cannot exceed artifact rarity
            raise ValueError("Too many substats provided.")
        else:
            self._artifact.substats = [SubStat(*spec) for spec in substats]

        return self

    def with_level(self, level: int) -> "ArtifactBuilder":
        """Set the level of the artifact. Set any values that are dependent on the
        level.

        :param level: The level to set.
        :type level: int
        :raises ValueError: If the level is not within the valid range
        :raises ValueError: If the number of substats exceeds the rarity of the artifact
        :return: The artifact builder object
        :rtype: ArtifactBuilder
        """
        if (rarity := self._artifact.rarity) > 0:
            # Constraint: The level cannot exceed the max level for the artifact rarity
            max_level = rarity * UPGRADE_STEP
            expected_range = range(0, max_level + 1)
            if level not in expected_range:
                raise ValueError(
                    f"Invalid level '{level}' for rarity '{rarity}'. "
                    f"(Expected {min(expected_range)}-{max(expected_range)})"
                )

            # Constraint: The number of substats must be less than the rarity.
            if (substat_length := len(self._artifact.substats)) >= rarity:
                raise ValueError(
                    f"Substat length mismatch with rarity '{rarity}' "
                    f"(Expected {rarity} substats, got {substat_length})"
                )
            self._artifact.mainstat.set_value_by_level(level)

        self._artifact.level = level
        return self

    def with_rarity(self, rarity: int) -> "ArtifactBuilder":
        """Set the rarity of the artifact. Set any values that are dependent on the
        rarity.

        :param rarity: The rarity to set.
        :type rarity: int
        :raises ValueError: If the rarity is not within the valid range
        :raises ValueError: If the number of substats exceeds the rarity of the artifact
        :raises ValueError: If the substats are already full
        :return: The artifact builder object
        :rtype: ArtifactBuilder
        """
        if (level := self._artifact.level) > 0:
            # Constraint: The level cannot exceed the max level for the artifact rarity
            max_level = rarity * UPGRADE_STEP
            expected_range = range(0, max_level + 1)
            if level not in expected_range:
                raise ValueError(
                    f"Invalid rarity '{rarity}' for current level '{level}'. "
                    f"(Expected {min(expected_range)}-{max(expected_range)})"
                )
        if rarity not in range(1, MAX_RARITY + 1):
            raise ValueError(f"Invalid rarity '{rarity}' for artifact.")
        if len(self._artifact.substats) >= rarity:
            raise ValueError("Substats are already full.")
        self._artifact.rarity = rarity
        return self

    def with_set(self, artifact_set: str) -> "ArtifactBuilder":
        """Set the artifact set.

        :param set: The set to set.
        :type set: str
        :return: The artifact builder object
        :rtype: ArtifactBuilder
        """
        self._artifact.artifact_set = artifact_set
        return self

    def with_slot(self, slot: str) -> "ArtifactBuilder":
        """Set the artifact slot.

        :param slot: The slot to set.
        :type slot: str
        :return: The artifact builder object
        :rtype: ArtifactBuilder
        """
        self._artifact.artifact_slot = slot
        return self

    def build(self) -> Artifact:
        """Build the artifact object based on the parameters passed into the builder.

        :return: The built artifact object
        :rtype: Artifact
        """
        return self._artifact
