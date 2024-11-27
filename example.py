"""The example script for the artipy package."""

from artipy import analysis
from artipy.artifacts import ArtifactBuilder
from artipy.types import ArtifactSet, ArtifactSlot, StatType


def main() -> None:
    artifact = (
        ArtifactBuilder()
        .with_level(8)
        .with_rarity(5)
        .with_mainstat(StatType.ATK_PERCENT, 0.228)
        .with_substats([
            (StatType.ATK, 19),
            (StatType.CRIT_RATE, 0.039),
            (StatType.HP_PERCENT, 0.053),
            (StatType.HP, 568),
        ])
        .with_slot(ArtifactSlot.SANDS)
        .with_set(ArtifactSet.GLADIATORS_FINALE)
        .build()
    )

    for _ in range(4):
        artifact.upgrade()
    print(artifact)

    roll_value = analysis.calculate_artifact_roll_value(artifact)
    max_roll_value = analysis.calculate_artifact_maximum_roll_value(artifact)
    crit_value = analysis.calculate_artifact_crit_value(artifact)
    print(f"Roll Value: {roll_value}")
    print(f"Max Roll Value: {max_roll_value}")
    print(f"Crit Value: {crit_value}")

    analysis.plot_artifact_substat_rolls(artifact)


if __name__ == "__main__":
    main()
