"""Module containing the types used in the artipy package."""

import re
from dataclasses import dataclass
from enum import Enum, StrEnum, auto
from typing import Iterator

from artipy.data_gen import camel_to_snake_case, json_to_dict


# -------- Artifact Types -------- #
class ArtifactSlot(StrEnum):
    """Enum representing the artifact slots in Genshin Impact."""

    FLOWER = auto()
    PLUME = auto()
    SANDS = auto()
    GOBLET = auto()
    CIRCLET = auto()


def key_to_constant(key: str) -> str:
    """Get a constant name from a key.

    PascalCase -> PASCAL_CASE

    Args:
        key (str): The key to convert.

    Returns:
        str: The converted key.
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", key).upper()


ArtifactSet = Enum(  # type: ignore
    "ArtifactSet",
    {
        key_to_constant(k): v
        for k, v in json_to_dict("artifacts/artifactNames_gen.json").items()
    },
)


@dataclass(frozen=True, kw_only=True, slots=True)
class ArtifactSetData:
    """Data class representing an artifact set in Genshin Impact."""

    set_name: str
    set_effects: dict[str, str]
    pieces: dict[ArtifactSlot, dict[str, str]]


def make_artifact_sets() -> Iterator[ArtifactSetData]:
    for key in ArtifactSet:
        data = json_to_dict(
            f"artifacts/artifact_{key.name.title().replace("_", "")}_gen.json"
        )
        data = {camel_to_snake_case(k): v for k, v in data.items()}
        yield ArtifactSetData(**data)


VALID_ARTIFACT_SETS: dict[ArtifactSet, ArtifactSetData] = {
    ArtifactSet(key): value for value in make_artifact_sets() for key in ArtifactSet
}


# ---------- Stat Types ---------- #
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
    ArtifactSlot.FLOWER: {StatType.HP: 100},
    ArtifactSlot.PLUME: {StatType.ATK: 100},
    ArtifactSlot.SANDS: {
        StatType.HP_PERCENT: 26.68,
        StatType.ATK_PERCENT: 26.66,
        StatType.DEF_PERCENT: 26.66,
        StatType.ENERGY_RECHARGE: 10.0,
        StatType.ELEMENTAL_MASTERY: 10.0,
    },
    ArtifactSlot.CIRCLET: {
        StatType.HP_PERCENT: 22.0,
        StatType.ATK_PERCENT: 22.0,
        StatType.DEF_PERCENT: 22.0,
        StatType.CRIT_RATE: 10.0,
        StatType.CRIT_DMG: 10.0,
        StatType.HEALING_BONUS: 10.0,
        StatType.ELEMENTAL_MASTERY: 4.0,
    },
    ArtifactSlot.GOBLET: {
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
