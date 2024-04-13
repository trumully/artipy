from copy import deepcopy

import pytest

from artipy.artifacts import (
    AddStatStrategy,
    Artifact,
    ArtifactBuilder,
    UpgradeStatStrategy,
)
from artipy.stats import StatType


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


def test_artifact_upgrade(artifact) -> None:
    previous: Artifact = deepcopy(artifact)

    artifact.upgrade()

    assert artifact.get_level() == previous.get_level() + 1
    assert len(artifact.get_substats()) > len(previous.get_substats())
    assert artifact.get_mainstat().value > previous.get_mainstat().value


def test_artifact_upgrade_until_max(artifact) -> None:
    old: Artifact = deepcopy(artifact)

    while artifact.get_level() < 20:
        artifact.upgrade()

    assert artifact.get_level() == 20
    assert len(artifact.get_substats()) == artifact.get_rarity() - 1
    assert artifact.get_mainstat().value > old.get_mainstat().value


def test_artifact_get_strategy(artifact) -> None:
    while len(artifact.get_substats()) < artifact.get_rarity() - 1:
        artifact.upgrade()
        if len(artifact.get_substats()) < artifact.get_rarity() - 1:
            assert isinstance(artifact.get_strategy(), AddStatStrategy)

    assert isinstance(artifact.get_strategy(), UpgradeStatStrategy)


def test_artifact_str(artifact) -> None:
    assert str(artifact) == (
        f"{artifact.get_artifact_slot()} [+{artifact.get_level()}]\n"
        f"{'★' * artifact.get_rarity()}\n{artifact.get_mainstat()}\n"
        f"{'\n'.join(str(s) for s in artifact.get_substats())}"
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
