from artipy.artifacts import ArtifactBuilder
from artipy.stats import MainStat, SubStat, StatType


def main() -> None:
    artifact = (
        ArtifactBuilder()
        .with_mainstat(MainStat(StatType.ATK, 46))
        .add_substat(SubStat(StatType.CRIT_RATE, 5.4))
        .add_substat(SubStat(StatType.CRIT_DMG, 11.9))
        .with_level(0)
        .with_rarity(5)
        .with_set("Gladiator's Finale")
        .with_slot("Flower of Life")
        .build()
    )
    print(artifact)


if __name__ == "__main__":
    main()
