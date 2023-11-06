"""
Class to process arguments, environment variables and return a set of
processed attribute values.
"""
from abc import ABC, abstractmethod
from inspect import stack
from os import environ
import logging

from box import Box

from ._arg import Arg
from ._config import read_config
from ._priority import Priority
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
        priority,
        env_prefix: str | None,
        use_kwargs,
        defaults,
        config,
        **kwargs,  # pylint: disable=unused-argument
    ):
        self._env_prefix = env_prefix
        self._priority = priority
        self._args = Box()
        calling_stack = stack()[self.STACK_LEVEL_OFFSET]
        calling_stack.frame.f_locals["arg1"] = 2
        name = self._get_name(calling_stack)
        self._config = read_config(config) if Priority.CONFIG in priority else {}
        if self._config:
            logger.debug("Section id in config file: %s", name)
        arg_config = self.config.get(name, {})
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
    def _get_arguments(self, frame, use_kwargs):
        """
        Returns a dictionary containing key value pairs of all
        named arguments and their values associated with the frame.
        """
        raise RuntimeError()  # pragma no cover

    @abstractmethod
    def _get_name(self, calling_stack):
        """
        Return the name of the item having arguments initialised.
        """
        raise RuntimeError()  # pragma no cover

    # @abstractmethod
    def _post_init(self, calling_stack):
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
                config=config.get(config_name),
                default=default_value
            )
            alt_name = self._get_alt_name(arg_defaults)
            self._args[name] = Arg(name, alt_name, values).resolve(name, self._priority)

    def _get_arg_defaults(self, name, defaults):
        """Check if any defaults exist for the named arg."""
        if defaults:
            for arg_defaults in defaults:
                if arg_defaults.name == name:
                    return arg_defaults
        return None

    @staticmethod
    def _get_alt_name(arg_defaults):
        """Return the alternate name for the argument."""
        if arg_defaults and arg_defaults.alt_name:
            return arg_defaults.alt_name
        return None

    @classmethod
    def _get_config_name(cls, name, arg_defaults):
        """Determine the name to use for the config."""
        alt_name = cls._get_alt_name(arg_defaults)
        return alt_name if alt_name else name

    @staticmethod
    def _construct_env_name(env_prefix, name):
        env_parts = [item for item in (env_prefix, name) if item]
        return "_".join(env_parts).upper()

    @classmethod
    def _get_env_name(cls, env_prefix, name, arg_defaults):
        """Determine the name to use for the env."""
        alt_name = cls._get_alt_name(arg_defaults)
        return (alt_name if alt_name else cls._construct_env_name(env_prefix, name)).upper()

    @staticmethod
    def _get_env_value(env_name) -> str | None:
        """Read the env value from environ."""
        logger.debug("Searching for env: %s", env_name)
        if env_name in environ:
            value = environ[env_name]
            logger.debug("Env found: %s=%s", env_name, value)
            return value
        logger.debug("Env not set")
        return None

    @staticmethod
    def _get_default_value(arg_defaults):
        if arg_defaults:
            return arg_defaults.default_value
        return None
