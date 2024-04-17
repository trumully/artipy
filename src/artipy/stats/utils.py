"""Utilities for stats module."""

from decimal import Decimal
from functools import lru_cache
from operator import attrgetter
from typing import Iterable

from artipy.data_gen import DataGen
from artipy.types import StatType

MAINSTAT_DATA = DataGen("ReliquaryLevelExcelConfigData.json")
SUBSTAT_DATA = DataGen("ReliquaryAffixExcelConfigData.json")


def map_to_decimal(values: Iterable[float | int]) -> tuple[Decimal, ...]:
    """Map the values to Decimal.

    Args:
        values (Iterable[float  |  int]): The values to map.

    Returns:
        tuple[Decimal, ...]: The mapped values.
    """
    return tuple(map(Decimal, values))


@lru_cache(maxsize=None)
def possible_mainstat_values(stat: StatType, rarity: int) -> tuple[Decimal, ...]:
    """Get the possible values for a mainstat based on the stat type and rarity.
    Map the values to Decimal.

    Args:
        stat (StatType): The stat type to get the values for.
        rarity (int): The rarity of the artifact.

    Returns:
        tuple[Decimal, ...]: The possible values for the mainstat.
    """
    values = list(MAINSTAT_DATA)[1:]
    data = [
        j.value
        for i in values
        if i.rank == rarity
        for j in i.add_props
        if j.prop_type == stat
    ]
    return map_to_decimal(data)


@lru_cache(maxsize=None)
def possible_substat_values(stat: StatType, rarity: int) -> tuple[Decimal, ...]:
    """Get the possible values for a substat based on the stat type and rarity.
    Map the values to Decimal.

    Args:
        stat (StatType): The stat type to get the values for.
        rarity (int): The rarity of the artifact.

    Returns:
        tuple[Decimal, ...]: The possible values for the substat.
    """
    data = [
        d
        for d in SUBSTAT_DATA
        if d.depot_id == int(f"{rarity}01") and d.prop_type == stat
    ]
    sorted_data = sorted(data, key=attrgetter("prop_value"))
    return map_to_decimal((d.prop_value for d in sorted_data))
