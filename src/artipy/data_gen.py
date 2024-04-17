"""Module that handles JSON data for the stats module."""

import json
import re
from pathlib import Path
from types import SimpleNamespace
from typing import Any, ClassVar, Iterator

from artipy import __data__


def camel_to_snake_case(s: str) -> str:
    """Convert a camel case string to snake case.

    Used by in the recursive_namespace function to make attribute names snake_case.

    Args:
        s (str): The string to convert.

    Returns:
        str: The converted string.
    """
    s = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def recursive_namespace(data: Any) -> Any | SimpleNamespace:
    """Recursively convert a dictionary to a SimpleNamespace.

    Convert any attribute names from camelCase to snake_case for consistency.

    Args:
        data (Any): The data to convert.

    Returns:
        Any | SimpleNamespace: The converted data.
    """
    if isinstance(data, dict):
        return SimpleNamespace(**{
            camel_to_snake_case(k): recursive_namespace(v) for k, v in data.items()
        })
    return data


class DataGen:
    """Handle JSON data.

    This is a singleton class that manages JSON data. Each instance of this class is
    associated with a specific JSON file, and the data from that file is loaded when
    the instance is created. The data is stored as a list of SimpleNamespace objects,
    which allows for easy attribute-style access.

    Attributes:
        _instances (dict[str, DataGen]): A dictionary that maps file names to DataGen
                                        instances.
        _data (list[SimpleNamespace]): The data loaded from the JSON file.
    """

    _instances: ClassVar[dict[str, "DataGen"]] = {}
    _data: list[SimpleNamespace] = []

    def __new__(cls, file_name: str) -> "DataGen":
        """Create a new instance of the class if an instance with the same file name
        does not exist.

        Args:
            file_name (str): The name of the file to load.

        Returns:
            DataGen: _description_
        """
        if file_name not in cls._instances:
            cls._instances[file_name] = super().__new__(cls)
        return cls._instances[file_name]

    def __init__(self, file_name: str) -> None:
        """Load the data from the JSON file.

        Args:
            file_name (str): _description_
        """
        with open(Path(__data__ / file_name), mode="r", encoding="utf-8") as f:
            self._data = json.load(f, object_hook=recursive_namespace)

    def as_dict(self) -> dict[str, dict[str, Any]]:
        """Convert the data to a dictionary.

        Sometimes we don't want to use the SimpleNamespace objects, so this method
        converts the data to a dictionary.

        Returns:
            dict[str, dict[str, Any]]: The data as a dictionary.
        """
        return {k: vars(v) for k, v in vars(self._data).items()}

    def __iter__(self) -> Iterator[SimpleNamespace]:
        return iter(self._data)

    def __getitem__(self, index: int) -> SimpleNamespace:
        return self._data[index]
