from decimal import Decimal
from functools import lru_cache
from operator import attrgetter

from .stat_data import StatData
from .stats import StatType

MAISTAT_DATA = StatData("mainstat_data.json")
SUBSTAT_DATA = StatData("substat_data.json")


def map_to_decimal(values: tuple[float, ...]) -> tuple[Decimal, ...]:
    """Helper function to map float values to Decimal."""
    return tuple(map(Decimal, values))


@lru_cache(maxsize=None)
def possible_mainstat_values(stat_type: StatType, rarity: int) -> tuple[Decimal, ...]:
    """Get the possible values for a mainstat based on the stat type and rarity.
    Map the values to Decimal.

    :param stat_type: The stat to get the values for.
    :type stat_type: StatType
    :param rarity: The rarity of the artifact.
    :type rarity: int
    :return: The possible values for the mainstat.
    :rtype: tuple[Decimal, ...]
    """
    data = [d.addProps for d in MAISTAT_DATA if d.rank == rarity]
    return map_to_decimal((d.value for d in data if d.propType == stat_type))


@lru_cache(maxsize=None)
def possible_substat_values(stat_type: StatType, rarity: int) -> tuple[Decimal, ...]:
    """Get the possible values for a substat based on the stat type and rarity.
    Map the values to Decimal.

    :param stat_type: The stat to get the values for.
    :type stat_type: StatType
    :param rarity: The rarity of the artifact.
    :type rarity: int
    :return: The possible values for the substat.
    :rtype: tuple[Decimal, ...]
    """
    data = [
        d
        for d in SUBSTAT_DATA
        if d.depotId == int(f"{rarity}01") and d.propType == stat_type
    ]
    sorted_data = sorted(data, key=attrgetter("propValue"))
    return map_to_decimal((d.propValue for d in sorted_data))
