import math
from decimal import Decimal

import pytest
from artipy.analysis import (
    calculate_artifact_crit_value,
    calculate_artifact_maximum_roll_value,
    calculate_artifact_roll_value,
    calculate_substat_roll_value,
    calculate_substat_rolls,
)
from artipy.artifacts import Artifact, ArtifactBuilder
from artipy.stats import SubStat
from artipy.types import ArtifactSet, ArtifactSlot, StatType


@pytest.fixture
def substat() -> SubStat:
    """This fixture creates a substat with the following properties:
    roll value = ~1.9 (190%)
    rolls = 2

    :return: A substat object
    :rtype: SubStat
    """
    return SubStat(StatType.HP, 568, 5)


@pytest.fixture
def artifact() -> Artifact:
    """This fixture creates an artifact with the following properties:
    roll value = ~4.8 (480%)
    max roll value = ~7.8 (780%)
    crit value = ~7.8
    rolls = 5

    :return: An artifact object
    :rtype: Artifact
    """
    return (
        ArtifactBuilder()
        .with_mainstat(StatType.ATK_PERCENT, 0.228)
        .with_substats([
            (StatType.ATK, 19),
            (StatType.CRIT_RATE, 0.039),
            (StatType.HP_PERCENT, 0.053),
            (StatType.HP, 568),
        ])
        .with_level(8)
        .with_rarity(5)
        .with_slot(ArtifactSlot.SANDS)
        .with_set(ArtifactSet.GLADIATORS_FINALE)
        .build()
    )


def test_calculate_substat_roll_value(substat) -> None:
    """This test verifies the roll_value of a given substat"""
    roll_value = calculate_substat_roll_value(substat)
    assert math.isclose(roll_value, Decimal(1.9), rel_tol=1e-2)


def test_calculate_substat_rolls(substat, artifact) -> None:
    """This test verifies the number of rolls of a given substat"""
    assert calculate_substat_rolls(substat) == 2

    expected_rolls = (1, 1, 1, 2)
    for idx, sub in enumerate(artifact.substats):
        assert calculate_substat_rolls(sub) == expected_rolls[idx]


def test_calcualte_artifact_roll_value(artifact) -> None:
    """This test verifies the roll value of the artifact"""
    roll_value = calculate_artifact_roll_value(artifact)
    assert math.isclose(roll_value, Decimal(4.8), rel_tol=1e-2)


def test_calculate_artifact_maximum_roll_value(artifact) -> None:
    """This test verifies the maximum roll value of the artifact"""
    maximum_roll_value = calculate_artifact_maximum_roll_value(artifact)
    assert math.isclose(maximum_roll_value, Decimal(7.8), rel_tol=1e-2)


def test_calculate_artifact_crit_value(artifact) -> None:
    """This test verifies the crit value of the artifact"""
    crit_value = calculate_artifact_crit_value(artifact)
    assert math.isclose(crit_value, Decimal(7.8), rel_tol=1e-2)
