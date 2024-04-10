from .artifact import Artifact
from artipy.stats import MainStat, SubStat


class ArtifactBuilder:
    """Builder class for creating an Artifact object."""

    def __init__(self) -> None:
        self._artifact: Artifact = Artifact()

    def with_mainstat(self, mainstat: MainStat) -> "ArtifactBuilder":
        self._artifact.set_mainstat(mainstat)
        return self

    def add_substat(self, substat: SubStat) -> "ArtifactBuilder":
        self._artifact.get_substats().append(substat)
        return self

    def with_substats(self, substats: list[SubStat]) -> "ArtifactBuilder":
        self._artifact.set_substats(substats)
        return self

    def with_level(self, level: int) -> "ArtifactBuilder":
        self._artifact.set_level(level)
        return self

    def with_rarity(self, rarity: int) -> "ArtifactBuilder":
        self._artifact.set_rarity(rarity)
        return self

    def with_set(self, set: str) -> "ArtifactBuilder":
        self._artifact.set_artifact_set(set)
        return self

    def with_slot(self, slot: str) -> "ArtifactBuilder":
        self._artifact.set_artifact_slot(slot)
        return self

    def build(self) -> Artifact:
        return self._artifact
