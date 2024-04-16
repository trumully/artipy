"""This module contains the tests for the stats module."""

import decimal
from typing import Union

import artipy.stats
from hypothesis import assume, given
from hypothesis import strategies as st


@given(
    name=st.sampled_from(artipy.types.StatType),
    _value=st.one_of(st.decimals(), st.floats(), st.integers()),
    rarity=st.integers(1, 5),
)
def test_fuzz_MainStat(
    name: artipy.types.StatType,
    _value: Union[float, int, decimal.Decimal],
    rarity: int,
) -> None:
    """This function tests the MainStat class. It verifies that the class can be
    instantiated with the given parameters.

    Args:
        name (artipy.types.StatType): The name of the stat.
        _value (Union[float, int, decimal.Decimal]): The value of the stat.
        rarity (int): The rarity of the stat.
    """
    artipy.stats.MainStat(name=name, _value=_value, rarity=rarity)


@given(
    name=st.sampled_from(artipy.types.StatType),
    _value=st.one_of(st.decimals(), st.floats(), st.integers()),
    rarity=st.integers(1, 5),
    level=st.integers(0, 20),
)
def test_fuzz_MainStat_set_value_by_level(
    name: artipy.types.StatType,
    _value: Union[float, int, decimal.Decimal],
    rarity: int,
    level: int,
) -> None:
    """This function tests the set_value_by_level method of the MainStat class. It
    verifies that the method can set the value of the mainstat based on the level of the
    artifact.

    Args:
        name (artipy.stats.stats.StatType): The name of the stat.
        _value (Union[float, int, decimal.Decimal]): The value of the stat.
        rarity (int): The rarity of the stat.
        level (int): The level of the artifact.
    """
    assume(level <= (4 * rarity if rarity >= 3 else 4))
    mainstat = artipy.stats.MainStat(name=name, _value=_value, rarity=rarity)
    mainstat.set_value_by_level(level)
    values = artipy.stats.utils.possible_mainstat_values(stat_type=name, rarity=rarity)
    assert mainstat.value in values


@given(
    name=st.sampled_from(artipy.types.StatType),
    _value=st.one_of(st.decimals(), st.floats(), st.integers()),
    rarity=st.integers(1, 5),
    level=st.integers(0, 20),
)
def test_fuzz_MainStat_str(
    name: artipy.types.StatType,
    _value: Union[float, int, decimal.Decimal],
    rarity: int,
    level: int,
) -> None:
    """This function tests the __str__ method of the MainStat class. It verifies that
    the method can return a string representation of the mainstat.

    Args:
        name (artipy.stats.stats.StatType): The name of the stat.
        _value (Union[float, int, decimal.Decimal]): The value of the stat.
        rarity (int): The rarity of the stat.
        level (int): The level of the artifact.
    """
    mainstat = artipy.stats.MainStat(name=name, _value=_value, rarity=rarity)
    stat_name = artipy.types.STAT_NAMES[mainstat.name].split("%")
    if mainstat.name.is_pct:
        assert str(mainstat) == f"{stat_name[0]}+{mainstat.value:.1%}"
    else:
        assert str(mainstat) == f"{stat_name[0]}+{mainstat.value:,.0f}"


@given(
    name=st.sampled_from(artipy.types.StatType),
    _value=st.one_of(st.decimals(), st.floats(), st.integers()),
    rarity=st.integers(1, 5),
)
def test_fuzz_SubStat(
    name: artipy.types.StatType,
    _value: Union[float, int, decimal.Decimal],
    rarity: int,
) -> None:
    """This function tests the SubStat class. It verifies that the class can be
    instantiated with the given parameters.

    Args:
        name (artipy.types.StatType): The name of the stat.
        _value (Union[float, int, decimal.Decimal]): The value of the stat.
        rarity (int): The rarity of the stat.
    """
    artipy.stats.SubStat(name=name, _value=_value, rarity=rarity)


@given(name=st.sampled_from(artipy.types.VALID_SUBSTATS), rarity=st.integers(1, 5))
def test_fuzz_create_substat(name: artipy.types.StatType, rarity: int) -> None:
    """This function tests the create_substat function. It creates a substat with the
    given name and rarity and also creates a substat with just the given rarity. This
    verifies that the function can create specified substats and that it can create
    random substats.

    Args:
        name (artipy.types.StatType): The name of the substat.
        rarity (int): The rarity of the substat.
    """
    artipy.stats.create_substat(name=name, rarity=rarity)
    artipy.stats.create_substat(rarity=rarity)


@given(name=st.sampled_from(artipy.types.VALID_SUBSTATS), rarity=st.integers(1, 5))
def test_fuzz_possible_substat_values(name: artipy.types.StatType, rarity: int) -> None:
    """This function tests the possible_substat_values function. It verifies that the
    function can return the correct values for the given substat name and rarity.

    Args:
        name (artipy.types.StatType): The name of the substat.
        rarity (int): The rarity of the substat.
    """
    artipy.stats.utils.possible_substat_values(stat=name, rarity=rarity)


@given(name=st.sampled_from(artipy.types.VALID_SUBSTATS), rarity=st.integers(1, 5))
def test_fuzz_SubStat_roll(name: artipy.types.StatType, rarity: int) -> None:
    """This function tests the roll method of the SubStat class. It verifies that the
    roll method can generate a random value for the substat.

    Args:
        name (artipy.types.StatType): The name of the substat.
        rarity (int): The rarity of the substat.
    """
    substat = artipy.stats.create_substat(name=name, rarity=rarity)
    roll = substat.roll()
    assert roll in artipy.stats.utils.possible_substat_values(stat=name, rarity=rarity)


@given(name=st.sampled_from(artipy.types.VALID_SUBSTATS), rarity=st.integers(1, 5))
def test_fuzz_SubStat_str(name: artipy.types.StatType, rarity: int) -> None:
    """This function tests the __str__ method of the SubStat class. It verifies that the
    method can return a string representation of the substat.

    Args:
        name (artipy.types.StatType): The name of the substat.
        rarity (int): The rarity of the substat.
    """
    substat = artipy.stats.create_substat(name=name, rarity=rarity)
    stat_name = artipy.types.STAT_NAMES[substat.name].split("%")
    if substat.name.is_pct:
        assert str(substat) == f"• {stat_name[0]}+{substat.value:.1%}"
    else:
        assert str(substat) == f"• {stat_name[0]}+{substat.value:,.0f}"
