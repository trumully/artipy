import itertools
import math
from decimal import Decimal
from enum import StrEnum, auto

from artipy.artifacts import Artifact
from artipy.artifacts.upgrade_strategy import UPGRADE_STEP
from artipy.stats import StatType, SubStat
from artipy.stats.utils import possible_substat_values

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
        """Get the magnitude of the roll. This is a value between 0.7 and 1.0.

        :return: The magnitude of the roll.
        :rtype: Decimal
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
        """Get the closest roll magnitude to a given value.

        :param value: The value to get the closest roll magnitude to.
        :type value: Decimal | float | int
        :return: The closest roll magnitude to the given value.
        :rtype: RollMagnitude
        """
        return RollMagnitude(
            min(cls, key=lambda x: abs(RollMagnitude(x).magnitude - Decimal(value)))
        )


def calculate_substat_roll_value(substat: SubStat) -> Decimal:
    """Get the substat roll value. This is a percentage of the current value over the
    highest potential value.

    :param substat: The substat to get the roll value for.
    :type substat: SubStat
    :return: The roll value of the substat.
    :rtype: Decimal
    """
    stat_value = substat.value
    highest_value = max(possible_substat_values(substat.name, substat.rarity))

    if substat.name.is_pct:
        stat_value *= 100
        highest_value *= 100

    return stat_value / highest_value


def calculate_substat_rolls(substat: SubStat) -> int:
    """Calculate the number of rolls a substat has gone through. This is the difference
    between the current value and the average value divided by the average value.

    :param substat: The substat to get the rolls for.
    :type substat: SubStat
    :return: The number of rolls the substat has gone through.
    :rtype: int
    """
    possible_rolls = possible_substat_values(substat.name, substat.rarity)
    average_roll = Decimal(sum(possible_rolls) / len(possible_rolls))
    return math.ceil((substat.value - average_roll) / average_roll)


def calculate_substat_roll_magnitudes(substat: SubStat) -> tuple[RollMagnitude, ...]:
    """Get the roll magnitudes for a substat. This is a tuple of the roll magnitudes
    for each roll the substat has gone through.

    :param substat: The substat to get the roll magnitudes for.
    :type substat: SubStat
    :return: The roll magnitudes for the substat.
    :rtype: tuple[RollMagnitude]
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
    """Get the current roll value of a given artifact. This is the sum of the roll
    values for all substats.

    :param artifact: The artifact to get the roll value for.
    :type artifact: Artifact
    :return: The roll value of the artifact roll.
    :rtype: Decimal
    """
    return Decimal(
        sum(
            calculate_substat_roll_value(substat) for substat in artifact.get_substats()
        )
    )


def calculate_artifact_maximum_roll_value(artifact: Artifact) -> Decimal:
    """Get the maximum roll value of a given artifact. This differs from the regular
    roll value by assuming remaining rolls are the highest possible value (i.e 100%
    roll value).

    :param artifact: The artifact to get the maximum roll value for.
    :type artifact: Artifact
    :return: The maximum roll value of the artifact roll.
    :rtype: Decimal
    """
    artifact_max_level = artifact.get_rarity() * 4
    remaining_rolls = (artifact_max_level - artifact.get_level()) // UPGRADE_STEP
    return Decimal(calculate_artifact_roll_value(artifact) + remaining_rolls)


def calculate_artifact_crit_value(artifact: Artifact) -> Decimal:
    """Get the crit value of a given artifact. This is the crit damage value plus
    the two times the crit rate.

    :param artifact: The artifact to get the crit value for.
    :type artifact: Artifact
    :return: The crit value of the artifact.
    :rtype: Decimal
    """
    crit_dmg = (
        sum(
            [
                substat.value
                for substat in artifact.get_substats()
                if substat.name == StatType.CRIT_DMG
            ]
        )
        * 100
    )
    crit_rate = (
        sum(
            [
                substat.value
                for substat in artifact.get_substats()
                if substat.name == StatType.CRIT_RATE
            ]
        )
        * 100
    )
    return Decimal(crit_dmg + crit_rate * 2)
