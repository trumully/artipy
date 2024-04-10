import toml
from pathlib import Path

__name__ = toml.load("pyproject.toml")["tool"]["poetry"]["name"]
__version__ = toml.load("pyproject.toml")["tool"]["poetry"]["version"]

__data__ = Path(__file__).parent / "data"
