from artipy import UPGRADE_STEP
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

    def with_mainstat(self, stat: StatType, value: float | int) -> "ArtifactBuilder":
        """Set the mainstat of the artifact."""
        try:
            self._artifact.get_mainstat()
        except ValueError:
            self._artifact.set_mainstat(MainStat(stat, value))
            return self
        # Constraint: The mainstat can only be set once
        raise ValueError("MainStat is already set.")

    def with_substat(self, stat: StatType, value: float | int) -> "ArtifactBuilder":
        """Add a substat to the artifact."""
        # Constraint: The number of substats cannot exceed the rarity of the artifact
        if len(self._artifact.get_substats()) >= self._artifact.get_rarity() - 1:
            raise ValueError("Substats are already full.")
        self._artifact.add_substat(SubStat(stat, value))
        return self

    def with_substats(
        self, substats: list[tuple[StatType, float | int]] = [], *, amount: int = 0
    ) -> "ArtifactBuilder":
        """Add multiple substats to the artifact. If substats is not provided and an
        amount is provided, random substats will be generated.

        :param substats: The substats to add, defaults to []
        :type substats: list[tuple[StatType, float | int]], optional
        :param amount: The amount of substats to add (if none are provided),
                       defaults to 0
        :type amount: int, optional
        :raises ValueError: If the amount is not within the valid range
        """
        if not substats:
            # Constraint: The number of substats cannot exceed artifact rarity - 1
            valid_range = range(1, self._artifact.get_rarity())
            if amount not in valid_range:
                raise ValueError(
                    f"Amount must be between {min(valid_range)} and {max(valid_range)}"
                )

            # Generate random substats
            strategy = AddStatStrategy()
            for _ in range(amount):
                new_stat = strategy.pick_stat(self._artifact)
                self._artifact.add_substat(new_stat)
        else:
            # Constraint: The number of substats cannot exceed artifact rarity
            if len(substats) > self._artifact.get_rarity() - 1:
                raise ValueError("Too many substats provided.")

            # Add the provided substats to the artifact
            self._artifact.set_substats([SubStat(*spec) for spec in substats])

        return self

    def with_level(self, level: int) -> "ArtifactBuilder":
        """Set the level of the artifact."""
        if (rarity := self._artifact.get_rarity()) > 0:
            # Constraint: The level cannot exceed the max level for the artifact rarity
            max_level = rarity * UPGRADE_STEP
            expected_range = range(0, max_level + 1)
            if level not in expected_range:
                raise ValueError(
                    f"Invalid level '{level}' for rarity '{rarity}'. "
                    f"(Expected {min(expected_range)}-{max(expected_range)})"
                )

        self._artifact.set_level(level)
        return self

    def with_rarity(self, rarity: int) -> "ArtifactBuilder":
        """Set the rarity of the artifact."""
        if (level := self._artifact.get_level()) > 0:
            # Constraint: The level cannot exceed the max level for the artifact rarity
            max_level = rarity * UPGRADE_STEP
            expected_range = range(0, max_level + 1)
            if level not in expected_range:
                raise ValueError(
                    f"Invalid rarity '{rarity}' for current level '{level}'. "
                    f"(Expected {min(expected_range)}-{max(expected_range)})"
                )
        self._artifact.set_rarity(rarity)
        return self

    def with_set(self, set: str) -> "ArtifactBuilder":
        """Set the artifact set."""
        self._artifact.set_artifact_set(set)
        return self

    def with_slot(self, slot: str) -> "ArtifactBuilder":
        """Set the artifact slot."""
        self._artifact.set_artifact_slot(slot)
        return self

    def build(self) -> Artifact:
        """Build the artifact object based on the parameters passed into the builder.

        :return: The built artifact object
        :rtype: Artifact
        """
        return self._artifact
