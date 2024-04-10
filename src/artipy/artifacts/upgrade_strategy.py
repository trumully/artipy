from typing import TYPE_CHECKING
import random

from artipy.stats import StatType, SubStat, create_substat
from .utils import choose

if TYPE_CHECKING:
    from .artifact import Artifact


substat_weights: dict[StatType, int] = {
    StatType.HP: 6,
    StatType.ATK: 6,
    StatType.DEF: 6,
    StatType.HP_PERCENT: 4,
    StatType.ATK_PERCENT: 4,
    StatType.DEF_PERCENT: 4,
    StatType.ENERGY_RECHARGE: 4,
    StatType.ELEMENTAL_MASTERY: 4,
    StatType.CRIT_RATE: 3,
    StatType.CRIT_DMG: 3,
}

UPGRADE_STEP = 4


class UpgradeStrategy:
    """A base Strategy class for upgrading artifacts."""

    def upgrade(self, artifact: "Artifact") -> None:
        """Upgrade the artifact.

        Increase the artifact level by 1 and upgrade the mainstat.
        """
        new_level = artifact.get_level() + 1
        artifact.set_level(new_level)
        artifact.get_mainstat().set_value(new_level)


class AddStatStrategy(UpgradeStrategy):
    """A Strategy class for adding a new substat to an artifact.

    This strategy is used when initially creating an artifact and when an artifact
    is capable of generating a new substat.
    """

    def pick_stat(self, artifact: "Artifact") -> SubStat:
        """Pick a new substat for the artifact."""
        stats = [s.name for s in (artifact.get_mainstat(), *artifact.get_substats())]
        pool = {s: w for s, w in substat_weights.items() if s not in stats}
        population, weights = map(tuple, zip(*pool.items()))
        new_stat_name = choose(population, weights)
        new_stat = create_substat(name=new_stat_name, rarity=artifact.get_rarity())
        return new_stat

    def upgrade(self, artifact: "Artifact") -> None:
        """Upgrade the artifact.

        Increase the artifact level by 1, upgrade the mainstat, and add a new substat.
        """
        super().upgrade(artifact)
        new_stat = self.pick_stat(artifact)
        artifact.add_substat(new_stat)


class UpgradeStatStrategy(UpgradeStrategy):
    """A Strategy class for upgrading a substat on an artifact.

    This strategy is used when an artifact is capable of upgrading a substat. The
    substat to upgrade is chosen randomly.
    """

    def upgrade(self, artifact: "Artifact") -> None:
        """Upgrade the artifact.

        Increase the artifact level by 1, upgrade the mainstat, and upgrade a substat.
        """
        super().upgrade(artifact)
        if artifact.get_level() % UPGRADE_STEP == 0:
            substat = random.choice(artifact.get_substats())
            substat.upgrade()
