import random
from copy import deepcopy

import pytest
from artipy import UPGRADE_STEP
from artipy.artifacts import (
    AddStatStrategy,
    Artifact,
    ArtifactBuilder,
    UpgradeStatStrategy,
)
from artipy.stats import VALID_SUBSTATS, StatType
from hypothesis import assume, given
from hypothesis import strategies as st


@pytest.fixture
def artifact() -> Artifact:
    return (
        ArtifactBuilder()
        .with_mainstat(StatType.HP, 0)
        .with_substat(StatType.HP_PERCENT, 5)
        .with_rarity(5)
        .with_level(0)
        .with_set("Gladiator's Finale")
        .with_slot("Flower of Life")
        .build()
    )


@given(
    level=st.integers(min_value=0, max_value=20),
    rarity=st.integers(min_value=1, max_value=5),
)
def test_artifact_upgrade(level: int, rarity: int) -> None:
    """Test the upgrade method of the Artifact class. This test verifies that the
    level of the artifact increases by 1 and the mainstat value increases after
    upgrading.

    Args:
        level (int): The level of the artifact.
        rarity (int): The rarity of the artifact.
    """
    max_level = rarity * UPGRADE_STEP if rarity > 2 else UPGRADE_STEP
    assume(level <= max_level)
    builder = (
        ArtifactBuilder()
        .with_mainstat(StatType.HP, 0)
        .with_rarity(rarity)
        .with_level(level)
        .with_set("Gladiator's Finale")
        .with_slot("Flower of Life")
    )

    substat_count = rarity - 2 if rarity > 1 else 0
    substat_sample = random.sample(VALID_SUBSTATS, substat_count)
    for sub in substat_sample:
        builder = builder.with_substat(sub, 5)

    artifact: Artifact = builder.build()
    previous: Artifact = deepcopy(artifact)

    if artifact.level < max_level:
        artifact.upgrade()

        assert artifact.level == previous.level + 1
        assert artifact.mainstat.value > previous.mainstat.value


@given(
    level=st.integers(min_value=0, max_value=20),
    rarity=st.integers(min_value=1, max_value=5),
)
def test_artifact_upgrade_until_max(level: int, rarity: int) -> None:
    max_level = rarity * UPGRADE_STEP if rarity > 2 else UPGRADE_STEP
    assume(level < max_level)
    builder = (
        ArtifactBuilder()
        .with_mainstat(StatType.HP, 0)
        .with_rarity(rarity)
        .with_level(level)
        .with_set("Gladiator's Finale")
        .with_slot("Flower of Life")
    )
    artifact = builder.build()
    old: Artifact = deepcopy(artifact)

    while artifact.level < max_level:
        artifact.upgrade()

    assert artifact.level == max_level
    assert artifact.mainstat.value > old.mainstat.value

    # Upgrade again
    artifact.upgrade()

    assert artifact.level == max_level


def test_artifact_get_strategy(artifact) -> None:
    while len(artifact.substats) < artifact.rarity - 1:
        artifact.upgrade()
        if len(artifact.substats) < artifact.rarity - 1:
            assert isinstance(artifact.strategy, AddStatStrategy)

    assert isinstance(artifact.strategy, UpgradeStatStrategy)


def test_artifact_str(artifact) -> None:
    assert str(artifact) == (
        f"{artifact.artifact_slot} [+{artifact.level}]\n"
        f"{'★' * artifact.rarity}\n{artifact.mainstat}\n"
        f"{'\n'.join(str(s) for s in artifact.substats)}"
    )


def test_builder_constraint_substats() -> None:
    # Case 1: Rarity is 5, so the number of substats can't exceed 4
    with pytest.raises(ValueError):
        (
            ArtifactBuilder()
            .with_substat(StatType.HP, 0)
            .with_substat(StatType.HP, 0)
            .with_substat(StatType.HP, 0)
            .with_substat(StatType.HP, 0)
            .with_substat(StatType.HP, 0)
            .with_rarity(5)
        )

    # Case 2: Rarity is 4, so the number of substats can't exceed 3
    with pytest.raises(ValueError):
        (ArtifactBuilder().with_substats(amount=4))


def test_builder_constraint_rarity() -> None:
    # Case 1: Rarity must not exceed 5
    with pytest.raises(ValueError):
        ArtifactBuilder().with_rarity(6)

    # Case 2: Rarity must not be less than 1
    with pytest.raises(ValueError):
        ArtifactBuilder().with_rarity(0)
