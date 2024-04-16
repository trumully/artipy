"""This module contains classes for upgrading artifacts."""

import random
from typing import TYPE_CHECKING

from artipy import UPGRADE_STEP
from artipy.stats import SubStat, create_substat
from artipy.types import StatType

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


class UpgradeStrategy:
    """A base Strategy class for upgrading artifacts."""

    def upgrade(self, artifact: "Artifact") -> None:
        """Upgrade the artifact; increase the artifact level by 1 and upgrade the
        mainstat.

        :param artifact: The artifact to upgrade.
        :type artifact: Artifact
        """
        new_level = artifact.level + 1
        artifact.level = new_level
        artifact.mainstat.set_value_by_level(new_level)


class AddStatStrategy(UpgradeStrategy):
    """A Strategy class for adding a new substat to an artifact.

    This strategy is used when initially creating an artifact and when an artifact
    is capable of generating a new substat.
    """

    def pick_stat(self, artifact: "Artifact") -> SubStat:
        """Pick a new substat to add to the artifact. The substat is chosen randomly
        based on the weights of the substats.

        :param artifact: The artifact to add the substat to.
        :type artifact: Artifact
        :return: The new substat to add to the artifact.
        :rtype: SubStat
        """
        stats = [s.name for s in (artifact.mainstat, *artifact.substats)]
        pool = {s: w for s, w in substat_weights.items() if s not in stats}
        population, weights = map(tuple, zip(*pool.items()))
        new_stat_name = choose(population, weights)
        new_stat = create_substat(name=new_stat_name, rarity=artifact.rarity)
        return new_stat

    def upgrade(self, artifact: "Artifact") -> None:
        """Upgrade the artifact. If the artifact level is divisible by the upgrade step,
        add a new substat to the artifact.

        :param artifact: The artifact to upgrade.
        :type artifact: Artifact
        """
        if artifact.level % UPGRADE_STEP == 0:
            new_stat = self.pick_stat(artifact)
            artifact.add_substat(new_stat)
        super().upgrade(artifact)


class UpgradeStatStrategy(UpgradeStrategy):
    """A Strategy class for upgrading a substat on an artifact.

    This strategy is used when an artifact is capable of upgrading a substat. The
    substat to upgrade is chosen randomly.
    """

    def upgrade(self, artifact: "Artifact") -> None:
        """Upgrade the artifact. If the artifact level is divisible by the upgrade step,
        upgrade a random substat on the artifact.

        :param artifact: The artifact to upgrade.
        :type artifact: Artifact
        """
        if artifact.level % UPGRADE_STEP == 0:
            substat = random.choice(artifact.substats)
            substat.upgrade()
        super().upgrade(artifact)
