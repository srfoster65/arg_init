"""
Class to process arguments, environment variables and return a set of
processed attribute values.
"""
import logging
from abc import ABC, abstractmethod
from collections.abc import Mapping
from inspect import ArgInfo, FrameInfo, stack
from os import environ
from pathlib import Path
from typing import Any

from box import Box

from ._aliases import Defaults, Priorities
from ._arg import Arg
from ._arg_defaults import ArgDefaults
from ._config import read_config
from ._enums import UseKWArgs
from ._priority import DEFAULT_PRIORITY, Priority
from ._values import Values

logger = logging.getLogger(__name__)


class ArgInit(ABC):
    """
    Class to resolve arguments of a function from passed in values, a config file,
    environment variables or default values.
    """

    STACK_LEVEL_OFFSET = 0  # Overridden by concrete class

    def __init__(  # noqa: PLR0913
        self,
        # *,
        priorities: Priorities = DEFAULT_PRIORITY,
        env_prefix: str | None = None,
        use_kwargs: UseKWArgs = UseKWArgs.FALSE,
        defaults: Defaults = None,
        config_name: str | Path = "config",
        **kwargs: dict[Any, Any],  # noqa: ARG002
    ) -> None:
        self._env_prefix = env_prefix
        self._priorities = priorities
        self._args = Box()
        calling_stack = stack()[self.STACK_LEVEL_OFFSET]
        name = self._get_name(calling_stack)
        config_data = self._read_config(config_name, name, priorities)
        self._init_args(name, calling_stack, use_kwargs, defaults, config_data)
        self._post_init(calling_stack)

    @property
    def args(self) -> Box:
        """Return the processed arguments."""
        return self._args

    @abstractmethod
    def _get_arguments(self, frame: object, use_kwargs: UseKWArgs) -> dict[str, object]:
        """
        Return a dictionary containing key value pairs of all
        named arguments and their values associated with the frame.
        """
        raise RuntimeError  # pragma no cover

    @abstractmethod
    def _get_name(self, calling_stack: FrameInfo) -> str:
        """Return the name of the item having arguments initialised."""
        raise RuntimeError  # pragma no cover

    @abstractmethod
    def _post_init(self, calling_stack: FrameInfo) -> None:
        """
        Class specific post initialisation actions.

        This can optionally be overridden by derived classes
        """

    def _init_args(  # noqa: PLR0913
        self,
        name: str,
        calling_stack: FrameInfo,
        use_kwargs: UseKWArgs,
        defaults: Defaults,
        config: dict[Any, Any],
    ) -> None:
        """Resolve argument values."""
        logger.debug("Creating arguments for: %s", name)
        arguments = self._get_arguments(calling_stack.frame, use_kwargs)
        self._make_args(arguments, defaults, config)

    def _get_kwargs(self, arginfo: ArgInfo, use_kwargs: UseKWArgs) -> dict[Any, Any]:
        """
        Return a dictionary containing kwargs to be resolved.

        Returns an empty dictionary if use_kwargs=False
        """
        if use_kwargs and arginfo.keywords:
            keywords = arginfo.keywords
            logger.debug("Adding kwargs: %s", arginfo.locals[keywords])
            return dict(arginfo.locals[keywords].items())
        return {}

    def _make_args(self, arguments: dict[Any, Any], defaults: Defaults, config: Mapping[Any, Any]) -> None:
        for name, value in arguments.items():
            arg_defaults = self._get_arg_defaults(name, defaults)
            config_name = self._get_config_name(name, arg_defaults)
            env_name = self._get_env_name(self._env_prefix, name, arg_defaults)
            default_value = self._get_default_value(arg_defaults)
            values = Values(
                arg=value,
                env=self._get_env_value(env_name),
                config=self._get_config_value(config, config_name),
                default=default_value,
            )
            self._args[name] = Arg(name, env_name, config_name, values).resolve(name, self._priorities)

    def _get_arg_defaults(self, name: str, defaults: Defaults) -> ArgDefaults | None:
        """Check if any defaults exist for the named arg."""
        if defaults:
            for arg_defaults in defaults:
                if arg_defaults.name == name:
                    return arg_defaults
        return None

    @staticmethod
    def _get_alt_name(arg_defaults: ArgDefaults | None) -> str | None:
        """Return the alternate name for the argument."""
        if arg_defaults and arg_defaults.alt_name:
            return arg_defaults.alt_name
        return None

    @classmethod
    def _get_config_name(cls, name: str, arg_defaults: ArgDefaults | None) -> str:
        """Determine the name to use for the config."""
        alt_name = cls._get_alt_name(arg_defaults)
        return alt_name if alt_name else name

    @staticmethod
    def _construct_env_name(env_prefix: str | None, name: str) -> str:
        env_parts = [item for item in (env_prefix, name) if item]
        return "_".join(env_parts).upper()

    @classmethod
    def _get_env_name(cls, env_prefix: str | None, name: str, arg_defaults: ArgDefaults | None) -> str:
        """Determine the name to use for the env."""
        alt_name = cls._get_alt_name(arg_defaults)
        return (alt_name if alt_name else cls._construct_env_name(env_prefix, name)).upper()

    @staticmethod
    def _get_value(name: str, dictionary: Mapping[Any, Any]) -> str | None:
        """Read the env value."""
        if name in dictionary:
            value = dictionary[name]
            logger.debug("Not found: %s=%s", name, value)
            return value
        logger.debug("%s not set", name)
        return None

    @classmethod
    def _get_config_value(cls, config: Mapping[Any, Any], name: str) -> object:
        logger.debug("Searching config for: %s", name)
        return cls._get_value(name, config)

    @classmethod
    def _get_env_value(cls, name: str) -> str | None:
        logger.debug("Searching environment for: %s", name)
        return cls._get_value(name, environ)

    @staticmethod
    def _get_default_value(arg_defaults: ArgDefaults | None) -> object:
        if arg_defaults:
            return arg_defaults.default_value
        return None

    def _read_config(
        self,
        config_name: str | Path,
        section_name: str,
        priorities: Priorities,
    ) -> dict[Any, Any]:
        if Priority.CONFIG in priorities:
            config = read_config(config_name)
            logger.debug("Checking for section '%s' in config file", section_name)
            if config and section_name in config:
                logger.debug("config=%s", config[section_name])
                return config[section_name]
            logger.debug("No section '%s' data found", section_name)
            return {}
        logger.debug("skipping file based config based on priorities")
        return {}
