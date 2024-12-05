"""Utility functions for the package."""

import random
from decimal import Decimal
from functools import lru_cache
from operator import attrgetter
from typing import NamedTuple, cast

from artipy.data_gen import DataGen
from artipy.types import StatType

type Seq[T] = tuple[T, ...] | list[T]

MAINSTAT_DATA = DataGen("ReliquaryLevelExcelConfigData.json")
SUBSTAT_DATA = DataGen("ReliquaryAffixExcelConfigData.json")


def choose[T](population: Seq[T], weights: tuple[float]) -> T:
    """Helper function to choose a random element from a population with weights.
    This skips having to do slicing of the result of random.choices.

    Args:
        population (Seq[T]): The population to choose from.
        weights (tuple[float]): The weights of the population.

    Returns:
        T: The chosen element.
    """
    return random.choices(population, weights)[0]


class StatData(NamedTuple):
    depot_id: int
    prop_type: StatType
    prop_value: float
    value: float


class StatContainer(NamedTuple):
    rank: int
    add_props: list[StatData]


@lru_cache(maxsize=1024)
def possible_mainstat_values(stat: StatType, rarity: int) -> list[Decimal]:
    """Get the possible values for a mainstat based on the stat type and rarity.
    Map the values to Decimal.

    Args:
        stat (StatType): The stat type to get the values for.
        rarity (int): The rarity of the artifact.

    Returns:
        list[Decimal]: The possible values for the mainstat.
    """
    mainstat_data = MAINSTAT_DATA.as_list()
    values = cast("list[StatContainer]", mainstat_data[1:])
    data = [
        j.value
        for i in values
        if i.rank == rarity
        for j in i.add_props
        if j.prop_type == stat
    ]
    return sorted(Decimal(str(x)) for x in data)


@lru_cache(maxsize=1024)
def possible_substat_values(stat: StatType, rarity: int) -> list[Decimal]:
    """Get the possible values for a substat based on the stat type and rarity.
    Map the values to Decimal.

    Args:
        stat (StatType): The stat type to get the values for.
        rarity (int): The rarity of the artifact.

    Returns:
        list[Decimal]: The possible values for the substat.
    """
    substat_data = cast("list[StatData]", SUBSTAT_DATA.as_list())
    data = [
        d
        for d in substat_data
        if d.depot_id == int(f"{rarity}01") and d.prop_type == stat
    ]
    sorted_data = sorted(data, key=attrgetter("prop_value"))
    return sorted(Decimal(str(x.prop_value)) for x in sorted_data)
