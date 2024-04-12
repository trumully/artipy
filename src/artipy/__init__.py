from pathlib import Path

import toml

__name__ = toml.load("pyproject.toml")["tool"]["poetry"]["name"]
__version__ = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

__data__ = Path(__file__).parent / "data"

# 4 decimal places
DECIMAL_PLACES = "1E-4"

# 5-star rarity
MAX_RARITY = 5

UPGRADE_STEP = 4
