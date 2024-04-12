from decimal import Decimal

from artipy.artifacts import Artifact
from artipy.artifacts.upgrade_strategy import UPGRADE_STEP
from artipy.stats import StatType, SubStat
from artipy.stats.utils import possible_substat_values


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

    # Convert values to percentage if necessary
    if substat.name.is_pct:
        stat_value *= 100
        highest_value *= 100

    return stat_value / highest_value


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
    crit_dmg = sum(
        [
            substat.value
            for substat in artifact.get_substats()
            if substat.name == StatType.CRIT_DMG
        ]
    )
    crit_rate = sum(
        [
            substat.value
            for substat in artifact.get_substats()
            if substat.name == StatType.CRIT_RATE
        ]
    )
    return Decimal((crit_dmg + crit_rate * 2) * 100)
