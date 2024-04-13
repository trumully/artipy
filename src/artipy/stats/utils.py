from decimal import Decimal
from functools import lru_cache
from operator import attrgetter
from typing import Iterable

from .stat_data import StatData
from .stats import StatType

MAINSTAT_DATA = StatData("mainstat_data.json")
SUBSTAT_DATA = StatData("substat_data.json")


def map_to_decimal(values: Iterable[float | int]) -> tuple[Decimal, ...]:
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
    values = list(MAINSTAT_DATA)[1:]
    data = [
        j.value
        for i in values
        if i.rank == rarity
        for j in i.addProps
        if j.propType == stat_type
    ]
    return map_to_decimal(data)


@lru_cache(maxsize=None)
def possible_substat_values(stat: StatType, rarity: int) -> tuple[Decimal, ...]:
    """Get the possible values for a substat based on the stat type and rarity.
    Map the values to Decimal.

    :param stat: The stat to get the values for.
    :type stat: StatType
    :param rarity: The rarity of the artifact.
    :type rarity: int
    :return: The possible values for the substat.
    :rtype: tuple[Decimal, ...]
    """
    data = [
        d
        for d in SUBSTAT_DATA
        if d.depotId == int(f"{rarity}01") and d.propType == stat
    ]
    sorted_data = sorted(data, key=attrgetter("propValue"))
    return map_to_decimal((d.propValue for d in sorted_data))
