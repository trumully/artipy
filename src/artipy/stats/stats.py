from dataclasses import dataclass, field
from decimal import Decimal
from enum import StrEnum

from artipy.stats import DECIMAL_PLACES


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


@dataclass
class Stat:
    name: StatType
    _value: float | int | Decimal = field(default=Decimal(0), repr=False)

    @property
    def value(self) -> Decimal:
        return Decimal(self._value)

    @value.setter
    def value(self, value: float | int | Decimal) -> None:
        self._value = value

    @property
    def rounded_value(self) -> Decimal:
        return self.value.quantize(Decimal(DECIMAL_PLACES))

    def __format__(self, format_spec: str) -> str:
        """Format the stat value based on the format specifier.

        If the format specifier is "v(erbose)", display stat type and unrounded value.
        """
        if format_spec in ("v", "verbose"):
            return f"{self.name} = {self.value}"
        return str(self)

    def __str__(self) -> str:
        name = STAT_NAMES[self.name].split("%")
        if self.name.is_pct:
            return f"{name[0]}+{self.value:.1%}"
        return f"{name[0]}+{self.value:,.0f}"
