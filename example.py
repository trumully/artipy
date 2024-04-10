from artipy.artifacts import ArtifactBuilder
from artipy.stats import MainStat, SubStat, StatType


def main() -> None:
    artifact = (
        ArtifactBuilder()
        .with_mainstat(MainStat(StatType.ATK, 46))
        .with_substat(SubStat(StatType.CRIT_RATE, 0.039))
        .with_substat(SubStat(StatType.CRIT_DMG, 0.078))
        .with_substats(
            [SubStat(StatType.ATK_PERCENT, 0.05), SubStat(StatType.DEF_PERCENT, 0.05)]
        )
        .with_level(0)
        .with_rarity(5)
        .with_set("Gladiator's Finale")
        .with_slot("Flower of Life")
        .build()
    )
    print(artifact)


if __name__ == "__main__":
    main()
