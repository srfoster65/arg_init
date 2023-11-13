"""Class to represent an Argument."""

import logging
from typing import Any

from ._aliases import Priorities
from ._priority import Priority
from ._values import Values

logger = logging.getLogger(__name__)


class Arg:
    """Class to represent argument attributes."""

    _mapping = {  # noqa: RUF012
        Priority.CONFIG: "config",
        Priority.ENV: "env",
        Priority.ARG: "arg",
        Priority.DEFAULT: "default",
    }

    def __init__(
        self,
        name: str,
        env_name: str | None = None,
        config_name: str | None = None,
        values: Values | None = None,
    ) -> None:
        self._name = name
        self._env_name = env_name
        self._config_name = config_name
        self._values = values
        self._value = None

    def __eq__(self, other: object) -> bool:
        """When testing for equality, test only the value attribute."""
        return self.value == other

    def _data(self) -> list[str]:
        return [
            f"name={self.name}",
            f"env_name={self.env_name}",
            f"config_name={self.config_name}",
            f"values={self.values}",
            f"value={self.value}",
        ]

    def __str__(self) -> str:
        return str(self.value)

    def __repr__(self) -> str:
        return "<Arg(" + ", ".join(self._data()) + ")>"

    @property
    def name(self) -> str:
        """Name of Arg."""
        return self._name

    @property
    def value(self) -> object | None:
        """Resolved value of Arg."""
        return self._value

    @property
    def env_name(self) -> str | None:
        """Env attribute."""
        return self._env_name

    @property
    def config_name(self) -> str | None:
        """Config_name attribute."""
        return self._config_name

    @property
    def values(self) -> Values | None:
        """Values to use when resolving Arg."""
        return self._values

    def resolve(self, name: str, priority_order: Priorities) -> object | None:
        """Resolve the value Arg using the selected priority system."""
        logger.debug("Resolving value for %s", repr(self))
        for priority in priority_order:
            logger.debug("Checking %s value", priority)
            value = self._get_value(priority)
            if value is not None:
                logger.debug("Resolved %s = %s from %s", name, value, priority)
                self._value = value
                break
        return self

    def _get_value(self, priority: Priority) -> Any | None:  # noqa: ANN401
        return getattr(self._values, self._mapping[priority])
