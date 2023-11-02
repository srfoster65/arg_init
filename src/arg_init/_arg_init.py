"""
Class to process arguments, environment variables and return a set of
processed attribute values.
"""
from abc import ABC, abstractmethod
from os import environ
import logging

from box import Box

from ._arg import Values, Arg


logger = logging.getLogger(__name__)


ARG_PRIORITY = "arg_priority"
ENV_PRIORITY = "env_priority"


class ArgInit(ABC):
    """
    Class to resolve arguments of a function from passed in values, environment
    variables or default values.
    """

    DEFAULT_PRIORITY_SYSTEM = ENV_PRIORITY
    STACK_LEVEL_OFFSET = 1  # The calling frame is 1 layer up

    def __init__(
        self,
        priority: bool = ENV_PRIORITY,
        env_prefix: str | None = None,
    ):
        self._env_prefix = env_prefix
        self._priority = priority
        self._args = Box()

    @property
    def args(self) -> Box:
        """Return the processed arguments."""
        return self._args

    @abstractmethod
    def _get_arguments(self, frame, use_kwargs):
        """
        Returns a dictionary containing key value pairs of all
        named arguments and their values associated with the frame.
        """
        raise RuntimeError()  # pragma no cover

    def _init_args(
        self,
        calling_stack,
        use_kwargs: bool,
        defaults,
    ) -> None:
        """Resolve argument values."""
        logger.debug("Creating arguments for function: %s", calling_stack.function)
        arguments = self._get_arguments(calling_stack.frame, use_kwargs)
        self._make_args(arguments, defaults)

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

    def _make_args(self, arguments, defaults) -> None:
        for name, value in arguments.items():
            arg_defaults = self._get_arg_defaults(name, defaults)
            env_name = self._get_env_name(name, arg_defaults)
            default_value = self._get_default_value(arg_defaults)
            values = Values(
                arg=value, env=self._get_env_value(env_name), default=default_value
            )
            self._args[name] = Arg(name, env_name, values).resolve(self._priority)

    def _get_arg_defaults(self, name, defaults):
        for arg_defaults in defaults:
            if arg_defaults.name == name:
                return arg_defaults
        return None

    def _get_env_name(self, name, arg_defaults):
        """Determine the name to use for the env."""
        if arg_defaults:
            if arg_defaults.disable_env:
                return None
            if arg_defaults.env_name:
                return arg_defaults.env_name.upper()
        env_parts = [item for item in (self._env_prefix, name) if item]
        return "_".join(env_parts).upper()

    @staticmethod
    def _get_env_value(env_name) -> str:
        """Read the env value from environ."""
        if env_name:
            logger.debug("Searching for env: %s", env_name)
            if env_name in environ:
                value = environ[env_name]
                logger.debug("Env found: %s=%s", env_name, value)
                return value
            logger.debug("Env not set")
            return None
        logger.debug("Env disabled")
        return None

    @staticmethod
    def _get_default_value(arg_defaults):
        if arg_defaults:
            return arg_defaults.default_value
        return None
