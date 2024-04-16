"""Stat types and data for Genshin Impact artifacts."""

from dataclasses import dataclass, field
from decimal import Decimal

from artipy.types import STAT_NAMES, StatType


@dataclass(slots=True)
class Stat:
    """Dataclass for a stat in Genshin Impact."""

    name: StatType
    _value: float | int | Decimal = field(default=Decimal(0), repr=False)

    @property
    def value(self) -> Decimal:
        """Get the value of the stat.

        :return: The value of the stat.
        :rtype: Decimal
        """
        return Decimal(self._value)

    @value.setter
    def value(self, value: float | int | Decimal) -> None:
        """Set the value of the stat.

        :param value: The value to set the stat to.
        :type value: float | int | Decimal
        """
        if not isinstance(value, Decimal):
            value = Decimal(value)
        self._value = value

    def __format__(self, format_spec: str) -> str:
        if format_spec in ("v", "verbose"):
            return f"{self.name} = {self.value}"
        return str(self)

    def __str__(self) -> str:
        name = STAT_NAMES[self.name].split("%")
        if self.name.is_pct:
            return f"{name[0]}+{self.value:.1%}"
        return f"{name[0]}+{self.value:,.0f}"
