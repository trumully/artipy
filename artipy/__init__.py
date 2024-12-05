"""artipy: A Python package for analysing artifacts in Genshin Impact."""

from pathlib import Path

__data__ = Path(__file__).parent / "data"

__version__ = "2.0.0"

# 4 decimal places
DECIMAL_PLACES = "1E-4"

# 5-star rarity
MAX_RARITY = 5

UPGRADE_STEP = 4
