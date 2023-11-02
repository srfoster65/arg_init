"""
Data Class used to customise ArgInit behaviour
"""

from dataclasses import dataclass
from os import environ
import logging


logger = logging.getLogger(__name__)


@dataclass
class Values:
    arg: any = None
    env: any = None
    default: any = None

    def __repr__(self):
        return f"<Values(arg={self.arg}, env={self.env}, default={self.default})>"


class Arg:
    """Class to represent argument attributes."""

    ARG_PRIORITY = "arg_priority"
    ENV_PRIORITY = "env_priority"
    DEFAULT_PRIORITY_SYSTEM = ENV_PRIORITY

    def __init__(
        self,
        name: str,
        env_name: str = None,
        values=None,
    ):
        self._name = name
        self._env_name = env_name
        self._values = values
        self._value = None

    def __eq__(self, other):
        """When testing for equality, test only the value attribute."""
        return self.value == other

    def _data(self):
        return [
            f"name={self.name}",
            f"env_name={self.env_name}",
            f"values={self.values}",
            f"value={self.value}",
        ]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "<Arg(" + ", ".join(self._data()) + ")>"

    @property
    def name(self):
        """Name of Arg."""
        return self._name

    @property
    def value(self):
        """Resolved value of Arg."""
        return self._value

    @property
    def env_name(self):
        """env attribute."""
        return self._env_name

    @property
    def values(self):
        """default attribute."""
        return self._values

    def resolve(self, priority=DEFAULT_PRIORITY_SYSTEM):
        """
        Resolve the value Arg using the selected priority system.
        """
        logger.debug("Resolving value for %s", repr(self))
        if priority == self.ARG_PRIORITY:
            value = self._resolve_arg_priority()
        if priority == self.ENV_PRIORITY:
            value = self._resolve_env_priority()
        self._value = value
        return self

    def _if_use_arg_value(self) -> bool:
        if self.values.arg:
            logger.debug("Using arg: value=%s", self.values.arg)
            return True
        return False

    def _if_use_env_value(self) -> bool:
        if self.values.env:
            logger.debug("Using env: value=%s", self.values.env)
            return True
        return False

    def _log_use_default_value(self):
        logger.debug("Using default: value=%s", self.values.default)

    def _resolve_arg_priority(self):
        logger.debug("Resolving using arg priority")
        if self._if_use_arg_value():
            return self.values.arg
        if self._if_use_env_value():
            return self.values.env
        self._log_use_default_value()
        return self.values.default

    def _resolve_env_priority(self):
        logger.debug("Resolving using env priority")
        if self._if_use_env_value():
            return self.values.env
        if self._if_use_arg_value():
            return self.values.arg
        self._log_use_default_value()
        return self.values.default
