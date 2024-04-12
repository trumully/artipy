from pathlib import Path

import toml

__name__ = toml.load("pyproject.toml")["tool"]["poetry"]["name"]
__version__ = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

__data__ = Path(__file__).parent / "data"

DECIMAL_PLACES = 1e-4
