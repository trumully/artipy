"""Builder class for creating an Artifact object."""

from __future__ import annotations

from typing import Optional

from artipy import MAX_RARITY, UPGRADE_STEP
from artipy.stats import MainStat, SubStat
from artipy.types import VALID_ARTIFACT_SETS, ArtifactSet, ArtifactSlot, StatType

from .artifact import Artifact
from .upgrade_strategy import AddStatStrategy


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
        - build: Build the artifact object based on the parameters passed into the
                 builder.
    """

    def __init__(self) -> None:
        self._artifact: Artifact = Artifact()

    def with_mainstat(
        self, stat: StatType, value: float | int = 0
    ) -> "ArtifactBuilder":
        """Set the mainstat of the artifact.

        Args:
            stat (StatType): The mainstat to set.
            value (float | int, optional): The value of the mainstat. Defaults to 0.

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        self._artifact.mainstat = MainStat(stat, value)
        self._artifact.mainstat.set_value_by_level(self._artifact.level)
        return self

    def with_substat(self, stat: StatType, value: float | int) -> "ArtifactBuilder":
        """Set a single substat of the artifact.

        Args:
            stat (StatType): The substat to set.
            value (float | int): The value of the substat.

        Raises:
            ValueError: If the substats are already full

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        if (rarity := self._artifact.rarity) > 0:
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
        """Set the substats of the artifact. If no substats are provided, generate
        random substats based on the rarity of the artifact.

        Args:
            substats (Optional[list[tuple[StatType, float  |  int]]], optional): The
                substats to set. Defaults to None.
            amount (int, optional): The amount of stats to generate. Defaults to 0.

        Raises:
            ValueError: If the amount is not within the valid range
            ValueError: If the number of substats exceeds the rarity of the artifact

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        rarity = self._artifact.rarity
        if substats is None:
            substats = []
            valid_range = range(1, rarity)
            if amount not in valid_range:
                raise ValueError(
                    f"Amount must be between {min(valid_range)} and {max(valid_range)}"
                )

            for _ in range(amount):
                new_stat = AddStatStrategy().pick_stat(self._artifact)
                self._artifact.add_substat(new_stat)
        elif len(substats) > rarity - 1 and rarity > 0:
            raise ValueError("Too many substats provided.")
        else:
            self._artifact.substats = [SubStat(*spec) for spec in substats]

        return self

    def with_level(self, level: int) -> "ArtifactBuilder":
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
            expected_range = range(0, self._artifact.max_level + 1)
            if level not in expected_range:
                raise ValueError(
                    f"Invalid level '{level}' for rarity '{rarity}'. "
                    f"(Expected {min(expected_range)}-{max(expected_range)})"
                )

            if (substat_length := len(self._artifact.substats)) >= rarity:
                raise ValueError(
                    f"Substat length mismatch with rarity '{rarity}' "
                    f"(Expected {rarity} substats, got {substat_length})"
                )
            if self._artifact.mainstat is not None:
                self._artifact.mainstat.set_value_by_level(level)

        self._artifact.level = level
        return self

    def with_rarity(self, rarity: int) -> "ArtifactBuilder":
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
            max_level = rarity * UPGRADE_STEP if rarity > 2 else UPGRADE_STEP
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

    def with_set(self, artifact_set: ArtifactSet) -> "ArtifactBuilder":
        """Set the artifact set.

        Args:
            artifact_set (ArtifactSet): The artifact set to set.

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        set_data = VALID_ARTIFACT_SETS[artifact_set]
        if self._artifact.artifact_slot is not None:
            if self._artifact.artifact_slot not in set_data.pieces:
                raise ValueError(
                    f"Invalid slot '{self._artifact.artifact_slot}' for set "
                    f"'{artifact_set}' (expected: {set_data.pieces})"
                )
        self._artifact.artifact_set = artifact_set
        return self

    def with_slot(self, artifact_slot: ArtifactSlot) -> "ArtifactBuilder":
        """Set the artifact slot.

        Args:
            artifact_slot (ArtifactSlot): The artifact slot to set.

        Returns:
            ArtifactBuilder: The artifact builder object
        """
        self._artifact.artifact_slot = artifact_slot
        return self

    def build(self) -> Artifact:
        """Build the artifact object based on the parameters passed into the builder.

        Returns:
            Artifact: The artifact object
        """
        return self._artifact
