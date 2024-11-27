"""Utilities for stats module."""

from decimal import Decimal
from functools import lru_cache
from operator import attrgetter
from typing import NamedTuple, cast

from artipy.data_gen import DataGen
from artipy.types import StatType

MAINSTAT_DATA = DataGen("ReliquaryLevelExcelConfigData.json")
SUBSTAT_DATA = DataGen("ReliquaryAffixExcelConfigData.json")


class StatData(NamedTuple):
    depot_id: int
    prop_type: StatType
    prop_value: float
    value: float


class StatContainer(NamedTuple):
    rank: int
    add_props: list[StatData]


@lru_cache
def possible_mainstat_values(stat: StatType, rarity: int) -> tuple[Decimal, ...]:
    """Get the possible values for a mainstat based on the stat type and rarity.
    Map the values to Decimal.

    Args:
        stat (StatType): The stat type to get the values for.
        rarity (int): The rarity of the artifact.

    Returns:
        tuple[Decimal, ...]: The possible values for the mainstat.
    """
    mainstat_data = MAINSTAT_DATA.as_list()
    values = cast(list[StatContainer], mainstat_data[1:])
    data = [j.value for i in values if i.rank == rarity for j in i.add_props if j.prop_type == stat]
    return tuple(x for x in map(Decimal, data))


@lru_cache
def possible_substat_values(stat: StatType, rarity: int) -> tuple[Decimal, ...]:
    """Get the possible values for a substat based on the stat type and rarity.
    Map the values to Decimal.

    Args:
        stat (StatType): The stat type to get the values for.
        rarity (int): The rarity of the artifact.

    Returns:
        tuple[Decimal, ...]: The possible values for the substat.
    """
    substat_data = cast(list[StatData], SUBSTAT_DATA.as_list())
    data = [d for d in substat_data if d.depot_id == int(f"{rarity}01") and d.prop_type == stat]
    sorted_data = sorted(data, key=attrgetter("prop_value"))
    return tuple(x for x in map(Decimal, (d.prop_value for d in sorted_data)))
