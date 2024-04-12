import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, ClassVar, Iterator

from artipy import __data__


def recursive_namespace(data: Any) -> Any | SimpleNamespace:
    """Helper function to recursively convert dictionaries and nested dictionaries
    into SimpleNamespace type.

    :param data: The data to convert to SimpleNamespace.
    :type data: Any
    :return: The data converted to SimpleNamespace. Return as is if not a dictionary.
    :rtype: Any | SimpleNamespace
    """
    if isinstance(data, dict):
        return SimpleNamespace(**{k: recursive_namespace(v) for k, v in data.items()})
    return data


class StatData:
    """Singleton class that handles JSON data for the stats module."""

    _instances: ClassVar[dict[str, "StatData"]] = {}

    _data: list[SimpleNamespace] = []

    def __new__(cls, file_name: str) -> "StatData":
        """Create a new instance of the StatData singleton class if it does not exist."""
        if file_name not in cls._instances:
            cls._instances[file_name] = super().__new__(cls)
        return cls._instances[file_name]

    def __init__(self, file_name: str) -> None:
        """Initialize the StatData singleton class."""
        with open(Path(__data__ / file_name), "r", encoding="utf-8") as f:
            self._data = json.load(f, object_hook=recursive_namespace)

    def __iter__(self) -> Iterator[SimpleNamespace]:
        return iter(self._data)

    def __getitem__(self, index: int) -> SimpleNamespace:
        return self._data[index]
