"""Stat types and data for Genshin Impact artifacts."""

from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum

from artipy import DECIMAL_PLACES


class StatType(StrEnum):
    """Enumeration of stat types in Genshin Impact."""

    HP = "FIGHT_PROP_HP"
    ATK = "FIGHT_PROP_ATTACK"
    DEF = "FIGHT_PROP_DEFENSE"
    HP_PERCENT = "FIGHT_PROP_HP_PERCENT"
    ATK_PERCENT = "FIGHT_PROP_ATTACK_PERCENT"
    DEF_PERCENT = "FIGHT_PROP_DEFENSE_PERCENT"
    ELEMENTAL_MASTERY = "FIGHT_PROP_ELEMENT_MASTERY"
    ENERGY_RECHARGE = "FIGHT_PROP_CHARGE_EFFICIENCY"
    CRIT_RATE = "FIGHT_PROP_CRITICAL"
    CRIT_DMG = "FIGHT_PROP_CRITICAL_HURT"
    HEALING_BONUS = "FIGHT_PROP_HEAL_ADD"
    ANEMO_DMG = "FIGHT_PROP_WIND_ADD_HURT"
    CRYO_DMG = "FIGHT_PROP_ICE_ADD_HURT"
    DENDRO_DMG = "FIGHT_PROP_GRASS_ADD_HURT"
    ELECTRO_DMG = "FIGHT_PROP_ELEC_ADD_HURT"
    GEO_DMG = "FIGHT_PROP_ROCK_ADD_HURT"
    HYDRO_DMG = "FIGHT_PROP_WATER_ADD_HURT"
    PYRO_DMG = "FIGHT_PROP_FIRE_ADD_HURT"
    PHYSICAL_DMG = "FIGHT_PROP_PHYSICAL_ADD_HURT"

    @property
    def is_pct(self) -> bool:
        return "%" in STAT_NAMES[self]


STAT_NAMES: dict[StatType, str] = {
    StatType.HP: "HP",
    StatType.ATK: "ATK",
    StatType.DEF: "DEF",
    StatType.HP_PERCENT: "HP%",
    StatType.ATK_PERCENT: "ATK%",
    StatType.DEF_PERCENT: "DEF%",
    StatType.ELEMENTAL_MASTERY: "Elemental Mastery",
    StatType.ENERGY_RECHARGE: "Energy Recharge%",
    StatType.CRIT_RATE: "CRIT Rate%",
    StatType.CRIT_DMG: "CRIT DMG%",
    StatType.HEALING_BONUS: "Healing Bonus%",
    StatType.ANEMO_DMG: "Anemo DMG Bonus%",
    StatType.CRYO_DMG: "Cryo DMG Bonus%",
    StatType.DENDRO_DMG: "Dendro DMG Bonus%",
    StatType.ELECTRO_DMG: "Electro DMG Bonus%",
    StatType.GEO_DMG: "Geo DMG Bonus%",
    StatType.HYDRO_DMG: "Hydro DMG Bonus%",
    StatType.PYRO_DMG: "Pyro DMG Bonus%",
    StatType.PHYSICAL_DMG: "Physical DMG Bonus%",
}


VALID_SUBSTATS: list[StatType] = [
    StatType.HP,
    StatType.ATK,
    StatType.DEF,
    StatType.HP_PERCENT,
    StatType.ATK_PERCENT,
    StatType.DEF_PERCENT,
    StatType.ELEMENTAL_MASTERY,
    StatType.ENERGY_RECHARGE,
    StatType.CRIT_RATE,
    StatType.CRIT_DMG,
]

VALID_MAINSTATS: dict[str, dict[StatType, float]] = {
    "flower": {StatType.HP: 100},
    "plume": {StatType.ATK: 100},
    "sands": {
        StatType.HP_PERCENT: 26.68,
        StatType.ATK_PERCENT: 26.66,
        StatType.DEF_PERCENT: 26.66,
        StatType.ENERGY_RECHARGE: 10.0,
        StatType.ELEMENTAL_MASTERY: 10.0,
    },
    "circlet": {
        StatType.HP_PERCENT: 22.0,
        StatType.ATK_PERCENT: 22.0,
        StatType.DEF_PERCENT: 22.0,
        StatType.CRIT_RATE: 10.0,
        StatType.CRIT_DMG: 10.0,
        StatType.HEALING_BONUS: 10.0,
        StatType.ELEMENTAL_MASTERY: 4.0,
    },
    "goblet": {
        StatType.HP_PERCENT: 19.25,
        StatType.ATK_PERCENT: 19.25,
        StatType.DEF_PERCENT: 19.0,
        StatType.PHYSICAL_DMG: 5.0,
        StatType.ANEMO_DMG: 5.0,
        StatType.CRYO_DMG: 5.0,
        StatType.DENDRO_DMG: 5.0,
        StatType.ELECTRO_DMG: 5.0,
        StatType.GEO_DMG: 5.0,
        StatType.HYDRO_DMG: 5.0,
        StatType.PYRO_DMG: 5.0,
        StatType.ELEMENTAL_MASTERY: 2.5,
    },
}


@dataclass(slots=True)
class Stat:
    """Dataclass for a stat in Genshin Impact."""

    name: StatType
    _value: float | int | Decimal = field(default=Decimal(0), repr=False)

    @property
    def value(self) -> Decimal:
        """Get the value of the stat.

        :return: The value of the stat.
        :rtype: Decimal
        """
        return Decimal(self._value)

    @value.setter
    def value(self, value: float | int | Decimal) -> None:
        """Set the value of the stat.

        :param value: The value to set the stat to.
        :type value: float | int | Decimal
        """
        if not isinstance(value, Decimal):
            value = Decimal(value)
        self._value = value

    @property
    def rounded_value(self) -> Decimal:
        """Get the rounded value of the stat. This is the value rounded to the nearest
        pre-defined decimal place.

        :return: The rounded value of the stat.
        :rtype: Decimal
        """
        return self.value.quantize(Decimal(DECIMAL_PLACES))

    def __format__(self, format_spec: str) -> str:
        if format_spec in ("v", "verbose"):
            return f"{self.name} = {self.value}"
        return str(self)

    def __str__(self) -> str:
        name = STAT_NAMES[self.name].split("%")
        if self.name.is_pct:
            return f"{name[0]}+{self.value:.1%}"
        return f"{name[0]}+{self.value:,.0f}"
