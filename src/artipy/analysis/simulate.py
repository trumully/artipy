"""This module contains functions to simulate artifacts."""

import random

from artipy.artifacts import Artifact, ArtifactBuilder
from artipy.artifacts.utils import choose
from artipy.stats import VALID_MAINSTATS


def create_random_artifact(
    slot: str = random.choice(("flower", "plume", "sands", "goblet", "circlet")),
) -> Artifact:
    """Create a random artifact.

    :return: The random artifact.
    :rtype: Artifact
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

    :param artifact: The artifact to upgrade.
    :type artifact: Artifact
    :return: The upgraded artifact.
    :rtype: Artifact
    """
    while artifact.level < artifact.rarity * 4:
        artifact.upgrade()
    return artifact


def create_multiple_random_artifacts(amount: int = 1) -> list[Artifact]:
    """Create multiple random artifacts.

    :param amount: The amount of artifacts to create, defaults to 1
    :type amount: int, optional
    :return: The list of random artifacts.
    :rtype: list[Artifact]
    """
    result = []
    for _ in range(amount):
        slot = random.choice(("flower", "plume", "sands", "goblet", "circlet"))
        result.append(create_random_artifact(slot))
    return result
