"""This module contains functions for analysing artifacts and their rolls."""

import itertools
import math
from decimal import Decimal
from enum import StrEnum, auto

from artipy.artifacts import Artifact
from artipy.artifacts.upgrade_strategy import UPGRADE_STEP
from artipy.stats import SubStat
from artipy.stats.utils import possible_substat_values
from artipy.types import StatType

ROLL_MULTIPLIERS: dict[int, tuple[float, ...]] = {
    1: (0.8, 1.0),
    2: (0.7, 0.85, 1.0),
    3: (0.7, 0.8, 0.9, 1.0),
    4: (0.7, 0.8, 0.9, 1.0),
    5: (0.7, 0.8, 0.9, 1.0),
}


class RollMagnitude(StrEnum):
    """The roll magnitude of a substat. This is a measure of how much the substat has
    been increased in relation to its maximum potential value."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    MAX = auto()

    @property
    def magnitude(self) -> Decimal:
        """Get the magnitude of the roll magnitude.

        Returns:
            Decimal: The magnitude of the roll magnitude.
        """
        if self == RollMagnitude.LOW:
            return Decimal("0.7")
        elif self == RollMagnitude.MEDIUM:
            return Decimal("0.8")
        elif self == RollMagnitude.HIGH:
            return Decimal("0.9")
        return Decimal("1.0")

    @classmethod
    def closest(cls, value: Decimal | float | int) -> "RollMagnitude":
        """The closest roll magnitude to a value.

        Args:
            value (Decimal | float | int): The value to find the closest roll magnitude

        Returns:
            RollMagnitude: The closest roll magnitude to the value.
        """
        return RollMagnitude(
            min(cls, key=lambda x: abs(RollMagnitude(x).magnitude - Decimal(value)))
        )


def calculate_substat_roll_value(substat: SubStat) -> Decimal:
    """Calculate the substat roll value. This is the value of the substat divided by the
    highest possible value of the substat.

    Args:
        substat (artipy.stats.SubStat): The substat to calculate the roll value for.

    Returns:
        Decimal: The roll value of the substat.
    """
    stat_value = substat.value
    highest_value = max(possible_substat_values(substat.name, substat.rarity))

    if substat.name.is_pct:
        stat_value *= 100
        highest_value *= 100

    return stat_value / highest_value


def calculate_substat_rolls(substat: SubStat) -> int:
    """Calculate the number of rolls of a substat. This is the difference between the
    actual roll value and the average roll value divided by the average roll value.

    Args:
        substat (artipy.stats.SubStat): The substat to calculate the rolls for.

    Returns:
        int: The number of rolls of the substat.
    """
    possible_rolls = possible_substat_values(substat.name, substat.rarity)
    average_roll = Decimal(sum(possible_rolls) / len(possible_rolls))
    return math.ceil((substat.value - average_roll) / average_roll)


def calculate_substat_roll_magnitudes(substat: SubStat) -> tuple[RollMagnitude, ...]:
    """Calculate the roll magnitudes of a substat. This is the closest roll magnitude
    to the actual roll value for each roll.

    Args:
        substat (artipy.stats.SubStat): The substat to calculate the roll magnitudes
                                        for.

    Returns:
        tuple[RollMagnitude, ...]: The roll magnitudes of the substat.
    """

    def get_magnitude(
        values: tuple[Decimal, ...], value_to_index: Decimal
    ) -> RollMagnitude:
        index = values.index(value_to_index)
        return RollMagnitude.closest(ROLL_MULTIPLIERS[substat.rarity][index])

    possible_rolls = possible_substat_values(substat.name, substat.rarity)
    rolls_actual = calculate_substat_rolls(substat)

    combinations = list(
        itertools.combinations_with_replacement(possible_rolls, rolls_actual)
    )
    combination = min(combinations, key=lambda x: abs(sum(x) - substat.value))
    return tuple(get_magnitude(possible_rolls, value) for value in combination)


def calculate_artifact_roll_value(artifact: Artifact) -> Decimal:
    """Calculate the roll value of an artifact. This is the sum of the roll values of
    all substats.

    Args:
        artifact (artipy.artifacts.Artifact): The artifact to calculate the roll value

    Returns:
        Decimal: The roll value of the artifact.
    """
    return Decimal(
        sum(calculate_substat_roll_value(substat) for substat in artifact.substats)
    )


def calculate_artifact_maximum_roll_value(artifact: Artifact) -> Decimal:
    """Calculate the maximum roll value of an artifact. This is the roll value of the
    artifact with all remaining rolls being maximum rolls.

    Args:
        artifact (artipy.artifacts.Artifact): The artifact to calculate the maximum

    Returns:
        Decimal: The maximum roll value of the artifact.
    """
    artifact_max_level = artifact.rarity * 4
    remaining_rolls = (artifact_max_level - artifact.level) // UPGRADE_STEP
    return Decimal(calculate_artifact_roll_value(artifact) + remaining_rolls)


def calculate_artifact_crit_value(artifact: Artifact) -> Decimal:
    """Calculate the crit value of an artifact. This is the sum of the crit damage and
    the crit rate times two.

    Args:
        artifact (artipy.artifacts.Artifact): The artifact to calculate the crit value

    Returns:
        Decimal: The crit value of the artifact.
    """
    crit_dmg = (
        sum([
            substat.value
            for substat in artifact.substats
            if substat.name == StatType.CRIT_DMG
        ])
        * 100
    )
    crit_rate = (
        sum([
            substat.value
            for substat in artifact.substats
            if substat.name == StatType.CRIT_RATE
        ])
        * 100
    )
    return Decimal(crit_dmg + crit_rate * 2)
