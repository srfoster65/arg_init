"""
Class to process arguments, environment variables and return a set of
processed attribute values.
"""
from abc import ABC, abstractmethod
from inspect import stack
from os import environ
from typing import Any
import logging

from box import Box

from ._arg import Arg
from ._arg_defaults import ArgDefaults
from ._config import read_config
from ._priority import Priority, DEFAULT_PRIORITY
from ._values import Values


logger = logging.getLogger(__name__)

class ArgInit(ABC):
    """
    Class to resolve arguments of a function from passed in values, environment
    variables or default values.
    """

    STACK_LEVEL_OFFSET = 2  # The calling frame is 2 layers up

    def __init__(
        self,
        priority = DEFAULT_PRIORITY,
        env_prefix: str | None = None,
        use_kwargs = False,
        defaults = None,
        config_name = "config",
        **kwargs,  # pylint: disable=unused-argument
    ) -> None:
        self._env_prefix = env_prefix
        self._priority = priority
        self._args = Box()
        calling_stack = stack()[self.STACK_LEVEL_OFFSET]
        name = self._get_name(calling_stack)
        arg_config = self._read_config(config_name, name, priority)
        self._init_args(name, calling_stack, use_kwargs, defaults, arg_config)
        self._post_init(calling_stack)

    @property
    def args(self) -> Box:
        """Return the processed arguments."""
        return self._args

    @property
    def config(self):
        """Return the config data"""
        return self._config

    @abstractmethod
    def _get_arguments(self, frame, use_kwargs) -> dict:
        """
        Returns a dictionary containing key value pairs of all
        named arguments and their values associated with the frame.
        """
        raise RuntimeError()  # pragma no cover

    @abstractmethod
    def _get_name(self, calling_stack) -> str:
        """
        Return the name of the item having arguments initialised.
        """
        raise RuntimeError()  # pragma no cover

    # @abstractmethod
    def _post_init(self, calling_stack) -> None:
        """
        Class specific post initialisation actions.
        This can optionally be overridden by derived classes
        """

    def _init_args(
        self,
        name,
        calling_stack,
        use_kwargs: bool,
        defaults,
        config,
    ) -> None:
        """Resolve argument values."""
        logger.debug("Creating arguments for: %s", name)
        arguments = self._get_arguments(calling_stack.frame, use_kwargs)
        self._make_args(arguments, defaults, config)

    def _get_kwargs(self, arginfo, use_kwargs) -> dict:
        """
        Return a dictionary containing kwargs to be resolved.
        Returns an empty dictionary if use_kwargs=False
        """
        if use_kwargs and arginfo.keywords:
            keywords = arginfo.keywords
            logger.debug("Adding kwargs: %s", arginfo.locals[keywords])
            return dict(arginfo.locals[keywords].items())
        return {}

    def _make_args(self, arguments, defaults, config) -> None:
        for name, value in arguments.items():
            arg_defaults = self._get_arg_defaults(name, defaults)
            config_name = self._get_config_name(name, arg_defaults)
            env_name = self._get_env_name(self._env_prefix, name, arg_defaults)
            default_value = self._get_default_value(arg_defaults)
            values = Values(
                arg=value,
                env=self._get_env_value(env_name),
                config=self._get_config_value(config, config_name),
                default=default_value
            )
            self._args[name] = Arg(name, env_name, config_name, values).resolve(name, self._priority)

    def _get_arg_defaults(self, name, defaults)-> ArgDefaults | None:
        """Check if any defaults exist for the named arg."""
        if defaults:
            for arg_defaults in defaults:
                if arg_defaults.name == name:
                    return arg_defaults
        return None

    @staticmethod
    def _get_alt_name(arg_defaults) -> str | None:
        """Return the alternate name for the argument."""
        if arg_defaults and arg_defaults.alt_name:
            return arg_defaults.alt_name
        return None

    @classmethod
    def _get_config_name(cls, name, arg_defaults) -> str:
        """Determine the name to use for the config."""
        alt_name = cls._get_alt_name(arg_defaults)
        return alt_name if alt_name else name

    @staticmethod
    def _construct_env_name(env_prefix, name) -> str:
        env_parts = [item for item in (env_prefix, name) if item]
        return "_".join(env_parts).upper()

    @classmethod
    def _get_env_name(cls, env_prefix, name, arg_defaults) -> str:
        """Determine the name to use for the env."""
        alt_name = cls._get_alt_name(arg_defaults)
        return (alt_name if alt_name else cls._construct_env_name(env_prefix, name)).upper()

    @staticmethod
    def _get_value(name, dictionary) -> str | None:
        """Read the env value."""
        # logger.debug("Searching for %s", name)
        if name in dictionary:
            value = dictionary[name]
            logger.debug("Not found: %s=%s", name, value)
            return value
        logger.debug("%s not set", name)
        return None

    @classmethod
    def _get_config_value(cls, config, name) -> Any:
        logger.debug("Searching config for: %s", name)
        return cls._get_value(name, config)

    @classmethod
    def _get_env_value(cls, name) -> str | None:
        logger.debug("Searching environment for: %s", name)
        return cls._get_value(name, environ)

    @staticmethod
    def _get_default_value(arg_defaults) -> Any:
        if arg_defaults:
            return arg_defaults.default_value
        return None

    def _read_config(
        self,
        config_name,
        section_name: str,
        priority: tuple,
    ) -> dict:
        config = config = (
            read_config(config_name) if Priority.CONFIG in priority else {}
        )
        if config:
            logger.debug("Checking for section '%s' in config file", section_name)
        if section_name in config:
            logger.debug("config=%s", config[section_name])
            return config[section_name]
        logger.debug("No config data found for section: %s", section_name)
        return {}
