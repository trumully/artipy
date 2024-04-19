"""This module contains functions to simulate artifacts."""

import random

from artipy.artifacts import Artifact, ArtifactBuilder
from artipy.artifacts.utils import choose
from artipy.types import VALID_MAINSTATS, ArtifactSlot


def create_random_artifact(slot: ArtifactSlot) -> Artifact:
    """Create a random artifact.

    Args:
        slot (artipy.types.ArtifactSlot): The slot of the artifact.

    Returns:
        artipy.artifacts.Artifact: The random artifact.
    """

    substat_count = 4 if random.random() < 0.2 else 3
    mainstats, mainstat_weights = zip(*VALID_MAINSTATS[slot].items())
    return (
        ArtifactBuilder()
        .with_mainstat(choose(mainstats, mainstat_weights))
        .with_rarity(5)
        .with_substats(amount=substat_count)
        .with_slot(slot)
        .build()
    )


def upgrade_artifact_to_max(artifact: Artifact) -> Artifact:
    """Upgrade an artifact to its maximum level.

    Args:
        artifact (artipy.artifacts.Artifact): The artifact to upgrade.

    Returns:
        artipy.artifacts.Artifact: The upgraded artifact.
    """
    while artifact.level < artifact.rarity * 4:
        artifact.upgrade()
    return artifact


def create_multiple_random_artifacts(amount: int = 1) -> list[Artifact]:
    """Create multiple random artifacts.

    Args:
        amount (int, optional): The amount of artifacts to generate. Defaults to 1.

    Returns:
        list[artipy.artifacts.Artifact]: The list of random artifacts.
    """
    result = []
    for _ in range(amount):
        slot: ArtifactSlot = ArtifactSlot(random.choice(list(ArtifactSlot)))
        result.append(create_random_artifact(slot))
    return result
