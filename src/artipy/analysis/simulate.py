"""This module contains functions to simulate artifacts."""

import random

from artipy.artifacts import Artifact, ArtifactBuilder, utils
from artipy.types import VALID_MAINSTATS, ArtifactSlot


def create_random_artifact(slot: ArtifactSlot, rarity: int = 5) -> Artifact:
    """Create a random artifact.

    Args:
        slot (artipy.types.ArtifactSlot): The slot of the artifact.
        rarity (int, optional): The rarity of the artifact. Defaults to 5.

    Returns:
        artipy.artifacts.Artifact: The random artifact.
    """

    max_substats = rarity - 1
    substat_count = max(0, max_substats if random.random() < 0.2 else max_substats - 1)
    mainstats, mainstat_weights = zip(*VALID_MAINSTATS[slot].items())
    return (
        ArtifactBuilder()
        .with_mainstat(utils.choose(mainstats, mainstat_weights))
        .with_rarity(rarity)
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
