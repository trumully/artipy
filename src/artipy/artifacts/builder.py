from .artifact import Artifact
from .upgrade_strategy import AddStatStrategy
from artipy.stats import MainStat, SubStat


class ArtifactBuilder:
    """Builder class for creating an Artifact object."""

    def __init__(self) -> None:
        self._artifact: Artifact = Artifact()

    def with_mainstat(self, mainstat: MainStat) -> "ArtifactBuilder":
        """Set the mainstat of the artifact."""
        self._artifact.set_mainstat(mainstat)
        return self

    def with_substat(self, substat: SubStat) -> "ArtifactBuilder":
        """Add a substat to the artifact."""
        self._artifact.add_substat(substat)
        return self

    def with_substats(
        self, substats: list[SubStat] = [], *, amount: int = 0
    ) -> "ArtifactBuilder":
        """Add multiple substats to the artifact. If substats is not provided and an
        amount is provided, random substats will be generated.

        :param substats: The substats to add, defaults to []
        :type substats: list[SubStat], optional
        :param amount: The amount of substats to add (if none are provided),
                       defaults to 0
        :type amount: int, optional
        :raises ValueError: If the amount is not within the valid range
        """
        if not substats:
            # Check if the specified amount of substats is within the valid range
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

        # Add the provided/generated substats to the artifact
        self._artifact.set_substats(substats)

        return self

    def with_level(self, level: int) -> "ArtifactBuilder":
        """Set the level of the artifact."""
        self._artifact.set_level(level)
        return self

    def with_rarity(self, rarity: int) -> "ArtifactBuilder":
        """Set the rarity of the artifact."""
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
