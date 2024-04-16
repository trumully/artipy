"""Artifacts module."""

from .artifact import Artifact, ArtifactSlot
from .builder import ArtifactBuilder
from .upgrade_strategy import AddStatStrategy, UpgradeStatStrategy, UpgradeStrategy

__all__ = (
    "Artifact",
    "ArtifactBuilder",
    "ArtifactSlot",
    "UpgradeStrategy",
    "UpgradeStatStrategy",
    "AddStatStrategy",
)
