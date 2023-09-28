"""
Class to process arguments, environment variables and return a set of
processed attribute values.
"""

# from __future__ import annotations

from inspect import stack
from os import environ
import logging

from box import Box

from .exceptions import AttributeExistsError
from .named_args import named_arguments
from .arg import Arg


logger = logging.getLogger(__name__)


class ArgInit:
    """
    Class to process arguments, environment variables and return a set of
    processed attribute values.
    """

    ARG_PRIORITY = "arg_priority"
    ENV_PRIORITY = "env_priority"
    DEFAULT_PRIORITY_SYSTEM = ENV_PRIORITY

    def __init__(
        self,
        env_prefix: str = "",
        priority: str = DEFAULT_PRIORITY_SYSTEM,
        use_kwargs: bool = False,
        args: None | list = None
    ):
        self._env_prefix = env_prefix
        self._priority = priority
        self._use_kwargs = use_kwargs
        self._args = Box()
        self._go(args)

    @property
    def args(self):
        """Return the processed arguments"""
        return self._args

    def _go(self, args: None | list = None):
        """
        Process args and envs, storing results in self._args
        """
        STACK_LEVEL_OFFSET = 2  # 0=ArgInit.__init__, 1 = This function, 2=calling function
        named_args = named_arguments(frame=stack()[STACK_LEVEL_OFFSET].frame, include_kwargs=self._use_kwargs)
        for name, value in named_args.items():
            logger.debug("Processing: %s", name)
            arg = self._find_arg(name, args)
            if self._priority == self.ARG_PRIORITY:
                self._arg_priority(arg, value)
            else:
                self._env_priority(arg, value)
        logger.debug("Finished processing arguments")

    def set(self, obj):
        """Set attributes as defined in "args" for the specified object."""
        for arg, value in self.args.items():
            if hasattr(obj, arg):
                raise AttributeExistsError(arg)
            setattr(obj, arg, value)

    @staticmethod
    def _find_arg(name: str, args: None | list) -> str:
        print("args=",args)
        if args:
            logger.debug("Searching for arg=%s", name)
            for arg in args:
                if arg.name == name:
                    logger.debug("Arg found")
                    return arg
            logger.debug("Arg not found")
        else:
            logger.debug("No Args defined")
        logger.debug("Creating arg(name=%s)", name)
        return Arg(name)

    def _arg_priority(self, arg: Arg, value: any) -> None:
        if self._try_arg(arg, value):
            return
        if self._try_env(arg):
            return
        self._try_default(arg)

    def _env_priority(self, arg: Arg, value: any) -> None:
        if self._try_env(arg):
            return
        if self._try_arg(arg, value):
            return
        self._try_default(arg)

    def _try_arg(self, arg: Arg, value: any) -> bool:
        """
        Try and set value from arg
        """
        logger.debug("Checking for a arg")
        if arg.force_arg or value is not None:
            logger.debug("Arg value found: %s", value)
            self._args[self._get_attr_name(arg)] = value
            return True
        logger.debug("Arg value is None and force_arg=False")
        return False

    def _try_env(self, arg: Arg) -> bool:
        """
        Try and set value from env
        """
        env_name = self._get_env_name(arg, self._env_prefix)
        logger.debug("Checking env = '%s'", env_name)
        logger.debug(arg.disable_env)
        if env_name and env_name in environ and not arg.disable_env:
            logger.debug("Found env: %s", env_name)
            value = environ[env_name]
            if arg.force_env or value:
                logger.debug("Env value found: %s", value)
                self._args[self._get_attr_name(arg)] = value
                return True
            logger.debug("env value is None and force_env=False. Checking default")
        else:
            logger.debug("env not found")
        return False

    def _try_default(self, arg: Arg) -> None:
        """
        Try and set value from item default
        """
        logger.debug("Checking for a default value")
        if arg.force_default or arg.default:
            logger.debug("Setting default: %s", arg.default)
            self._args[self._get_attr_name(arg)] = arg.default
        else:
            logger.debug(
                "Not setting %s. Value is None and force_default=False", arg.name
            )

    @staticmethod
    def _get_attr_name(arg: Arg) -> str:
        """Return the name to use for the attribute."""
        return arg.attr if arg.attr else arg.name

    @staticmethod
    def _get_env_name(arg: Arg, prefix: str) -> str:
        """
        Return the env name to check for a value.
        """
        env = arg.env if arg.env else arg.name
        env_parts = [item for item in (prefix, env) if item]
        return "_".join(env_parts)
