"""
Data Class used to customise ArgInit behaviour
"""

from dataclasses import dataclass
from os import environ
import logging


logger = logging.getLogger(__name__)


@dataclass
class Attribute:
    """Dataclass"""

    name: str
    value: any = None
    force: bool = False

    def __repr__(self):
        return f"<Attribute(name={self.name}, value={self.value}, force={self.force})>"


class Arg:
    """Class to represent argument attrubutes."""

    ARG_PRIORITY = "arg_priority"
    ENV_PRIORITY = "env_priority"
    DEFAULT_PRIORITY_SYSTEM = ENV_PRIORITY

    def __init__(
        self,
        name: str,
        env: str = None,
        default: any = None,
        attr: str = None,
        force_arg: bool = False,  # Force use of arg value if value = None
        force_env: bool = False,  # Force use of env value if value = None
        disable_env: bool = False,  # Do not search for an env value.
    ):
        self._arg = Attribute(name, force=force_arg)
        self._env = Attribute(
            self._get_env_name(env),
            force=force_env,
        )
        self._default = Attribute("default", default, force=True)
        self._value = None
        self._disable_env = disable_env
        self._attr = attr or name
        self._disable_env = disable_env
        self._priority = None

    def __eq__(self, other):
        """When testing for equality, test only the value attribute."""
        return self.value == other

    def _data(self):
        return [
            f"arg={self.arg}",
            f"env={self.env}",
            f"default={self.default}",
            f"attr={self._attr}",
            f"disable_env={self._disable_env}",
            f"priority={self._priority}",
            f"value={self.value}"
        ]

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "<Arg(" + ", ".join(self._data()) + ")>"

    @property
    def name(self):
        """Name of Arg."""
        return self.attr

    @property
    def value(self):
        """Resolved value of Arg."""
        return self._value

    @property
    def arg(self):
        """arg attribute."""
        return self._arg

    @property
    def env(self):
        """env attribute."""
        return self._env

    @property
    def default(self):
        """default attribute."""
        return self._default

    @property
    def attr(self):
        """attr is the alternate name for the argument."""
        return self._attr

    def resolve(self, priority=DEFAULT_PRIORITY_SYSTEM):
        """
        Resolve the value Arg using the selected priority system.
        This method should only be called by ArgInit()
        """
        if not self._priority:
            self._env.value = self._get_env_value()
            self._priority = priority
            logger.debug(
                "Resolving value for %s", repr(self)
            )
            if priority == self.ARG_PRIORITY:
                value = self._resolve_arg_priority()
            if priority == self.ENV_PRIORITY:
                value = self._resolve_env_priority()
            self._value = value
        return self

    def _set_arg_value(self) -> bool:
        if self._arg.value or self._arg.force:
            logger.debug("Using arg: value=%s", self._arg.value)
            return True
        return False

    def _set_env_value(self) -> bool:
        if (self._env.value or self._env.force) and not self._disable_env:
            logger.debug("Using env: value=%s", self._env.value)
            return True
        return False

    def _set_default_value(self):
        logger.debug("Using default: value=%s", self._default.value)

    def _resolve_arg_priority(self):
        if self._set_arg_value():
            return self._arg.value
        if self._set_env_value():
            return self._env.value
        self._set_default_value()
        return self._default.value

    def _resolve_env_priority(self):
        if self._set_env_value():
            return self._env.value
        if self._set_arg_value():
            return self._arg.value
        self._set_default_value()
        return self._default.value

    def _get_env_value(self) -> str:
        """Read the env value from environ."""
        env = self._env
        logger.debug("Searching for env: %s", env.name)
        if env.name and env.name in environ:
            value = environ[env.name]
            logger.debug("Env found: %s=%s", env.name, value)
            return value
        logger.debug("Env not found")
        return None

    def _get_env_name(self, env_name) -> str:
        """Return the env name to check for a value."""
        return (env_name if env_name else self._arg.name).upper()
