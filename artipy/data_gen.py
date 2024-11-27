"""Module that handles JSON data for the stats module."""

import json
import re
from collections.abc import Iterator, Mapping, MutableMapping, Sequence
from pathlib import Path
from types import SimpleNamespace
from typing import Any, ClassVar

from artipy import __data__


def camel_to_snake_case(s: str) -> str:
    """Convert a camel case string to snake case.

    Used by in the recursive_namespace function to make attribute names snake_case.

    Args:
        s (str): The string to convert.

    Returns:
        str: The converted string.
    """
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def recursive_namespace(data: Mapping[str, Any]) -> Any | SimpleNamespace:
    """Recursively convert a dictionary to a SimpleNamespace.

    Convert any attribute names from camelCase to snake_case for consistency.

    Args:
        data (Any): The data to convert.

    Returns:
        Any | SimpleNamespace: The converted data.
    """
    if isinstance(data, dict):
        return SimpleNamespace(**{camel_to_snake_case(k): recursive_namespace(v) for k, v in data.items()})
    return data


class DataGen:
    """Handle JSON data.

    This is a singleton class that manages JSON data. Each instance of this class is
    associated with a specific JSON file, and the data from that file is loaded when
    the instance is created. The data is stored as a list of SimpleNamespace objects,
    which allows for easy attribute-style access.

    Attributes:
        _instances (MutableMapping[str, DataGen]): A dictionary that maps file names to DataGen instances.
        _data (Sequence[SimpleNamespace]): The data loaded from the JSON file.
    """

    _instances: ClassVar[MutableMapping[str, "DataGen"]] = {}
    _data: Sequence[SimpleNamespace]

    def __new__(cls, file_name: str) -> "DataGen":
        """Create a new instance of the class if an instance with the same file name
        does not exist.

        Args:
            file_name (str): The name of the file to load.

        Returns:
            DataGen: The instance of the class.
        """
        if file_name not in cls._instances:
            cls._instances[file_name] = super().__new__(cls)
        return cls._instances[file_name]

    def __init__(self, file_name: str) -> None:
        """Load the data from the JSON file.

        Args:
            file_name (str): The name of the file to load.
        """
        with Path(__data__ / file_name).open(encoding="utf-8") as f:
            self._data = json.load(f, object_hook=recursive_namespace)

    def as_list(self) -> list[SimpleNamespace]:
        """Return the data as a list.

        Returns:
            list[SimpleNamespace]: The data as a list.
        """
        return list(self._data)

    def __iter__(self) -> Iterator[SimpleNamespace]:
        return iter(self._data)

    def __getitem__(self, index: int) -> SimpleNamespace:
        return self._data[index]


def json_to_dict(file_name: str) -> Mapping[str, Any]:
    """Load JSON data from a file and return it as a dictionary.

    Sometimes we just want to load the JSON data as a dictionary instead of a list of
    SimpleNamespace objects. This function provides a way to do that.

    Args:
        file_name (str): The name of the file to load.

    Returns:
        dict[str, Any]: The data from the JSON file.
    """
    with Path(__data__ / file_name).open(encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
        return data
