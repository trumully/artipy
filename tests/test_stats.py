import math
from decimal import Decimal

import pytest
from artipy import DECIMAL_PLACES
from artipy.stats import MainStat, StatType, SubStat
from artipy.stats.utils import possible_mainstat_values, possible_substat_values


@pytest.fixture
def mainstat() -> MainStat:
    return MainStat(StatType.HP, 1000)


@pytest.fixture
def substat() -> SubStat:
    return SubStat(StatType.HP_PERCENT, 0.05)


@pytest.fixture
def verbose_mainstat() -> MainStat:
    return MainStat(StatType.HP, 1000.123456789)


@pytest.fixture
def verbose_substat() -> SubStat:
    return SubStat(StatType.HP_PERCENT, 0.123456789)


def test_mainstat(mainstat) -> None:
    assert mainstat.name == StatType.HP
    assert mainstat.value == 1000
    assert mainstat.rarity == 5


def test_possible_mainstat_values() -> None:
    values = possible_mainstat_values(StatType.HP, 5)
    assert len(values) == 21


def test_mainstat_set_value_by_level(mainstat) -> None:
    mainstat.set_value_by_level(1)
    assert mainstat.value == possible_mainstat_values(StatType.HP, 5)[1]


def test_mainstat_str(mainstat) -> None:
    assert str(mainstat) == "HP+1,000"
    assert f"{mainstat:v}" == f"{StatType.HP} = {mainstat.value}"


def test_substat(substat) -> None:
    assert substat.name == StatType.HP_PERCENT
    assert substat.value == 0.05
    assert substat.rarity == 5


def test_possible_substat_values() -> None:
    values = possible_substat_values(StatType.HP_PERCENT, 5)
    assert len(values) == 4


def test_substat_roll(substat) -> None:
    value = substat.roll()
    assert value in possible_substat_values(StatType.HP_PERCENT, 5)


def test_substat_upgrade(substat) -> None:
    old_value = substat.value
    substat.upgrade()
    assert substat.value > old_value
    diff = substat.value - old_value
    assert any(
        math.isclose(i, diff, rel_tol=1e8)
        for i in possible_substat_values(StatType.HP_PERCENT, 5)
    )


def test_substat_str(substat) -> None:
    assert str(substat) == "• HP+5.0%"
    assert f"{substat:v}" == f"{StatType.HP_PERCENT} = {substat.value}"


def test_rounded_value(verbose_mainstat, verbose_substat) -> None:
    dp = Decimal(DECIMAL_PLACES)
    assert verbose_mainstat.rounded_value == verbose_mainstat.value.quantize(dp)
    assert verbose_substat.rounded_value == verbose_substat.value.quantize(dp)
