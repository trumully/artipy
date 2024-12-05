"""Module that handles JSON data for the stats module."""

import orjson
import re
from collections.abc import Iterator, Mapping, MutableMapping, Sequence
from types import SimpleNamespace
from typing import Any, ClassVar, cast

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


def recursive_namespace(data: Any) -> Any | SimpleNamespace:
    """Recursively convert a dictionary to a SimpleNamespace.

    Convert any attribute names from camelCase to snake_case for consistency.

    Args:
        data (Any): The data to convert.

    Returns:
        Any | SimpleNamespace: The converted data.
    """
    if isinstance(data, Mapping):
        data = cast(Mapping[str, Any], data)
        return SimpleNamespace(**{
            camel_to_snake_case(k): recursive_namespace(v) for k, v in data.items()
        })
    if isinstance(data, list):
        data = cast("Sequence[Any]", data)
        return [recursive_namespace(item) for item in data]
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

    def __new__(cls, file_name: str) -> "DataGen":
        """Create a new instance of the class if an instance with the same file name
        does not exist.

        Args:
            file_name (str): The name of the JSON file to load.

        Returns:
            DataGen: The instance of the DataGen class.
        """
        if file_name not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[file_name] = instance
            instance._load_data(file_name)
        return cls._instances[file_name]

    def _load_data(self, file_name: str) -> None:
        """Load data from a JSON file.

        Args:
            file_name (str): The name of the JSON file to load.
        """
        with (__data__ / file_name).open("rb") as f:
            data = orjson.loads(f.read())
            if not hasattr(self, "_data"):
                self._data = [recursive_namespace(item) for item in data]  # type: ignore

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
    with (__data__ / file_name).open("rb") as f:
        data: dict[str, Any] = orjson.loads(f.read())
        return data
