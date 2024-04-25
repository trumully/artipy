"""Module containing the types used in the artipy package."""

import re
from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum, auto
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
    """Get a constant name from a key i.e: PascalCase -> PASCAL_CASE

    Args:
        key (str): The key to convert.

    Returns:
        str: The converted key.
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", key).upper()


def generate_artifact_sets() -> None:
    """Use this if artifactNames_gen.json ever changes."""
    data = {
        key_to_constant(k): v
        for k, v in json_to_dict("artifacts/artifactNames_gen.json").items()
    }
    print("\n".join(f"{k} = {v}" for k, v in data.items()))


class ArtifactSet(StrEnum):
    """The artifact sets in Genshin Impact."""

    RESOLUTION_OF_SOJOURNER = "Resolution of Sojourner"
    BRAVE_HEART = "Brave Heart"
    DEFENDERS_WILL = "Defender's Will"
    TINY_MIRACLE = "Tiny Miracle"
    BERSERKER = "Berserker"
    MARTIAL_ARTIST = "Martial Artist"
    INSTRUCTOR = "Instructor"
    GAMBLER = "Gambler"
    THE_EXILE = "The Exile"
    ADVENTURER = "Adventurer"
    LUCKY_DOG = "Lucky Dog"
    SCHOLAR = "Scholar"
    TRAVELING_DOCTOR = "Traveling Doctor"
    BLIZZARD_STRAYER = "Blizzard Strayer"
    THUNDERSOOTHER = "Thundersoother"
    LAVAWALKER = "Lavawalker"
    MAIDEN_BELOVED = "Maiden Beloved"
    GLADIATORS_FINALE = "Gladiator's Finale"
    VIRIDESCENT_VENERER = "Viridescent Venerer"
    WANDERERS_TROUPE = "Wanderer's Troupe"
    THUNDERING_FURY = "Thundering Fury"
    CRIMSON_WITCH_OF_FLAMES = "Crimson Witch of Flames"
    NOBLESSE_OBLIGE = "Noblesse Oblige"
    BLOODSTAINED_CHIVALRY = "Bloodstained Chivalry"
    PRAYERS_FOR_ILLUMINATION = "Prayers for Illumination"
    PRAYERS_FOR_DESTINY = "Prayers for Destiny"
    PRAYERS_FOR_WISDOM = "Prayers for Wisdom"
    PRAYERS_TO_SPRINGTIME = "Prayers to Springtime"
    ARCHAIC_PETRA = "Archaic Petra"
    RETRACING_BOLIDE = "Retracing Bolide"
    HEART_OF_DEPTH = "Heart of Depth"
    TENACITY_OF_THE_MILLELITH = "Tenacity of the Millelith"
    PALE_FLAME = "Pale Flame"
    SHIMENAWAS_REMINISCENCE = "Shimenawa's Reminiscence"
    EMBLEM_OF_SEVERED_FATE = "Emblem of Severed Fate"
    HUSK_OF_OPULENT_DREAMS = "Husk of Opulent Dreams"
    OCEAN_HUED_CLAM = "Ocean-Hued Clam"
    VERMILLION_HEREAFTER = "Vermillion Hereafter"
    ECHOES_OF_AN_OFFERING = "Echoes of an Offering"
    DEEPWOOD_MEMORIES = "Deepwood Memories"
    GILDED_DREAMS = "Gilded Dreams"
    DESERT_PAVILION_CHRONICLE = "Desert Pavilion Chronicle"
    FLOWER_OF_PARADISE_LOST = "Flower of Paradise Lost"
    NYMPHS_DREAM = "Nymph's Dream"
    VOURUKASHAS_GLOW = "Vourukasha's Glow"
    MARECHAUSSEE_HUNTER = "Marechaussee Hunter"
    GOLDEN_TROUPE = "Golden Troupe"
    SONG_OF_DAYS_PAST = "Song of Days Past"
    NIGHTTIME_WHISPERS_IN_THE_ECHOING_WOODS = "Nighttime Whispers in the Echoing Woods"


@dataclass(frozen=True, kw_only=True, slots=True)
class ArtifactSetData:
    """Data class representing an artifact set in Genshin Impact."""

    set_name: str
    set_effects: dict[str, str]
    pieces: dict[ArtifactSlot, dict[str, str]]


def make_artifact_sets() -> Iterator[ArtifactSetData]:
    """Make artifact sets from the artifact data.

    Yields:
        Iterator[ArtifactSetData]: The artifact set data.
    """
    for key in ArtifactSet:
        data = json_to_dict(
            f"artifacts/artifact_{key.name.title().replace("_", "")}_gen.json"
        )
        yield ArtifactSetData(**{camel_to_snake_case(k): v for k, v in data.items()})


VALID_ARTIFACT_SETS: dict[ArtifactSet, ArtifactSetData] = {
    ArtifactSet(key): value for value in make_artifact_sets() for key in ArtifactSet
}


class RollMagnitude(StrEnum):
    """The roll magnitude of a substat. This is a measure of how much the substat has
    been increased in relation to its maximum potential value."""

    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    MAX = auto()

    @property
    def magnitude(self) -> Decimal:
        """Get the magnitude of the roll magnitude.

        Returns:
            Decimal: The magnitude of the roll magnitude.
        """
        if self == RollMagnitude.LOW:
            return Decimal("0.7")
        elif self == RollMagnitude.MEDIUM:
            return Decimal("0.8")
        elif self == RollMagnitude.HIGH:
            return Decimal("0.9")
        return Decimal("1.0")

    @classmethod
    def closest(cls, value: Decimal | float | int) -> "RollMagnitude":
        """The closest roll magnitude to a value.

        Args:
            value (Decimal | float | int): The value to find the closest roll magnitude

        Returns:
            RollMagnitude: The closest roll magnitude to the value.
        """
        return RollMagnitude(
            min(cls, key=lambda x: abs(RollMagnitude(x).magnitude - Decimal(value)))
        )


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
